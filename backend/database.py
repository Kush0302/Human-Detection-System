import sqlite3
import os
DB_PATH=os.path.join(os.path.dirname(__file__), "detections.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  #this allows accessing columns by name
    return conn

def create_tables():
    conn = get_connection()
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
    print("Database tables created successfully")

def get_l_detections(limit=100):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.exexute(
        "SELECT * FROM detectionsORDER BY timestamp DESC LIMIT ?",
        (limit,)
    )
    results = cursor.fetchall()
    conn.close()
    return results

def get_detection_stats():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            COUNT(*) as total_detections,
            SUM(people_count) as total_people,
            AVG(people_count) as avg_people,
            MAX(people_count) as max_people,
            AVG(confidence) as avg_confidence
        FROM detections
    """)
    stats = cursor.fetchone()
    conn.close()
    return stats

if __name__ == "__main__":
    create_tables()