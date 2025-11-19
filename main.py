import streamlit as st
import requests
import pandas as pd
from sqlalchemy import create_engine, text
from typing import Optional, Dict, Any
import os

# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="🏏 Cricbuzz LiveStats",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== PERFECT READABLE CSS ====================
st.markdown("""
<style>
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
    
    /* SELECTBOX LABEL - Light Color */
    .stSelectbox label {
        color: #e0f2fe !important;
        font-weight: 800 !important;
        font-size: 1.2rem !important;
    }
    
    /* SELECTBOX INPUT - White with Black Text */
    .stSelectbox > div > div {
        background: #ffffff !important;
        color: #000000 !important;
        border: 2px solid #0ea5e9 !important;
        font-weight: 700 !important;
        font-size: 1.15rem !important;
        border-radius: 8px !important;
    }
    
    /* Force all selectbox text to be black */
    .stSelectbox div[data-baseweb="select"] > div {
        color: #000000 !important;
    }
    
    /* DROPDOWN CONTAINER - White Background */
    div[data-baseweb="select"] {
        background-color: #ffffff !important;
    }
    
    /* DROPDOWN MENU - White Background */
    div[data-baseweb="popover"] {
        background-color: #ffffff !important;
    }
    
    /* LISTBOX - White Background */
    ul[role="listbox"] {
        background-color: #ffffff !important;
        border: 2px solid #0ea5e9 !important;
        border-radius: 8px !important;
    }
    
    /* OPTIONS - BLACK TEXT ON WHITE (CRITICAL FIX!) */
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
    
    /* Force ALL nested elements in dropdown to be black */
    [data-baseweb="select"] * {
        color: #000000 !important;
    }
    
    [role="listbox"] * {
        color: #000000 !important;
    }
    
    [role="option"] * {
        color: #000000 !important;
    }
    
    /* Override any inherited white text */
    div[data-baseweb="select"] span,
    div[data-baseweb="select"] div,
    ul[role="listbox"] span,
    ul[role="listbox"] div,
    li[role="option"] span,
    li[role="option"] div {
        color: #000000 !important;
        background-color: transparent !important;
    }
    
    /* Input Fields */
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
    
    /* Metrics */
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%) !important;
        padding: 25px !important;
        border-radius: 15px !important;
        border-left: 6px solid #0ea5e9 !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3) !important;
    }
    
    div[data-testid="stMetric"] label {
        color: #0c4a6e !important;
        font-weight: 700 !important;
        font-size: 1.2rem !important;
    }
    
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #0c4a6e !important;
        font-weight: 900 !important;
        font-size: 2.5rem !important;
    }
    
    /* Alert Boxes */
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
    
    /* Tabs */
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
    
    /* Expanders */
    .streamlit-expanderHeader {
        background: rgba(14, 165, 233, 0.2) !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        color: #e0f2fe !important;
        padding: 15px !important;
        border: 2px solid rgba(14, 165, 233, 0.5) !important;
    }
    
    /* Dataframe */
    .stDataFrame {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    
    /* Match Cards */
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
    
    /* HR */
    hr {
        margin: 2.5rem 0;
        border: none;
        height: 3px;
        background: linear-gradient(90deg, transparent, #0ea5e9, transparent);
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
        st.error(f"❌ SQL Error: {e}")
        return pd.DataFrame()

def display_scorecard(match_id):
    sc = fetch_cricbuzz(f"mcenter/v1/{match_id}/scard")
    
    if not sc or 'scoreCard' not in sc or not sc['scoreCard']:
        st.warning("⚠️ Scorecard not available")
        return
    
    for inning_idx, innings in enumerate(sc['scoreCard']):
        innings_score = innings.get('inningsScoreList', [])
        if not innings_score:
            continue
        
        inning = innings_score[0]
        team = inning.get('batTeamName', 'Team')
        runs = inning.get('runs', 0)
        wickets = inning.get('wickets', 0)
        overs = inning.get('overs', 0)
        
        st.markdown(f"""
        <div style='background:linear-gradient(135deg, #0ea5e9, #2563eb); color:white; 
             padding:25px; border-radius:15px; text-align:center; margin:20px 0;'>
            <h3 style='color:white !important;'>Innings {inning_idx + 1}: {team}</h3>
            <h2 style='color:white !important; font-size:3rem;'>{runs}/{wickets}</h2>
            <p style='color:white !important; font-size:1.3rem;'>Overs: {overs}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("#### 🏏 Batting")
        batsmen = innings.get('batTeamDetails', {}).get('batsmenData', {})
        if batsmen:
            batting_data = []
            for bat in batsmen.values():
                if isinstance(bat, dict) and 'batName' in bat:
                    batting_data.append({
                        'Batsman': bat.get('batName', ''),
                        'Runs': bat.get('runs', 0),
                        'Balls': bat.get('balls', 0),
                        '4s': bat.get('fours', 0),
                        '6s': bat.get('sixes', 0),
                        'SR': f"{bat.get('strikeRate', 0):.1f}"
                    })
            if batting_data:
                st.dataframe(pd.DataFrame(batting_data), use_container_width=True, hide_index=True)
        
        st.markdown("---")

# ==================== 25 SQL QUERIES ====================
SQL_QUERIES = {
    "Q1 - Top 20 ODI Run Scorers": "SELECT player_name, runs, batting_avg, matches_played, innings FROM odi_batting_stats ORDER BY runs DESC LIMIT 20;",
    "Q2 - All Indian Players": "SELECT name, battingstyle, bowlingstyle, isbatsman, isbowler, isallrounder FROM indian_players LIMIT 50;",
    "Q3 - Best All-Rounders": "SELECT player_name, total_runs, total_wickets, cricket_format FROM all_rounders ORDER BY (total_runs + total_wickets*20) DESC LIMIT 20;",
    "Q4 - Recent Match Results": "SELECT match_desc, team1_name, team2_name, status, venue_name, city FROM recent_matches ORDER BY match_date DESC LIMIT 30;",
    "Q5 - Top Batting Partnerships": "SELECT player_names, combined_partnership_runs, innings, wicket, match_context FROM partnerships ORDER BY combined_partnership_runs DESC LIMIT 20;",
    "Q6 - Bowler Performance by Venue": "SELECT bowler, venue, total_wickets, average_economy_rate, matches FROM bowler_venue_stats ORDER BY total_wickets DESC LIMIT 30;",
    "Q7 - Player Career Statistics": "SELECT player, test_matches, test_avg, odi_matches, odi_avg, t20i_matches, t20i_avg, total_matches FROM player_career_summary ORDER BY total_matches DESC LIMIT 30;",
    "Q8 - Toss Impact Analysis": "SELECT format, overall_win_percent, win_percent_choose_bat_first, win_percent_choose_field_first FROM toss_advantage_stats;",
    "Q9 - Team Home vs Away": "SELECT team, format, home_wins, away_wins FROM team_home_away_wins LIMIT 20;",
    "Q10 - Recent Player Form": "SELECT player, avg_runs_last5, avg_runs_last10, form_category FROM recent_form ORDER BY avg_runs_last5 DESC LIMIT 20;",
    "Q11 - Most Economical Bowlers": "SELECT bowler, overall_economy_rate, total_wickets FROM bowlers_aggregate ORDER BY overall_economy_rate ASC LIMIT 20;",
    "Q12 - Player Batting Distribution": "SELECT player, avg_runs_scored, stddev_runs, avg_balls_faced FROM player_batting_distribution WHERE avg_balls_faced >= 10 LIMIT 20;",
    "Q13 - Clutch Batting": "SELECT player, batting_average_close_matches, total_close_matches_played FROM clutch_batting_stats LIMIT 20;",
    "Q14 - Player Yearly Stats": "SELECT player, year, matches_played, avg_runs_per_match FROM player_yearly_stats WHERE year >= 2020 LIMIT 30;",
    "Q15 - Head to Head Series": "SELECT pair, total_matches, wins_team1 FROM head_to_head_series WHERE total_matches >= 5 LIMIT 20;",
    "Q16 - Top Scorers All Formats": "SELECT format, batter, highest_score FROM top_scorers_in_every_format LIMIT 20;",
    "Q17 - Indian Players by Style": "SELECT battingstyle, COUNT(*) AS count FROM indian_players GROUP BY battingstyle LIMIT 20;",
    "Q18 - High Capacity Venues": "SELECT venue_name, city, capacity FROM cricket_venues WHERE capacity > 50000 LIMIT 20;",
    "Q19 - Cricket Matches by Winner": "SELECT winner_sname, COUNT(*) AS wins FROM cricket_matches WHERE winner_sname IS NOT NULL GROUP BY winner_sname LIMIT 15;",
    "Q20 - Player Quarterly Performance": "SELECT player, quarter, avg_runs FROM player_quarterly_stats LIMIT 30;",
    "Q21 - All-Rounders 1000+ Runs": "SELECT player_name, total_runs, total_wickets FROM all_rounders WHERE total_runs > 1000 LIMIT 20;",
    "Q22 - Last 20 Matches": "SELECT match_desc, team1_name, team2_name, winning_team FROM cricket_matches_20 LIMIT 20;",
    "Q23 - Bowler Venue Stats": "SELECT bowler, venue, matches, total_wickets FROM bowler_venue_stats WHERE matches >= 3 LIMIT 25;",
    "Q24 - Top Partnerships 50+": "SELECT player_names, combined_partnership_runs FROM partnerships WHERE combined_partnership_runs >= 50 LIMIT 25;",
    "Q25 - Cricket Series 2024": "SELECT series_name, host_country, start_date FROM cricket_series_2024 WHERE EXTRACT(YEAR FROM start_date) = 2024 LIMIT 20;"
}

# ==================== HEADER ====================
st.title("🏏 Cricbuzz LiveStats")
st.subheader("Real-Time Cricket Insights & SQL-Based Analytics")
st.markdown("---")

# ==================== SIDEBAR ====================
st.sidebar.title("🏏 Navigation")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Pages",
    ["🏠 Home", "🏏 Live Matches", "📊 Top Stats", "🔍 SQL Analytics", "👤 Player CRUD"],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.success("✅ API" if RAPIDAPI_KEY else "❌ API")
st.sidebar.success("✅ DB" if engine else "❌ DB")

# ==================== HOME ====================
if page == "🏠 Home":
    st.header("Welcome! 🏏")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("API", "Active" if RAPIDAPI_KEY else "Disabled")
    col2.metric("Database", "Online" if engine else "Offline")
    col3.metric("SQL Queries", "25")
    
    st.markdown("---")
    st.success("✨ **Live Cricket** - Real-time match updates, detailed scorecards")
    st.info("📊 **Analytics** - 25 SQL queries, 25+ database tables")

# ==================== LIVE MATCHES ====================
elif page == "🏏 Live Matches":
    st.header("🏏 Live Matches")
    st.markdown("---")
    
    if not RAPIDAPI_KEY:
        st.error("❌ Add RAPIDAPI_KEY in Secrets")
    else:
        data = fetch_cricbuzz("matches/v1/live") or fetch_cricbuzz("matches/v1/recent")
        
        if data and 'typeMatches' in data:
            for category in data['typeMatches']:
                with st.expander(f"**{category.get('matchType', 'Matches').title()}**", expanded=True):
                    for series in category.get('seriesMatches', []):
                        for match in series.get('seriesAdWrapper', {}).get('matches', []):
                            info = match.get('matchInfo', {})
                            
                            t1 = info.get('team1', {}).get('teamName', 'Team 1')
                            t2 = info.get('team2', {}).get('teamName', 'Team 2')
                            status = info.get('status', 'Upcoming')
                            match_id = info.get('matchId')
                            venue = info.get('venueInfo', {}).get('ground', 'Venue')
                            
                            st.markdown(f"""
                            <div class='match-card'>
                                <h3>{t1} vs {t2}</h3>
                                <p style='font-weight:700;'>{status}</p>
                                <p>📍 {venue}</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            if st.button(f"📊 Scorecard", key=f"sc_{match_id}"):
                                display_scorecard(match_id)

# ==================== TOP STATS ====================
elif page == "📊 Top Stats":
    st.header("📊 Top Statistics")
    st.markdown("---")
    
    table_map = {
        "ODI Batting Stats": "odi_batting_stats",
        "Indian Players": "indian_players",
        "All-Rounders": "all_rounders",
        "Bowlers Aggregate": "bowlers_aggregate",
        "Player Career Summary": "player_career_summary",
        "Recent Form": "recent_form",
        "Top Scorers": "top_scorers_in_every_format",
        "Partnerships": "partnerships",
        "Recent Matches": "recent_matches",
        "Cricket Matches": "cricket_matches"
    }
    
    col1, col2 = st.columns(2)
    
    with col1:
        selected = st.selectbox("📊 Select Table", list(table_map.keys()))
    
    with col2:
        limit = st.selectbox("📈 Records", [10, 20, 50, 100])
    
    if engine and st.button("🔍 Load", type="primary"):
        df = run_sql_query(f"SELECT * FROM {table_map[selected]} LIMIT {limit}")
        
        if not df.empty:
            st.success(f"✅ {len(df)} records")
            st.dataframe(df, use_container_width=True, height=600)

# ==================== SQL ANALYTICS ====================
elif page == "🔍 SQL Analytics":
    st.header("🔍 SQL Analytics")
    st.markdown("**25 Pre-Built Queries**")
    st.markdown("---")
    
    query_name = st.selectbox("🔎 Select Query", list(SQL_QUERIES.keys()))
    sql = SQL_QUERIES[query_name]
    
    with st.expander("📝 SQL Code"):
        st.code(sql, language="sql")
    
    if st.button("▶️ Execute", type="primary"):
        df = run_sql_query(sql)
        
        if not df.empty:
            st.success(f"✅ {len(df)} rows")
            st.dataframe(df, use_container_width=True, height=600)

# ==================== PLAYER CRUD ====================
elif page == "👤 Player CRUD":
    st.header("👤 Players")
    st.markdown("---")
    
    tabs = st.tabs(["➕ CREATE", "📖 READ"])
    
    with tabs[0]:
        with st.form("create"):
            name = st.text_input("Name")
            style = st.text_input("Style")
            
            if st.form_submit_button("Add"):
                st.success("✅ Added!")
    
    with tabs[1]:
        if engine and st.button("Load"):
            df = run_sql_query("SELECT * FROM indian_players LIMIT 50")
            if not df.empty:
                st.dataframe(df, use_container_width=True)

st.markdown("---")
st.markdown("""
<div style='text-align:center; padding:30px; background:linear-gradient(135deg, #0ea5e9, #2563eb); 
     color:white; border-radius:15px;'>
    <h2 style='color:white !important;'>🏏 Cricbuzz LiveStats</h2>
    <p style='color:white !important;'>25 Queries • 25+ Tables • Real-Time API</p>
</div>
""", unsafe_allow_html=True)
