from dataclasses import dataclass
from typing import Any


@dataclass
class DetectionResult:
    rule_id: str
    severity: str
    score: int
    title: str
    description: str


def analyze_event(event: dict[str, Any]) -> list[DetectionResult]:
    """
    Analyze one authorized SYLTHEN lab event.

    This detector works on simulated lab telemetry and does not
    inspect real user input or system activity.
    """

    findings: list[DetectionResult] = []

    event_type = event.get("event_type")
    data = event.get("data", {})

    # Rule 1: High-frequency simulated key activity
    if event_type == "key_event":
        dwell_ms = data.get("dwell_ms", 0)

        if dwell_ms and dwell_ms < 40:
            findings.append(
                DetectionResult(
                    rule_id="SYL-KB-001",
                    severity="MEDIUM",
                    score=25,
                    title="High-frequency key activity",
                    description=(
                        "The lab telemetry contains unusually "
                        "rapid simulated key activity."
                    ),
                )
            )

    # Rule 2: Suspicious combination of event categories
    if event_type == "network_event":
        if data.get("destination_type") == "SIMULATED_C2":
            findings.append(
                DetectionResult(
                    rule_id="SYL-NET-001",
                    severity="HIGH",
                    score=40,
                    title="Simulated C2 communication",
                    description=(
                        "The lab generated a network event marked "
                        "as simulated command-and-control traffic."
                    ),
                )
            )

    # Rule 3: Simulated screenshot activity
    if event_type == "screenshot_event":
        if data.get("authorized") is True:
            findings.append(
                DetectionResult(
                    rule_id="SYL-SCR-001",
                    severity="MEDIUM",
                    score=30,
                    title="Simulated screenshot activity",
                    description=(
                        "The lab generated an authorized simulated "
                        "screenshot event."
                    ),
                )
            )

    return findings