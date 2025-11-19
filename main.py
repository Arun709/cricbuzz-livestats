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

# ==================== EMI PROJECT THEME CSS ====================
st.markdown("""
<style>
    /* Main Background - EMI Blue Theme */
    .stApp {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
    }
    
    .main .block-container {
        padding: 2rem 3rem;
        background: #ffffff;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.3);
    }
    
    /* Headers - Bright Blue Gradient */
    h1 {
        color: #ffffff !important;
        font-weight: 900 !important;
        font-size: 3.5rem !important;
        background: linear-gradient(120deg, #0ea5e9, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        border-bottom: 5px solid #0ea5e9;
        padding-bottom: 1rem;
        margin-bottom: 2rem;
        text-shadow: 0 0 20px rgba(14, 165, 233, 0.5);
    }
    
    h2 {
        color: #0c4a6e !important;
        font-weight: 800 !important;
        font-size: 2.2rem !important;
        margin-top: 2rem;
        padding: 15px 0;
        border-left: 6px solid #0ea5e9;
        padding-left: 20px;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
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
    
    /* All Text - Dark on Light */
    p, li, span, div {
        color: #1e293b !important;
        font-size: 1.1rem !important;
        line-height: 1.8 !important;
    }
    
    strong {
        color: #0c4a6e !important;
        font-weight: 800 !important;
    }
    
    /* Buttons - EMI Style */
    .stButton > button {
        background: linear-gradient(135deg, #0ea5e9 0%, #2563eb 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 18px 36px !important;
        font-weight: 800 !important;
        font-size: 1.2rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 6px 20px rgba(14, 165, 233, 0.5) !important;
        text-transform: uppercase !important;
        letter-spacing: 1.5px !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 10px 30px rgba(14, 165, 233, 0.7) !important;
        background: linear-gradient(135deg, #3b82f6 0%, #0ea5e9 100%) !important;
    }
    
    /* Sidebar - Light Blue */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f0f9ff 0%, #e0f2fe 100%) !important;
        padding: 1.5rem !important;
        border-right: 3px solid #0ea5e9 !important;
    }
    
    section[data-testid="stSidebar"] * {
        color: #0c4a6e !important;
        font-weight: 600 !important;
    }
    
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #0c4a6e !important;
        font-weight: 800 !important;
    }
    
    /* Radio Buttons - White with Blue Text */
    section[data-testid="stSidebar"] .stRadio > label {
        color: #0c4a6e !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
    }
    
    section[data-testid="stSidebar"] .stRadio > div {
        background: white !important;
        padding: 10px !important;
        border-radius: 10px !important;
        border: 2px solid #0ea5e9 !important;
    }
    
    section[data-testid="stSidebar"] .stRadio label {
        color: #0c4a6e !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
    }
    
    /* Selectbox - WHITE BACKGROUND WITH DARK TEXT */
    .stSelectbox label {
        color: #0c4a6e !important;
        font-weight: 800 !important;
        font-size: 1.2rem !important;
    }
    
    .stSelectbox > div > div {
        background: white !important;
        color: #0f172a !important;
        border: 2px solid #0ea5e9 !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        border-radius: 8px !important;
    }
    
    /* Selectbox options */
    [data-baseweb="select"] {
        background: white !important;
    }
    
    [data-baseweb="select"] div {
        color: #0f172a !important;
        font-weight: 600 !important;
    }
    
    /* Input Fields - White with Dark Text */
    .stTextInput label,
    .stNumberInput label {
        color: #0c4a6e !important;
        font-weight: 800 !important;
        font-size: 1.1rem !important;
    }
    
    .stTextInput input,
    .stNumberInput input {
        background: white !important;
        color: #0f172a !important;
        border: 2px solid #0ea5e9 !important;
        font-weight: 600 !important;
        font-size: 1.05rem !important;
    }
    
    /* Metrics - Light Blue Cards */
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%) !important;
        padding: 25px !important;
        border-radius: 15px !important;
        border-left: 6px solid #0ea5e9 !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
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
    
    /* Alert Boxes - EMI Style */
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
    
    /* Tabs - EMI Style */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: linear-gradient(135deg, #e5e7eb 0%, #d1d5db 100%);
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
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: #dbeafe !important;
        border-color: #0ea5e9 !important;
        transform: translateY(-2px);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #0ea5e9 0%, #2563eb 100%) !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(14, 165, 233, 0.5);
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%) !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        color: #0c4a6e !important;
        padding: 15px !important;
        border: 2px solid #0ea5e9 !important;
    }
    
    .streamlit-expanderHeader:hover {
        background: linear-gradient(135deg, #bfdbfe 0%, #93c5fd 100%) !important;
    }
    
    /* Dataframe */
    .stDataFrame {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    /* Match Cards */
    .match-card {
        padding: 25px;
        border-radius: 15px;
        margin: 15px 0;
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        border: 3px solid #0ea5e9;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    
    .match-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
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
        color: #64748b !important;
        font-size: 1rem !important;
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
    """Display scorecard with EMI project styling"""
    sc = fetch_cricbuzz(f"mcenter/v1/{match_id}/scard")
    
    if not sc or 'scoreCard' not in sc or not sc['scoreCard']:
        match_info = fetch_cricbuzz(f"mcenter/v1/{match_id}")
        
        if match_info:
            st.info("📊 **Match Information Available**")
            match_header = match_info.get('matchHeader', {})
            team1 = match_header.get('team1', {}).get('name', 'Team 1')
            team2 = match_header.get('team2', {}).get('name', 'Team 2')
            status = match_header.get('status', 'Status unavailable')
            
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); 
                 padding: 20px; border-radius: 12px; border-left: 6px solid #0ea5e9;'>
                <h3 style='color: #0c4a6e !important;'>{team1} vs {team2}</h3>
                <p style='color: #0284c7 !important; font-weight: 700;'>{status}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ Scorecard not available yet")
        return
    
    # Display full scorecard
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
             margin: 20px 0; box-shadow: 0 4px 15px rgba(14, 165, 233, 0.4);'>
            <h3 style='color: white !important; margin: 0;'>Innings {inning_idx + 1}: {team}</h3>
            <h2 style='color: white !important; font-size: 3rem; margin: 15px 0;'>{runs}/{wickets}</h2>
            <p style='color: white !important; font-size: 1.3rem; margin: 0;'>Overs: {overs}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Batting
        st.markdown("#### 🏏 Batting Performance")
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
                st.dataframe(pd.DataFrame(batting_data), use_container_width=True, hide_index=True, height=400)
        
        st.markdown("---")
        
        # Bowling
        st.markdown("#### ⚾ Bowling Performance")
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
                st.dataframe(pd.DataFrame(bowling_data), use_container_width=True, hide_index=True, height=400)
        
        st.markdown("---")

# ==================== HEADER ====================
st.title("🏏 Cricbuzz LiveStats")
st.subheader("Real-Time Cricket Insights & SQL-Based Analytics")
st.caption("📊 Live Match Data • Player Statistics • Advanced SQL Queries • Full CRUD Operations")
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

if RAPIDAPI_KEY:
    st.sidebar.success("✅ API Connected")
else:
    st.sidebar.error("❌ API Disabled")

if engine:
    st.sidebar.success("✅ Database Online")
else:
    st.sidebar.error("❌ Database Offline")

# ==================== HOME ====================
if page == "🏠 Home":
    st.header("Welcome to Cricbuzz LiveStats! 🏏")
    st.markdown("**Your comprehensive cricket analytics platform**")
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    col1.metric("🏏 Live API", "Active" if RAPIDAPI_KEY else "Disabled", "+Real-time")
    col2.metric("🗄️ Database", "Connected" if engine else "Disabled", "+25 Tables")
    col3.metric("📊 Features", "Complete", "+100%")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success("""
        ### ✨ Live Cricket Features
        - **Real-time** match updates from Cricbuzz API
        - **Detailed** scorecards with batting & bowling stats
        - **Historical** completed match data
        - **Player** performance tracking
        """)
        
        st.info("""
        ### 📊 Analytics Features
        - **25 database tables** with cricket statistics
        - **Advanced SQL** query engine
        - **CSV export** for all data
        - **Custom queries** support
        """)
    
    with col2:
        st.success("""
        ### 🗄️ Database Management
        - **Full CRUD** operations on player data
        - **CREATE** - Add new players
        - **READ** - Search and view players
        - **UPDATE** - Modify player information
        - **DELETE** - Remove players with confirmation
        """)
        
        st.info("""
        ### 🎯 Data Tables Available
        - ODI Batting & Bowling Stats
        - Indian Players Database
        - All-Rounders Performance
        - Recent Match History
        - Player Career Summaries
        - And 20+ more tables!
        """)
    
    st.markdown("---")
    st.info("👈 **Get Started:** Use the sidebar navigation to explore different features!")

# ==================== LIVE MATCHES ====================
elif page == "🏏 Live Matches":
    st.header("🏏 Live & Recent Matches")
    st.markdown("**Real-time match updates from Cricbuzz API**")
    st.markdown("---")
    
    if not RAPIDAPI_KEY:
        st.error("❌ **API Key Required** - Add RAPIDAPI_KEY in Streamlit Cloud Secrets")
        st.info("📝 **Setup:** Go to App Settings → Secrets → Add your RAPIDAPI_KEY")
    else:
        data = fetch_cricbuzz("matches/v1/live")
        
        if not data or 'typeMatches' not in data:
            data = fetch_cricbuzz("matches/v1/recent")
        
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
                            match_format = info.get('matchFormat', '')
                            
                            has_live = True
                            
                            st.markdown(f"""
                            <div class='match-card'>
                                <h3 style='color:#0c4a6e; margin:0 0 10px 0;'>🏏 {t1} vs {t2}</h3>
                                <p style='color:#0284c7; font-weight:700; font-size:1.2rem; margin:8px 0;'>{status}</p>
                                <p style='color:#64748b; margin:0; font-size:1.05rem;'>📍 {venue} • {match_format}</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            if st.button(f"📊 View Detailed Scorecard", key=f"sc_{match_id}", type="primary"):
                                st.markdown("---")
                                display_scorecard(match_id)
            
            if not has_live:
                st.info("ℹ️ **No Live Matches Currently**")
                st.markdown("### 📋 Recent Completed Matches")
                
                if engine:
                    completed = run_sql_query("""
                        SELECT match_desc AS Match, team1_name AS Team1, team2_name AS Team2, 
                               winner_sname AS Winner, venue_name AS Venue 
                        FROM recent_matches 
                        ORDER BY match_date DESC 
                        LIMIT 15
                    """)
                    
                    if not completed.empty:
                        st.success(f"✅ Showing {len(completed)} recent completed matches")
                        st.dataframe(completed, use_container_width=True, hide_index=True, height=600)
                    else:
                        st.warning("No completed matches found in database")
        else:
            st.warning("⚠️ Unable to fetch match data from API")

# ==================== TOP STATS ====================
elif page == "📊 Top Stats":
    st.header("📊 Top Player Statistics")
    st.markdown("**Explore cricket statistics from 25+ database tables**")
    st.markdown("---")
    
    table_map = {
        "ODI Batting Stats": "odi_batting_stats",
        "Indian Players": "indian_players",
        "All-Rounders": "all_rounders",
        "Bowlers Aggregate": "bowlers_aggregate",
        "Player Career Summary": "player_career_summary",
        "Recent Form": "recent_form",
        "Top Scorers (All Formats)": "top_scorers_in_every_format",
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
        limit = st.selectbox("📈 Number of Records", [10, 20, 50, 100, 200])
    
    if engine and st.button("🔍 Load Statistics", type="primary"):
        table_name = table_map[selected_table]
        
        with st.spinner(f"📊 Loading {selected_table}..."):
            df = run_sql_query(f"SELECT * FROM {table_name} LIMIT {limit}")
        
        if not df.empty:
            st.success(f"✅ Successfully loaded {len(df):,} records from **{selected_table}**")
            st.dataframe(df, use_container_width=True, height=600)
            
            csv = df.to_csv(index=False).encode()
            st.download_button("📥 Download as CSV", csv, f"{table_name}.csv", "text/csv", type="primary")
        else:
            st.warning(f"⚠️ No data found in {selected_table}")
    elif not engine:
        st.error("❌ Database not connected")
    else:
        st.info("👆 **Select a table and click 'Load Statistics' to view data**")

# ==================== SQL ANALYTICS ====================
elif page == "🔍 SQL Analytics":
    st.header("🔍 SQL Query Analytics")
    st.markdown("**Run pre-built queries on cricket database**")
    st.markdown("---")
    
    queries = {
        "Top 20 Run Scorers (ODI)": "SELECT player_name, runs, batting_avg, matches FROM odi_batting_stats ORDER BY runs DESC LIMIT 20;",
        "All Indian Players": "SELECT name, playing_role, batting_style, bowling_style FROM indian_players LIMIT 50;",
        "Best All-Rounders": "SELECT player_name, total_runs, total_wickets, cricket_format FROM all_rounders ORDER BY (total_runs + total_wickets*20) DESC LIMIT 20;",
        "Recent Match Results": "SELECT match_desc, team1_name, team2_name, winner_sname, venue_name FROM recent_matches ORDER BY match_date DESC LIMIT 30;",
        "Top Batting Partnerships": "SELECT player_names, combined_partnership_runs, match_context FROM partnerships ORDER BY combined_partnership_runs DESC LIMIT 20;",
        "Bowler Performance by Venue": "SELECT bowler, venue, total_wickets, average_economy_rate, matches FROM bowler_venue_stats ORDER BY total_wickets DESC LIMIT 30;",
        "Player Career Statistics": "SELECT player, test_matches, odi_matches, t20i_matches, total_matches FROM player_career_summary ORDER BY total_matches DESC LIMIT 30;",
        "Toss Impact Analysis": "SELECT format, win_percent_choose_bat_first, win_percent_choose_field_first, overall_win_percent FROM toss_advantage_stats;",
        "Team Home vs Away Performance": "SELECT team, format, home_wins, away_wins, (home_wins + away_wins) AS total_wins FROM team_home_away_wins ORDER BY total_wins DESC LIMIT 20;",
        "Recent Player Form": "SELECT player, avg_runs_last5, avg_runs_last10, form_category, consistency_score_sd FROM recent_form ORDER BY avg_runs_last5 DESC LIMIT 20;"
    }
    
    query_name = st.selectbox("🔎 Select Pre-Built Query", list(queries.keys()))
    sql = queries[query_name]
    
    with st.expander("📝 View SQL Code", expanded=False):
        st.code(sql, language="sql")
    
    if st.button("▶️ Execute Query", type="primary"):
        with st.spinner("⚡ Executing SQL query..."):
            df = run_sql_query(sql)
        
        if not df.empty:
            st.success(f"✅ Query executed successfully - Returned {len(df):,} rows")
            st.dataframe(df, use_container_width=True, height=600)
            
            csv = df.to_csv(index=False).encode()
            st.download_button("📥 Download Results", csv, f"{query_name}.csv", "text/csv", type="primary")
        else:
            st.warning("⚠️ Query returned no results")

# ==================== FULL CRUD ====================
elif page == "👤 Player CRUD":
    st.header("👤 Player Database Management")
    st.markdown("**Complete CRUD Operations - Create, Read, Update, Delete**")
    st.markdown("---")
    
    tabs = st.tabs(["➕ CREATE", "📖 READ", "✏️ UPDATE", "🗑️ DELETE"])
    
    # CREATE
    with tabs[0]:
        st.subheader("➕ Add New Player to Database")
        st.markdown("Fill in the player details below")
        
        with st.form("create_player", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Full Name *", placeholder="e.g., Virat Kohli")
                role = st.text_input("Playing Role *", placeholder="e.g., Batsman")
                batting = st.text_input("Batting Style", placeholder="e.g., Right-hand bat")
            
            with col2:
                bowling = st.text_input("Bowling Style", placeholder="e.g., Right-arm medium")
                country = st.text_input("Country *", placeholder="e.g., India")
            
            submitted = st.form_submit_button("➕ Add Player to Database", type="primary")
            
            if submitted:
                if not all([name, role, country]):
                    st.error("❌ Please fill all required fields marked with (*)")
                elif not engine:
                    st.error("❌ Database connection not available")
                else:
                    try:
                        with engine.connect() as conn:
                            conn.execute(text("""
                                INSERT INTO players (full_name, playing_role, batting_style, bowling_style, country)
                                VALUES (:n, :r, :bat, :bowl, :c)
                            """), {"n": name, "r": role, "bat": batting or None, "bowl": bowling or None, "c": country})
                            conn.commit()
                        st.success(f"✅ **Success!** Player '{name}' has been added to the database")
                        st.balloons()
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Database Error: {e}")
    
    # READ
    with tabs[1]:
        st.subheader("📖 View All Players in Database")
        st.markdown("Search and explore player records")
        
        if not engine:
            st.error("❌ Database not connected")
        else:
            search = st.text_input("🔍 Search by player name", placeholder="Type player name...")
            
            col1, col2 = st.columns([3, 1])
            with col1:
                if st.button("🔍 Search Players", type="primary"):
                    if search:
                        sql = f"SELECT * FROM players WHERE LOWER(full_name) LIKE LOWER('%{search}%') ORDER BY id DESC LIMIT 100"
                    else:
                        sql = "SELECT * FROM players ORDER BY id DESC LIMIT 100"
                    
                    df = run_sql_query(sql)
                    
                    if not df.empty:
                        st.success(f"✅ Found {len(df):,} player(s)")
                        st.dataframe(df, use_container_width=True, height=600)
                        
                        csv = df.to_csv(index=False).encode()
                        st.download_button("📥 Download Player List", csv, "players.csv", "text/csv")
                    else:
                        st.info("ℹ️ No players found. Try a different search term or add players in CREATE tab.")
    
    # UPDATE
    with tabs[2]:
        st.subheader("✏️ Update Player Information")
        st.markdown("Modify existing player records")
        
        player_id = st.number_input("🔢 Enter Player ID to Update", min_value=1, step=1, help="Find ID in READ tab")
        
        if st.button("🔍 Load Player Data", type="primary"):
            if not engine:
                st.error("❌ Database not connected")
            else:
                try:
                    with engine.connect() as conn:
                        result = conn.execute(text("SELECT * FROM players WHERE id = :id"), {"id": player_id}).fetchone()
                    
                    if result:
                        st.session_state['update_player'] = result
                        st.success(f"✅ Loaded player: **{result.full_name}**")
                    else:
                        st.warning(f"⚠️ No player found with ID {player_id}")
                except Exception as e:
                    st.error(f"❌ Error: {e}")
        
        if 'update_player' in st.session_state:
            player = st.session_state['update_player']
            
            st.info(f"📝 **Editing:** {player.full_name} (ID: {player.id})")
            
            with st.form("update_player"):
                col1, col2 = st.columns(2)
                
                with col1:
                    new_name = st.text_input("Full Name", value=player.full_name)
                    new_role = st.text_input("Playing Role", value=player.playing_role)
                    new_batting = st.text_input("Batting Style", value=player.batting_style or "")
                
                with col2:
                    new_bowling = st.text_input("Bowling Style", value=player.bowling_style or "")
                    new_country = st.text_input("Country", value=player.country)
                
                update_submitted = st.form_submit_button("💾 Save Changes", type="primary")
                
                if update_submitted:
                    try:
                        with engine.connect() as conn:
                            conn.execute(text("""
                                UPDATE players 
                                SET full_name=:n, playing_role=:r, batting_style=:bat, 
                                    bowling_style=:bowl, country=:c
                                WHERE id=:id
                            """), {"n": new_name, "r": new_role, "bat": new_batting or None, 
                                   "bowl": new_bowling or None, "c": new_country, "id": player_id})
                            conn.commit()
                        st.success(f"✅ **Updated!** Player ID {player_id} has been updated successfully")
                        del st.session_state['update_player']
                        st.balloons()
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
    
    # DELETE
    with tabs[3]:
        st.subheader("🗑️ Delete Player from Database")
        st.warning("⚠️ **Warning:** This action cannot be undone! Player will be permanently removed.")
        
        delete_id = st.number_input("🔢 Enter Player ID to Delete", min_value=1, step=1, key="delete_id")
        
        confirm = st.checkbox("✅ I understand this action is permanent and cannot be reversed")
        
        if st.button("🗑️ Permanently Delete Player", type="secondary"):
            if not confirm:
                st.error("❌ Please confirm deletion by checking the box above")
            elif not engine:
                st.error("❌ Database not connected")
            else:
                try:
                    with engine.connect() as conn:
                        check = conn.execute(text("SELECT full_name FROM players WHERE id = :id"), {"id": delete_id}).fetchone()
                        
                        if check:
                            conn.execute(text("DELETE FROM players WHERE id = :id"), {"id": delete_id})
                            conn.commit()
                            st.success(f"✅ **Deleted!** Player '{check.full_name}' (ID: {delete_id}) has been removed from database")
                            st.rerun()
                        else:
                            st.warning(f"⚠️ No player found with ID {delete_id}")
                except Exception as e:
                    st.error(f"❌ Error: {e}")

# ==================== FOOTER ====================
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 30px; background: linear-gradient(135deg, #0ea5e9 0%, #2563eb 100%); 
     color: white; border-radius: 15px; box-shadow: 0 4px 15px rgba(14, 165, 233, 0.3);'>
    <h2 style='color: white !important; margin: 0;'>🏏 Cricbuzz LiveStats</h2>
    <p style='color: white !important; font-size: 1.1rem; margin: 10px 0;'>
        Real-Time Cricket Insights & SQL-Based Analytics
    </p>
    <p style='color: #bae6fd !important; margin: 5px 0;'>
        Powered by Cricbuzz API & Neon PostgreSQL | Built with Streamlit
    </p>
</div>
""", unsafe_allow_html=True)
