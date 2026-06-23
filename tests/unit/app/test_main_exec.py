from fastapi.testclient import TestClient

from app.main import main


def test_root_endpoint_returns_expected():
    from app.main import app

    client = TestClient(app)
    res = client.get("/")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "running"
    assert "service" in data
    assert "env" in data


def test_running_module_calls_uvicorn_run(monkeypatch):
    called = {}

    def fake_run(*args, **kwargs):
        called["args"] = args
        called["kwargs"] = kwargs

    # patch uvicorn.run so the real server doesn't start
    monkeypatch.setattr("uvicorn.run", fake_run)

    # execute the module as __main__ which should invoke uvicorn.run
    main()

    assert "args" in called or "kwargs" in called
    # the code calls uvicorn.run("app.main:app", ...)
    if called.get("args"):
        assert called["args"][0] == "app.main:app"
    else:
        assert called["kwargs"].get("app") == "app.main:app"
