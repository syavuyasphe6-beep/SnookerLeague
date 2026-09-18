import os

from flask import Flask, render_template, request, redirect, session
from standings import calculate_standings
from database import initialize_database, get_connection


app = Flask(__name__)

# ==========================================
# SECURITY SETTINGS
# ==========================================

app.secret_key = os.environ.get("SECRET_KEY", "development-secret-key")

ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")


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

    connection = get_connection()
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

    cursor.close()
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

    connection = get_connection()
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

    cursor.close()
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

        if (
            username == ADMIN_USERNAME
            and ADMIN_PASSWORD
            and password == ADMIN_PASSWORD
        ):

            session["admin_logged_in"] = True

            return redirect("/admin")

        return "Invalid username or password"

    return render_template("login.html")


# ==========================================
# ADMIN PAGE
# ==========================================

@app.route("/admin")
def admin():

    if not session.get("admin_logged_in"):
        return redirect("/login")

    connection = get_connection()
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

    cursor.close()
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

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO players (name)
    VALUES (%s)
    ON CONFLICT (name) DO NOTHING
    """, (player_name,))

    connection.commit()

    cursor.close()
    connection.close()

    return redirect("/admin")


# ==========================================
# REMOVE PLAYER
# ==========================================

@app.route("/admin/remove-player/<int:player_id>", methods=["POST"])
def remove_player(player_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    DELETE FROM players
    WHERE id = %s
    """, (player_id,))

    connection.commit()

    cursor.close()
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

    connection = get_connection()
    cursor = connection.cursor()

    # --------------------------------------
    # CHECK FOR DUPLICATE FIXTURE
    # --------------------------------------

    cursor.execute("""
    SELECT id
    FROM fixtures
    WHERE (
        player1_id = %s
        AND player2_id = %s
    )
    AND match_date = %s
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

        cursor.close()
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
    VALUES (%s, %s, %s, 'Scheduled')
    """, (
        player1_id,
        player2_id,
        match_date
    ))

    connection.commit()

    cursor.close()
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

    # --------------------------------------
    # NO DRAWS
    # --------------------------------------

    if player1_score == player2_score:
        return redirect("/admin")

    # --------------------------------------
    # NO NEGATIVE SCORES
    # --------------------------------------

    if player1_score < 0 or player2_score < 0:
        return redirect("/admin")

    connection = get_connection()
    cursor = connection.cursor()

    # --------------------------------------
    # FIND FIXTURE
    # --------------------------------------

    cursor.execute("""
    SELECT
        player1_id,
        player2_id,
        status
    FROM fixtures
    WHERE id = %s
    """, (fixture_id,))

    fixture = cursor.fetchone()

    # --------------------------------------
    # CHECK FIXTURE EXISTS
    # --------------------------------------

    if fixture is None:

        cursor.close()
        connection.close()

        return redirect("/admin")

    player1_id = fixture[0]
    player2_id = fixture[1]
    status = fixture[2]

    # --------------------------------------
    # PREVENT DUPLICATE RESULT
    # --------------------------------------

    if status == "Completed":

        cursor.close()
        connection.close()

        return redirect("/admin")

    # --------------------------------------
    # SAVE RESULT
    # --------------------------------------

    cursor.execute("""
    INSERT INTO matches
    (
        player1_id,
        player2_id,
        player1_score,
        player2_score
    )
    VALUES (%s, %s, %s, %s)
    """, (
        player1_id,
        player2_id,
        player1_score,
        player2_score
    ))

    # --------------------------------------
    # MARK FIXTURE COMPLETED
    # --------------------------------------

    cursor.execute("""
    UPDATE fixtures
    SET status = 'Completed'
    WHERE id = %s
    """, (fixture_id,))

    connection.commit()

    cursor.close()
    connection.close()

    return redirect("/results")


# ==========================================
# DELETE FIXTURE
# ==========================================

@app.route("/admin/delete-fixture/<int:fixture_id>", methods=["POST"])
def delete_fixture(fixture_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    DELETE FROM fixtures
    WHERE id = %s
    """, (fixture_id,))

    connection.commit()

    cursor.close()
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