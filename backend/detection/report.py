from typing import Any


def format_report(result: dict[str, Any]) -> str:
    """Create a human-readable SYLTHEN security analysis report."""

    risk = result["risk"]
    findings = result["findings"]

    lines = [
        "",
        "=" * 60,
        "SYLTHEN SECURITY ANALYSIS",
        "=" * 60,
        f"Events analyzed: {result['events_analyzed']}",
        "",
        f"Risk Score: {risk['score']}/100",
        f"Severity:   {risk['severity']}",
        f"Findings:   {risk['finding_count']}",
        "",
        "DETECTIONS",
        "-" * 60,
    ]

    if not findings:
        lines.append("No suspicious activity detected.")
    else:
        for finding in findings:
            lines.append(
                f"[{finding.severity:<8}] "
                f"{finding.title} "
                f"(+{finding.score})"
            )
            lines.append(f"           {finding.description}")

    lines.extend([
        "",
        "=" * 60,
    ])

    return "\n".join(lines)