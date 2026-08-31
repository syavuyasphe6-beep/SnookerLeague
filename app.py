from flask import Flask, render_template, request, redirect, session
from standings import calculate_standings
from database import initialize_database

import sqlite3


app = Flask(__name__)

app.secret_key = "79288"
initialize_database()

# ==========================================
# STANDINGS PAGE
# ==========================================

@app.route("/")
def home():

    standings = calculate_standings()

    return render_template(
        "index.html",
        standings=standings
    )


# ==========================================
# FIXTURES PAGE
# ==========================================

@app.route("/fixtures")
def fixtures():

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

    connection.close()

    return render_template(
        "fixtures.html",
        fixtures=fixtures
    )


# ==========================================
# RESULTS PAGE
# ==========================================

@app.route("/results")
def results():

    connection = sqlite3.connect("snooker.db")
    cursor = connection.cursor()

    cursor.execute("""
    SELECT
        matches.id,
        p1.name,
        p2.name,
        matches.player1_score,
        matches.player2_score
    FROM matches
    JOIN players AS p1
        ON matches.player1_id = p1.id
    JOIN players AS p2
        ON matches.player2_id = p2.id
    ORDER BY matches.id DESC
    """)

    results = cursor.fetchall()

    connection.close()

    return render_template(
        "results.html",
        results=results
    )

# ==========================================
# ADMIN LOGIN
# ==========================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "Syavuya10@gmail":

            session["admin_logged_in"] = True

            return redirect("/admin")

        return "Invalid username or password"

    return render_template("login.html")

# ==========================================
# ADMIN PAGE
# ==========================================


# ==========================================
# ADMIN PAGE
# ==========================================

@app.route("/admin")
def admin():

    if not session.get("admin_logged_in"):
        return redirect("/login")

    connection = sqlite3.connect("snooker.db")
    cursor = connection.cursor()

    # GET PLAYERS
    cursor.execute("""
    SELECT id, name
    FROM players
    ORDER BY name
    """)

    players = cursor.fetchall()

    # GET ALL FIXTURES
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

    connection.close()

    return render_template(
        "admin.html",
        players=players,
        fixtures=fixtures
    )



# ==========================================
# ADD PLAYER
# ==========================================

@app.route("/admin/add-player", methods=["POST"])
def add_player():

    player_name = request.form["name"]

    connection = sqlite3.connect("snooker.db")
    cursor = connection.cursor()

    cursor.execute("""
    INSERT OR IGNORE INTO players (name)
    VALUES (?)
    """, (player_name,))

    connection.commit()
    connection.close()

    return redirect("/admin")


# ==========================================
# REMOVE PLAYER
# ==========================================

@app.route("/admin/remove-player/<int:player_id>", methods=["POST"])
def remove_player(player_id):

    connection = sqlite3.connect("snooker.db")
    cursor = connection.cursor()

    cursor.execute("""
    DELETE FROM players
    WHERE id = ?
    """, (player_id,))

    connection.commit()
    connection.close()

    return redirect("/admin")


# ==========================================
# CREATE FIXTURE
# ==========================================

@app.route("/admin/create-fixture", methods=["POST"])
def create_fixture():

    player1_id = request.form["player1_id"]
    player2_id = request.form["player2_id"]
    match_date = request.form["match_date"]


    # --------------------------------------
    # PLAYER CANNOT PLAY THEMSELVES
    # --------------------------------------

    if player1_id == player2_id:

        return redirect("/admin")


    # --------------------------------------
    # SAVE FIXTURE
    # --------------------------------------

    connection = sqlite3.connect("snooker.db")
    cursor = connection.cursor()


    # Check whether this exact fixture
    # already exists

    cursor.execute("""
    SELECT id
    FROM fixtures
    WHERE player1_id = ?
    AND player2_id = ?
    AND match_date = ?
    """, (
        player1_id,
        player2_id,
        match_date
    ))


    existing_fixture = cursor.fetchone()


    # --------------------------------------
    # DON'T CREATE DUPLICATE FIXTURE
    # --------------------------------------

    if existing_fixture is not None:

        connection.close()

        return redirect("/fixtures")


    # --------------------------------------
    # INSERT NEW FIXTURE
    # --------------------------------------

    cursor.execute("""
    INSERT INTO fixtures
    (
        player1_id,
        player2_id,
        match_date,
        status
    )
    VALUES (?, ?, ?, 'Scheduled')
    """, (
        player1_id,
        player2_id,
        match_date
    ))


    connection.commit()

    connection.close()


    return redirect("/fixtures")



# ==========================================
# ENTER RESULT
# ==========================================

@app.route("/admin/enter-result", methods=["POST"])
def enter_result():

    fixture_id = request.form["fixture_id"]
    player1_score = int(request.form["player1_score"])
    player2_score = int(request.form["player2_score"])

    # Make sure the match is not a draw
    if player1_score == player2_score:
        return redirect("/admin")

    # Make sure scores are not negative
    if player1_score < 0 or player2_score < 0:
        return redirect("/admin")

    connection = sqlite3.connect("snooker.db")
    cursor = connection.cursor()

    # Find the selected fixture
    cursor.execute("""
    SELECT
        player1_id,
        player2_id,
        status
    FROM fixtures
    WHERE id = ?
    """, (fixture_id,))

    fixture = cursor.fetchone()

    # Check that the fixture exists
    if fixture is None:
        connection.close()
        return redirect("/admin")

    player1_id = fixture[0]
    player2_id = fixture[1]
    status = fixture[2]

    # Prevent entering the same result twice
    if status == "Completed":
        connection.close()
        return redirect("/admin")

    # Save result
    cursor.execute("""
    INSERT INTO matches
    (
        player1_id,
        player2_id,
        player1_score,
        player2_score
    )
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

    # Go to results page
    return redirect("/results")


# ==========================================
# DELETE FIXTURE
# ==========================================

@app.route("/admin/delete-fixture/<int:fixture_id>", methods=["POST"])
def delete_fixture(fixture_id):

    connection = sqlite3.connect("snooker.db")
    cursor = connection.cursor()

    cursor.execute("""
    DELETE FROM fixtures
    WHERE id = ?
    """, (fixture_id,))

    connection.commit()
    connection.close()

    return redirect("/admin")

# ==========================================
# LOGOUT
# ==========================================

@app.route("/logout")
def logout():

    session.pop("admin_logged_in", None)

    return redirect("/")

# ==========================================
# START APPLICATION
# ==========================================

if __name__ == "__main__":

    print()
    print("========================================")
    print("          FLASK ROUTES")
    print("========================================")

    for rule in app.url_map.iter_rules():

        print(
            rule,
            "->",
            rule.endpoint
        )

    print("========================================")
    print()

    app.run(debug=True)