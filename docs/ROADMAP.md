# Project Roadmap — Snooker League Management System

This roadmap records potential improvements to the Snooker League Management System. Items below are planned work, not claims about features already implemented.

## Priority 1 — Data integrity

Implement a safe workflow for correcting an incorrectly recorded match result.
Ensure correcting a result updates the standings consistently.
Review fixture deletion so related records are handled safely.
Validate scores, player selections, and fixture data.
Prevent duplicate or invalid match entries.

**Goal:** Keep league records accurate and protect existing data.

## Priority 2 — Testing

Add tests for points calculations.
Test goals for, goals against, and goal difference.
Test ranking order when players have equal points.
Test result entry and correction workflows.
Test invalid input and unauthorised administrative access.

**Goal:** Detect errors before they affect the league table or production data.

## Priority 3 — Player statistics

Add an individual profile for each player.
Display wins, losses, matches played, and goals scored.
Show player performance across a season.
Improve the presentation of individual statistics.

**Goal:** Make the application more informative for players.

## Priority 4 — Season management

Design a way to archive completed seasons.
Preserve historical standings and results.
Separate new seasons from previous seasons.
Test season changes without losing existing records.

**Goal:** Support repeated use of the application over multiple seasons.

## Priority 5 — Security and maintainability

Confirm production secrets are stored in environment variables.
Configure a strong Flask secret key in production.
Review authentication and administrative routes.
Improve error handling and user feedback.
Document deployment and database recovery procedures.

**Goal:** Make the application safer to maintain and easier to troubleshoot.

## Development Principles

- Back up important production data before making database changes.
- Develop and test changes separately before deploying them.
- Never run database-reset scripts against production data.
- Update this roadmap when work is completed.
- Only mark an item complete after implementing and testing it.

## Current Status

The application has been deployed and used to manage a completed four-player league season. Further improvements will be prioritised according to their value, safety, and learning benefits.
