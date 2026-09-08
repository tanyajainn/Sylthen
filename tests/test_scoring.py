from backend.detection.rules import DetectionResult
from backend.detection.scoring import calculate_risk


def test_no_findings():
    result = calculate_risk([])

    assert result["score"] == 0
    assert result["severity"] == "NONE"
    assert result["finding_count"] == 0


def test_medium_risk():
    findings = [
        DetectionResult(
            rule_id="TEST-001",
            severity="MEDIUM",
            score=25,
            title="Test finding",
            description="Test description",
        )
    ]

    result = calculate_risk(findings)

    assert result["score"] == 25
    assert result["severity"] == "MEDIUM"


def test_high_risk():
    findings = [
        DetectionResult(
            rule_id="TEST-001",
            severity="HIGH",
            score=40,
            title="Test finding",
            description="Test description",
        )
    ]

    result = calculate_risk(findings)

    assert result["score"] == 40
    assert result["severity"] == "HIGH"