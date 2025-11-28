import sqlite3
DB_NAME="detections.db"

def create_tables():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS detections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            image_path TEXT,
            people_count INTEGER NOT NULL,
            confidence REAL
        )
    """)

    conn.commit()
    conn.close()


def log_event(timestamp, image_path, people_count, confidence):
    conn = sqlite3.connect(DB_NAME)
    conn.execute(
        "INSERT INTO detections (timestamp, image_path, people_count, confidence) VALUES (?, ?, ?, ?)",
        (timestamp, image_path, people_count, confidence)
    )
    conn.commit()
    conn.close()


create_tables()