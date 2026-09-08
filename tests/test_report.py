from backend.detection.engine import analyze_events
from backend.detection.report import format_report


def test_security_report_contains_risk_information():
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
    report = format_report(result)

    assert "SYLTHEN SECURITY ANALYSIS" in report
    assert "Risk Score: 65/100" in report
    assert "Severity:   HIGH" in report
    assert "High-frequency key activity" in report
    assert "Simulated C2 communication" in report