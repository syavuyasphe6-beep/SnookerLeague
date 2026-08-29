import sqlite3


# ==========================================
# CONNECT TO DATABASE
# ==========================================

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


players = [
    "Siyavuya Mkhize",
    "Sphumelele Ngidi",
    "Wandile Zuke",
    "Samkelo Jili"
]


for player in players:
    cursor.execute(
        "INSERT OR IGNORE INTO players (name) VALUES (?)",
        (player,)
    )


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

    UNIQUE(
        player1_id,
        player2_id,
        player1_score,
        player2_score
    ),

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

    UNIQUE(player1_id, player2_id, match_date),

    FOREIGN KEY (player1_id) REFERENCES players(id),
    FOREIGN KEY (player2_id) REFERENCES players(id)
)
""")


# ==========================================
# GENERATE FIXTURES
# ==========================================

def generate_fixtures():

    cursor.execute("SELECT id, name FROM players")

    players = cursor.fetchall()

    match_date = "2026-08-28"

    print("\nGENERATING FIXTURES")
    print("-------------------")

    fixture_number = 1

    for i in range(len(players)):

        for j in range(i + 1, len(players)):

            player1_id = players[i][0]
            player1_name = players[i][1]

            player2_id = players[j][0]
            player2_name = players[j][1]

            cursor.execute("""
            INSERT OR IGNORE INTO fixtures
            (player1_id, player2_id, match_date)
            VALUES (?, ?, ?)
            """, (
                player1_id,
                player2_id,
                match_date
            ))

            print(
                fixture_number,
                ".",
                player1_name,
                "vs",
                player2_name
            )

            fixture_number += 1


generate_fixtures()


# ==========================================
# SAVE DATABASE
# ==========================================

connection.commit()


# ==========================================
# DISPLAY FIXTURES
# ==========================================

cursor.execute("""
SELECT
    fixtures.id,
    p1.name,
    p2.name,
    fixtures.match_date,
    fixtures.status
FROM fixtures
JOIN players AS p1
    ON fixtures.player1_id = p1.id
JOIN players AS p2
    ON fixtures.player2_id = p2.id
ORDER BY fixtures.id
""")


fixtures = cursor.fetchall()


print("\nFIXTURES IN DATABASE")
print("--------------------")


for fixture in fixtures:

    print(
        "Fixture ID:", fixture[0],
        "|",
        fixture[1],
        "vs",
        fixture[2],
        "| Date:",
        fixture[3],
        "| Status:",
        fixture[4]
    )


# ==========================================
# CLOSE DATABASE
# ==========================================

connection.close()





# ==========================================
# RESET TEST RESULTS
# ==========================================

import sqlite3

connection = sqlite3.connect("snooker.db")
cursor = connection.cursor()

# Delete all recorded match results
cursor.execute("DELETE FROM matches")

# Reset all fixtures
cursor.execute("""
UPDATE fixtures
SET status = 'Scheduled'
""")

connection.commit()

print("\n========================================")
print("DATABASE RESET")
print("========================================")

# Check matches
cursor.execute("SELECT COUNT(*) FROM matches")
match_count = cursor.fetchone()[0]

# Check fixtures
cursor.execute("SELECT COUNT(*) FROM fixtures")
fixture_count = cursor.fetchone()[0]

print("Matches remaining:", match_count)
print("Fixtures remaining:", fixture_count)

connection.close()

