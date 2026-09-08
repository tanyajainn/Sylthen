from typing import Any

from .rules import analyze_event
from .scoring import calculate_risk


def analyze_events(events: list[dict[str, Any]]) -> dict[str, Any]:
    """Analyze a collection of authorized SYLTHEN lab events."""

    findings = []
    seen_rules = set()

    for event in events:
        event_findings = analyze_event(event)

        for finding in event_findings:
            if finding.rule_id not in seen_rules:
                findings.append(finding)
                seen_rules.add(finding.rule_id)

    risk = calculate_risk(findings)

    return {
        "risk": risk,
        "findings": findings,
        "events_analyzed": len(events),
    }
