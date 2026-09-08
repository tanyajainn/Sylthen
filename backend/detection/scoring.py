from typing import Any

from .rules import DetectionResult


def calculate_risk(findings: list[DetectionResult]) -> dict[str, Any]:
    """Calculate an overall risk score from detection findings."""

    score = sum(finding.score for finding in findings)

    if score >= 70:
        severity = "CRITICAL"
    elif score >= 40:
        severity = "HIGH"
    elif score >= 20:
        severity = "MEDIUM"
    elif score > 0:
        severity = "LOW"
    else:
        severity = "NONE"

    return {
        "score": min(score, 100),
        "severity": severity,
        "finding_count": len(findings),
    }