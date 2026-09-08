from backend.detection.behavior import analyze_behavior


def test_behavior_analysis():
    events = [
        {"event_type": "session_event", "data": {}},
        {"event_type": "key_event", "data": {}},
        {"event_type": "key_event", "data": {}},
        {"event_type": "network_event", "data": {}},
    ]

    result = analyze_behavior(events)

    assert result["total_events"] == 4
    assert result["key_event_count"] == 2
    assert result["network_event_count"] == 1
    assert result["screenshot_event_count"] == 0
    assert result["behavior_flags"]["input_activity"] is True
    assert result["behavior_flags"]["network_activity"] is True