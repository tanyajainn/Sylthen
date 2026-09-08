import sqlite3
from pathlib import Path


DATABASE_PATH = Path("data") / "sylthen.db"


class Database:
    """SQLite storage for encrypted SYLTHEN telemetry."""

    def __init__(self, path: Path = DATABASE_PATH):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(self.path)

        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS telemetry (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                algorithm TEXT NOT NULL,
                nonce TEXT NOT NULL,
                ciphertext TEXT NOT NULL,
                aad TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        self.connection.commit()

    def insert_event(self, encrypted_event: dict[str, str]) -> int:
        cursor = self.connection.execute(
            """
            INSERT INTO telemetry
            (algorithm, nonce, ciphertext, aad)
            VALUES (?, ?, ?, ?)
            """,
            (
                encrypted_event["algorithm"],
                encrypted_event["nonce"],
                encrypted_event["ciphertext"],
                encrypted_event["aad"],
            ),
        )

        self.connection.commit()
        return cursor.lastrowid

    def get_event(self, event_id: int) -> dict[str, str] | None:
        cursor = self.connection.execute(
            """
            SELECT algorithm, nonce, ciphertext, aad
            FROM telemetry
            WHERE id = ?
            """,
            (event_id,),
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return {
            "algorithm": row[0],
            "nonce": row[1],
            "ciphertext": row[2],
            "aad": row[3],
        }

    def count(self) -> int:
        cursor = self.connection.execute(
            "SELECT COUNT(*) FROM telemetry"
        )

        return cursor.fetchone()[0]

    def close(self) -> None:
        self.connection.close()