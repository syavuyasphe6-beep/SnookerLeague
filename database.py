import sqlite3


def initialize_database():

    connection = sqlite3.connect("snooker.db")
    cursor = connection.cursor()


    # ==========================================
    # PLAYERS TABLE
    # ==========================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS players (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    )
    """)


    # ==========================================
    # MATCHES TABLE
    # ==========================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS matches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
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
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        player1_id INTEGER NOT NULL,
        player2_id INTEGER NOT NULL,
        match_date TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'Scheduled',

        FOREIGN KEY (player1_id) REFERENCES players(id),
        FOREIGN KEY (player2_id) REFERENCES players(id)
    )
    """)


    connection.commit()
    connection.close()