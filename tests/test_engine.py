from backend.detection.engine import analyze_events


def test_engine_detects_suspicious_activity():
    events = [
        {
            "event_type": "key_event",
            "data": {
                "key_category": "ALPHANUMERIC",
                "action": "DOWN",
                "dwell_ms": 25,
            },
        },
        {
            "event_type": "network_event",
            "data": {
                "destination_type": "SIMULATED_C2",
            },
        },
    ]

    result = analyze_events(events)

    assert result["events_analyzed"] == 2
    assert result["risk"]["score"] == 65
    assert result["risk"]["severity"] == "HIGH"
    assert len(result["findings"]) == 2