from collections import Counter
from typing import Any


def analyze_behavior(events: list[dict[str, Any]]) -> dict[str, Any]:
    """Analyze behavioral patterns across an authorized lab session."""

    event_types = Counter(
        event.get("event_type", "unknown")
        for event in events
    )

    total_events = len(events)

    key_events = event_types.get("key_event", 0)
    network_events = event_types.get("network_event", 0)
    screenshot_events = event_types.get("screenshot_event", 0)

    return {
        "total_events": total_events,
        "event_types": dict(event_types),
        "key_event_count": key_events,
        "network_event_count": network_events,
        "screenshot_event_count": screenshot_events,
        "behavior_flags": {
            "input_activity": key_events > 0,
            "network_activity": network_events > 0,
            "screen_activity": screenshot_events > 0,
        },
    }