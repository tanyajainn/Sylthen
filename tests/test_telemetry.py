from backend.telemetry.collector import TelemetryCollector


def test_record_lab_event():
    collector = TelemetryCollector("lab-session-001")

    event = collector.record(
        event_type="key_event",
        data={
            "key_category": "ALPHANUMERIC",
            "action": "DOWN",
            "dwell_ms": 84,
        },
    )

    assert event.session_id == "lab-session-001"
    assert event.event_type == "key_event"
    assert event.data["key_category"] == "ALPHANUMERIC"
    assert collector.count() == 1


def test_multiple_events():
    collector = TelemetryCollector("lab-session-002")

    collector.record("key_event", {"key_category": "ALPHANUMERIC"})
    collector.record("focus_event", {"state": "ACTIVE"})
    collector.record("session_event", {"state": "STARTED"})

    assert collector.count() == 3