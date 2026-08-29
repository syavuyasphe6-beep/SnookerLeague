import sqlite3


def calculate_standings():

    connection = sqlite3.connect("snooker.db")
    cursor = connection.cursor()

    cursor.execute("""
    SELECT id, name
    FROM players
    """)

    players = cursor.fetchall()

    standings = []

    for player in players:

        player_id = player[0]
        player_name = player[1]

        cursor.execute("""
        SELECT
            player1_id,
            player2_id,
            player1_score,
            player2_score
        FROM matches
        WHERE player1_id = ? OR player2_id = ?
        """, (
            player_id,
            player_id
        ))

        matches = cursor.fetchall()

        matches_played = 0
        wins = 0
        losses = 0
        goals_for = 0
        goals_against = 0
        points = 0

        for match in matches:

            player1_id = match[0]
            player2_id = match[1]

            player1_score = match[2]
            player2_score = match[3]

            matches_played += 1

            if player_id == player1_id:

                goals_for += player1_score
                goals_against += player2_score

                if player1_score > player2_score:
                    wins += 1
                    points += 3
                else:
                    losses += 1

            else:

                goals_for += player2_score
                goals_against += player1_score

                if player2_score > player1_score:
                    wins += 1
                    points += 3
                else:
                    losses += 1

        goal_difference = goals_for - goals_against

        standings.append({
            "name": player_name,
            "matches_played": matches_played,
            "wins": wins,
            "losses": losses,
            "goals_for": goals_for,
            "goals_against": goals_against,
            "goal_difference": goal_difference,
            "points": points
        })

    connection.close()

    standings.sort(
        key=lambda player: (
            player["points"],
            player["goal_difference"],
            player["name"]
        ),
        reverse=True
    )

    return standings