import logging as pylogging

from app.core import logging as core_logging


def test_request_id_filter_sets_request_id(monkeypatch):
    # Ensure the filter will use our test value
    monkeypatch.setattr(core_logging, "get_request_id", lambda: "req-xyz")

    filt = core_logging.RequestIdFilter()

    # create a LogRecord to pass to the filter
    record = pylogging.LogRecord(
        name="test",
        level=pylogging.INFO,
        pathname=__file__,
        lineno=1,
        msg="x",
        args=(),
        exc_info=None,
    )

    result = filt.filter(record)

    assert result is True
    assert hasattr(record, "request_id")
    assert record.request_id == "req-xyz"


def test_setup_logging_adds_stream_handler_and_filter():
    root = pylogging.getLogger()
    # snapshot existing handlers
    existing = list(root.handlers)
    try:
        core_logging.setup_logging()

        # find newly added handlers
        new_handlers = [h for h in root.handlers if h not in existing]
        assert new_handlers, "setup_logging did not add any handlers"

        # find a StreamHandler among them
        stream_handlers = [h for h in new_handlers if isinstance(h, pylogging.StreamHandler)]
        assert stream_handlers, "no StreamHandler added"

        handler = stream_handlers[0]
        # formatter should include request_id placeholder
        fmt = handler.formatter._fmt if handler.formatter is not None else ""
        assert "request_id=%(request_id)s" in fmt

        # handler should have RequestIdFilter attached
        filters = handler.filters
        assert any(isinstance(f, core_logging.RequestIdFilter) for f in filters)

        # root level should be INFO
        assert root.level == pylogging.INFO
    finally:
        # restore original handlers to avoid side effects for other tests
        root.handlers[:] = existing
