# Snooker League Management System 🎱

A web-based snooker league management application built with **Python, Flask, PostgreSQL, and HTML/CSS**. The system manages players, fixtures, match results, and league standings for a university snooker league.

**Live Demo:** https://snookerleague-2.onrender.com  
**Source Code:** https://github.com/syavuyasphe6-beep/SnookerLeague

## Overview

The Snooker League Management System was developed to make it easier to organise and manage a competitive league. It replaces manual tracking of fixtures, scores, and standings with a centralised web application.

The application was used to manage a completed league season involving four players, providing a practical opportunity to develop, deploy, and use a real software project.

## Features

- **League standings:** Displays player rankings based on points, goal difference, and name.
- **Player management:** Allows the administrator to add players and manage the player list.
- **Fixture management:** Creates and displays scheduled fixtures, including match dates and statuses.
- **Match results:** Records match scores and displays completed results.
- **Automatic standings calculations:** Calculates matches played, wins, losses, goals for, goals against, goal difference, and points.
- **Administrator login:** Protects administrative functions behind a login.
- **Persistent database storage:** Uses PostgreSQL so league data can survive application restarts and redeployments.
- **Online deployment:** Makes the application accessible through a public web address.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic and data processing |
| Flask | Web framework and routing |
| PostgreSQL | Persistent relational database |
| Psycopg | Python connection to PostgreSQL |
| HTML | Web page structure |
| CSS | Styling and layout |
| Git and GitHub | Version control and source-code hosting |
| Render | Web application deployment |
| Neon | Hosted PostgreSQL database |

## How the System Works

1. The administrator logs in to access the management area.
2. Players are added to the database.
3. Fixtures are created with the participating players and match dates.
4. Match results are entered when games are completed.
5. The application stores the results in PostgreSQL.
6. The standings are calculated from the recorded match results and displayed on the homepage.

A win earns three points, while a loss earns zero points. Goal difference is calculated by subtracting goals against from goals scored.

## Live Application

Explore the deployed application:

- **Standings:** https://snookerleague-2.onrender.com/
- **Fixtures:** https://snookerleague-2.onrender.com/fixtures
- **Results:** https://snookerleague-2.onrender.com/results

Administrative functions require valid login credentials.

## Running Locally

### Prerequisites

- Python 3.10 or later
- Git
- A PostgreSQL database
- A terminal or command prompt

### 1. Clone the repository

```bash
git clone https://github.com/syavuyasphe6-beep/SnookerLeague.git
cd SnookerLeague
```

### 2. Create and activate a virtual environment

On Windows:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Configure the following environment variables before running the application:

| Variable | Purpose |
|---|---|
| `DATABASE_URL` | PostgreSQL connection string |
| `ADMIN_USERNAME` | Administrator username |
| `ADMIN_PASSWORD` | Administrator password |
| `SECRET_KEY` | Secret used to protect Flask sessions |

Use your own PostgreSQL database and credentials. Do not commit passwords, connection strings, or secret keys to GitHub.

For local development, set these variables in your terminal or a suitable local environment configuration. The application requires a working PostgreSQL connection.

### 5. Start the application

```bash
python app.py
```

Open the local address printed by Flask in your browser, usually:

`http://127.0.0.1:5000`

The application initialises its database tables when it starts. A fresh database will still need players and fixtures to be added through the application.

## Project Structure

```text
SnookerLeague/
├── app.py
├── database.py
├── standings.py
├── main.py
├── reset_database.py
├── requirements.txt
├── templates/
│   ├── admin.html
│   ├── fixtures.html
│   ├── index.html
│   ├── login.html
│   └── results.html
└── static/
    └── style.css
```

- `app.py` — Flask application, routes, authentication, and league operations.
- `database.py` — PostgreSQL connection and database initialisation.
- `standings.py` — Calculates and sorts the league standings.
- `templates/` — HTML templates for the application pages.
- `static/style.css` — Application styling.
- `requirements.txt` — Python dependencies.
- `reset_database.py` — Development/maintenance script for resetting recorded match results. **Do not run this against the production database**, as it deletes recorded matches.

## Future Improvements

Potential future enhancements include:

- Editing and safely deleting recorded match results.
- Player profiles and individual statistics.
- Improved fixture validation and administration.
- Season archives and historical standings.
- Additional automated testing and security improvements.

These are planned enhancements and are not all implemented in the current version.

## Security Notes

- Keep database credentials and administrator passwords out of source control.
- Use a strong, private Flask `SECRET_KEY` in deployed environments.
- Use HTTPS when accessing the deployed application.
- Do not run database-reset scripts against production data.

## Author

**Siyavuya Mkhize**  
BScEng Computer Engineering Student  
University of KwaZulu-Natal

This project demonstrates practical experience with Python web development, relational databases, SQL, application deployment, and version control.
