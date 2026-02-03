import streamlit as st
import requests
import pandas as pd
from sqlalchemy import create_engine, text
from typing import Optional, Dict, Any
from datetime import datetime
import os

# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="Cricbuzz LiveStats",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== PERFECT READABLE CSS  ====================
st.markdown("""
<style>
    /* Hide Streamlit's default menu */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e3b5a 100%);
    }
   
    .main .block-container {
        padding: 2rem 3rem;
        background: rgba(15, 23, 42, 0.7);
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.5);
        backdrop-filter: blur(10px);
    }
   
    h1 {
        color: #ffffff !important;
        font-weight: 900 !important;
        font-size: 3.5rem !important;
        text-shadow: 0 0 20px rgba(14, 165, 233, 0.5);
        border-bottom: 5px solid #0ea5e9;
        padding-bottom: 1rem;
        background: linear-gradient(120deg, #0ea5e9, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
   
    h2 {
        color: #e0f2fe !important;
        font-weight: 800 !important;
        font-size: 2.2rem !important;
        border-left: 6px solid #0ea5e9;
        padding-left: 20px;
    }
   
    h3, h4 {
        color: #bae6fd !important;
        font-weight: 700 !important;
    }
   
    p, li, span, div {
        color: #f1f5f9 !important;
        font-size: 1.1rem !important;
        line-height: 1.8 !important;
    }
   
    strong {
        color: #ffffff !important;
        font-weight: 800 !important;
    }
   
    .stButton > button {
        background: linear-gradient(135deg, #0ea5e9 0%, #2563eb 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 18px 36px !important;
        font-weight: 800 !important;
        font-size: 1.2rem !important;
        box-shadow: 0 6px 20px rgba(14, 165, 233, 0.5) !important;
        text-transform: uppercase !important;
    }
   
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 10px 30px rgba(14, 165, 233, 0.7) !important;
    }
   
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%) !important;
        padding: 1.5rem !important;
    }
   
    section[data-testid="stSidebar"] * {
        color: #f1f5f9 !important;
        font-weight: 600 !important;
    }
   
    .stSelectbox label {
        color: #e0f2fe !important;
        font-weight: 800 !important;
        font-size: 1.2rem !important;
    }
   
    .stSelectbox > div > div {
        background: #ffffff !important;
        color: #000000 !important;
        border: 2px solid #0ea5e9 !important;
        font-weight: 700 !important;
        font-size: 1.15rem !important;
        border-radius: 8px !important;
    }
   
    div[data-baseweb="select"] {
        background-color: #ffffff !important;
    }
   
    ul[role="listbox"] {
        background-color: #ffffff !important;
        border: 2px solid #0ea5e9 !important;
        border-radius: 8px !important;
    }
   
    li[role="option"] {
        background-color: #ffffff !important;
        color: #000000 !important;
        font-weight: 600 !important;
        font-size: 1.15rem !important;
        padding: 14px 18px !important;
    }
   
    li[role="option"]:hover {
        background-color: #dbeafe !important;
        color: #0c4a6e !important;
    }
   
    li[role="option"][aria-selected="true"] {
        background-color: #bfdbfe !important;
        color: #0c4a6e !important;
        font-weight: 800 !important;
    }
   
    [data-baseweb="select"] *,
    [role="listbox"] *,
    [role="option"] * {
        color: #000000 !important;
    }
   
    .stTextInput label,
    .stNumberInput label {
        color: #e0f2fe !important;
        font-weight: 800 !important;
        font-size: 1.1rem !important;
    }
   
    .stTextInput input,
    .stNumberInput input {
        background: #ffffff !important;
        color: #000000 !important;
        border: 2px solid #0ea5e9 !important;
        font-weight: 600 !important;
    }
   
    .stCheckbox label {
        color: #e0f2fe !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
    }
   
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%) !important;
        padding: 25px !important;
        border-radius: 15px !important;
        border-left: 6px solid #0ea5e9 !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3) !important;
    }
   
    div[data-testid="stMetric"] label {
        color: #0c4a6e !important;
        font-weight: 800 !important;
        font-size: 1.3rem !important;
    }
   
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #0c4a6e !important;
        font-weight: 900 !important;
        font-size: 2.8rem !important;
    }
   
    div[data-testid="stMetric"] * {
        color: #0c4a6e !important;
    }
   
    .stInfo {
        background: linear-gradient(135deg, #dbeafe 0%, #bae6fd 100%) !important;
        border-left: 6px solid #0284c7 !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
    }
   
    .stInfo * {
        color: #0c4a6e !important;
        font-weight: 600 !important;
    }
   
    .stSuccess {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%) !important;
        border-left: 6px solid #059669 !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
    }
   
    .stSuccess * {
        color: #064e3b !important;
        font-weight: 600 !important;
    }
   
    .stWarning {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%) !important;
        border-left: 6px solid #d97706 !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
    }
   
    .stWarning * {
        color: #78350f !important;
        font-weight: 600 !important;
    }
   
    .stError {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%) !important;
        border-left: 6px solid #dc2626 !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
    }
   
    .stError * {
        color: #7f1d1d !important;
        font-weight: 600 !important;
    }
   
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: rgba(226, 232, 240, 0.1);
        padding: 15px;
        border-radius: 15px;
    }
   
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px !important;
        padding: 14px 28px !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        color: #e0f2fe !important;
        border: 2px solid rgba(14, 165, 233, 0.3) !important;
    }
   
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #0ea5e9 0%, #2563eb 100%) !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(14, 165, 233, 0.5);
    }
   
    .streamlit-expanderHeader {
        background: rgba(14, 165, 233, 0.2) !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        color: #e0f2fe !important;
        padding: 15px !important;
        border: 2px solid rgba(14, 165, 233, 0.5) !important;
    }
   
    .stDataFrame {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
   
    .match-card {
        padding: 25px;
        border-radius: 15px;
        margin: 15px 0;
        background: rgba(14, 165, 233, 0.1);
        border: 3px solid #0ea5e9;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        backdrop-filter: blur(10px);
    }
   
    .match-card h3, .match-card p {
        color: #e0f2fe !important;
    }
   
    .score-box {
        background: linear-gradient(135deg, #0ea5e9, #2563eb);
        color: white;
        padding: 16px;
        border-radius: 12px;
        text-align: center;
        font-weight: bold;
        font-size: 1.4rem;
        margin: 10px 0;
    }

    hr {
        margin: 2.5rem 0;
        border: none;
        height: 3px;
        background: linear-gradient(90deg, transparent, #0ea5e9, transparent);
    }
    
    /* Radio button styling for sidebar */
    .stRadio > label {
        color: #e0f2fe !important;
        font-weight: 800 !important;
        font-size: 1.2rem !important;
    }
    
    .stRadio > div {
        background: rgba(14, 165, 233, 0.1);
        padding: 10px;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ==================== SETUP ====================
DATABASE_URL = st.secrets.get("DATABASE_URL") or st.secrets.get("postgres", {}).get("url") or os.environ.get("DATABASE_URL")
RAPIDAPI_KEY = st.secrets.get("RAPIDAPI_KEY") or st.secrets.get("rapidapi_key") or os.environ.get("RAPIDAPI_KEY")

engine = None
if DATABASE_URL:
    @st.cache_resource
    def get_engine(db_url):
        return create_engine(db_url, pool_pre_ping=True, pool_size=10)
    try:
        engine = get_engine(DATABASE_URL)
        with engine.connect():
            pass
    except:
        engine = None

def fetch_cricbuzz(endpoint: str) -> Optional[Dict]:
    if not RAPIDAPI_KEY:
        return None
    try:
        r = requests.get(
            f"https://cricbuzz-cricket.p.rapidapi.com/{endpoint}",
            headers={"X-RapidAPI-Key": RAPIDAPI_KEY, "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com"},
            timeout=15
        )
        return r.json() if r.status_code == 200 else None
    except:
        return None

def run_sql_query(sql: str) -> pd.DataFrame:
    if not engine:
        return pd.DataFrame()
    try:
        with engine.connect() as conn:
            return pd.read_sql_query(text(sql), conn)
    except Exception as e:
        st.error(f"SQL Error: {e}")
        return pd.DataFrame()

def format_time(ms):
    if not ms: return "N/A"
    try:
        return datetime.fromtimestamp(int(ms)/1000).strftime("%d %b %Y, %I:%M %p")
    except:
        return "N/A"

# ==================== 25 SQL QUERIES (ALL KEPT) ====================
SQL_QUERIES = {
    "Q1 - Top 20 ODI Run Scorers": "SELECT player_name, runs, batting_avg, matches_played FROM odi_batting_stats ORDER BY runs DESC LIMIT 20;",
    "Q2 - All Indian Players": "SELECT name, battingstyle, bowlingstyle FROM indian_players LIMIT 50;",
    "Q3 - Best All-Rounders": "SELECT player_name, total_runs, total_wickets FROM all_rounders ORDER BY (total_runs + total_wickets*20) DESC LIMIT 20;",
    "Q4 - Recent Match Results": "SELECT match_desc, team1_name, team2_name, status FROM recent_matches ORDER BY match_date DESC LIMIT 30;",
    "Q5 - Top Partnerships": "SELECT player_names, combined_partnership_runs FROM partnerships ORDER BY combined_partnership_runs DESC LIMIT 20;",
    "Q6 - Bowler by Venue": "SELECT bowler, venue, total_wickets FROM bowler_venue_stats ORDER BY total_wickets DESC LIMIT 30;",
    "Q7 - Player Career": "SELECT player, test_matches, odi_matches, total_matches FROM player_career_summary LIMIT 30;",
    "Q8 - Toss Impact": "SELECT format, win_percent_choose_bat_first FROM toss_advantage_stats;",
    "Q9 - Team Performance": "SELECT team, home_wins, away_wins FROM team_home_away_wins LIMIT 20;",
    "Q10 - Recent Form": "SELECT player, avg_runs_last5 FROM recent_form LIMIT 20;",
    "Q11 - Economical Bowlers": "SELECT bowler, overall_economy_rate FROM bowlers_aggregate ORDER BY overall_economy_rate ASC LIMIT 20;",
    "Q12 - Batting Distribution": "SELECT player, avg_runs_scored FROM player_batting_distribution LIMIT 20;",
    "Q13 - Clutch Batting": "SELECT player, batting_average_close_matches FROM clutch_batting_stats LIMIT 20;",
    "Q14 - Yearly Stats": "SELECT player, year, matches_played FROM player_yearly_stats WHERE year >= 2020 LIMIT 30;",
    "Q15 - Head to Head": "SELECT pair, total_matches FROM head_to_head_series LIMIT 20;",
    "Q16 - Top Scorers": "SELECT format, batter, highest_score FROM top_scorers_in_every_format LIMIT 20;",
    "Q17 - Player Styles": "SELECT battingstyle, COUNT(*) FROM indian_players GROUP BY battingstyle LIMIT 20;",
    "Q18 - High Capacity Venues": "SELECT venue_name, capacity FROM cricket_venues WHERE capacity > 50000 LIMIT 20;",
    "Q19 - Matches by Winner": "SELECT winner_sname, COUNT(*) FROM cricket_matches WHERE winner_sname IS NOT NULL GROUP BY winner_sname LIMIT 15;",
    "Q20 - Quarterly Performance": "SELECT player, quarter, avg_runs FROM player_quarterly_stats LIMIT 30;",
    "Q21 - All-Rounders 1000+": "SELECT player_name, total_runs FROM all_rounders WHERE total_runs > 1000 LIMIT 20;",
    "Q22 - Last 20 Matches": "SELECT match_desc, team1_name FROM cricket_matches_20 LIMIT 20;",
    "Q23 - Bowler Venue 3+": "SELECT bowler, venue, matches FROM bowler_venue_stats WHERE matches >= 3 LIMIT 25;",
    "Q24 - Partnerships 50+": "SELECT player_names, combined_partnership_runs FROM partnerships WHERE combined_partnership_runs >= 50 LIMIT 25;",
    "Q25 - Series 2024": "SELECT series_name, host_country FROM cricket_series_2024 LIMIT 20;"
}

# ==================== HEADER & SIDEBAR - SINGLE MENU ====================
st.title("🏏 Cricbuzz LiveStats")
st.subheader("Real-Time Cricket Insights & SQL-Based Analytics")
st.markdown("---")

# SIDEBAR - SINGLE NAVIGATION
st.sidebar.title("📊 Navigation")
st.sidebar.markdown("---")

# Single menu using radio buttons
page = st.sidebar.radio(
    "Choose a page:",
    ["🏠 Home", "🔴 Live Matches", "📈 Top Stats", "💻 SQL Analytics", "👥 Player CRUD"],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.markdown("### System Status")
st.sidebar.success("✅ API Connected" if RAPIDAPI_KEY else "❌ API Disconnected")
st.sidebar.success("✅ Database Online" if engine else "❌ Database Offline")

# ==================== HOME ====================
if page == "🏠 Home":
    st.header("Welcome to Cricbuzz LiveStats!")
    col1, col2, col3 = st.columns(3)
    col1.metric("API Status", "🟢 Active" if RAPIDAPI_KEY else "🔴 Disabled")
    col2.metric("Database", "🟢 Online" if engine else "🔴 Offline")
    col3.metric("SQL Queries", "25")
    st.markdown("---")
    st.success("**📺 Live Cricket** - Real-time match updates, detailed scorecards, live scores")
    st.info("**📊 Analytics** - 25 SQL queries, 25+ database tables, full CRUD operations")
    st.warning("**⚡ Performance** - Fast queries, real-time data, responsive UI")

# ==================== LIVE MATCHES ====================
elif page == "🔴 Live Matches":
    st.header("🔴 Live Cricket Matches")
    st.markdown("---")

    if not RAPIDAPI_KEY:
        st.error("❌ Add RAPIDAPI_KEY in Streamlit Secrets to view live matches")
        st.stop()

    data = fetch_cricbuzz("matches/v1/live")
    if not data or "typeMatches" not in data:
        st.warning("⚠️ No live matches currently. Showing recent matches...")
        data = fetch_cricbuzz("matches/v1/recent")

    if not data:
        st.error("❌ Failed to fetch matches from API")
        st.stop()

    for category in data.get("typeMatches", []):
        match_type = category.get("matchType", "").upper()
        with st.expander(f"🏏 {match_type} Matches", expanded=True):
            for series in category.get("seriesMatches", []):
                series_info = series.get("seriesAdWrapper", {}) or series.get("adWrapper", {})
                if not series_info:
                    continue
                series_name = series_info.get("seriesName", "Match")
                matches = series_info.get("matches", [])
                if matches:
                    st.subheader(f"📍 {series_name}")

                for match in matches:
                    info = match.get("matchInfo", {})
                    score = match.get("matchScore", {})
                    match_id = str(info.get("matchId", ""))

                    t1 = info.get("team1", {}).get("teamName", "Team 1")
                    t2 = info.get("team2", {}).get("teamName", "Team 2")
                    t1s = info.get("team1", {}).get("teamSName", "T1")
                    t2s = info.get("team2", {}).get("teamSName", "T2")

                    # Match card
                    st.markdown(f"""
                    <div style="text-align:center; padding:20px; background:linear-gradient(135deg,#0ea5e9,#2563eb); border-radius:15px; color:white; margin:20px 0;">
                        <h3 style="margin:0;">{t1} vs {t2}</h3>
                        <p style="margin:8px 0; font-size:1.1rem;">{info.get('matchDesc','')} • {info.get('matchFormat','')}</p>
                        <p style="margin:8px 0; font-weight:bold; color:#86efac; font-size:1.3rem;">{info.get('status','Starting soon')}</p>
                        <p style="margin:5px 0; font-size:0.95rem;">Venue: {info.get('venueInfo', {}).get('ground','')} • Start: {format_time(info.get('startDate'))}</p>
                    </div>
                    """, unsafe_allow_html=True)

                    # Live scores
                    c1, c2, c3 = st.columns([2, 2, 2])
                    with c1:
                        if score.get("team1Score", {}).get("inngs1"):
                            s = score["team1Score"]["inngs1"]
                            st.markdown(f"<div style='text-align:center; background:#0ea5e9; color:white; padding:15px; border-radius:12px; font-weight:bold;'>{t1s}<br>{s.get('runs',0)}/{s.get('wickets',0)} ({s.get('overs','')})</div>", unsafe_allow_html=True)
                    with c2:
                        st.markdown("<h2 style='text-align:center; color:#0ea5e9; margin-top:20px;'>VS</h2>", unsafe_allow_html=True)
                    with c3:
                        if score.get("team2Score", {}).get("inngs1"):
                            s = score["team2Score"]["inngs1"]
                            st.markdown(f"<div style='text-align:center; background:#0ea5e9; color:white; padding:15px; border-radius:12px; font-weight:bold;'>{t2s}<br>{s.get('runs',0)}/{s.get('wickets',0)} ({s.get('overs','')})</div>", unsafe_allow_html=True)

                    # Full scorecard button
                    if st.button("📊 Full Scorecard", key=f"sc_{match_id}", use_container_width=True):
                        with st.spinner("Loading scorecard..."):
                            sc = fetch_cricbuzz(f"mcenter/v1/{match_id}/scard")
                            if not sc or ("scorecard" not in sc and "scoreCard" not in sc):
                                st.warning("⚠️ Scorecard not available yet")
                                continue

                            scorecard = sc.get("scorecard") or sc.get("scoreCard", [])

                            for i, inn in enumerate(scorecard, 1):
                                team = inn.get("batTeamName") or inn.get("batteamname", "Team")

                                st.markdown(f"""
                                <div style="text-align:center; margin:30px 0 20px 0;">
                                    <h3 style="color:#0ea5e9; margin:0;">Innings {i} — {team}</h3>
                                </div>
                                """, unsafe_allow_html=True)

                                col_left, col_right = st.columns(2)
                                with col_left:
                                    st.markdown("**⚾ Batting**")
                                    bats = []
                                    batsmen_data = inn.get("batsmenData") or inn.get("batsman") or {}
                                    for p in batsmen_data.values() if isinstance(batsmen_data, dict) else batsmen_data:
                                        if isinstance(p, dict):
                                            bats.append({
                                                "Batsman": p.get("batName") or p.get("name", "—"),
                                                "R": p.get("runs", 0),
                                                "B": p.get("balls", 0),
                                                "4s": p.get("fours", 0),
                                                "6s": p.get("sixes", 0),
                                                "SR": p.get("strikeRate") or p.get("strkrate", "0"),
                                                "Out": p.get("outDesc") or p.get("outdec", "not out")
                                            })
                                    if bats:
                                        st.dataframe(pd.DataFrame(bats), use_container_width=True, hide_index=True)
                                    else:
                                        st.info("No batting data")

                                with col_right:
                                    st.markdown("**🎯 Bowling**")
                                    bowls = []
                                    bowlers_data = inn.get("bowlersData") or inn.get("bowler") or {}
                                    for p in bowlers_data.values() if isinstance(bowlers_data, dict) else bowlers_data:
                                        if isinstance(p, dict):
                                            bowls.append({
                                                "Bowler": p.get("bowlName") or p.get("name", "—"),
                                                "O": p.get("overs", "0"),
                                                "M": p.get("maidens", 0),
                                                "R": p.get("runs", 0),
                                                "W": p.get("wickets", 0),
                                                "Econ": p.get("economy") or "0.0"
                                            })
                                    if bowls:
                                        st.dataframe(pd.DataFrame(bowls), use_container_width=True, hide_index=True)
                                    else:
                                        st.info("No bowling data")

                                st.markdown("---")

                    st.markdown("<hr style='border:2px solid #0ea5e9; margin:50px 0;'>", unsafe_allow_html=True)

# ==================== TOP STATS ====================
elif page == "📈 Top Stats":
    st.header("📈 Top Cricket Statistics")
    st.markdown("---")
    table_map = {
        "ODI Batting Stats": "odi_batting_stats",
        "Indian Players": "indian_players",
        "All-Rounders": "all_rounders",
        "Bowlers Aggregate": "bowlers_aggregate",
        "Recent Matches": "recent_matches"
    }
    col1, col2 = st.columns(2)
    with col1:
        selected = st.selectbox("Select Table", list(table_map.keys()))
    with col2:
        limit = st.selectbox("Number of Records", [10, 20, 50, 100])
    if engine and st.button("📊 Load Data", type="primary"):
        df = run_sql_query(f"SELECT * FROM {table_map[selected]} LIMIT {limit}")
        if not df.empty:
            st.success(f"✅ Loaded {len(df)} records")
            st.dataframe(df, use_container_width=True, height=600)
        else:
            st.warning("⚠️ No data found")

# ==================== SQL ANALYTICS ====================
elif page == "💻 SQL Analytics":
    st.header("💻 SQL Analytics Dashboard")
    st.markdown("**25 Pre-Built SQL Queries**")
    st.markdown("---")
    query_name = st.selectbox("Select Query", list(SQL_QUERIES.keys()))
    sql = SQL_QUERIES[query_name]
    with st.expander("📝 View SQL Code"):
        st.code(sql, language="sql")
    if st.button("▶️ Execute Query", type="primary"):
        df = run_sql_query(sql)
        if not df.empty:
            st.success(f"✅ Query returned {len(df)} rows")
            st.dataframe(df, use_container_width=True, height=600)
        else:
            st.warning("⚠️ Query returned no results")

# ==================== PLAYER CRUD - IMPROVED ====================
elif page == "👥 Player CRUD":
    st.header("👥 Player Management - Full CRUD Operations")
    st.markdown("**Create • Read • Update • Delete**")
    st.markdown("---")
    
    if not engine:
        st.error("❌ Database not connected. Cannot perform CRUD operations.")
        st.stop()
    
    tabs = st.tabs(["➕ CREATE", "📖 READ", "✏️ UPDATE", "🗑️ DELETE"])

    # ==================== CREATE - WITH CUSTOM ID ====================
    with tabs[0]:
        st.subheader("➕ Add New Player")
        st.info("💡 Tip: Leave Player ID empty to auto-generate, or enter a custom ID")
        
        with st.form("create_player", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                player_id = st.number_input(
                    "Player ID (Optional - leave blank for auto-generate)", 
                    min_value=1, 
                    step=1,
                    value=None,
                    help="Leave empty to auto-generate ID"
                )
                name = st.text_input(
                    "Player Name *", 
                    placeholder="e.g., Virat Kohli, MS Dhoni, Sachin Tendulkar",
                    help="Enter any player name you want"
                )
                batting = st.text_input(
                    "Batting Style", 
                    placeholder="e.g., Right-hand bat, Left-hand bat"
                )
            with col2:
                bowling = st.text_input(
                    "Bowling Style", 
                    placeholder="e.g., Right-arm medium, Left-arm orthodox"
                )
                st.markdown("### Preview")
                if name:
                    st.success(f"✅ Ready to add: **{name}**")
                else:
                    st.warning("⚠️ Enter player name")
            
            submitted = st.form_submit_button("➕ Add Player", type="primary", use_container_width=True)
            
            if submitted:
                if not name or name.strip() == "":
                    st.error("❌ Player name is required!")
                else:
                    try:
                        with engine.connect() as conn:
                            # Check if custom ID is provided
                            if player_id is not None:
                                # Check if ID already exists
                                check = conn.execute(
                                    text("SELECT id FROM indian_players WHERE id = :id"), 
                                    {"id": player_id}
                                ).fetchone()
                                
                                if check:
                                    st.error(f"❌ Player ID {player_id} already exists! Choose a different ID or leave blank for auto-generate.")
                                else:
                                    # Insert with custom ID
                                    conn.execute(
                                        text("INSERT INTO indian_players (id, name, battingstyle, bowlingstyle) VALUES (:id, :n, :bat, :bowl)"),
                                        {"id": player_id, "n": name.strip(), "bat": batting.strip() or None, "bowl": bowling.strip() or None}
                                    )
                                    conn.commit()
                                    st.success(f"✅ Player '{name}' added successfully with ID: {player_id}!")
                                    st.balloons()
                            else:
                                # Auto-generate ID
                                conn.execute(
                                    text("INSERT INTO indian_players (name, battingstyle, bowlingstyle) VALUES (:n, :bat, :bowl)"),
                                    {"n": name.strip(), "bat": batting.strip() or None, "bowl": bowling.strip() or None}
                                )
                                conn.commit()
                                st.success(f"✅ Player '{name}' added successfully with auto-generated ID!")
                                st.balloons()
                                
                    except Exception as e:
                        st.error(f"❌ Database Error: {e}")

    # ==================== READ ====================
    with tabs[1]:
        st.subheader("📖 View All Players")
        search = st.text_input("🔍 Search by player name", placeholder="Type player name to search...")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📊 Load All Players", type="primary", use_container_width=True):
                sql = "SELECT * FROM indian_players ORDER BY id DESC LIMIT 100"
                df = run_sql_query(sql)
                if not df.empty:
                    st.success(f"✅ Found {len(df)} player(s)")
                    st.dataframe(df, use_container_width=True, height=600)
                    csv = df.to_csv(index=False).encode()
                    st.download_button("⬇️ Download CSV", csv, "players.csv", "text/csv", use_container_width=True)
                else:
                    st.warning("⚠️ No players found in database")
        
        with col2:
            if st.button("🔍 Search Players", type="secondary", use_container_width=True):
                if search:
                    sql = f"SELECT * FROM indian_players WHERE LOWER(name) LIKE LOWER('%{search}%') ORDER BY id DESC LIMIT 100"
                    df = run_sql_query(sql)
                    if not df.empty:
                        st.success(f"✅ Found {len(df)} player(s) matching '{search}'")
                        st.dataframe(df, use_container_width=True, height=600)
                    else:
                        st.warning(f"⚠️ No players found matching '{search}'")
                else:
                    st.warning("⚠️ Enter a search term first")

    # ==================== UPDATE ====================
    with tabs[2]:
        st.subheader("✏️ Update Player Information")
        
        player_id = st.number_input("Enter Player ID to Update", min_value=1, step=1, key="update_id")
        
        if st.button("🔍 Load Player Data", type="primary"):
            if engine:
                try:
                    with engine.connect() as conn:
                        result = conn.execute(
                            text("SELECT * FROM indian_players WHERE id = :id"), 
                            {"id": player_id}
                        ).fetchone()
                        
                        if result:
                            st.session_state['update_player'] = {
                                'id': result.id,
                                'name': result.name,
                                'battingstyle': result.battingstyle,
                                'bowlingstyle': result.bowlingstyle
                            }
                            st.success(f"✅ Loaded player: **{result.name}** (ID: {result.id})")
                        else:
                            st.error(f"❌ No player found with ID: {player_id}")
                except Exception as e:
                    st.error(f"❌ Error: {e}")
        
        if 'update_player' in st.session_state:
            player = st.session_state['update_player']
            
            with st.form("update_player"):
                st.info(f"Editing Player ID: **{player['id']}**")
                
                col1, col2 = st.columns(2)
                with col1:
                    new_name = st.text_input("Player Name", value=player['name'])
                    new_batting = st.text_input("Batting Style", value=player['battingstyle'] or "")
                with col2:
                    new_bowling = st.text_input("Bowling Style", value=player['bowlingstyle'] or "")
                
                col_save, col_cancel = st.columns(2)
                with col_save:
                    save_btn = st.form_submit_button("💾 Save Changes", type="primary", use_container_width=True)
                with col_cancel:
                    cancel_btn = st.form_submit_button("❌ Cancel", use_container_width=True)
                
                if save_btn:
                    if not new_name or new_name.strip() == "":
                        st.error("❌ Player name cannot be empty!")
                    else:
                        try:
                            with engine.connect() as conn:
                                conn.execute(
                                    text("UPDATE indian_players SET name=:n, battingstyle=:bat, bowlingstyle=:bowl WHERE id=:id"),
                                    {
                                        "n": new_name.strip(), 
                                        "bat": new_batting.strip() or None, 
                                        "bowl": new_bowling.strip() or None, 
                                        "id": player['id']
                                    }
                                )
                                conn.commit()
                            st.success(f"✅ Player updated successfully!")
                            del st.session_state['update_player']
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Update failed: {e}")
                
                if cancel_btn:
                    del st.session_state['update_player']
                    st.rerun()

    # ==================== DELETE ====================
    with tabs[3]:
        st.subheader("🗑️ Delete Player")
        st.warning("⚠️ **Warning:** This action cannot be undone!")
        
        delete_id = st.number_input("Enter Player ID to Delete", min_value=1, step=1, key="delete_id")
        
        # Preview player before delete
        if st.button("👁️ Preview Player", type="secondary"):
            try:
                with engine.connect() as conn:
                    check = conn.execute(
                        text("SELECT * FROM indian_players WHERE id = :id"), 
                        {"id": delete_id}
                    ).fetchone()
                    
                    if check:
                        st.info(f"**Player Details:**\n- ID: {check.id}\n- Name: {check.name}\n- Batting: {check.battingstyle or 'N/A'}\n- Bowling: {check.bowlingstyle or 'N/A'}")
                        st.session_state['delete_preview'] = check.name
                    else:
                        st.error(f"❌ No player found with ID: {delete_id}")
            except Exception as e:
                st.error(f"❌ Error: {e}")
        
        confirm = st.checkbox("✅ I confirm I want to delete this player permanently")
        
        if st.button("🗑️ DELETE PLAYER", type="secondary", use_container_width=True):
            if not confirm:
                st.error("❌ Please check the confirmation box first!")
            elif engine:
                try:
                    with engine.connect() as conn:
                        check = conn.execute(
                            text("SELECT name FROM indian_players WHERE id = :id"), 
                            {"id": delete_id}
                        ).fetchone()
                        
                        if check:
                            conn.execute(
                                text("DELETE FROM indian_players WHERE id = :id"), 
                                {"id": delete_id}
                            )
                            conn.commit()
                            st.success(f"✅ Player '{check.name}' (ID: {delete_id}) has been deleted!")
                            if 'delete_preview' in st.session_state:
                                del st.session_state['delete_preview']
                            st.rerun()
                        else:
                            st.error(f"❌ No player found with ID: {delete_id}")
                except Exception as e:
                    st.error(f"❌ Delete failed: {e}")

# ==================== FOOTER ====================
st.markdown("---")
st.markdown("""
<div style='text-align:center; padding:30px; background:linear-gradient(135deg, #0ea5e9, #2563eb);
     color:white; border-radius:15px;'>
    <h2 style='color:white !important;'>🏏 Cricbuzz LiveStats</h2>
    <p style='color:white !important; font-size:1.1rem;'>25 Queries • 25+ Tables • Full CRUD • Real-Time API</p>
    <p style='color:#bae6fd !important; font-size:0.9rem; margin-top:10px;'>Built with Streamlit • Powered by RapidAPI & PostgreSQL</p>
</div>
""", unsafe_allow_html=True)
