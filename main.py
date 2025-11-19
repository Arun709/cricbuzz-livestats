import streamlit as st
import requests
import pandas as pd
from sqlalchemy import create_engine, text
from typing import Optional, Dict, Any
import os

# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="Cricbuzz LiveStats - Real-Time Cricket Analytics",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== ULTRA READABLE CSS ====================
st.markdown("""
<style>
    /* Clean White Background */
    .stApp {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
    }
    
    .main .block-container {
        padding: 2rem 3rem;
        background: #ffffff;
        border-radius: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
    
    /* Headers - High Contrast */
    h1 {
        color: #0c4a6e !important;
        font-weight: 900 !important;
        font-size: 3.5rem !important;
        border-bottom: 5px solid #0ea5e9;
        padding-bottom: 1rem;
        margin-bottom: 2rem;
    }
    
    h2 {
        color: #0c4a6e !important;
        font-weight: 800 !important;
        font-size: 2.2rem !important;
        margin-top: 2rem;
        padding: 15px 0;
        border-left: 6px solid #0ea5e9;
        padding-left: 20px;
    }
    
    h3 {
        color: #075985 !important;
        font-weight: 700 !important;
        font-size: 1.8rem !important;
    }
    
    h4 {
        color: #0c4a6e !important;
        font-weight: 700 !important;
        font-size: 1.4rem !important;
    }
    
    /* All Text - Dark and Readable */
    p, li, span, div, label, td, th {
        color: #1e293b !important;
        font-size: 1.1rem !important;
        line-height: 1.8 !important;
    }
    
    strong, b {
        color: #0c4a6e !important;
        font-weight: 800 !important;
    }
    
    /* Buttons - Large and Visible */
    .stButton > button {
        background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 16px 32px !important;
        font-weight: 800 !important;
        font-size: 1.15rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(14, 165, 233, 0.4) !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(14, 165, 233, 0.6) !important;
    }
    
    /* Sidebar - Light Theme */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f0f9ff 0%, #e0f2fe 100%) !important;
        padding: 1.5rem !important;
    }
    
    section[data-testid="stSidebar"] * {
        color: #0c4a6e !important;
        font-weight: 600 !important;
    }
    
    /* Metrics - Light Blue Cards */
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%) !important;
        padding: 25px !important;
        border-radius: 15px !important;
        border-left: 6px solid #0ea5e9 !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
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
    
    /* Alert Boxes - Light Backgrounds */
    .stInfo {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%) !important;
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
    
    /* Match Card - Clean White Card */
    .match-card {
        padding: 25px;
        border-radius: 15px;
        margin: 15px 0;
        background: #ffffff;
        border: 3px solid #0ea5e9;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    
    .match-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
    }
    
    /* Scorecard Table */
    .scorecard-table {
        width: 100%;
        border-collapse: collapse;
        margin: 20px 0;
        background: white;
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .scorecard-table th {
        background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%);
        color: white !important;
        padding: 15px;
        text-align: left;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
    }
    
    .scorecard-table td {
        padding: 12px 15px;
        border-bottom: 1px solid #e2e8f0;
        color: #1e293b !important;
        font-size: 1.05rem !important;
    }
    
    .scorecard-table tr:hover {
        background: #f0f9ff;
    }
    
    /* Score Header */
    .score-header {
        background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%);
        color: white !important;
        padding: 25px;
        border-radius: 15px;
        margin: 20px 0;
        text-align: center;
        box-shadow: 0 4px 15px rgba(14, 165, 233, 0.3);
    }
    
    .score-header h3, .score-header p {
        color: white !important;
        margin: 5px 0;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: #f0f9ff;
        padding: 15px;
        border-radius: 15px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: white !important;
        border-radius: 10px !important;
        padding: 14px 28px !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        color: #0c4a6e !important;
        border: 2px solid transparent !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        border-color: #0ea5e9 !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%) !important;
        color: white !important;
    }
    
    /* Dataframe */
    .stDataFrame {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background: #f0f9ff !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        color: #0c4a6e !important;
        padding: 15px !important;
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
        DATABASE_URL = secrets.get("DATABASE_URL") or DATABASE_URL
    RAPIDAPI_KEY = secrets.get("RAPIDAPI_KEY") or secrets.get("rapidapi_key") or RAPIDAPI_KEY

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
        st.error(f"❌ DB Error: {e}")
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
        with st.spinner(f"🔄 Fetching {endpoint}..."):
            r = requests.get(url, headers=headers, params=params, timeout=15)
        if r.status_code == 200:
            return r.json()
        st.error(f"❌ API Error {r.status_code}")
    except Exception as e:
        st.error(f"⚠️ Error: {e}")
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

# ==================== BEAUTIFUL SCORECARD DISPLAY ====================
def display_scorecard(scorecard_data):
    """Display a beautiful, readable scorecard"""
    
    if not scorecard_data:
        st.warning("⚠️ No scorecard data available")
        return
    
    # Extract match info
    scorecard = scorecard_data.get('scoreCard', [])
    if not scorecard:
        st.info("ℹ️ Scorecard not yet available")
        return
    
    for inning_idx, innings in enumerate(scorecard):
        innings_info = innings.get('inningsScoreList', [])
        batsman_data = innings.get('batTeamDetails', {}).get('batsmenData', {})
        bowler_data = innings.get('bowlTeamDetails', {}).get('bowlersData', {})
        
        if not innings_info:
            continue
        
        # Display innings header
        inning_score = innings_info[0] if innings_info else {}
        team_name = inning_score.get('batTeamName', 'Team')
        runs = inning_score.get('runs', 0)
        wickets = inning_score.get('wickets', 0)
        overs = inning_score.get('overs', 0)
        
        st.markdown(f"""
        <div class='score-header'>
            <h3>Innings {inning_idx + 1}: {team_name}</h3>
            <h2 style='color:white !important; font-size:2.5rem; margin:10px 0;'>{runs}/{wickets}</h2>
            <p style='font-size:1.2rem;'>Overs: {overs}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Batting Table
        st.markdown("#### 🏏 Batting Performance")
        
        if batsman_data:
            batting_rows = []
            for bat_id, bat_info in batsman_data.items():
                if isinstance(bat_info, dict) and 'runs' in bat_info:
                    batting_rows.append({
                        'Batsman': bat_info.get('batName', 'Unknown'),
                        'Runs': bat_info.get('runs', 0),
                        'Balls': bat_info.get('balls', 0),
                        '4s': bat_info.get('fours', 0),
                        '6s': bat_info.get('sixes', 0),
                        'SR': f"{bat_info.get('strikeRate', 0):.2f}" if bat_info.get('strikeRate') else '0.00',
                        'Dismissal': bat_info.get('outDesc', 'Not Out')
                    })
            
            if batting_rows:
                df_batting = pd.DataFrame(batting_rows)
                st.dataframe(df_batting, use_container_width=True, hide_index=True)
            else:
                st.info("ℹ️ No batting data available yet")
        
        st.markdown("---")
        
        # Bowling Table
        st.markdown("#### ⚾ Bowling Performance")
        
        if bowler_data:
            bowling_rows = []
            for bowl_id, bowl_info in bowler_data.items():
                if isinstance(bowl_info, dict) and 'overs' in bowl_info:
                    bowling_rows.append({
                        'Bowler': bowl_info.get('bowlName', 'Unknown'),
                        'Overs': bowl_info.get('overs', 0),
                        'Maidens': bowl_info.get('maidens', 0),
                        'Runs': bowl_info.get('runs', 0),
                        'Wickets': bowl_info.get('wickets', 0),
                        'Economy': f"{bowl_info.get('economy', 0):.2f}" if bowl_info.get('economy') else '0.00',
                        'Dots': bowl_info.get('dots', 0)
                    })
            
            if bowling_rows:
                df_bowling = pd.DataFrame(bowling_rows)
                st.dataframe(df_bowling, use_container_width=True, hide_index=True)
            else:
                st.info("ℹ️ No bowling data available yet")
        
        st.markdown("---")

# ==================== QUERIES ====================
queries = {
    "Beginner": {
        "Q1 - Indian Players": ("Find all Indian players", "SELECT name, playing_role FROM indian_players LIMIT 50;"),
        "Q2 - Recent Matches": ("Recent 30 days matches", "SELECT match_desc, team1_name, team2_name FROM recent_matches LIMIT 50;"),
    },
    "Intermediate": {
        "Q9 - All-Rounders": ("All-rounders >1000 runs", "SELECT player_name, total_runs, total_wickets FROM all_rounders WHERE total_runs > 1000 LIMIT 50;"),
    },
    "Advanced": {
        "Q17 - Toss Stats": ("Toss advantage analysis", "SELECT format, win_percent_choose_bat_first FROM toss_advantage_stats LIMIT 10;"),
    }
}

# ==================== HEADER ====================
st.title("🏏 Cricbuzz LiveStats")
st.subheader("Real-Time Cricket Insights & SQL-Based Analytics")
st.markdown("---")

# ==================== SIDEBAR ====================
st.sidebar.image("https://upload.wikimedia.org/wikipedia/en/8/89/Cricbuzz_logo.png", width=150)
page = st.sidebar.selectbox("📍 Navigate", ["🏠 Home", "🏏 Live Matches", "📊 Top Stats", "🔍 SQL Analytics", "👤 Player CRUD"])

# ==================== HOME ====================
if page == "🏠 Home":
    st.header("Welcome to Cricbuzz LiveStats! 🏏")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("🏏 Live API", "Active" if RAPIDAPI_KEY else "Disabled")
    with col2:
        st.metric("🗄️ Database", "Connected" if engine else "Disconnected")
    with col3:
        st.metric("📊 SQL Queries", "25")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success("""
        **✨ Live Cricket Data**
        - Real-time match updates
        - Beautiful scorecards
        - Player statistics
        """)
        
        st.info("""
        **📊 SQL Analytics**
        - 25 pre-built queries
        - Custom exploration
        - CSV export
        """)
    
    with col2:
        st.success("""
        **🗄️ Database**
        - 400K+ records
        - Fast Neon PostgreSQL
        - Cloud-powered
        """)
        
        st.info("""
        **👤 Player CRUD**
        - Add players
        - Update records
        - Delete entries
        """)

# ==================== LIVE MATCHES ====================
elif page == "🏏 Live Matches":
    st.header("🏏 Live & Recent Matches")
    st.markdown("---")
    
    if not RAPIDAPI_KEY:
        st.warning("⚠️ **API Key Missing:** Add RAPIDAPI_KEY in Streamlit Secrets")
    else:
        data = fetch_cricbuzz("matches/v1/recent")
        
        if not data or 'typeMatches' not in data:
            data = fetch_cricbuzz("matches/v1/current")
        
        if data and 'typeMatches' in data:
            for category in data['typeMatches']:
                cat_name = category.get('matchType', 'Unknown').title()
                
                with st.expander(f"**{cat_name}**", expanded=True):
                    series_matches = category.get('seriesMatches', [])
                    
                    for series in series_matches:
                        for match in series.get('seriesAdWrapper', {}).get('matches', []):
                            info = match.get('matchInfo', {})
                            
                            t1 = info.get('team1', {}).get('teamName', 'Team 1')
                            t2 = info.get('team2', {}).get('teamName', 'Team 2')
                            status = info.get('status', 'Upcoming')
                            match_id = info.get('matchId')
                            venue = info.get('venueInfo', {}).get('ground', 'Unknown')
                            city = info.get('venueInfo', {}).get('city', '')
                            
                            # Beautiful Match Card
                            st.markdown(f"""
                            <div class='match-card'>
                                <h3 style='color:#0c4a6e; margin:0 0 10px 0;'>🏏 {t1} vs {t2}</h3>
                                <p style='color:#0284c7; font-weight:700; font-size:1.15rem; margin:5px 0;'>{status}</p>
                                <p style='color:#64748b; margin:0;'>📍 {venue}, {city}</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Scorecard Button
                            if st.button(f"📊 View Detailed Scorecard", key=f"sc_{match_id}", type="primary"):
                                with st.spinner("🔄 Loading scorecard..."):
                                    sc = fetch_cricbuzz(f"mcenter/v1/{match_id}/scard")
                                    if sc:
                                        st.markdown("---")
                                        display_scorecard(sc)
                                    else:
                                        st.error("❌ Unable to load scorecard")
        else:
            st.warning("⚠️ No matches available right now")

# ==================== TOP STATS ====================
elif page == "📊 Top Stats":
    st.header("📊 Top Player Statistics")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        stat = st.selectbox("📈 Select Stat", ["Most Runs", "Most Wickets", "Highest Score"])
    with col2:
        fmt = st.selectbox("🏏 Format", ["test", "odi", "t20"])
    
    sql = "SELECT player_name AS Player, runs AS Value, batting_avg AS Average FROM odi_batting_stats ORDER BY runs DESC LIMIT 20;"
    
    if engine:
        df = run_sql_query(sql)
        if not df.empty:
            st.success(f"✅ Top 20 {stat} in {fmt.upper()}")
            st.dataframe(df, use_container_width=True, height=600)
            csv = df.to_csv(index=False).encode()
            st.download_button("📥 Download CSV", csv, f"top_stats_{stat}.csv")
        else:
            st.info("ℹ️ No data available")
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
    with st.expander("📝 View SQL"):
        st.code(sql, language="sql")
    
    if st.button("▶️ Run Query", type="primary"):
        df = run_sql_query(sql)
        if not df.empty:
            st.success(f"✅ {len(df):,} rows")
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("⚠️ No results")

# ==================== PLAYER CRUD ====================
elif page == "👤 Player CRUD":
    st.header("👤 Player Management")
    st.markdown("---")
    
    tabs = st.tabs(["➕ Create", "📖 Read", "✏️ Update", "🗑️ Delete"])
    
    with tabs[0]:
        with st.form("create"):
            st.subheader("➕ Add Player")
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Name *")
                role = st.text_input("Role *")
            with col2:
                bat = st.selectbox("Batting", ["Right-hand", "Left-hand", "N/A"])
                bowl = st.selectbox("Bowling", ["Right-arm fast", "Left-arm spin", "N/A"])
            country = st.text_input("Country *")
            
            if st.form_submit_button("➕ Add", type="primary"):
                if engine and all([name, role, country]):
                    try:
                        with engine.connect() as conn:
                            conn.execute(text("INSERT INTO players (full_name, playing_role, batting_style, bowling_style, country) VALUES (:n, :r, :bat, :bowl, :c)"), 
                                       {"n": name, "r": role, "bat": bat if bat != "N/A" else None, "bowl": bowl if bowl != "N/A" else None, "c": country})
                            conn.commit()
                        st.success(f"✅ Added {name}!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
                else:
                    st.error("❌ Fill all fields")
    
    with tabs[1]:
        st.subheader("📖 All Players")
        if engine:
            df = run_sql_query("SELECT id, full_name, playing_role, country FROM players LIMIT 200")
            if not df.empty:
                st.dataframe(df, use_container_width=True, height=600)
            else:
                st.info("ℹ️ No players found")

st.markdown("---")
st.caption("🏏 Cricbuzz LiveStats | Powered by Cricbuzz API & Neon PostgreSQL")
