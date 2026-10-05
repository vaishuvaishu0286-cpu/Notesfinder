import sqlite3

DB_NAME = "notes.db"


def create_database():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            file_type TEXT NOT NULL,
            file_data BLOB NOT NULL,
            extracted_text TEXT
        )
    """)

    conn.commit()
    conn.close()


def add_note(filename, file_type, file_data, extracted_text):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    # Avoid saving the exact same filename again
    cursor.execute(
        "SELECT id FROM notes WHERE filename = ?",
        (filename,)
    )

    existing = cursor.fetchone()

    if existing:
        conn.close()
        return False

    cursor.execute("""
        INSERT INTO notes
        (filename, file_type, file_data, extracted_text)
        VALUES (?, ?, ?, ?)
    """, (
        filename,
        file_type,
        file_data,
        extracted_text
    ))

    conn.commit()
    conn.close()

    return True


def search_notes(keyword):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            filename,
            file_type,
            file_data,
            extracted_text
        FROM notes
        WHERE LOWER(extracted_text) LIKE LOWER(?)
        ORDER BY id DESC
    """, (
        "%" + keyword + "%",
    ))

    results = cursor.fetchall()

    conn.close()

    return results


def get_all_notes():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            filename,
            file_type,
            file_data,
            extracted_text
        FROM notes
        ORDER BY id DESC
    """)

    results = cursor.fetchall()

    conn.close()

    return results