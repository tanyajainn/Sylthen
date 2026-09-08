from pathlib import Path

from backend.crypto.encryption import generate_key
from backend.database.database import Database
from backend.telemetry.secure_collector import SecureTelemetryCollector


def test_encrypted_event_is_stored(tmp_path: Path):
    database = Database(tmp_path / "test.db")
    key = generate_key()

    collector = SecureTelemetryCollector(
        session_id="db-test-001",
        key=key,
    )

    encrypted = collector.record(
        event_type="key_event",
        data={
            "key_category": "ALPHANUMERIC",
            "action": "DOWN",
        },
    )

    event_id = database.insert_event(encrypted)

    stored = database.get_event(event_id)

    assert stored is not None
    assert stored["algorithm"] == "AES-256-GCM"
    assert stored["ciphertext"] == encrypted["ciphertext"]
    assert database.count() == 1

    database.close()