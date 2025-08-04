import sqlite3
from datetime import datetime

def init_db (db_path='metric.db'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS system_metrics (
            timestamp TEXT,
            cpu_percent REAL,
            memory_percent REAL,
            disk_percent REAL,
            log_error_count INTEGER)'''
    )

    conn.commit()
    conn.close()

def insert_metrics(metrics, db_path='metric.db'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    timestamp = datetime.now().isoformat()
    cursor.execute('''
        INSERT INTO system_metrics (timestamp, cpu_percent, memory_percent, disk_percent, log_error_count)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        timestamp,
        metrics.get('cpu_percent'),
        metrics.get('memory_percent'),
        metrics.get('disk_percent'),
        metrics.get('log_error_count')

    ))

    conn.commit()
    conn.close()

init_db()