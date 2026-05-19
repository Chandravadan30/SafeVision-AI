import sqlite3
import os
from datetime import datetime
from config import DB_PATH

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    con = sqlite3.connect(DB_PATH)
    con.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            event     TEXT,
            angle     REAL,
            snapshot  TEXT
        )
    """)
    con.commit()
    con.close()
    print("[logger] Database ready")

def log_event(event, angle=None, snapshot_path=None):
    con = sqlite3.connect(DB_PATH)
    con.execute(
        "INSERT INTO events (timestamp, event, angle, snapshot) VALUES (?,?,?,?)",
        (datetime.now().isoformat(), event, angle, snapshot_path)
    )
    con.commit()
    con.close()

def get_recent_events(n=50):
    con = sqlite3.connect(DB_PATH)
    rows = con.execute(
        "SELECT timestamp, event, angle, snapshot FROM events ORDER BY id DESC LIMIT ?",
        (n,)
    ).fetchall()
    con.close()
    return rows
