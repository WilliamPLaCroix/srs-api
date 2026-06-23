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


# def test_routers_registered():
#     # Verify router modules expose routers and app included health router
#     import importlib

#     mod = importlib.import_module("app.main")
#     app = mod.app

#     # Ensure router modules exist and expose a router with routes
#     cards_mod = importlib.import_module("app.modules.cards.router")
#     decks_mod = importlib.import_module("app.modules.decks.router")
#     reviews_mod = importlib.import_module("app.modules.reviews.router")

#     assert hasattr(cards_mod, "router") and len(cards_mod.router.routes) > 0
#     assert hasattr(decks_mod, "router") and len(decks_mod.router.routes) > 0
#     assert hasattr(reviews_mod, "router") and len(reviews_mod.router.routes) > 0

#     # Rather than introspecting FastAPI internals (which can vary between
#     # FastAPI versions), verify inclusion by performing a real request against
#     # the core health endpoint. This ensures the router was registered and
#     # the endpoint is reachable.
#     from fastapi.testclient import TestClient

#     client = TestClient(app)
#     resp = client.get("/core/health")
#     assert resp.status_code == 200


def test_app_health_route():
    from fastapi.testclient import TestClient

    from app.main import app

    client = TestClient(app)
    assert client.get("/core/health").status_code == 200


def test_main_exec_invokes_uvicorn(monkeypatch):
    """Running app.main as __main__ should call uvicorn.run — patch uvicorn
    with a fake module so the server does not actually start."""
    import runpy
    import sys
    import types

    called = {}

    def fake_run(app_arg, **kwargs):
        called["app_arg"] = app_arg
        called["kwargs"] = kwargs

    fake_uvicorn = types.SimpleNamespace(run=fake_run)
    # Ensure the module loader will import our fake uvicorn
    monkeypatch.setitem(sys.modules, "uvicorn", fake_uvicorn)

    # Execute the module as __main__ which triggers the if __name__ == '__main__' block
    runpy.run_module("app.main", run_name="__main__")

    assert called.get("app_arg") == "app.main:app"
    assert isinstance(called.get("kwargs"), dict)
