# Cricbuzz LiveStats

**Real-time cricket data • Top stats • 25 SQL queries • Player CRUD**  
A **Streamlit-powered web app** that combines **live Cricbuzz API**, **PostgreSQL analytics**, and **interactive player management**.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://cricbuzz-livestats.streamlit.app)
[![GitHub](https://img.shields.io/github/stars/arunds23/cricbuzz-livestats?style=social)](https://github.com/arunds23/cricbuzz-livestats)
---

## Features

| Feature | Description |
|-------|-----------|
| **Live Matches** | Real-time scores & scorecards from Cricbuzz |
| **Top Stats** | Most Runs, Wickets, Highest Score (with retry + fallback) |
| **25 SQL Queries** | Beginner → Advanced analytics on PostgreSQL |
| **Player CRUD** | Full Create, Read, Update, Delete on `players` table |
| **CSV Export** | Download any result instantly |
| **Responsive UI** | Clean, modern, mobile-friendly design |

---

## Live Demo

**Try it now**: [https://cricbuzz-livestats.streamlit.app](https://cricbuzz-livestats.streamlit.app)


---

## Screenshots

<div align="center">
  <img src="https://via.placeholder.com/800x450/1a1a1a/ffffff?text=Live+Matches+Dashboard" alt="Live Matches" width="48%" />
  <img src="https://via.placeholder.com/800x450/1a1a1a/ffffff?text=Top+Stats+with+CSV" alt="Top Stats" width="48%" />
  <img src="https://via.placeholder.com/800x450/1a1a1a/ffffff?text=25+SQL+Queries" alt="SQL Analytics" width="48%" />
  <img src="https://via.placeholder.com/800x450/1a1a1a/ffffff?text=Player+CRUD" alt="Player CRUD" width="48%" />
</div>

---

## Tech Stack

```yaml
Frontend: Streamlit
Backend: Python, SQLAlchemy, PostgreSQL
API: Cricbuzz Cricket (RapidAPI)
Deployment: Streamlit Cloud

Database: Neon.tech / Local PostgreSQL
