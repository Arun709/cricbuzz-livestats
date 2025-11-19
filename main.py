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

# ==================== PERFECT EMI THEME + READABLE DROPDOWNS ====================
st.markdown("""
<style>
    /* Main Background - SAME AS EMI PROJECT */
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
    
    /* Headers - Light for Dark Background */
    h1 {
        color: #ffffff !important;
        font-weight: 900 !important;
        font-size: 3.5rem !important;
        text-shadow: 0 0 20px rgba(14, 165, 233, 0.5);
        border-bottom: 5px solid #0ea5e9;
        padding-bottom: 1rem;
        margin-bottom: 2rem;
        background: linear-gradient(120deg, #0ea5e9, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    h2 {
        color: #e0f2fe !important;
        font-weight: 800 !important;
        font-size: 2.2rem !important;
        margin-top: 2rem;
        padding: 15px 0;
        border-left: 6px solid #0ea5e9;
        padding-left: 20px;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    h3, h4 {
        color: #bae6fd !important;
        font-weight: 700 !important;
    }
    
    /* ALL TEXT - LIGHT FOR DARK BACKGROUND */
    p, li, span, div {
        color: #f1f5f9 !important;
        font-size: 1.1rem !important;
        line-height: 1.8 !important;
    }
    
    strong, b {
        color: #ffffff !important;
        font-weight: 800 !important;
    }
    
    /* Buttons */
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
        letter-spacing: 1.5px !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 10px 30px rgba(14, 165, 233, 0.7) !important;
    }
    
    /* Sidebar - Dark Theme */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%) !important;
        padding: 1.5rem !important;
    }
    
    section[data-testid="stSidebar"] * {
        color: #f1f5f9 !important;
        font-weight: 600 !important;
    }
    
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2 {
        color: #ffffff !important;
    }
    
    /* Radio Buttons in Sidebar - Light Text */
    section[data-testid="stSidebar"] .stRadio label {
        color: #f1f5f9 !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
    }
    
    /* SELECTBOX - WHITE BACKGROUND WITH BLACK TEXT (READABLE!) */
    .stSelectbox label {
        color: #e0f2fe !important;
        font-weight: 800 !important;
        font-size: 1.2rem !important;
    }
    
    /* Selectbox Input - White with Black Text */
    .stSelectbox > div > div {
        background: #ffffff !important;
        color: #000000 !important;
        border: 2px solid #0ea5e9 !important;
        font-weight: 700 !important;
        font-size: 1.15rem !important;
        border-radius: 8px !important;
    }
    
    /* DROPDOWN OPTIONS - WHITE WITH BLACK TEXT (CRITICAL FIX!) */
    [data-baseweb="select"] {
        background: #ffffff !important;
    }
    
    [data-baseweb="select"] div {
        background: #ffffff !important;
        color: #000000 !important;
        font-weight: 600 !important;
    }
    
    [data-baseweb="popover"] {
        background: #ffffff !important;
    }
    
    [role="listbox"] {
        background: #ffffff !important;
    }
    
    [role="option"] {
        background: #ffffff !important;
        color: #000000 !important;
        font-weight: 600 !important;
        padding: 10px !important;
    }
    
    [role="option"]:hover {
        background: #e0f2fe !important;
        color: #0c4a6e !important;
    }
    
    [aria-selected="true"] {
        background: #dbeafe !important;
        color: #0c4a6e !important;
        font-weight: 700 !important;
    }
    
    /* Input Fields - White with Black Text */
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
        font-size: 1.05rem !important;
    }
    
    /* Metrics - Light Background */
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
        backdrop-filter: blur(10px);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px !important;
        padding: 14px 28px !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        color: #e0f2fe !important;
        border: 2px solid rgba(14, 165, 233, 0.3) !important;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(14, 165, 233, 0.2) !important;
        color: #ffffff !important;
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
        backdrop-filter: blur(10px);
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(14, 165, 233, 0.3) !important;
        color: #ffffff !important;
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
        transition: transform 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    .match-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(14, 165, 233, 0.4);
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
        box-shadow: 0 0 10px rgba(14, 165, 233, 0.5);
    }
    
    /* Caption */
    .stCaption {
        color: #94a3b8 !important;
    }
</style>
""", unsafe_allow_html=True)

# ==================== DATABASE & API SETUP ====================
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

# ==================== API HELPER ====================
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

# ==================== SQL HELPER ====================
def run_sql_query(sql: str) -> pd.DataFrame:
    if not engine:
        return pd.DataFrame()
    try:
        with engine.connect() as conn:
            return pd.read_sql_query(text(sql), conn)
    except Exception as e:
        st.error(f"❌ SQL Error: {e}")
        return pd.DataFrame()

# ==================== SCORECARD DISPLAY ====================
def display_scorecard(match_id):
    """Display scorecard with dark theme styling"""
    sc = fetch_cricbuzz(f"mcenter/v1/{match_id}/scard")
    
    if not sc or 'scoreCard' not in sc or not sc['scoreCard']:
        st.warning("⚠️ Scorecard not available yet")
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
        <div style='background: linear-gradient(135deg, #0ea5e9 0%, #2563eb 100%); 
             color: white; padding: 25px; border-radius: 15px; text-align: center; 
             margin: 20px 0; box-shadow: 0 4px 15px rgba(14, 165, 233, 0.5);'>
            <h3 style='color: white !important; margin: 0;'>Innings {inning_idx + 1}: {team}</h3>
            <h2 style='color: white !important; font-size: 3rem; margin: 15px 0;'>{runs}/{wickets}</h2>
            <p style='color: white !important; font-size: 1.3rem; margin: 0;'>Overs: {overs}</p>
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
                        'SR': f"{bat.get('strikeRate', 0):.1f}",
                        'Status': bat.get('outDesc', 'Not Out')
                    })
            if batting_data:
                st.dataframe(pd.DataFrame(batting_data), use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        st.markdown("#### ⚾ Bowling")
        bowlers = innings.get('bowlTeamDetails', {}).get('bowlersData', {})
        if bowlers:
            bowling_data = []
            for bowl in bowlers.values():
                if isinstance(bowl, dict) and 'bowlName' in bowl:
                    bowling_data.append({
                        'Bowler': bowl.get('bowlName', ''),
                        'Overs': bowl.get('overs', 0),
                        'Runs': bowl.get('runs', 0),
                        'Wickets': bowl.get('wickets', 0),
                        'Econ': f"{bowl.get('economy', 0):.2f}"
                    })
            if bowling_data:
                st.dataframe(pd.DataFrame(bowling_data), use_container_width=True, hide_index=True)
        
        st.markdown("---")

# ==================== HEADER ====================
st.title("🏏 Cricbuzz LiveStats")
st.subheader("Real-Time Cricket Insights & SQL-Based Analytics")
st.caption("📊 Live Match Data • 25+ Database Tables • Advanced SQL Queries • Full CRUD Operations")
st.markdown("---")

# ==================== SIDEBAR ====================
st.sidebar.title("🏏 Navigation")
st.sidebar.caption("Select a page to explore")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Pages",
    ["🏠 Home", "🏏 Live Matches", "📊 Top Stats", "🔍 SQL Analytics", "👤 Player CRUD"],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📡 System Status")
st.sidebar.success("✅ API Connected" if RAPIDAPI_KEY else "❌ API Disabled")
st.sidebar.success("✅ DB Online" if engine else "❌ DB Offline")

# ==================== HOME ====================
if page == "🏠 Home":
    st.header("Welcome to Cricbuzz LiveStats! 🏏")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("🏏 API", "Active" if RAPIDAPI_KEY else "Disabled")
    col2.metric("🗄️ Database", "Online" if engine else "Offline")
    col3.metric("📊 Tables", "25+")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success("""
        ### ✨ Live Cricket
        - Real-time match updates
        - Detailed scorecards
        - Player statistics
        """)
    
    with col2:
        st.info("""
        ### 📊 Analytics
        - 25+ database tables
        - SQL query engine
        - Full CRUD operations
        """)

# ==================== LIVE MATCHES ====================
elif page == "🏏 Live Matches":
    st.header("🏏 Live & Recent Matches")
    st.markdown("---")
    
    if not RAPIDAPI_KEY:
        st.error("❌ Add RAPIDAPI_KEY in Secrets")
    else:
        data = fetch_cricbuzz("matches/v1/live") or fetch_cricbuzz("matches/v1/recent")
        
        if data and 'typeMatches' in data:
            has_live = False
            
            for category in data['typeMatches']:
                cat_name = category.get('matchType', 'Unknown').title()
                
                with st.expander(f"**{cat_name}**", expanded=True):
                    for series in category.get('seriesMatches', []):
                        for match in series.get('seriesAdWrapper', {}).get('matches', []):
                            info = match.get('matchInfo', {})
                            
                            t1 = info.get('team1', {}).get('teamName', 'Team 1')
                            t2 = info.get('team2', {}).get('teamName', 'Team 2')
                            status = info.get('status', 'Upcoming')
                            match_id = info.get('matchId')
                            venue = info.get('venueInfo', {}).get('ground', 'Venue')
                            
                            has_live = True
                            
                            st.markdown(f"""
                            <div class='match-card'>
                                <h3>{t1} vs {t2}</h3>
                                <p style='font-weight:700; font-size:1.2rem;'>{status}</p>
                                <p>📍 {venue}</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            if st.button(f"📊 View Scorecard", key=f"sc_{match_id}"):
                                st.markdown("---")
                                display_scorecard(match_id)
            
            if not has_live:
                st.info("ℹ️ No Live Matches")
                
                if engine:
                    df = run_sql_query("SELECT match_desc, team1_name, team2_name, winner_sname FROM recent_matches LIMIT 15")
                    if not df.empty:
                        st.dataframe(df, use_container_width=True)

# ==================== TOP STATS ====================
elif page == "📊 Top Stats":
    st.header("📊 Top Player Statistics")
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
        "Clutch Batting Stats": "clutch_batting_stats",
        "Player Roles": "player_roles",
        "Recent Matches": "recent_matches",
        "Cricket Matches": "cricket_matches",
        "Team Home/Away Wins": "team_home_away_wins",
        "Toss Advantage Stats": "toss_advantage_stats",
        "Bowler Venue Stats": "bowler_venue_stats"
    }
    
    col1, col2 = st.columns(2)
    
    with col1:
        selected_table = st.selectbox("📊 Select Statistics Table", list(table_map.keys()))
    
    with col2:
        limit = st.selectbox("📈 Number of Records", [10, 20, 50, 100])
    
    if engine and st.button("🔍 Load Statistics", type="primary"):
        table_name = table_map[selected_table]
        df = run_sql_query(f"SELECT * FROM {table_name} LIMIT {limit}")
        
        if not df.empty:
            st.success(f"✅ Loaded {len(df)} records")
            st.dataframe(df, use_container_width=True, height=600)
            
            csv = df.to_csv(index=False).encode()
            st.download_button("📥 Download CSV", csv, f"{table_name}.csv")
    else:
        st.info("👆 Select table and click Load")

# ==================== SQL ANALYTICS ====================
elif page == "🔍 SQL Analytics":
    st.header("🔍 SQL Analytics")
    st.markdown("---")
    
    queries = {
        "Top 20 Run Scorers (ODI)": "SELECT player_name, runs, batting_avg FROM odi_batting_stats ORDER BY runs DESC LIMIT 20;",
        "All Indian Players": "SELECT name, playing_role FROM indian_players LIMIT 50;",
        "Best All-Rounders": "SELECT player_name, total_runs, total_wickets FROM all_rounders LIMIT 20;",
        "Recent Matches": "SELECT match_desc, team1_name, team2_name FROM recent_matches LIMIT 30;",
        "Top Partnerships": "SELECT player_names, combined_partnership_runs FROM partnerships ORDER BY combined_partnership_runs DESC LIMIT 20;",
        "Bowler Stats": "SELECT bowler, venue, total_wickets FROM bowler_venue_stats LIMIT 30;",
        "Player Careers": "SELECT player, total_matches FROM player_career_summary LIMIT 30;",
        "Toss Impact": "SELECT format, win_percent_choose_bat_first FROM toss_advantage_stats;",
        "Team Performance": "SELECT team, home_wins, away_wins FROM team_home_away_wins LIMIT 20;",
        "Recent Form": "SELECT player, avg_runs_last5 FROM recent_form LIMIT 20;"
    }
    
    query_name = st.selectbox("🔎 Select Pre-Built Query", list(queries.keys()))
    sql = queries[query_name]
    
    with st.expander("📝 View SQL"):
        st.code(sql, language="sql")
    
    if st.button("▶️ Execute Query", type="primary"):
        df = run_sql_query(sql)
        
        if not df.empty:
            st.success(f"✅ {len(df)} rows")
            st.dataframe(df, use_container_width=True)

# ==================== PLAYER CRUD ====================
elif page == "👤 Player CRUD":
    st.header("👤 Player Management")
    st.markdown("---")
    
    tabs = st.tabs(["➕ CREATE", "📖 READ", "✏️ UPDATE", "🗑️ DELETE"])
    
    with tabs[0]:
        st.subheader("➕ Add Player")
        with st.form("create"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Name *")
                role = st.text_input("Role *")
            with col2:
                country = st.text_input("Country *")
            
            if st.form_submit_button("➕ Add", type="primary"):
                if engine and all([name, role, country]):
                    try:
                        with engine.connect() as conn:
                            conn.execute(text("INSERT INTO players (full_name, playing_role, country) VALUES (:n, :r, :c)"), 
                                       {"n": name, "r": role, "c": country})
                            conn.commit()
                        st.success(f"✅ Added {name}!")
                        st.balloons()
                    except Exception as e:
                        st.error(f"❌ {e}")
    
    with tabs[1]:
        st.subheader("📖 View Players")
        if engine and st.button("🔍 Load"):
            df = run_sql_query("SELECT * FROM players LIMIT 100")
            if not df.empty:
                st.dataframe(df, use_container_width=True)
    
    with tabs[2]:
        st.subheader("✏️ Update Player")
        st.info("Enter Player ID and load data to update")
    
    with tabs[3]:
        st.subheader("🗑️ Delete Player")
        st.warning("⚠️ This action cannot be undone")

st.markdown("---")
st.markdown("""
<div style='text-align:center; padding:30px; background:linear-gradient(135deg, #0ea5e9, #2563eb); 
     color:white; border-radius:15px;'>
    <h2 style='color:white !important;'>🏏 Cricbuzz LiveStats</h2>
    <p style='color:white !important;'>Powered by Cricbuzz API & Neon PostgreSQL</p>
</div>
""", unsafe_allow_html=True)
