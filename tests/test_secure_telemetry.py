from backend.crypto.encryption import generate_key
from backend.telemetry.secure_collector import SecureTelemetryCollector


def test_secure_telemetry_round_trip():
    key = generate_key()

    collector = SecureTelemetryCollector(
        session_id="lab-secure-001",
        key=key,
    )

    encrypted = collector.record(
        event_type="key_event",
        data={
            "key_category": "ALPHANUMERIC",
            "action": "DOWN",
            "dwell_ms": 91,
        },
    )

    decrypted = collector.decrypt(encrypted)

    assert decrypted["session_id"] == "lab-secure-001"
    assert decrypted["event_type"] == "key_event"
    assert decrypted["data"]["dwell_ms"] == 91
    assert collector.count() == 1


def test_ciphertext_does_not_contain_plaintext():
    key = generate_key()

    collector = SecureTelemetryCollector(
        session_id="lab-secure-002",
        key=key,
    )

    encrypted = collector.record(
        event_type="key_event",
        data={
            "key_category": "ALPHANUMERIC",
            "action": "DOWN",
        },
    )

    assert "ALPHANUMERIC" not in encrypted["ciphertext"]