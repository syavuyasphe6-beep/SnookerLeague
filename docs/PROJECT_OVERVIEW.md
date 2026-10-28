# Project Overview — Snooker League Management System

## 1. Project Background

The Snooker League Management System is a web application developed to manage a university snooker league. The project addresses the practical challenge of keeping track of players, fixtures, match scores, and league standings in one place.

Instead of relying entirely on manual calculations and separate records, the application provides a centralised system for recording match information and presenting the league table.

The application was deployed online and used to manage a completed league season involving four players.

## 2. Project Objectives

The main objectives were to:

- Provide a central place to view league standings.
- Manage player information and match fixtures.
- Record completed match results.
- Calculate player statistics and league points from recorded results.
- Make league information accessible through a web browser.
- Store league data persistently in a relational database.

## 3. Technology Stack

| Technology | Role |
|---|---|
| Python | Application logic and calculations |
| Flask | Web framework and HTTP routes |
| PostgreSQL | Persistent relational data storage |
| Psycopg | Connecting Python to PostgreSQL |
| HTML | Structure of the web pages |
| CSS | Styling and layout |
| Git and GitHub | Source control and code hosting |
| Render | Hosting the web application |
| Neon | Hosted PostgreSQL database |

## 4. High-Level System Architecture

The application can be understood as three main layers.

### Presentation layer

HTML templates provide the pages that users see in their browsers. CSS controls the visual presentation of those pages.

The templates include the league homepage, fixtures page, results page, login page, and administration page.

### Application layer

The Flask application handles requests, routes users to the appropriate pages, processes administrative actions, and coordinates operations involving players, fixtures, and match results.

The standings module calculates player statistics and determines the league table order.

### Data layer

PostgreSQL stores the league information so that it can persist beyond an individual application session or restart. Psycopg allows the Python application to communicate with the database.

The application is hosted on Render, while the PostgreSQL database is hosted on Neon.

## 5. How the Application Works

The typical league-management workflow is:

1. The administrator signs in to access administrative functions.
2. Player records are added or managed.
3. Fixtures are created for the league.
4. Results are recorded when matches have been completed.
5. The application stores match information in the database.
6. The standings logic processes the recorded results.
7. The homepage presents the resulting league table.

A win awards three points, while a loss awards zero points. Goal difference is calculated by subtracting goals against from goals scored.

The standings include statistics such as matches played, wins, losses, goals for, goals against, goal difference, and points.

## 6. Main Application Modules

- `app.py` — Main Flask application, routes, authentication, and league operations.
- `database.py` — Database connection and initialisation logic.
- `standings.py` — Standings calculations and ranking logic.
- `main.py` — Additional Python entry point or supporting module.
- `templates/` — HTML templates for the application's pages.
- `static/style.css` — Styles used by the interface.
- `requirements.txt` — Python dependencies.
- `reset_database.py` — Database maintenance script. This script must not be run against the live production database because it can delete recorded match results.

## 7. Deployment

The application is available online at:

https://snookerleague-2.onrender.com

The source code is hosted at:

https://github.com/syavuyasphe6-beep/SnookerLeague

The web application uses environment variables for deployment configuration and credentials. The database is hosted separately from the web application.

## 8. Engineering Lessons

This project provided practical experience with:

- Building a web application using Python and Flask.
- Separating application logic into different modules.
- Connecting an application to a relational database.
- Persisting and retrieving application data.
- Implementing administrative authentication.
- Deploying an application and database using hosted services.
- Using Git and GitHub to maintain and publish source code.
- Developing software for a real organisational need.

## 9. Future Development

Possible improvements include safe result editing, more extensive validation, player profiles, season archives, automated tests, and additional security hardening.

These items are future enhancements and should not be considered implemented features until they have been developed and tested.

## 10. Project Status

The application was used to manage a completed four-player league season. The existing deployed version is available for demonstration.

**Developer:** Siyavuya Mkhize  
**Programme:** BScEng Computer Engineering  
**Institution:** University of KwaZulu-Natal
