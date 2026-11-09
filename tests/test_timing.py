from backend.detection.engine import analyze_events
from backend.telemetry.timing import KeyTiming


def test_detector_uses_measured_hold_duration():
    timing = KeyTiming()
    for duration, expected in [(25, ["SYL-KB-001"]), (40, []), (125, [])]:
        timing.press(65, "a", 100)
        data = timing.release(65, 100 + duration)
        assert data == {"action": "UP", "key_category": "ALPHANUMERIC", "dwell_ms": duration}
        result = analyze_events([{"event_type": "key_event", "data": data}])
        assert [finding.rule_id for finding in result["findings"]] == expected


def test_overlap_repeat_and_focus_loss():
    timing = KeyTiming()
    timing.press(65, "a", 100)
    timing.press(65, "a", 130)
    timing.press(32, "space", 150)
    assert timing.release(65, 180)["dwell_ms"] == 80
    timing.clear()
    assert timing.release(32, 200) is None


def test_timestamp_rollover():
    timing = KeyTiming()
    timing.press(9, "Tab", 2**32 - 10)
    assert timing.release(9, 20)["dwell_ms"] == 30
