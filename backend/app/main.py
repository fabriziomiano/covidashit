"""FastAPI entry point for the modern COVIDash application."""

from __future__ import annotations

from contextlib import asynccontextmanager
import logging
from pathlib import Path
from urllib.parse import quote

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

from backend.app.api.routes import router
from backend.app.core.constants import ITALY_MAP, VERSION
from backend.app.core.sql_db import SqlDashboardStore
from backend.app.core.settings import get_settings

load_dotenv()
logger = logging.getLogger(__name__)
SITE_URL = "https://covidash.it"


def wants_html(request: Request) -> bool:
    """Return True when a browser is more likely than an API client."""

    accept = request.headers.get("accept", "")
    return "text/html" in accept and "application/json" not in accept


def error_page(status_code: int, title: str, message: str) -> HTMLResponse:
    """Render a compact branded error page independent of the React bundle."""

    html = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{status_code} | COVIDash.it</title>
    <style>
      * {{ box-sizing: border-box; }}
      body {{
        margin: 0; min-width: 320px; min-height: 100vh; display: grid; place-items: center;
        background: #0f131a; color: #f5f7fb;
        font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      }}
      main {{
        width: min(680px, calc(100% - 32px)); border: 1px solid #354258; border-left: 4px solid #f05d6a;
        border-radius: 8px; background: #151b24; padding: clamp(24px, 5vw, 44px);
        box-shadow: 0 24px 60px rgba(0, 0, 0, 0.28);
      }}
      .brand {{ display: flex; align-items: center; gap: 10px; font-weight: 800; margin-bottom: 28px; }}
      .brand img {{ width: 32px; height: 32px; }}
      .code {{ color: #4db6ac; font-size: 0.78rem; font-weight: 800; text-transform: uppercase; }}
      h1 {{ margin: 8px 0 12px; font-size: clamp(2rem, 5vw, 3.6rem); line-height: 1; }}
      p {{ margin: 0; color: #aeb7c6; line-height: 1.6; }}
      a {{
        display: inline-flex; margin-top: 24px; border: 1px solid #4db6ac; border-radius: 6px;
        padding: 9px 13px; color: #ffffff; background: #18302f; text-decoration: none; font-weight: 800;
      }}
    </style>
  </head>
  <body>
    <main>
      <div class="brand"><img src="/static/img/covidash_32.png" alt="" /> COVIDash.it</div>
      <div class="code">Error {status_code}</div>
      <h1>{title}</h1>
      <p>{message}</p>
      <a href="/">Back to dashboard</a>
    </main>
  </body>
</html>"""
    return HTMLResponse(html, status_code=status_code)


def build_sitemap() -> str:
    """Return a sitemap covering static dashboards and known Italian areas."""

    paths = ["/", "/vaccines", "/thanks"]
    regions = list(ITALY_MAP)
    provinces = [province for province_list in ITALY_MAP.values() for province in province_list]
    paths.extend(f"/regions/{quote(region)}" for region in regions)
    paths.extend(f"/vaccines/{quote(region)}" for region in regions)
    paths.extend(f"/provinces/{quote(province)}" for province in provinces)
    urls = "\n".join(f"  <url><loc>{SITE_URL}{path}</loc></url>" for path in paths)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}
</urlset>
"""


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create and close the SQL dashboard data store."""

    app.state.data_store = SqlDashboardStore(get_settings())
    try:
        yield
    finally:
        app.state.data_store.close()


def create_app() -> FastAPI:
    """Build the FastAPI application used by ASGI servers and tests."""

    settings = get_settings()
    app = FastAPI(
        title="COVIDash.it API",
        description="Modern API facade over the COVIDash PostgreSQL analytics warehouse.",
        version=VERSION,
        lifespan=lifespan,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=list(settings.cors_origins),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(router)

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        """Return JSON for API errors and a branded page for browser errors."""

        if request.url.path.startswith("/api") or not wants_html(request):
            return JSONResponse({"detail": exc.detail}, status_code=exc.status_code, headers=getattr(exc, "headers", None))
        title = "Page not found" if exc.status_code == 404 else "Request error"
        message = "The dashboard route or asset you requested does not exist." if exc.status_code == 404 else str(exc.detail)
        return error_page(exc.status_code, title, message)

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        """Avoid leaking tracebacks and keep server errors visually aligned."""

        logger.exception("Unhandled request error on %s", request.url.path, exc_info=exc)
        if request.url.path.startswith("/api") or not wants_html(request):
            return JSONResponse({"detail": "Internal server error"}, status_code=500)
        return error_page(
            500,
            "Dashboard temporarily unavailable",
            "Something went wrong while serving COVIDash.it. Please retry in a moment.",
        )

    dist_path = Path(settings.frontend_dist)
    if dist_path.exists():
        assets_path = dist_path / "assets"
        if assets_path.exists():
            app.mount("/assets", StaticFiles(directory=assets_path), name="assets")
        static_path = dist_path / "static"
        if static_path.exists():
            app.mount("/static", StaticFiles(directory=static_path), name="static")

        @app.api_route("/favicon.ico", methods=["GET", "HEAD"], include_in_schema=False)
        def favicon() -> FileResponse:
            """Serve the favicon at the conventional browser path."""

            return FileResponse(static_path / "favicon.ico")

        @app.api_route("/robots.txt", methods=["GET", "HEAD"], include_in_schema=False)
        def robots():
            """Serve crawlers without falling through to the React app."""

            robots_path = static_path / "robots.txt"
            if robots_path.exists():
                return FileResponse(robots_path, media_type="text/plain")
            return PlainTextResponse(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n")

        @app.api_route("/sitemap.xml", methods=["GET", "HEAD"], include_in_schema=False)
        def sitemap() -> PlainTextResponse:
            """Expose known dashboard routes for search crawlers."""

            return PlainTextResponse(build_sitemap(), media_type="application/xml")

        @app.api_route("/500.html", methods=["GET", "HEAD"], include_in_schema=False)
        @app.api_route("/50x.html", methods=["GET", "HEAD"], include_in_schema=False)
        def server_error_page() -> HTMLResponse:
            """Expose a branded error page for reverse-proxy error_page rules."""

            return error_page(
                500,
                "Dashboard temporarily unavailable",
                "Something went wrong while serving COVIDash.it. Please retry in a moment.",
            )

        @app.get("/{path:path}", include_in_schema=False)
        def spa_fallback(path: str) -> FileResponse:
            """Serve the React single-page app for non-API routes."""

            if path.startswith("api/"):
                raise HTTPException(status_code=404, detail="API endpoint not found")
            requested = dist_path / path
            if requested.is_file():
                return FileResponse(requested)
            if "." in Path(path).name:
                raise HTTPException(status_code=404, detail="Asset not found")
            return FileResponse(dist_path / "index.html")

    return app


app = create_app()
