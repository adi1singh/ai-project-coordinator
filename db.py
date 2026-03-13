import sqlite3


DB_NAME = "tasks.db"


def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_name TEXT NOT NULL,
            owner TEXT,
            due_date TEXT,
            priority TEXT,
            blocker TEXT,
            status TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_tasks(tasks):
    conn = get_connection()
    cursor = conn.cursor()

    for task in tasks:
        cursor.execute("""
            INSERT INTO tasks (task_name, owner, due_date, priority, blocker, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            task.get("task_name", ""),
            task.get("owner", ""),
            task.get("due_date", ""),
            task.get("priority", ""),
            task.get("blocker", ""),
            task.get("status", "Open")
        ))

    conn.commit()
    conn.close()


def get_all_tasks():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, task_name, owner, due_date, priority, blocker, status
        FROM tasks
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()
    conn.close()
    return rows