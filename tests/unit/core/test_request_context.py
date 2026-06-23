import threading

from app.core.request_context import get_request_id, set_request_id


def test_default_request_id_is_none():
    # fresh import should start with default None
    assert get_request_id() is None


def test_set_and_get_request_id():
    set_request_id("req-123")
    assert get_request_id() == "req-123"


def test_contextvar_is_isolated_between_threads():
    set_request_id("main-thread")

    results = {}

    def worker():
        # new thread should start with the ContextVar default (None)
        results["before"] = get_request_id()
        set_request_id("worker-thread")
        results["after"] = get_request_id()

    t = threading.Thread(target=worker)
    t.start()
    t.join()

    # thread saw default then its own value
    assert results["before"] is None
    assert results["after"] == "worker-thread"

    # main thread still has its value
    assert get_request_id() == "main-thread"
