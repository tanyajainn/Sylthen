from backend.detection.rules import analyze_event


def test_normal_key_event_has_no_finding():
    event = {
        "event_type": "key_event",
        "data": {
            "key_category": "ALPHANUMERIC",
            "action": "DOWN",
            "dwell_ms": 84,
        },
    }

    findings = analyze_event(event)

    assert findings == []


def test_rapid_key_activity_is_detected():
    event = {
        "event_type": "key_event",
        "data": {
            "key_category": "ALPHANUMERIC",
            "action": "DOWN",
            "dwell_ms": 25,
        },
    }

    findings = analyze_event(event)

    assert len(findings) == 1
    assert findings[0].rule_id == "SYL-KB-001"
    assert findings[0].severity == "MEDIUM"
    assert findings[0].score == 25


def test_simulated_c2_is_detected():
    event = {
        "event_type": "network_event",
        "data": {
            "destination_type": "SIMULATED_C2",
        },
    }

    findings = analyze_event(event)

    assert len(findings) == 1
    assert findings[0].rule_id == "SYL-NET-001"
    assert findings[0].severity == "HIGH"
    assert findings[0].score == 40