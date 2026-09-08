from backend.crypto.encryption import generate_key
from backend.database.database import Database
from backend.telemetry.secure_collector import SecureTelemetryCollector
from backend.detection.engine import analyze_events
from backend.detection.report import format_report


def main():
    print("=" * 50)
    print("SYLTHEN — LAB TELEMETRY DEMO")
    print("=" * 50)

    key = generate_key()
    database = Database()

    collector = SecureTelemetryCollector(
        session_id="demo-session-001",
        key=key,
    )

    events = [
        (
            "session_event",
            {"state": "STARTED"},
        ),
        (
            "key_event",
            {
                "key_category": "ALPHANUMERIC",
                "action": "DOWN",
                "dwell_ms": 25,
            },
        ),
        (
            "network_event",
            {
                "destination_type": "SIMULATED_C2",
            },
        ),
        (
            "focus_event",
            {"state": "ACTIVE"},
        ),
    ]

    print("\n[1] Generating lab telemetry...")

    decrypted_events = []

    for event_type, data in events:
        encrypted = collector.record(event_type, data)
        event_id = database.insert_event(encrypted)

        decrypted_events.append(
            collector.decrypt(encrypted)
        )

        print(
            f"  ✓ {event_type:<20}"
            f" encrypted → database ID {event_id}"
        )

    print("\n[2] Running detection engine...")

    result = analyze_events(decrypted_events)

    print(format_report(result))

    database.close()

    print("\nSYLTHEN CORE DEMO COMPLETE.")
    print("=" * 50)


if __name__ == "__main__":
    main()