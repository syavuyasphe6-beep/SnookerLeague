import os
import psycopg


def get_connection():

    database_url = os.environ.get("DATABASE_URL")

    if not database_url:
        raise Exception("DATABASE_URL environment variable is not set")

    return psycopg.connect(database_url)


def initialize_database():

    connection = get_connection()
    cursor = connection.cursor()

    # ==========================================
    # PLAYERS TABLE
    # ==========================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS players (
        id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        name TEXT NOT NULL UNIQUE
    )
    """)

    # ==========================================
    # MATCHES TABLE
    # ==========================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS matches (
        id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        player1_id INTEGER NOT NULL,
        player2_id INTEGER NOT NULL,
        player1_score INTEGER NOT NULL,
        player2_score INTEGER NOT NULL,

        FOREIGN KEY (player1_id) REFERENCES players(id),
        FOREIGN KEY (player2_id) REFERENCES players(id)
    )
    """)

    # ==========================================
    # FIXTURES TABLE
    # ==========================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS fixtures (
        id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        player1_id INTEGER NOT NULL,
        player2_id INTEGER NOT NULL,
        match_date TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'Scheduled',

        FOREIGN KEY (player1_id) REFERENCES players(id),
        FOREIGN KEY (player2_id) REFERENCES players(id)
    )
    """)

    connection.commit()

    cursor.close()
    connection.close()