import sqlite3
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database path
DB_NAME = os.getenv("DATABASE_NAME", "detections.db")
DB_PATH = os.path.join(os.path.dirname(__file__), DB_NAME)


def get_connection():
    """Create a database connection with proper settings"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # this allows accessing columns by name
    return conn


def create_tables():
    """Create database tables if they don't exist"""
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
    print(" Database tables created successfully")


def log_event(timestamp, image_path, people_count, confidence):
    """Log a detection event to the database"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO detections (timestamp, image_path, people_count, confidence) VALUES (?, ?, ?, ?)",
        (timestamp, image_path, people_count, confidence)
    )
    conn.commit()
    conn.close()


def get_all_detections(limit=100):
    """Retrieve detection history"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM detections ORDER BY timestamp DESC LIMIT ?",
        (limit,)
    )
    results = cursor.fetchall()
    conn.close()
    return results


def get_detection_stats():
    """Get summary statistics"""
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


# Initialize database on module import
create_tables()


if __name__ == "__main__":
    # Test the database
    print("Testing database functions...")
    from datetime import datetime
    
    # Test log_event
    test_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_event(test_timestamp, "test.jpg", 2, 0.85)
    print("Test event logged")
    
    # Test get_all_detections
    detections = get_all_detections(5)
    print(f"Retrieved {len(detections)} detections")
    
    # Test get_detection_stats
    stats = get_detection_stats()
    print(f"Stats: {dict(stats) if stats else 'No data'}")