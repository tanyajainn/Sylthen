from typing import Any

from backend.crypto.encryption import encrypt_event, decrypt_event
from backend.telemetry.collector import TelemetryCollector


class SecureTelemetryCollector:
    """Collects and encrypts authorized SYLTHEN lab telemetry."""

    def __init__(self, session_id: str, key: bytes):
        self.collector = TelemetryCollector(session_id)
        self.key = key
        self.encrypted_events: list[dict[str, str]] = []

    def record(
        self,
        event_type: str,
        data: dict[str, Any] | None = None,
    ) -> dict[str, str]:

        event = self.collector.record(event_type, data)

        encrypted = encrypt_event(
            event.model_dump(mode="json"),
            self.key,
        )

        self.encrypted_events.append(encrypted)
        return encrypted

    def decrypt(self, encrypted_event: dict[str, str]) -> dict[str, Any]:
        """Decrypt an authorized SYLTHEN lab event."""
        return decrypt_event(encrypted_event, self.key)

    def count(self) -> int:
        return len(self.encrypted_events)