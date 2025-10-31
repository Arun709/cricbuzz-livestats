import streamlit as st
import requests
import pandas as pd
from sqlalchemy import create_engine, text
from typing import Optional, Dict, Any
import os
import time

# -------------------------------------------------
#  CONFIG & PAGE SETUP
# -------------------------------------------------
st.set_page_config(
    page_title="Cricbuzz LiveStats",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/arun709/cricbuzz-livestats',
        'Report a bug': 'https://github.com/arun709/cricbuzz-livestats/issues',
        'About': 'Live cricket stats + SQL analytics powered by Cricbuzz & PostgreSQL'
    }
)

# -------------------------------------------------
#  SECRETS & DB CONNECTION
# -------------------------------------------------
DATABASE_URL = None
RAPIDAPI_KEY = None

try:
    secrets = st.secrets or {}
except Exception:
    secrets = {}

# --- Logic to retrieve secrets from Streamlit Cloud ---
if isinstance(secrets, dict):
    # Try to get URL from the 'postgres' section (if using st.connection)
    pg = secrets.get("postgres")
    if isinstance(pg, dict):
        DATABASE_URL = pg.get("url")
    else:
        # Fallback to general DATABASE_URL key
        DATABASE_URL = secrets.get("DATABASE_URL") or DATABASE_URL
        
    # Get API key
    RAPIDAPI_KEY = secrets.get("RAPIDAPI_KEY") or secrets.get("rapidapi_key") or RAPIDAPI_KEY

# Fallback to environment variables (for local development)
DATABASE_URL = DATABASE_URL or os.environ.get("DATABASE_URL")
RAPIDAPI_KEY = RAPIDAPI_KEY or os.environ.get("RAPIDAPI_KEY")

if not RAPIDAPI_KEY:
    st.warning("Missing RAPIDAPI_KEY. Live API features disabled.")

if not DATABASE_URL:
    st.error("Missing DATABASE_URL. DB features disabled.") # Changed to error

# Cached DB engine
engine = None
if DATABASE_URL:
    # Use st.cache_resource for the SQLAlchemy Engine
    @st.cache_resource
    def get_engine(db_url):
        # Increased pool size and added pre-ping for better cloud connection stability
        return create_engine(db_url, pool_pre_ping=True, pool_size=10)
    
    try:
        engine = get_engine(DATABASE_URL)
        # Test connection once
        with engine.connect():
            pass 
    except Exception as e:
        st.error(f"DB Connection Error: {e}")
        engine = None
        
# -------------------------------------------------
#  RAPIDAPI HELPER (Only for Live Matches)
# -------------------------------------------------
def fetch_cricbuzz(endpoint: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict]:
    if not RAPIDAPI_KEY:
        # st.info("Cricbuzz API disabled: set RAPIDAPI_KEY.") # Remove redundant warning
        return None

    url = f"https://cricbuzz-cricket.p.rapidapi.com/{endpoint}"
    # Use the securely loaded RAPIDAPI_KEY
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY, 
        "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com"
    }
    try:
        with st.spinner(f"Fetching {endpoint}..."):
            r = requests.get(url, headers=headers, params=params, timeout=15)
        if r.status_code == 200:
            return r.json()
        st.error(f"API Error {r.status_code}: {r.text[:300]}")
    except Exception as e:
        st.error(f"Network Error: {e}")
    return None

# -------------------------------------------------
#                 25 SQL QUERIES (NO CHANGE)
# -------------------------------------------------
queries = {
    "Beginner": {
        "Q1 - INDIAN PLAYERS": (
            "Find all players who represent India.",
            """
            SELECT name,
                   CASE 
                     WHEN isbatsman = true AND isbowler = false THEN 'Batsman'
                     WHEN isbatsman = false AND isbowler = true THEN 'Bowler'
                     WHEN isallrounder = true THEN 'All-rounder'
                     ELSE 'Wicket-keeper'
                   END AS playing_role,
                   battingstyle AS batting_style,
                   bowlingstyle AS bowling_style
            FROM indian_players
            ORDER BY name;
            """
        ),
        "Q2 - RECENT MATCHES": (
            "Show matches from last 30 days.",
            """
            SELECT match_desc AS match_description,
                   team1_name,
                   team2_name,
                   venue_name || ', ' || city AS venue,
                   to_timestamp(match_date / 1000) AS match_date
            FROM recent_matches
            WHERE to_timestamp(match_date / 1000) >= CURRENT_TIMESTAMP - INTERVAL '30 days'
            ORDER BY to_timestamp(match_date / 1000) DESC;
            """
        ),
        "Q3 - ODI BATTING STATS": (
            "Top 10 ODI run scorers.",
            """
            SELECT player_name,
                   runs AS total_runs,
                   batting_avg AS batting_average,
                   0 AS centuries
            FROM odi_batting_stats
            ORDER BY runs DESC
            LIMIT 10;
            """
        ),
        "Q4 - CRICKET VENUES": (
            "Venues with capacity > 50,000.",
            """
            SELECT venue_name, city, country, capacity
            FROM cricket_venues
            WHERE capacity > 50000
            ORDER BY capacity DESC;
            """
        ),
        "Q5 - CRICKET MATCHES": (
            "Team win counts.",
            """
            SELECT winner_sname AS team_name, COUNT(*) AS total_wins
            FROM cricket_matches
            WHERE winner_sname IS NOT NULL
            GROUP BY winner_sname
            ORDER BY total_wins DESC;
            """
        ),
        "Q6 - PLAYER ROLES": (
            "Players per role.",
            """
            SELECT role, COUNT(*) AS player_count
            FROM player_roles
            GROUP BY role
            ORDER BY player_count DESC;
            """
        ),
        "Q7 - TOP SCORERS IN EVERY FORMAT": (
            "Highest score per format.",
            """
            SELECT format, highest_score
            FROM top_scorers_in_every_format
            ORDER BY highest_score DESC;
            """
        ),
        "Q8 - CRICKET SERIES 2024": (
            "Series in 2024.",
            """
            SELECT series_name, host_country, match_type, start_date, total_matches
            FROM cricket_series_2024
            WHERE EXTRACT(YEAR FROM start_date) = 2024
            ORDER BY start_date;
            """
        ),
    },

    "Intermediate": {
        "Q9 - ALL ROUNDERS": (
            "All-rounders >1000 runs & >50 wickets.",
            """
            SELECT player_name, total_runs, total_wickets, cricket_format AS format
            FROM all_rounders
            WHERE total_runs > 1000 AND total_wickets > 50;
            """
        ),
        "Q10 - CRICKET MATCHES 20": (
            "Last 20 completed matches.",
            """
            SELECT match_desc, team1_name, team2_name, winning_team, victory_margin, victory_type, venue_name
            FROM cricket_matches_20
            ORDER BY match_date DESC
            LIMIT 20;
            """
        ),
        "Q11 - PLAYER CAREER SUMMARY": (
            "Runs in ODI/T20I.",
            """
            SELECT player,
                   odi_avg * odi_matches AS runs_odi,
                   t20i_avg * t20i_matches AS runs_t20i,
                   (test_avg * test_matches + odi_avg * odi_matches + t20i_avg * t20i_matches) AS runs_overall,
                   ROUND(
                     (test_avg * test_matches + odi_avg * odi_matches + t20i_avg * t20i_matches) 
                     / NULLIF(test_matches + odi_matches + t20i_matches, 0), 2
                   ) AS batting_average
            FROM player_career_summary;
            """
        ),
        "Q12 - TEAM HOME AWAY WINS": (
            "Home vs Away wins.",
            """
            SELECT team, format, home_wins, away_wins
            FROM team_home_away_wins
            ORDER BY (home_wins + away_wins) DESC;
            """
        ),
        "Q13 - PARTNERSHIPS": (
            "Partnerships ≥100 runs.",
            """
            SELECT player_names, combined_partnership_runs, innings, match_context
            FROM partnerships
            WHERE combined_partnership_runs >= 100
            ORDER BY combined_partnership_runs DESC;
            """
        ),
        "Q14 - BOWLER VENUE STATS": (
            "Bowling at venues (≥3 matches).",
            """
            SELECT bowler, venue, matches, total_wickets, average_economy_rate
            FROM bowler_venue_stats
            WHERE matches >= 3;
            """
        ),
        "Q15 - CLUTCH BATTING STATS": (
            "Batting in close matches.",
            """
            SELECT player, batting_average_close_matches, total_close_matches_played, team_wins_when_they_batted
            FROM clutch_batting_stats;
            """
        ),
        "Q16 - PLAYER YEARLY STATS": (
            "Yearly stats since 2020.",
            """
            SELECT player, year, matches_played, avg_runs_per_match, avg_strike_rate
            FROM player_yearly_stats
            WHERE year >= 2020
            ORDER BY year DESC, avg_runs_per_match DESC;
            """
        ),
    },

    "Advanced": {
        "Q17 - TOSS ADVANTAGE STATS": (
            "Toss win %.",
            """
            SELECT format, win_percent_choose_bat_first, win_percent_choose_field_first, overall_win_percent
            FROM toss_advantage_stats;
            """
        ),
        "Q18 - BOWLERS AGGREGATE": (
            "Most economical bowlers.",
            """
            SELECT bowler, overall_economy_rate, total_wickets
            FROM bowlers_aggregate
            ORDER BY overall_economy_rate ASC;
            """
        ),
        "Q19 - PLAYER BATTING DISTRIBUTION": (
            "Consistent batsmen.",
            """
            SELECT player, avg_runs_scored, stddev_runs AS consistency_sd, avg_balls_faced
            FROM player_batting_distribution
            WHERE avg_balls_faced >= 10;
            """
        ),
        "Q20 - PLAYER CAREER SUMMARY": (
            "Matches & avg per format.",
            """
            SELECT player, test_matches, test_avg, odi_matches, odi_avg, t20i_matches, t20i_avg, total_matches
            FROM player_career_summary
            WHERE total_matches >= 20;
            """
        ),
        "Q21 - ALL ROUNDERS": (
            "All-rounder ranking.",
            """
            SELECT player_name AS player,
                   (total_runs * 0.01) + 
                   (CASE WHEN total_wickets > 0 THEN 50 - (total_runs::float / total_wickets) ELSE 0 END * 0.5) AS total_score
            FROM all_rounders
            ORDER BY total_score DESC;
            """
        ),
        "Q22 - HEAD TO HEAD SERIES": (
            "Head-to-head stats (≥5 matches).",
            """
            SELECT 
                pair AS team_pair,
                total_matches,
                CAST(
                    TRIM(REGEXP_REPLACE(SPLIT_PART(wins_team1, '/', 1), '[^0-9]', '', 'g'))
                    AS INTEGER
                ) AS team1_wins,
                CAST(
                    TRIM(REGEXP_REPLACE(SPLIT_PART(wins_team1, '/', 2), '[^0-9]', '', 'g'))
                    AS INTEGER
                ) AS team2_wins,
                CAST(REPLACE(win_percent_team1, '%', '') AS REAL) AS team1_win_pct,
                CAST(REPLACE(win_percent_team2, '%', '') AS REAL) AS team2_win_pct
            FROM head_to_head_series
            WHERE total_matches >= 5
              AND wins_team1 LIKE '%/%'
            ORDER BY total_matches DESC;
            """
        ),
        "Q23 - RECENT FORM": (
            "Recent form analysis.",
            """
            SELECT player, avg_runs_last5, avg_runs_last10, sr_trend_last5_last10, scores_over_50_last10, consistency_score_sd, form_category
            FROM recent_form;
            """
        ),
        "Q24 - TOP PARTNERSHIPS": (
            "Best batting partnerships.",
            """
            SELECT pair_team, avg_partnership_runs, partnerships_over_50, highest_partnership_score, success_rate_percent
            FROM top_partnerships
            ORDER BY avg_partnership_runs DESC;
            """
        ),
        "Q25 - PLAYER QUARTERLY STATS": (
            "Quarterly performance trend.",
            """
            SELECT player, quarter, avg_runs, avg_strike_rate, trend
            FROM player_quarterly_stats
            ORDER BY player, quarter;
            """
        ),
    }
}


def run_sql_query(sql: str, params: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    if engine is None:
        # st.error("Database not connected.") # Avoid redundant error message
        return pd.DataFrame()
    try:
        with engine.connect() as conn:
            # Use text() and params for secure, parameterized query execution
            df = pd.read_sql_query(text(sql), conn, params=params) 
        return df
    except Exception as e:
        st.error(f"SQL Error: {e}")
        return pd.DataFrame()

# -------------------------------------------------
#  STREAMLIT UI
# -------------------------------------------------
st.title("Cricbuzz LiveStats")
st.caption("Real-time cricket data • Top stats • 25 SQL queries • Player CRUD")

st.sidebar.image("https://upload.wikimedia.org/wikipedia/en/8/89/Cricbuzz_logo.png", width=150)
page = st.sidebar.selectbox("Go to", ["Home", "Live Matches", "Top Stats", "SQL Analytics", "Player CRUD"], index=0)

# -------------------------------------------------
#  HOME
# -------------------------------------------------
if page == "Home":
    st.header("Welcome to Cricbuzz LiveStats!")
    col1, col2, col3 = st.columns(3)
    
    # Attempt to query player count for the Home page metric
    player_count = "Loading..."
    if engine:
        try:
            with engine.connect() as conn:
                count_result = conn.execute(text("SELECT COUNT(id) FROM players")).scalar()
                player_count = f"{count_result:,}" if count_result is not None else "N/A"
        except Exception:
            player_count = "Error"
    
    with col1:
        st.metric("Live Matches", "API Status: OK" if RAPIDAPI_KEY else "API Disabled")
    with col2:
        st.metric("Players in DB", player_count)
    with col3:
        st.metric("SQL Queries", "25")

    st.markdown("""
    ### Features
    - **Live match updates** from Cricbuzz (API required)
    - **Top stats**: Most Runs, Wickets, High Scores (Now powered by Neon DB)
    - **25 SQL queries** across 3 difficulty levels (Your static data)
    - **Full CRUD** on `players` table (User-managed data)
    - **Export results** to CSV
    """)
    st.info("Use the sidebar to explore!")

# -------------------------------------------------
#  LIVE MATCHES (Uses API - No change to logic)
# -------------------------------------------------
elif page == "Live Matches":
    st.header("Live & Recent Matches")
    data = fetch_cricbuzz("matches/v1/current")
    
    if not data or 'typeMatches' not in data:
        st.info("No live matches right now. Check back later!")
    else:
        for category in data['typeMatches']:
            cat_name = category.get('matchType', 'Unknown').title()
            if 'seriesMatches' not in category:
                continue
            with st.expander(f"**{cat_name}**", expanded=True):
                for series in category['seriesMatches']:
                    for match in series.get('matches', []):
                        info = match.get('matchInfo', {})
                        if not info:
                            continue
                        t1 = info.get('team1', {}).get('teamName', 'Team 1')
                        t2 = info.get('team2', {}).get('teamName', 'Team 2')
                        status = info.get('status', 'No status')
                        match_id = info.get('matchId')

                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.write(f"**{t1} vs {t2}**")
                            st.caption(f"*{status}*")
                        with col2:
                            if st.button("Scorecard", key=f"sc_{match_id}"):
                                sc = fetch_cricbuzz(f"mcenter/v1/{match_id}/scard")
                                if sc:
                                    st.json(sc, expanded=False)

# -------------------------------------------------
#  TOP STATS (REWRITTEN TO USE NEON DB)
# -------------------------------------------------
elif page == "Top Stats":
    st.header("Top Player Statistics (DB Powered)")
    st.markdown("Stats are loaded from the fast and reliable **Neon PostgreSQL database**.")

    # 1. User selects the statistic and format
    col1, col2 = st.columns(2)
    with col1:
        stat = st.selectbox("Select Stat", ["Most Runs", "Most Wickets", "Highest Score"])
    with col2:
        fmt = st.selectbox("Format", ["test", "odi", "t20"])

    # 2. Define the SQL query based on user selection
    # **REQUIRES TABLE: top_stats_data** in your Neon DB
    sql_template = """
    SELECT 
        player_name AS Player,
        total_value AS Value,
        cricket_format AS Format
    FROM 
        top_stats_data
    WHERE 
        stat_type = :stat_type AND cricket_format = :format_type
    ORDER BY 
        total_value DESC
    LIMIT 20;
    """

    # Map the dropdown selection to a clean stat_type name for your SQL table
    stat_map = {"Most Runs": "runs", "Most Wickets": "highscore", "Highest Score": "highest_score"} 
    
    # 3. Check for DB connection and run the query
    if engine is None:
        st.warning("Database not connected. Cannot load Top Stats.")
    else:
        # Define the parameter values for the query
        params = {"stat_type": stat_map[stat], "format_type": fmt}

        # Use st.cache_data for performance, only re-run if inputs change
        @st.cache_data(ttl=3600, show_spinner="Fetching Top Stats from Neon...")
        def get_top_stats(sql, query_params):
            return run_sql_query(sql, params=query_params)

        # Run the cached function
        df_stats = get_top_stats(sql_template, params)

        # 4. Display results
        if not df_stats.empty:
            st.success(f"Top 20 {stat} in {fmt.upper()} loaded from Neon DB.")
            st.dataframe(df_stats, use_container_width=True)
            csv = df_stats.to_csv(index=False).encode()
            st.download_button("Download CSV", csv, f"top_stats_{stat_map[stat]}_{fmt}.csv", "text/csv")
        else:
            st.info(f"No data found for '{stat}' in '{fmt.upper()}' in the database. Please check your `top_stats_data` table.")


# -------------------------------------------------
#  SQL ANALYTICS (NO CHANGE)
# -------------------------------------------------
elif page == "SQL Analytics":
    st.header("SQL Analytics Engine")
    st.markdown("Run 25 pre-built queries on cricket data.")

    level = st.selectbox("Difficulty Level", list(queries.keys()))
    q_key = st.selectbox("Select Query", list(queries[level].keys()))
    title, sql = queries[level][q_key]

    st.subheader(title)
    with st.expander("View SQL", expanded=False):
        st.code(sql.strip(), language="sql")

    if st.button("Run Query", type="primary"):
        with st.spinner("Executing..."):
            # Uses the run_sql_query function defined above
            df = run_sql_query(sql) 
            if not df.empty:
                st.success(f"Returned **{len(df):,}** rows")
                st.dataframe(df, use_container_width=True)
                csv = df.to_csv(index=False).encode()
                st.download_button("Download CSV", csv, f"{q_key}.csv", "text/csv")
            else:
                st.warning("No results or error running query.")

# -------------------------------------------------
#  PLAYER CRUD (NO CHANGE)
# -------------------------------------------------
elif page == "Player CRUD":
    st.header("Player Management (CRUD)")

    tabs = st.tabs(["Create", "Read", "Update", "Delete"])

    # CREATE
    with tabs[0]:
        with st.form("create_player"):
            st.subheader("Add New Player")
            name = st.text_input("Full Name *")
            role = st.text_input("Playing Role *")
            bat = st.selectbox("Batting Style", ["Right-hand bat", "Left-hand bat", "N/A"])
            bowl = st.selectbox("Bowling Style", ["Right-arm fast", "Left-arm spin", "N/A"])
            country = st.text_input("Country *")

            submitted = st.form_submit_button("Add Player")
            if submitted:
                if not all([name, role, country]):
                    st.error("Please fill all required fields.")
                else:
                    if engine is None:
                        st.error("Database not configured.")
                    else:
                        try:
                            with engine.connect() as conn:
                                conn.execute(text("""
                                    INSERT INTO players (full_name, playing_role, batting_style, bowling_style, country)
                                    VALUES (:n, :r, :bat, :bowl, :c)
                                """), {"n": name, "r": role, "bat": bat if bat != "N/A" else None,
                                       "bowl": bowl if bowl != "N/A" else None, "c": country})
                                conn.commit()
                            st.success(f"Player **{name}** added!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error: {e}")

    # READ
    with tabs[1]:
        st.subheader("All Players")
        if engine is None:
            st.warning("Database not configured.")
        else:
            try:
                # FIX: Use run_sql_query wrapper for better error handling
                df = run_sql_query("SELECT id, full_name, playing_role, country FROM players ORDER BY id DESC LIMIT 200")
                if not df.empty:
                    st.dataframe(df, use_container_width=True)
                else:
                    st.info("The 'players' table is empty. Add a player using the 'Create' tab.")
            except Exception as e:
                # The 'players' table may not exist yet, show a specific error
                st.error("Error reading players. Did you run the 'CREATE TABLE players' script in Neon?")

    # UPDATE
    with tabs[2]:
        st.subheader("Update Player")
        player_id = st.number_input("Player ID to Update", min_value=1, step=1)
        if st.button("Load Player"):
            if engine is None:
                st.error("Database not configured.")
            else:
                # Use a specific session for connection for the fetchone() call
                try:
                    with engine.connect() as conn:
                        result = conn.execute(text("SELECT * FROM players WHERE id = :id"), {"id": player_id}).fetchone()
                except Exception as e:
                    st.error(f"Error loading player: {e}")
                    result = None # Ensure result is None if an error occurred

                if result:
                    with st.form("update_form"):
                        cols = st.columns(2)
                        with cols[0]:
                            name = st.text_input("Name", value=result.full_name)
                            role = st.text_input("Role", value=result.playing_role)
                        with cols[1]:
                            bat = st.text_input("Batting", value=result.batting_style or "")
                            bowl = st.text_input("Bowling", value=result.bowling_style or "")
                        country = st.text_input("Country", value=result.country)

                        if st.form_submit_button("Update"):
                            if engine is None:
                                st.error("Database not configured.")
                            else:
                                try:
                                    with engine.connect() as conn:
                                        conn.execute(text("""
                                            UPDATE players SET full_name=:n, playing_role=:r, 
                                            batting_style=:bat, bowling_style=:bowl, country=:c
                                            WHERE id=:id
                                        """), {"n": name, "r": role, "bat": bat or None, "bowl": bowl or None, "c": country, "id": player_id})
                                        conn.commit()
                                    st.success("Updated!")
                                    st.rerun()
                                except Exception as e:
                                    st.error(e)
                else:
                    st.warning("Player not found.")

    # DELETE
    with tabs[3]:
        st.subheader("Delete Player")
        del_id = st.number_input("Player ID to Delete", min_value=1, step=1)
        
        # Confirmation checkbox outside the button click to prevent accidental deletion
        confirm_delete = st.checkbox("Yes, I confirm permanent deletion of this player.") 

        if st.button("Delete Player", type="secondary"):
            if confirm_delete:
                if engine is None:
                    st.error("Database not configured.")
                else:
                    try:
                        with engine.connect() as conn:
                            # Added conditional logic to check if a player with that ID exists before attempting delete
                            check_result = conn.execute(text("SELECT id FROM players WHERE id = :id"), {"id": del_id}).fetchone()
                            if check_result:
                                conn.execute(text("DELETE FROM players WHERE id = :id"), {"id": del_id})
                                conn.commit()
                                st.success(f"Player ID {del_id} deleted.")
                                st.rerun()
                            else:
                                st.warning(f"Deletion failed: Player ID {del_id} not found.")
                    except Exception as e:
                        st.error(e)
            else:
                st.info("Please confirm deletion by checking the box.")

# -------------------------------------------------
#  FOOTER
# -------------------------------------------------
st.sidebar.markdown("---")
st.sidebar.caption("Built with Streamlit • Data: Cricbuzz API • DB: PostgreSQL (Neon)")
