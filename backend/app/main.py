"""FastAPI entry point for the modern COVIDash application."""

from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from backend.app.api.routes import router
from backend.app.core.db import MongoStore
from backend.app.core.settings import get_settings

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create and close the Mongo client with the application lifecycle."""

    app.state.mongo_store = MongoStore(get_settings())
    try:
        yield
    finally:
        app.state.mongo_store.close()


def create_app() -> FastAPI:
    """Build the FastAPI application used by ASGI servers and tests."""

    settings = get_settings()
    app = FastAPI(
        title="COVIDash.it API",
        description="Modern API facade over the covidashflow MongoDB analytics contract.",
        version="7.0-modern",
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

    static_path = Path("covidashit/static")
    if static_path.exists():
        app.mount("/static", StaticFiles(directory=static_path), name="static")

    dist_path = Path(settings.frontend_dist)
    if dist_path.exists():
        assets_path = dist_path / "assets"
        if assets_path.exists():
            app.mount("/assets", StaticFiles(directory=assets_path), name="assets")

        @app.get("/{path:path}", include_in_schema=False)
        def spa_fallback(path: str) -> FileResponse:
            """Serve the React single-page app for non-API routes."""

            requested = dist_path / path
            if requested.is_file():
                return FileResponse(requested)
            return FileResponse(dist_path / "index.html")

    return app


app = create_app()
