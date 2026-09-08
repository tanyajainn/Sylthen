from typing import Any

from .rules import analyze_event
from .scoring import calculate_risk


def analyze_events(events: list[dict[str, Any]]) -> dict[str, Any]:
    """Analyze a collection of authorized SYLTHEN lab events."""

    findings = []

    for event in events:
        findings.extend(analyze_event(event))

    risk = calculate_risk(findings)

    return {
        "risk": risk,
        "findings": findings,
        "events_analyzed": len(events),
    }