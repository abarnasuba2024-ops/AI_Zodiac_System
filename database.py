import sqlite3


def create_database():

    connection = sqlite3.connect("zodiac.db")

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            dob TEXT,
            zodiac TEXT,
            personality TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


def save_user(
        name,
        dob,
        zodiac,
        personality
):

    connection = sqlite3.connect("zodiac.db")

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO users
        (name, dob, zodiac, personality)
        VALUES (?, ?, ?, ?)
    """, (
        name,
        dob,
        zodiac,
        personality
    ))

    connection.commit()
    connection.close()


def get_users():

    connection = sqlite3.connect("zodiac.db")

    cursor = connection.cursor()

    cursor.execute("""
        SELECT name, dob, zodiac, personality, created_at
        FROM users
        ORDER BY id DESC
    """)

    data = cursor.fetchall()

    connection.close()

    return data