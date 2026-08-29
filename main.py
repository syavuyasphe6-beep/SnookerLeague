import sqlite3


# ==========================================
# SHOW FIXTURES
# ==========================================

def show_fixtures():

    connection = sqlite3.connect("snooker.db")
    cursor = connection.cursor()

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

    print("\n========================================")
    print("              FIXTURES")
    print("========================================")

    for fixture in fixtures:

        print(
            fixture[0],
            ".",
            fixture[1],
            "vs",
            fixture[2],
            "|",
            fixture[3],
            "|",
            fixture[4]
        )

    connection.close()


# ==========================================
# ENTER RESULT
# ==========================================

def enter_result():

    connection = sqlite3.connect("snooker.db")
    cursor = connection.cursor()

    show_fixtures()

    print("\n========================================")
    print("          ENTER MATCH RESULT")
    print("========================================")

    fixture_id = int(
        input("Enter Fixture ID: ")
    )


    # Find fixture
    cursor.execute("""
    SELECT
        fixtures.id,
        fixtures.player1_id,
        fixtures.player2_id,
        p1.name,
        p2.name,
        fixtures.status
    FROM fixtures
    JOIN players AS p1
        ON fixtures.player1_id = p1.id
    JOIN players AS p2
        ON fixtures.player2_id = p2.id
    WHERE fixtures.id = ?
    """, (fixture_id,))


    fixture = cursor.fetchone()


    # Check fixture exists
    if fixture is None:

        print("\n❌ Fixture not found.")

        connection.close()

        return


    # Check if already completed
    if fixture[5] == "Completed":

        print("\n❌ This fixture has already been completed.")

        connection.close()

        return


    player1_id = fixture[1]
    player2_id = fixture[2]

    player1_name = fixture[3]
    player2_name = fixture[4]


    print("\n")
    print(player1_name, "vs", player2_name)


    # Enter scores
    player1_score = int(
        input(player1_name + " score: ")
    )

    player2_score = int(
        input(player2_name + " score: ")
    )


    # Make sure the scores are not negative
    if player1_score < 0 or player2_score < 0:

        print("\n❌ Score cannot be negative.")

        connection.close()

        return


    # Make sure the game is not a draw
    if player1_score == player2_score:

        print("\n❌ A snooker match cannot end in a draw.")

        connection.close()

        return


    # Save match result
    cursor.execute("""
    INSERT INTO matches
    (player1_id, player2_id, player1_score, player2_score)
    VALUES (?, ?, ?, ?)
    """, (
        player1_id,
        player2_id,
        player1_score,
        player2_score
    ))


    # Mark fixture as completed
    cursor.execute("""
    UPDATE fixtures
    SET status = 'Completed'
    WHERE id = ?
    """, (fixture_id,))


    connection.commit()

    connection.close()


    print("\n✅ RESULT SAVED!")

    print(
        player1_name,
        player1_score,
        "-",
        player2_score,
        player2_name
    )


# ==========================================
# CALCULATE STANDINGS
# ==========================================

def calculate_standings():

    connection = sqlite3.connect("snooker.db")
    cursor = connection.cursor()


    # Get all players
    cursor.execute("""
    SELECT id, name
    FROM players
    """)

    players = cursor.fetchall()


    standings = []


    # Calculate each player's statistics
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


        # Go through every match
        for match in matches:

            player1_id = match[0]
            player2_id = match[1]

            player1_score = match[2]
            player2_score = match[3]


            matches_played += 1


            # If our player is Player 1
            if player_id == player1_id:

                goals_for += player1_score
                goals_against += player2_score


                if player1_score > player2_score:

                    wins += 1
                    points += 3

                else:

                    losses += 1


            # Otherwise our player is Player 2
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


    # Sort:
    # 1. Points
    # 2. Goal difference
    # 3. Name

    standings.sort(
        key=lambda player: (
            player["points"],
            player["goal_difference"],
            player["name"]
        ),
        reverse=True
    )


    return standings


# ==========================================
# DISPLAY STANDINGS
# ==========================================

def show_standings():

    standings = calculate_standings()


    print("\n==============================================")
    print("              🏆 STANDINGS")
    print("==============================================")


    print(
        f"{'POS':<5}"
        f"{'PLAYER':<22}"
        f"{'P':<5}"
        f"{'W':<5}"
        f"{'L':<5}"
        f"{'GF':<5}"
        f"{'GA':<5}"
        f"{'GD':<6}"
        f"{'PTS':<5}"
    )


    print("-" * 63)


    for position, player in enumerate(
        standings,
        start=1
    ):

        print(
            f"{position:<5}"
            f"{player['name']:<22}"
            f"{player['matches_played']:<5}"
            f"{player['wins']:<5}"
            f"{player['losses']:<5}"
            f"{player['goals_for']:<5}"
            f"{player['goals_against']:<5}"
            f"{player['goal_difference']:<6}"
            f"{player['points']:<5}"
        )


# ==========================================
# MAIN PROGRAM
# ==========================================

print("========================================")
print("          🎱 SNOOKER LEAGUE")
print("========================================")


enter_result()


show_standings()