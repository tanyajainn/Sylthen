import tkinter as tk
from tkinter import messagebox
from uuid import uuid4

from backend.crypto.encryption import generate_key
from backend.database.database import Database
from backend.telemetry.timing import KeyTiming
from backend.telemetry.secure_collector import SecureTelemetryCollector
from backend.detection.engine import analyze_events
from backend.detection.report import format_report


def main():
    key = generate_key()
    database = Database()

    collector = SecureTelemetryCollector(
        session_id=f"lab-{uuid4()}",
        key=key,
    )

    root = tk.Tk()
    root.title("SYLTHEN — Keylogger Lab")
    root.geometry("650x450")

    tk.Label(
        root,
        text="SYLTHEN",
        font=("Arial", 24, "bold"),
    ).pack(pady=(25, 5))

    tk.Label(
        root,
        text="Authorized Keylogger Simulation",
        font=("Arial", 13),
    ).pack()

    tk.Label(
        root,
        text="Type ONLY in the box below. Events are encrypted and stored locally.",
        wraplength=550,
    ).pack(pady=20)

    text_box = tk.Text(
        root,
        height=8,
        width=65,
        font=("Consolas", 12),
    )
    text_box.pack()

    status = tk.Label(root, text="Ready")
    status.pack(pady=10)

    events = []

    timing = KeyTiming()

    def press(event):
        timing.press(event.keycode, event.keysym, event.time)

    def release(event):
        data = timing.release(event.keycode, event.time)
        if data is None:
            return
        encrypted = collector.record("key_event", data)
        event_id = database.insert_event(encrypted)
        decrypted = collector.decrypt(encrypted)
        events.append(decrypted)

        status.config(
            text=f"Captured lab event #{len(events)} → database ID {event_id}"
        )

    def analyze():
        if not events:
            messagebox.showinfo(
                "SYLTHEN",
                "Type something in the lab box first."
            )
            return

        result = analyze_events(events)

        print("\n" + "=" * 60)
        print("SYLTHEN SECURITY ANALYSIS")
        print("=" * 60)
        print(f"Events analyzed: {len(events)}")
        print()
        print(format_report(result))

        messagebox.showinfo(
            "SYLTHEN Analysis",
            f"Events analyzed: {len(events)}\n\n"
            f"{format_report(result)}"
        )

    def finish():
        database.close()
        root.destroy()

    text_box.bind("<KeyPress>", press)
    text_box.bind("<KeyRelease>", release)
    text_box.bind("<FocusOut>", lambda event: timing.clear())

    tk.Button(
        root,
        text="Run Security Analysis",
        command=analyze,
        width=25,
        height=2,
    ).pack(pady=15)

    tk.Button(
        root,
        text="Exit",
        command=finish,
        width=15,
    ).pack()

    text_box.focus_set()
    root.protocol("WM_DELETE_WINDOW", finish)

    root.mainloop()


if __name__ == "__main__":
    main()
