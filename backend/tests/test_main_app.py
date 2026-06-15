"""Tests for FastAPI shell routing and error handling."""

from __future__ import annotations

from fastapi.testclient import TestClient
from backend.app.core.settings import get_settings
from backend.app.main import create_app


def test_static_shortcuts_do_not_fall_back_to_spa(tmp_path, monkeypatch) -> None:
    """Browser convention paths should return static assets, not index.html."""

    dist = tmp_path / "dist"
    static = dist / "static"
    static.mkdir(parents=True)
    (dist / "index.html").write_text("<!doctype html><title>SPA</title>", encoding="utf-8")
    (static / "favicon.ico").write_bytes(b"ico")
    (static / "robots.txt").write_text("User-agent: *\nAllow: /\n", encoding="utf-8")

    monkeypatch.setenv("FRONTEND_DIST", str(dist))
    get_settings.cache_clear()
    client = TestClient(create_app())

    favicon = client.get("/favicon.ico")
    robots = client.get("/robots.txt")
    favicon_head = client.head("/favicon.ico")
    robots_head = client.head("/robots.txt")

    assert favicon.status_code == 200
    assert favicon.content == b"ico"
    assert robots.status_code == 200
    assert robots.text == "User-agent: *\nAllow: /\n"
    assert favicon_head.status_code == 200
    assert robots_head.status_code == 200


def test_unknown_api_path_returns_json_404(tmp_path, monkeypatch) -> None:
    """API typos should not be masked by the React fallback."""

    dist = tmp_path / "dist"
    dist.mkdir()
    (dist / "index.html").write_text("<!doctype html><title>SPA</title>", encoding="utf-8")

    monkeypatch.setenv("FRONTEND_DIST", str(dist))
    get_settings.cache_clear()
    client = TestClient(create_app())

    response = client.get("/api/not-real", headers={"accept": "application/json"})

    assert response.status_code == 404
    assert response.json() == {"detail": "API endpoint not found"}


def test_api_exception_returns_clean_json_500(tmp_path, monkeypatch) -> None:
    """Unexpected API errors should not leak internals or render old HTML."""

    dist = tmp_path / "dist"
    dist.mkdir()
    (dist / "index.html").write_text("<!doctype html><title>SPA</title>", encoding="utf-8")

    monkeypatch.setenv("FRONTEND_DIST", str(dist))
    get_settings.cache_clear()
    client = TestClient(create_app(), raise_server_exceptions=False)

    response = client.get("/api/config", headers={"accept": "application/json"})

    assert response.status_code == 500
    assert response.json() == {"detail": "Internal server error"}


def test_health_returns_503_when_database_is_unavailable(tmp_path, monkeypatch) -> None:
    """Database outages should fail quickly and clearly for proxy health checks."""

    class FailingStore:
        """Small stand-in for a configured store that cannot reach the database."""

        def ping(self) -> bool:
            raise RuntimeError("database unavailable")

    dist = tmp_path / "dist"
    dist.mkdir()
    (dist / "index.html").write_text("<!doctype html><title>SPA</title>", encoding="utf-8")

    monkeypatch.setenv("FRONTEND_DIST", str(dist))
    get_settings.cache_clear()
    app = create_app()
    client = TestClient(app, raise_server_exceptions=False)
    app.state.data_store = FailingStore()

    response = client.get("/api/health", headers={"accept": "application/json"})

    assert response.status_code == 503
    assert response.json() == {"detail": "Database unavailable"}


def test_reverse_proxy_500_page_is_branded(tmp_path, monkeypatch) -> None:
    """Nginx/Cloudflare error-page paths should use the modern visual style."""

    dist = tmp_path / "dist"
    static = dist / "static" / "img"
    static.mkdir(parents=True)
    (dist / "index.html").write_text("<!doctype html><title>SPA</title>", encoding="utf-8")
    (static / "covidash_32.png").write_bytes(b"png")

    monkeypatch.setenv("FRONTEND_DIST", str(dist))
    get_settings.cache_clear()
    client = TestClient(create_app())

    response = client.get("/500.html", headers={"accept": "text/html"})
    head_response = client.head("/50x.html", headers={"accept": "text/html"})

    assert response.status_code == 500
    assert "COVIDash.it" in response.text
    assert "Dashboard temporarily unavailable" in response.text
    assert head_response.status_code == 500


def test_sitemap_exposes_dashboard_routes(tmp_path, monkeypatch) -> None:
    """Search crawlers should discover static and area dashboard routes."""

    dist = tmp_path / "dist"
    static = dist / "static"
    static.mkdir(parents=True)
    (dist / "index.html").write_text("<!doctype html><title>SPA</title>", encoding="utf-8")
    (static / "favicon.ico").write_bytes(b"ico")

    monkeypatch.setenv("FRONTEND_DIST", str(dist))
    get_settings.cache_clear()
    client = TestClient(create_app())

    response = client.get("/sitemap.xml")
    openapi = client.get("/openapi.json")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/xml")
    assert "<loc>https://covidash.it/</loc>" in response.text
    assert "<loc>https://covidash.it/vaccines</loc>" in response.text
    assert "<loc>https://covidash.it/regions/Lombardia</loc>" in response.text
    assert "<loc>https://covidash.it/provinces/Milano</loc>" in response.text
    assert openapi.json()["info"]["version"] == "8.0.0"


def teardown_module() -> None:
    """Avoid leaking environment-derived settings into later tests."""

    get_settings.cache_clear()
