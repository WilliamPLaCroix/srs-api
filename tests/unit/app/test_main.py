def test_app_starts():
    from fastapi.testclient import TestClient

    from app.main import app

    client = TestClient(app)
    response = client.get("/core/health")
    assert response.status_code == 200


def test_cards_endpoint_exists():
    from fastapi.testclient import TestClient

    from app.main import app

    client = TestClient(app)
    response = client.get("/cards/")
    assert response.status_code != 404


def test_create_card_api_flow():
    from fastapi.testclient import TestClient

    from app.main import app

    client = TestClient(app)
    payload = {"front": "Q", "back": "A", "deck_id": 1}

    response = client.post("/cards/", json=payload)

    assert response.status_code in (200, 201)
    data = response.json()
    assert "id" in data


def test_lifespan_calls_setup_logging(monkeypatch):
    import importlib

    called = {"v": False}

    def fake_setup_logging():
        called["v"] = True

    monkeypatch.setattr("app.core.logging.setup_logging", fake_setup_logging)

    # reload the app.main module so the lifespan uses the patched setup_logging
    mod = importlib.reload(importlib.import_module("app.main"))
    app = mod.app

    from fastapi.testclient import TestClient

    with TestClient(app):
        pass

    assert called["v"] is True


def test_request_context_middleware_registered():
    import importlib

    mod = importlib.import_module("app.main")
    app = mod.app

    # FastAPI stores added middleware classes in app.user_middleware
    names = [m.cls.__name__ for m in app.user_middleware]
    assert "RequestContextMiddleware" in names


def get_paths(app):
    from fastapi.routing import APIRoute

    return {route.path for route in app.routes if isinstance(route, APIRoute)}


def test_routers_registered():
    # from app.main import app
    import importlib

    mod = importlib.import_module("app.main")
    app = mod.app

    paths = get_paths(app)

    assert any(p.startswith("/cards") for p in paths)
    assert any(p.startswith("/decks") for p in paths)
    assert any(p.startswith("/reviews") for p in paths)
