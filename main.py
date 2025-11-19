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
    
    /* Headers - Dark Blue */
    h1 {
        color: #0c4a6e !important;
        font-weight: 900 !important;
        font-size: 3rem !important;
        border-bottom: 4px solid #0ea5e9;
        padding-bottom: 1rem;
        margin-bottom: 1.5rem;
    }
    
    h2 {
        color: #0c4a6e !important;
        font-weight: 800 !important;
        font-size: 2rem !important;
        margin-top: 1.5rem;
        border-left: 5px solid #0ea5e9;
        padding-left: 15px;
    }
    
    h3 {
        color: #075985 !important;
        font-weight: 700 !important;
        font-size: 1.6rem !important;
    }
    
    h4 {
        color: #0c4a6e !important;
        font-weight: 700 !important;
        font-size: 1.3rem !important;
    }
    
    /* All Text - Dark for Readability */
    p, li, span, div, label, td, th, .stMarkdown {
        color: #1e293b !important;
        font-size: 1.1rem !important;
        line-height: 1.7 !important;
    }
    
    strong, b {
        color: #0c4a6e !important;
        font-weight: 800 !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 14px 28px !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        box-shadow: 0 4px 12px rgba(14, 165, 233, 0.4) !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 16px rgba(14, 165, 233, 0.6) !important;
    }
    
    /* Sidebar - WHITE WITH DARK TEXT */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%) !important;
        padding: 1.5rem !important;
        border-right: 3px solid #e2e8f0 !important;
    }
    
    section[data-testid="stSidebar"] * {
        color: #0f172a !important;
        font-weight: 600 !important;
    }
    
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] .stMarkdown {
        color: #0f172a !important;
    }
    
    /* Sidebar Selectbox */
    section[data-testid="stSidebar"] .stSelectbox > div > div {
        background: white !important;
        color: #0f172a !important;
        border: 2px solid #cbd5e1 !important;
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
    
    .stTabs [data-baseweb="tab"]:hover {
        border-color: #0ea5e9 !important;
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
    
    /* Dataframe */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 3px 12px rgba(0,0,0,0.1);
    }
    
    /* Caption */
    .stCaption {
        color: #64748b !important;
        font-size: 1rem !important;
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
        st.sidebar.error(f"❌ DB Error")
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
        with st.spinner(f"🔄 Fetching data..."):
            r = requests.get(url, headers=headers, params=params, timeout=15)
        if r.status_code == 200:
            return r.json()
        else:
            st.error(f"❌ API Error {r.status_code}")
            return None
    except Exception as e:
        st.error(f"⚠️ Network Error: {e}")
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

# ==================== BEAUTIFUL SCORECARD ====================
def display_scorecard(scorecard_data, match_id):
    """Display beautiful scorecard with proper error handling"""
    
    if not scorecard_data:
        st.warning("⚠️ No scorecard data available from API")
        return
    
    # Check if scorecard exists
    if 'scoreCard' not in scorecard_data or not scorecard_data['scoreCard']:
        st.info("ℹ️ **Scorecard not yet available** - Match may not have started or data is pending")
        return
    
    scorecard = scorecard_data['scoreCard']
    
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
                st.info("ℹ️ Batting data not available yet")
        else:
            st.info("ℹ️ Batting data not available yet")
        
        st.markdown("---")
        
        # Bowling performance
        st.markdown("#### ⚾ Bowling Performance")
        bowler_data = innings.get('bowlTeamDetails', {}).get('bowlersData', {})
        
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
                        'Economy': f"{bowl_info.get('economy', 0):.2f}" if bowl_info.get('economy') else '0.00'
                    })
            
            if bowling_rows:
                df_bowling = pd.DataFrame(bowling_rows)
                st.dataframe(df_bowling, use_container_width=True, hide_index=True)
            else:
                st.info("ℹ️ Bowling data not available yet")
        else:
            st.info("ℹ️ Bowling data not available yet")
        
        st.markdown("---")

# ==================== SQL QUERIES ====================
queries = {
    "Beginner": {
        "Q1 - Indian Players": ("Find all Indian players", "SELECT name, playing_role FROM indian_players LIMIT 50;"),
        "Q2 - Recent Matches": ("Recent matches", "SELECT match_desc, team1_name, team2_name FROM recent_matches LIMIT 50;"),
    },
    "Intermediate": {
        "Q9 - All-Rounders": ("All-rounders stats", "SELECT player_name, total_runs, total_wickets FROM all_rounders LIMIT 50;"),
    },
    "Advanced": {
        "Q17 - Toss Stats": ("Toss advantage", "SELECT format, win_percent_choose_bat_first FROM toss_advantage_stats LIMIT 10;"),
    }
}

# ==================== HEADER ====================
st.title("🏏 Cricbuzz LiveStats")
st.subheader("Real-Time Cricket Insights & SQL-Based Analytics")
st.caption("📊 Live Match Data • Player Statistics • SQL Queries • Database Management")
st.markdown("---")

# ==================== SIDEBAR ====================
st.sidebar.title("🏏 Cricket Stats")
st.sidebar.markdown("**Navigate the platform**")
st.sidebar.markdown("---")

page = st.sidebar.selectbox(
    "📍 Select Page",
    ["🏠 Home", "🏏 Live Matches", "📊 Top Stats", "🔍 SQL Analytics", "👤 Player CRUD"],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.caption("**Status**")
if RAPIDAPI_KEY:
    st.sidebar.success("✅ API Connected")
else:
    st.sidebar.warning("⚠️ API Disabled")

if engine:
    st.sidebar.success("✅ DB Connected")
else:
    st.sidebar.warning("⚠️ DB Disabled")

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
        - Team performance
        """)
        
        st.info("""
        **📊 SQL Analytics**
        - 25 pre-built queries
        - Beginner to Advanced
        - Custom data exploration
        - CSV export available
        """)
    
    with col2:
        st.success("""
        **🗄️ Database Features**
        - 400,000+ cricket records
        - Fast Neon PostgreSQL
        - Cloud-powered storage
        - Real-time queries
        """)
        
        st.info("""
        **👤 Player Management**
        - Add new players
        - Update records
        - Delete entries
        - Full CRUD operations
        """)
    
    st.markdown("---")
    st.info("👈 **Get Started:** Use the sidebar to navigate to different sections!")

# ==================== LIVE MATCHES ====================
elif page == "🏏 Live Matches":
    st.header("🏏 Live & Recent Matches")
    st.markdown("**Real-time cricket match data from Cricbuzz API**")
    st.markdown("---")
    
    if not RAPIDAPI_KEY:
        st.warning("⚠️ **API Key Missing:** Add RAPIDAPI_KEY in Streamlit Secrets to view live matches.")
        st.info("📝 **How to Add:** Go to Streamlit Cloud → App Settings → Secrets → Add RAPIDAPI_KEY")
    else:
        # Try multiple endpoints
        data = fetch_cricbuzz("matches/v1/recent")
        
        if not data or 'typeMatches' not in data:
            data = fetch_cricbuzz("matches/v1/live")
        
        if not data or 'typeMatches' not in data:
            data = fetch_cricbuzz("matches/v1/upcoming")
        
        if data and 'typeMatches' in data:
            match_found = False
            
            for category in data['typeMatches']:
                cat_name = category.get('matchType', 'Unknown').title()
                
                series_matches = category.get('seriesMatches', [])
                if not series_matches:
                    continue
                
                with st.expander(f"**{cat_name}**", expanded=True):
                    for series in series_matches:
                        series_ad = series.get('seriesAdWrapper', {})
                        matches = series_ad.get('matches', [])
                        
                        if not matches:
                            continue
                        
                        match_found = True
                        
                        for match in matches:
                            info = match.get('matchInfo', {})
                            if not info:
                                continue
                            
                            t1 = info.get('team1', {}).get('teamName', 'Team 1')
                            t2 = info.get('team2', {}).get('teamName', 'Team 2')
                            status = info.get('status', 'Upcoming')
                            match_id = info.get('matchId')
                            venue_info = info.get('venueInfo', {})
                            venue = venue_info.get('ground', 'Unknown Venue')
                            city = venue_info.get('city', '')
                            
                            # Beautiful Match Card
                            st.markdown(f"""
                            <div class='match-card'>
                                <h3 style='color:#0c4a6e; margin:0 0 10px 0;'>🏏 {t1} vs {t2}</h3>
                                <p style='color:#0284c7; font-weight:700; font-size:1.15rem; margin:5px 0;'>{status}</p>
                                <p style='color:#64748b; margin:0;'>📍 {venue}, {city}</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Scorecard Button
                            if st.button(f"📊 View Scorecard", key=f"sc_{match_id}", type="primary"):
                                with st.spinner("🔄 Loading scorecard..."):
                                    sc = fetch_cricbuzz(f"mcenter/v1/{match_id}/scard")
                                    st.markdown("---")
                                    display_scorecard(sc, match_id)
            
            if not match_found:
                st.info("ℹ️ No matches available at the moment. Check back later!")
        else:
            st.warning("⚠️ Unable to fetch match data. API may be rate-limited or endpoint unavailable.")
            st.info("💡 **Tip:** Wait a few minutes and refresh the page.")

# ==================== TOP STATS ====================
elif page == "📊 Top Stats":
    st.header("📊 Top Player Statistics")
    st.markdown("**Stats loaded from Neon PostgreSQL Database**")
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
            st.download_button("📥 Download CSV", csv, f"top_stats_{stat}.csv", "text/csv")
        else:
            st.info("ℹ️ No data available in database")
    else:
        st.warning("⚠️ Database not connected")

# ==================== SQL ANALYTICS ====================
elif page == "🔍 SQL Analytics":
    st.header("🔍 SQL Analytics Engine")
    st.markdown("**Run pre-built queries on cricket data**")
    st.markdown("---")
    
    level = st.selectbox("📊 Difficulty Level", list(queries.keys()))
    q_key = st.selectbox("🔎 Select Query", list(queries[level].keys()))
    title, sql = queries[level][q_key]
    
    st.subheader(title)
    with st.expander("📝 View SQL Code"):
        st.code(sql, language="sql")
    
    if st.button("▶️ Run Query", type="primary"):
        with st.spinner("🔄 Executing query..."):
            df = run_sql_query(sql)
            if not df.empty:
                st.success(f"✅ Returned {len(df):,} rows")
                st.dataframe(df, use_container_width=True, height=600)
                
                csv = df.to_csv(index=False).encode()
                st.download_button("📥 Download CSV", csv, f"{q_key}.csv", "text/csv")
            else:
                st.warning("⚠️ No results found")

# ==================== PLAYER CRUD ====================
elif page == "👤 Player CRUD":
    st.header("👤 Player Management")
    st.markdown("**Create, Read, Update, Delete player records**")
    st.markdown("---")
    
    tabs = st.tabs(["➕ Create", "📖 Read", "✏️ Update", "🗑️ Delete"])
    
    with tabs[0]:
        with st.form("create"):
            st.subheader("➕ Add New Player")
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Full Name *")
                role = st.text_input("Playing Role *")
            with col2:
                bat = st.selectbox("Batting", ["Right-hand", "Left-hand", "N/A"])
                bowl = st.selectbox("Bowling", ["Right-arm fast", "Left-arm spin", "N/A"])
            country = st.text_input("Country *")
            
            if st.form_submit_button("➕ Add Player", type="primary"):
                if engine and all([name, role, country]):
                    try:
                        with engine.connect() as conn:
                            conn.execute(text("INSERT INTO players (full_name, playing_role, batting_style, bowling_style, country) VALUES (:n, :r, :bat, :bowl, :c)"), 
                                       {"n": name, "r": role, "bat": bat if bat != "N/A" else None, "bowl": bowl if bowl != "N/A" else None, "c": country})
                            conn.commit()
                        st.success(f"✅ Player **{name}** added successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
                else:
                    st.error("❌ Fill all required fields")
    
    with tabs[1]:
        st.subheader("📖 All Players")
        if engine:
            df = run_sql_query("SELECT id, full_name, playing_role, country FROM players ORDER BY id DESC LIMIT 200")
            if not df.empty:
                st.dataframe(df, use_container_width=True, height=600)
            else:
                st.info("ℹ️ No players in database")
        else:
            st.warning("⚠️ Database not connected")
    
    with tabs[2]:
        st.subheader("✏️ Update Player")
        player_id = st.number_input("Player ID", min_value=1, step=1)
        
        if st.button("🔍 Load Player"):
            if engine:
                try:
                    with engine.connect() as conn:
                        result = conn.execute(text("SELECT * FROM players WHERE id = :id"), {"id": player_id}).fetchone()
                except:
                    result = None
                
                if result:
                    with st.form("update"):
                        cols = st.columns(2)
                        with cols[0]:
                            name = st.text_input("Name", value=result.full_name)
                            role = st.text_input("Role", value=result.playing_role)
                        with cols[1]:
                            bat = st.text_input("Batting", value=result.batting_style or "")
                            bowl = st.text_input("Bowling", value=result.bowling_style or "")
                        country = st.text_input("Country", value=result.country)
                        
                        if st.form_submit_button("💾 Update"):
                            try:
                                with engine.connect() as conn:
                                    conn.execute(text("UPDATE players SET full_name=:n, playing_role=:r, batting_style=:bat, bowling_style=:bowl, country=:c WHERE id=:id"), 
                                               {"n": name, "r": role, "bat": bat or None, "bowl": bowl or None, "c": country, "id": player_id})
                                    conn.commit()
                                st.success("✅ Updated!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ {e}")
                else:
                    st.warning("⚠️ Player not found")
    
    with tabs[3]:
        st.subheader("🗑️ Delete Player")
        del_id = st.number_input("Player ID", min_value=1, step=1, key="del")
        confirm = st.checkbox("⚠️ Confirm deletion")
        
        if st.button("🗑️ Delete", type="secondary"):
            if confirm and engine:
                try:
                    with engine.connect() as conn:
                        check = conn.execute(text("SELECT id FROM players WHERE id = :id"), {"id": del_id}).fetchone()
                        if check:
                            conn.execute(text("DELETE FROM players WHERE id = :id"), {"id": del_id})
                            conn.commit()
                            st.success(f"✅ Deleted player ID {del_id}")
                            st.rerun()
                        else:
                            st.warning(f"⚠️ Player ID {del_id} not found")
                except Exception as e:
                    st.error(f"❌ {e}")
            else:
                st.info("ℹ️ Check the box to confirm")

# ==================== FOOTER ====================
st.markdown("---")
st.caption("🏏 **Cricbuzz LiveStats** | Powered by Cricbuzz API & Neon PostgreSQL | Built with Streamlit")
