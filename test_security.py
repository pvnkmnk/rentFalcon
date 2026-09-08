"""
Security regression tests: CSRF protection and SECRET_KEY management.

Covers the findings in GitHub issue #80:
  - POST endpoints reject requests without a valid CSRF token (400)
  - POST endpoints accept requests with a valid token
  - the rendered search form embeds the CSRF token
  - /api/csrf-token issues a token that works via the X-CSRFToken header
  - SECRET_KEY comes from the environment, never the old hardcoded value
"""

import importlib
import os

import pytest


@pytest.fixture()
def client(monkeypatch):
    """Flask test client with a deterministic SECRET_KEY from the environment."""
    monkeypatch.setenv("SECRET_KEY", "test-secret-key-not-the-dev-value")
    import app as app_module

    importlib.reload(app_module)
    app_module.app.config["TESTING"] = True
    app_module.app.config["WTF_CSRF_ENABLED"] = True
    return app_module.app.test_client()


def _extract_csrf_token(html: str) -> str:
    """Pull the csrf_token value out of the rendered form."""
    marker = 'name="csrf_token"'
    idx = html.find(marker)
    assert idx != -1, "search form does not embed a csrf_token field"
    value_idx = html.find('value="', idx) + len('value="')
    end_idx = html.find('"', value_idx)
    return html[value_idx:end_idx]


def test_secret_key_comes_from_environment(client):
    """SECRET_KEY must be read from the environment, not hardcoded."""
    from app import app

    assert app.config["SECRET_KEY"] == "test-secret-key-not-the-dev-value"
    assert app.config["SECRET_KEY"] != "dev-secret-key-change-in-production"


def test_secret_key_ephemeral_fallback(monkeypatch):
    """Without SECRET_KEY in the env, the app still boots with a random key."""
    monkeypatch.delenv("SECRET_KEY", raising=False)
    import app as app_module

    importlib.reload(app_module)
    key = app_module.app.config["SECRET_KEY"]
    assert key
    assert key != "dev-secret-key-change-in-production"
    assert len(key) >= 32  # token_hex(32) -> 64 hex chars


def test_search_post_without_csrf_token_rejected(client):
    """POST / without a CSRF token must be rejected (400)."""
    resp = client.post("/", data={"location": "newmarket"})
    assert resp.status_code == 400


def test_api_search_without_csrf_token_rejected(client):
    """POST /api/search without a CSRF token must be rejected (400)."""
    resp = client.post("/api/search", json={"location": "newmarket"})
    assert resp.status_code == 400


def test_search_post_with_valid_csrf_token_accepted(client, monkeypatch):
    """POST / with a valid CSRF token passes the CSRF check.

    The manager is stubbed so the test only exercises the CSRF layer and the
    form path; passing the token must get past CSRF (no 400) and render the
    results page.
    """
    import app as app_module

    monkeypatch.setattr(
        app_module.manager,
        "search_all",
        lambda location, min_price, max_price: {
            "listings": [],
            "stats": {"scrapers_succeeded": 0, "execution_time": 0.0},
            "errors": {},
        },
    )
    page = client.get("/")
    token = _extract_csrf_token(page.get_data(as_text=True))

    resp = client.post(
        "/",
        data={"location": "newmarket", "csrf_token": token},
        follow_redirects=False,
    )
    assert resp.status_code == 200


def test_api_search_with_header_token_passes_csrf(client, monkeypatch):
    """POST /api/search with X-CSRFToken header passes the CSRF check."""
    token_resp = client.get("/api/csrf-token")
    assert token_resp.status_code == 200
    token = token_resp.get_json()["token"]

    # The scraper call is network-bound; stub the manager so the test only
    # exercises the CSRF layer and the endpoint contract.
    import app as app_module

    monkeypatch.setattr(
        app_module.manager,
        "search_all",
        lambda location, min_price, max_price: {
            "listings": [],
            "stats": {"scrapers_succeeded": 0, "execution_time": 0.0},
            "errors": {},
        },
    )

    resp = client.post(
        "/api/search",
        json={"location": "newmarket"},
        headers={"X-CSRFToken": token},
    )
    assert resp.status_code == 200
    assert "listings" in resp.get_json()


def test_csrf_token_endpoint_shape(client):
    """GET /api/csrf-token returns a token and sets the session cookie."""
    resp = client.get("/api/csrf-token")
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["token"]
    # The token is bound to the session; the client must have received it.
    assert client.get_cookie("session") is not None


def test_get_routes_stay_public(client):
    """CSRF only protects state-changing requests; GETs are unaffected."""
    assert client.get("/").status_code == 200
    assert client.get("/api/sources").status_code == 200
