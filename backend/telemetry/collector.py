from typing import Any

from .events import TelemetryEvent


class TelemetryCollector:
    """Collects authorized SYLTHEN lab telemetry."""

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.events: list[TelemetryEvent] = []

    def record(
        self,
        event_type: str,
        data: dict[str, Any] | None = None,
    ) -> TelemetryEvent:

        event = TelemetryEvent(
            session_id=self.session_id,
            event_type=event_type,
            data=data or {},
        )

        self.events.append(event)
        return event

    def get_events(self) -> list[TelemetryEvent]:
        return self.events

    def count(self) -> int:
        return len(self.events)