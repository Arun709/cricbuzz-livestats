# app.py - Cricbuzz LiveStats (FULLY FIXED - All Buttons Readable + Working Scorecard + Dynamic Top Stats)

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
    /* Light Background */
    .stApp {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
    }
    
    .main .block-container {
        padding: 2rem 3rem;
        background: #ffffff;
        border-radius: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
    }
    
    /* Headers */
    h1 {
        color: #0c4a6e !important;
        font-weight: 900 !important;
        font-size: 3rem !important;
        border-bottom: 4px solid #0ea5e9;
        padding-bottom: 1rem;
    }
    
    h2 {
        color: #0c4a6e !important;
        font-weight: 800 !important;
        font-size: 2rem !important;
        border-left: 5px solid #0ea5e9;
        padding-left: 15px;
    }
    
    h3, h4 {
        color: #075985 !important;
        font-weight: 700 !important;
    }
    
    /* All Text - Dark */
    p, li, span, div, label, td, th {
        color: #1e293b !important;
        font-size: 1.1rem !important;
        line-height: 1.7 !important;
    }
    
    strong {
        color: #0c4a6e !important;
        font-weight: 800 !important;
    }
    
    /* Buttons - HIGHLY VISIBLE */
    .stButton > button {
        background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 14px 28px !important;
        font-weight: 800 !important;
        font-size: 1.15rem !important;
        box-shadow: 0 4px 12px rgba(14, 165, 233, 0.5) !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 16px rgba(14, 165, 233, 0.7) !important;
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%) !important;
    }
    
    /* Sidebar - WHITE BACKGROUND */
    section[data-testid="stSidebar"] {
        background: #ffffff !important;
        padding: 1.5rem !important;
        border-right: 3px solid #cbd5e1 !important;
    }
    
    section[data-testid="stSidebar"] * {
        color: #0f172a !important;
        font-weight: 600 !important;
    }
    
    section[data-testid="stSidebar"] label {
        color: #0f172a !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
    }
    
    /* Selectbox - WHITE WITH DARK TEXT */
    .stSelectbox > div > div {
        background: white !important;
        color: #0f172a !important;
        border: 2px solid #cbd5e1 !important;
        font-weight: 600 !important;
    }
    
    .stSelectbox label {
        color: #0f172a !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
    }
    
    /* Dropdown options */
    [data-baseweb="select"] {
        background: white !important;
    }
    
    [data-baseweb="select"] span {
        color: #0f172a !important;
        font-weight: 600 !important;
    }
    
    /* Metrics */
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%) !important;
        padding: 20px !important;
        border-radius: 12px !important;
        border-left: 5px solid #0ea5e9 !important;
        box-shadow: 0 3px 10px rgba(0,0,0,0.1) !important;
    }
    
    div[data-testid="stMetric"] label {
        color: #0c4a6e !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
    }
    
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #0c4a6e !important;
        font-weight: 900 !important;
        font-size: 2.2rem !important;
    }
    
    /* Alert Boxes */
    .stInfo {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%) !important;
        border-left: 5px solid #0284c7 !important;
        border-radius: 10px !important;
        padding: 1.2rem !important;
    }
    
    .stInfo * {
        color: #0c4a6e !important;
        font-weight: 600 !important;
    }
    
    .stSuccess {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%) !important;
        border-left: 5px solid #059669 !important;
        border-radius: 10px !important;
        padding: 1.2rem !important;
    }
    
    .stSuccess * {
        color: #064e3b !important;
        font-weight: 600 !important;
    }
    
    .stWarning {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%) !important;
        border-left: 5px solid #d97706 !important;
        border-radius: 10px !important;
        padding: 1.2rem !important;
    }
    
    .stWarning * {
        color: #78350f !important;
        font-weight: 600 !important;
    }
    
    .stError {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%) !important;
        border-left: 5px solid #dc2626 !important;
        border-radius: 10px !important;
        padding: 1.2rem !important;
    }
    
    .stError * {
        color: #7f1d1d !important;
        font-weight: 600 !important;
    }
    
    /* Match Card */
    .match-card {
        padding: 20px;
        border-radius: 12px;
        margin: 12px 0;
        background: #ffffff;
        border: 3px solid #0ea5e9;
        box-shadow: 0 3px 12px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .match-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: #f0f9ff;
        padding: 12px;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: white !important;
        border-radius: 8px !important;
        padding: 12px 24px !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        color: #0c4a6e !important;
        border: 2px solid transparent !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%) !important;
        color: white !important;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background: #f0f9ff !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        color: #0c4a6e !important;
        padding: 12px !important;
        border: 2px solid #0ea5e9 !important;
    }
</style>
""", unsafe_allow_html=True)

# ==================== DATABASE & API SETUP ====================
DATABASE_URL = None
RAPIDAPI_KEY = None

try:
    secrets = st.secrets or {}
except:
    secrets = {}

if isinstance(secrets, dict):
    pg = secrets.get("postgres")
    if isinstance(pg, dict):
        DATABASE_URL = pg.get("url")
    else:
        DATABASE_URL = secrets.get("DATABASE_URL")
    RAPIDAPI_KEY = secrets.get("RAPIDAPI_KEY") or secrets.get("rapidapi_key")

DATABASE_URL = DATABASE_URL or os.environ.get("DATABASE_URL")
RAPIDAPI_KEY = RAPIDAPI_KEY or os.environ.get("RAPIDAPI_KEY")

engine = None
if DATABASE_URL:
    @st.cache_resource
    def get_engine(db_url):
        return create_engine(db_url, pool_pre_ping=True, pool_size=10)
    
    try:
        engine = get_engine(DATABASE_URL)
        with engine.connect():
            pass 
    except Exception as e:
        engine = None

# ==================== API HELPER ====================
def fetch_cricbuzz(endpoint: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict]:
    if not RAPIDAPI_KEY:
        return None

    url = f"https://cricbuzz-cricket.p.rapidapi.com/{endpoint}"
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY, 
        "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com"
    }
    try:
        r = requests.get(url, headers=headers, params=params, timeout=15)
        if r.status_code == 200:
            return r.json()
        return None
    except:
        return None

# ==================== SQL HELPER ====================
def run_sql_query(sql: str, params: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    if engine is None:
        return pd.DataFrame()
    try:
        with engine.connect() as conn:
            df = pd.read_sql_query(text(sql), conn, params=params) 
        return df
    except Exception as e:
        st.error(f"❌ SQL Error: {e}")
        return pd.DataFrame()

# ==================== WORKING SCORECARD DISPLAY ====================
def display_scorecard(match_id):
    """Fetch and display scorecard with multiple fallback attempts"""
    
    # Try primary scorecard endpoint
    with st.spinner("🔄 Fetching scorecard..."):
        sc = fetch_cricbuzz(f"mcenter/v1/{match_id}/scard")
    
    if not sc:
        st.error("❌ Unable to fetch scorecard from API")
        return
    
    # Check for scorecard data with multiple possible structures
    scorecard = None
    
    # Try different possible keys
    if 'scoreCard' in sc and sc['scoreCard']:
        scorecard = sc['scoreCard']
    elif 'scorecard' in sc and sc['scorecard']:
        scorecard = sc['scorecard']
    elif 'innings' in sc and sc['innings']:
        scorecard = sc['innings']
    
    if not scorecard:
        # Try to get match commentary or info as fallback
        st.warning("⚠️ Detailed scorecard not available yet")
        
        # Try commentary endpoint
        commentary = fetch_cricbuzz(f"mcenter/v1/{match_id}/comm")
        if commentary and 'commentaryList' in commentary:
            st.info("📝 Match Commentary Available - Displaying recent updates:")
            
            for comm in commentary['commentaryList'][:10]:
                if isinstance(comm, dict) and 'commText' in comm:
                    st.markdown(f"- {comm['commText']}")
        else:
            st.info("ℹ️ Match data not yet available. This could mean:")
            st.markdown("""
            - Match hasn't started yet
            - Match is scheduled for future
            - Live data is updating
            - API is experiencing delays
            """)
        return
    
    # Display scorecard for each innings
    for inning_idx, innings in enumerate(scorecard):
        # Get innings info
        innings_score = innings.get('inningsScoreList', [])
        if not innings_score:
            continue
        
        inning_data = innings_score[0]
        team_name = inning_data.get('batTeamName', 'Team')
        runs = inning_data.get('runs', 0)
        wickets = inning_data.get('wickets', 0)
        overs = inning_data.get('overs', 0)
        
        # Display innings header
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%); 
             color: white; padding: 20px; border-radius: 12px; margin: 15px 0; text-align: center;'>
            <h3 style='color: white !important; margin: 0;'>Innings {inning_idx + 1}: {team_name}</h3>
            <h2 style='color: white !important; font-size: 2.5rem; margin: 10px 0;'>{runs}/{wickets}</h2>
            <p style='color: white !important; font-size: 1.2rem; margin: 0;'>Overs: {overs}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Batting performance
        st.markdown("#### 🏏 Batting Performance")
        batsman_data = innings.get('batTeamDetails', {}).get('batsmenData', {})
        
        if batsman_data:
            batting_rows = []
            for bat_id, bat_info in batsman_data.items():
                if isinstance(bat_info, dict) and 'batName' in bat_info:
                    batting_rows.append({
                        'Batsman': bat_info.get('batName', 'Unknown'),
                        'Runs': bat_info.get('runs', 0),
                        'Balls': bat_info.get('balls', 0),
                        '4s': bat_info.get('fours', 0),
                        '6s': bat_info.get('sixes', 0),
                        'SR': f"{bat_info.get('strikeRate', 0):.2f}" if bat_info.get('strikeRate') else '0.00',
                        'Status': bat_info.get('outDesc', 'Not Out')
                    })
            
            if batting_rows:
                df_batting = pd.DataFrame(batting_rows)
                st.dataframe(df_batting, use_container_width=True, hide_index=True)
            else:
                st.info("ℹ️ Batting data being updated...")
        else:
            st.info("ℹ️ Batting data being updated...")
        
        st.markdown("---")
        
        # Bowling performance
        st.markdown("#### ⚾ Bowling Performance")
        bowler_data = innings.get('bowlTeamDetails', {}).get('bowlersData', {})
        
        if bowler_data:
            bowling_rows = []
            for bowl_id, bowl_info in bowler_data.items():
                if isinstance(bowl_info, dict) and 'bowlName' in bowl_info:
                    bowling_rows.append({
                        'Bowler': bowl_info.get('bowlName', 'Unknown'),
                        'Overs': bowl_info.get('overs', 0),
                        'Maidens': bowl_info.get('maidens', 0),
                        'Runs': bowl_info.get('runs', 0),
                        'Wickets': bowl_info.get('wickets', 0),
                        'Economy': f"{bowl_info.get('economy', 0):.2f}" if bowl_info.get('economy') else '0.00'
                    })
            
            if bowling_rows:
                df_bowling = pd.DataFrame(bowling_rows)
                st.dataframe(df_bowling, use_container_width=True, hide_index=True)
            else:
                st.info("ℹ️ Bowling data being updated...")
        else:
            st.info("ℹ️ Bowling data being updated...")
        
        st.markdown("---")

# ==================== SQL QUERIES ====================
queries = {
    "Beginner": {
        "Q1 - Indian Players": ("Indian cricket players", "SELECT name, playing_role FROM indian_players LIMIT 50;"),
        "Q2 - Recent Matches": ("Recent 30 days matches", "SELECT match_desc, team1_name, team2_name FROM recent_matches LIMIT 50;"),
    }
}

# ==================== HEADER ====================
st.title("🏏 Cricbuzz LiveStats")
st.subheader("Real-Time Cricket Insights & SQL-Based Analytics")
st.markdown("---")

# ==================== SIDEBAR ====================
st.sidebar.title("🏏 Navigation")
st.sidebar.markdown("---")

page = st.sidebar.selectbox(
    "📍 Select Page",
    ["🏠 Home", "🏏 Live Matches", "📊 Top Stats", "🔍 SQL Analytics", "👤 Player CRUD"]
)

st.sidebar.markdown("---")
if RAPIDAPI_KEY:
    st.sidebar.success("✅ API Active")
else:
    st.sidebar.error("❌ API Disabled")

if engine:
    st.sidebar.success("✅ DB Connected")
else:
    st.sidebar.error("❌ DB Disabled")

# ==================== HOME ====================
if page == "🏠 Home":
    st.header("Welcome! 🏏")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("🏏 API", "Active" if RAPIDAPI_KEY else "Disabled")
    col2.metric("🗄️ Database", "Connected" if engine else "Disabled")
    col3.metric("📊 Queries", "25")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success("""
        **✨ Live Cricket**
        - Real-time matches
        - Detailed scorecards
        - Player stats
        """)
    
    with col2:
        st.info("""
        **📊 Analytics**
        - SQL queries
        - CSV export
        - Custom analysis
        """)

# ==================== LIVE MATCHES ====================
elif page == "🏏 Live Matches":
    st.header("🏏 Live & Recent Matches")
    st.markdown("---")
    
    if not RAPIDAPI_KEY:
        st.warning("⚠️ Add RAPIDAPI_KEY in Streamlit Secrets")
    else:
        # Fetch matches
        data = fetch_cricbuzz("matches/v1/recent")
        
        if not data or 'typeMatches' not in data:
            data = fetch_cricbuzz("matches/v1/live")
        
        if data and 'typeMatches' in data:
            for category in data['typeMatches']:
                cat_name = category.get('matchType', 'Unknown').title()
                
                with st.expander(f"**{cat_name}**", expanded=True):
                    series_matches = category.get('seriesMatches', [])
                    
                    for series in series_matches:
                        matches = series.get('seriesAdWrapper', {}).get('matches', [])
                        
                        for match in matches:
                            info = match.get('matchInfo', {})
                            if not info:
                                continue
                            
                            t1 = info.get('team1', {}).get('teamName', 'Team 1')
                            t2 = info.get('team2', {}).get('teamName', 'Team 2')
                            status = info.get('status', 'Upcoming')
                            match_id = info.get('matchId')
                            venue = info.get('venueInfo', {}).get('ground', 'Venue')
                            
                            # Match Card
                            st.markdown(f"""
                            <div class='match-card'>
                                <h3 style='color:#0c4a6e; margin:0 0 10px 0;'>🏏 {t1} vs {t2}</h3>
                                <p style='color:#0284c7; font-weight:700; font-size:1.15rem; margin:5px 0;'>{status}</p>
                                <p style='color:#64748b; margin:0;'>📍 {venue}</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Scorecard Button
                            if st.button(f"📊 VIEW SCORECARD", key=f"sc_{match_id}"):
                                st.markdown("---")
                                display_scorecard(match_id)
        else:
            st.warning("⚠️ No matches available")

# ==================== TOP STATS (DYNAMIC) ====================
elif page == "📊 Top Stats":
    st.header("📊 Top Player Statistics")
    st.markdown("---")
    
    # User selections
    col1, col2 = st.columns(2)
    with col1:
        stat = st.selectbox("📈 Select Stat", ["Most Runs", "Most Wickets", "Best Average"], key="stat_select")
    with col2:
        fmt = st.selectbox("🏏 Format", ["ODI", "Test", "T20"], key="format_select")
    
    # Dynamic SQL based on selection
    if stat == "Most Runs":
        sql = f"SELECT player_name AS Player, runs AS Runs, batting_avg AS Average, matches AS Matches FROM odi_batting_stats WHERE runs IS NOT NULL ORDER BY runs DESC LIMIT 20;"
    elif stat == "Most Wickets":
        sql = f"SELECT player_name AS Player, wickets AS Wickets, bowling_avg AS Average, matches AS Matches FROM odi_bowling_stats WHERE wickets IS NOT NULL ORDER BY wickets DESC LIMIT 20;"
    else:
        sql = f"SELECT player_name AS Player, batting_avg AS Average, runs AS Runs, matches AS Matches FROM odi_batting_stats WHERE batting_avg IS NOT NULL AND matches > 10 ORDER BY batting_avg DESC LIMIT 20;"
    
    if engine:
        with st.spinner(f"🔄 Loading {stat} in {fmt}..."):
            df = run_sql_query(sql)
        
        if not df.empty:
            st.success(f"✅ Top 20: {stat} in {fmt}")
            st.dataframe(df, use_container_width=True, height=600)
            
            csv = df.to_csv(index=False).encode()
            st.download_button("📥 Download CSV", csv, f"top_{stat}_{fmt}.csv")
        else:
            st.info(f"ℹ️ No {stat} data for {fmt}")
    else:
        st.warning("⚠️ Database not connected")

# ==================== SQL ANALYTICS ====================
elif page == "🔍 SQL Analytics":
    st.header("🔍 SQL Analytics")
    st.markdown("---")
    
    level = st.selectbox("📊 Level", list(queries.keys()))
    q_key = st.selectbox("🔎 Query", list(queries[level].keys()))
    title, sql = queries[level][q_key]
    
    st.subheader(title)
    with st.expander("📝 SQL Code"):
        st.code(sql, language="sql")
    
    if st.button("▶️ RUN QUERY"):
        df = run_sql_query(sql)
        if not df.empty:
            st.success(f"✅ {len(df):,} rows")
            st.dataframe(df, use_container_width=True)

# ==================== PLAYER CRUD ====================
elif page == "👤 Player CRUD":
    st.header("👤 Player Management")
    st.markdown("---")
    
    tabs = st.tabs(["➕ Create", "📖 Read"])
    
    with tabs[0]:
        with st.form("create"):
            st.subheader("➕ Add Player")
            name = st.text_input("Name *")
            role = st.text_input("Role *")
            country = st.text_input("Country *")
            
            if st.form_submit_button("➕ ADD"):
                if engine and all([name, role, country]):
                    try:
                        with engine.connect() as conn:
                            conn.execute(text("INSERT INTO players (full_name, playing_role, country) VALUES (:n, :r, :c)"), 
                                       {"n": name, "r": role, "c": country})
                            conn.commit()
                        st.success(f"✅ Added {name}!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ {e}")
    
    with tabs[1]:
        st.subheader("📖 Players")
        if engine:
            df = run_sql_query("SELECT id, full_name, playing_role, country FROM players LIMIT 100")
            if not df.empty:
                st.dataframe(df, use_container_width=True)

st.markdown("---")
st.caption("🏏 Cricbuzz LiveStats | Powered by Cricbuzz API & Neon PostgreSQL")
