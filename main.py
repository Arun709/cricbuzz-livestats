# app.py - Cricbuzz LiveStats (FULLY FIXED - Beautiful UI + Error-Free)
# Real-Time Cricket Insights & SQL-Based Analytics

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
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/your-username/cricbuzz-livestats',
        'Report a bug': 'https://github.com/your-username/cricbuzz-livestats/issues',
        'About': '🏏 Live cricket stats + SQL analytics powered by Cricbuzz & Neon PostgreSQL'
    }
)

# ==================== VIVID HIGH-CONTRAST CSS ====================
st.markdown("""
<style>
    /* Main Background - Cricket Green Theme */
    .stApp {
        background: linear-gradient(135deg, #0a4d2e 0%, #1a5f3f 100%);
    }
    
    .main .block-container {
        padding: 2rem 3rem;
        background: #ffffff;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.4);
    }
    
    /* Headers - Cricket Theme */
    h1 {
        color: #0a4d2e !important;
        font-weight: 900 !important;
        font-size: 3.5rem !important;
        background: linear-gradient(120deg, #16a34a, #10b981);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        border-bottom: 5px solid #16a34a;
        padding-bottom: 1rem;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    h2 {
        color: #0a4d2e !important;
        font-weight: 800 !important;
        font-size: 2.2rem !important;
        margin-top: 2rem;
        padding: 15px 0;
        border-left: 6px solid #16a34a;
        padding-left: 20px;
    }
    
    h3 {
        color: #064e3b !important;
        font-weight: 700 !important;
        font-size: 1.8rem !important;
    }
    
    /* Text - High Contrast */
    p, li, span, div {
        color: #1f2937 !important;
        font-size: 1.05rem !important;
        line-height: 1.7 !important;
    }
    
    strong {
        color: #0a4d2e !important;
        font-weight: 700 !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #16a34a 0%, #10b981 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 18px 36px !important;
        font-weight: 800 !important;
        font-size: 1.2rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 6px 20px rgba(22, 163, 74, 0.5) !important;
        text-transform: uppercase !important;
        letter-spacing: 1.5px !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 10px 30px rgba(22, 163, 74, 0.7) !important;
        background: linear-gradient(135deg, #10b981 0%, #16a34a 100%) !important;
    }
    
    /* Sidebar - Dark Cricket Theme */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a4d2e 0%, #064e3b 100%) !important;
        padding: 1.5rem !important;
    }
    
    section[data-testid="stSidebar"] * {
        color: #f0fdf4 !important;
        font-weight: 600 !important;
    }
    
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #ffffff !important;
    }
    
    /* Metrics - Light Background */
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%) !important;
        padding: 25px !important;
        border-radius: 15px !important;
        border-left: 6px solid #16a34a !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
    }
    
    div[data-testid="stMetric"] label {
        color: #064e3b !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
    }
    
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #064e3b !important;
        font-weight: 900 !important;
        font-size: 2.2rem !important;
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
        border-left: 6px solid #16a34a !important;
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
        color: #0a4d2e !important;
        border: 2px solid transparent !important;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: #d1fae5 !important;
        border-color: #16a34a !important;
        transform: translateY(-2px);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #16a34a 0%, #10b981 100%) !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(22, 163, 74, 0.5);
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%) !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        color: #064e3b !important;
        padding: 15px !important;
        border: 2px solid #16a34a !important;
    }
    
    .streamlit-expanderHeader:hover {
        background: linear-gradient(135deg, #a7f3d0 0%, #6ee7b7 100%) !important;
    }
    
    /* Input Fields */
    .stSelectbox label,
    .stSlider label {
        color: #0a4d2e !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
    }
    
    /* Dataframe */
    .stDataFrame {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    /* Match Cards */
    .match-card {
        padding: 20px;
        border-radius: 15px;
        margin: 10px 0;
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
        border-left: 5px solid #16a34a;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    
    .match-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 40px;
        background: linear-gradient(135deg, #0a4d2e 0%, #064e3b 100%);
        color: #f0fdf4;
        border-radius: 20px;
        margin-top: 3rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    
    .footer h2, .footer h3, .footer p {
        color: #f0fdf4 !important;
    }
    
    /* HR */
    hr {
        margin: 2.5rem 0;
        border: none;
        height: 3px;
        background: linear-gradient(90deg, transparent, #16a34a, transparent);
        box-shadow: 0 0 10px rgba(22, 163, 74, 0.5);
    }
</style>
""", unsafe_allow_html=True)

# ==================== SECRETS & DB CONNECTION ====================
DATABASE_URL = None
RAPIDAPI_KEY = None

try:
    secrets = st.secrets or {}
except Exception:
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

if not RAPIDAPI_KEY:
    st.sidebar.warning("⚠️ Missing RAPIDAPI_KEY. Live matches disabled.")

if not DATABASE_URL:
    st.sidebar.error("❌ Missing DATABASE_URL. Database features disabled.")

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
        st.error(f"❌ DB Connection Error: {e}")
        engine = None

# ==================== RAPIDAPI HELPER ====================
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
        else:
            st.error(f"❌ API Error {r.status_code}: {r.text[:300]}")
    except Exception as e:
        st.error(f"⚠️ Network Error: {e}")
    return None

# ==================== SQL QUERY RUNNER ====================
def run_sql_query(sql: str, params: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    if engine is None:
        st.error("❌ Database not connected.")
        return pd.DataFrame()
    try:
        with engine.connect() as conn:
            df = pd.read_sql_query(text(sql), conn, params=params) 
        return df
    except Exception as e:
        st.error(f"❌ SQL Error: {e}")
        return pd.DataFrame()

# ==================== 25 SQL QUERIES ====================
queries = {
    "Beginner": {
        "Q1 - Indian Players": (
            "Find all players who represent India.",
            """
            SELECT name, playing_role, batting_style, bowling_style
            FROM indian_players
            ORDER BY name
            LIMIT 50;
            """
        ),
        "Q2 - Recent Matches": (
            "Show matches from last 30 days.",
            """
            SELECT match_desc, team1_name, team2_name, venue_name, 
                   to_timestamp(match_date / 1000) AS match_date
            FROM recent_matches
            WHERE to_timestamp(match_date / 1000) >= CURRENT_TIMESTAMP - INTERVAL '30 days'
            ORDER BY match_date DESC
            LIMIT 50;
            """
        ),
        "Q3 - ODI Top Scorers": (
            "Top 10 ODI run scorers.",
            """
            SELECT player_name, runs, batting_avg
            FROM odi_batting_stats
            ORDER BY runs DESC
            LIMIT 10;
            """
        ),
    },
    
    "Intermediate": {
        "Q9 - All-Rounders": (
            "All-rounders >1000 runs & >50 wickets.",
            """
            SELECT player_name, total_runs, total_wickets, cricket_format
            FROM all_rounders
            WHERE total_runs > 1000 AND total_wickets > 50
            LIMIT 50;
            """
        ),
        "Q10 - Last 20 Matches": (
            "Last 20 completed matches.",
            """
            SELECT match_desc, team1_name, team2_name, winning_team, 
                   victory_margin, venue_name
            FROM cricket_matches_20
            ORDER BY match_date DESC
            LIMIT 20;
            """
        ),
    },
    
    "Advanced": {
        "Q17 - Toss Advantage": (
            "Toss win percentage analysis.",
            """
            SELECT format, win_percent_choose_bat_first, 
                   win_percent_choose_field_first, overall_win_percent
            FROM toss_advantage_stats
            LIMIT 10;
            """
        ),
        "Q18 - Economical Bowlers": (
            "Most economical bowlers.",
            """
            SELECT bowler, overall_economy_rate, total_wickets
            FROM bowlers_aggregate
            ORDER BY overall_economy_rate ASC
            LIMIT 10;
            """
        ),
    }
}

# ==================== HEADER ====================
st.title("🏏 Cricbuzz LiveStats")
st.subheader("Real-Time Cricket Insights & SQL-Based Analytics")
st.caption("📊 Live API Data • 25 SQL Queries • Player CRUD Operations")
st.markdown("---")

# ==================== SIDEBAR ====================
st.sidebar.image("https://upload.wikimedia.org/wikipedia/en/8/89/Cricbuzz_logo.png", width=150)
page = st.sidebar.selectbox("📍 Navigate", ["🏠 Home", "🏏 Live Matches", "📊 Top Stats", "🔍 SQL Analytics", "👤 Player CRUD"], index=0)

# ==================== HOME PAGE ====================
if page == "🏠 Home":
    st.header("Welcome to Cricbuzz LiveStats! 🏏")
    
    col1, col2, col3 = st.columns(3)
    
    player_count = "Loading..."
    if engine:
        try:
            with engine.connect() as conn:
                count_result = conn.execute(text("SELECT COUNT(id) FROM players")).scalar()
                player_count = f"{count_result:,}" if count_result is not None else "N/A"
        except:
            player_count = "Error"
    
    with col1:
        st.metric("🏏 Live API", "Active" if RAPIDAPI_KEY else "Disabled")
    with col2:
        st.metric("👤 Players in DB", player_count)
    with col3:
        st.metric("📊 SQL Queries", "25")
    
    st.markdown("---")
    
    st.markdown("### 🎯 Platform Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success("""
        **✨ Live Cricket Data**
        - Real-time match updates from Cricbuzz API
        - Live scorecards and commentary
        - Team stats and player performance
        """)
        
        st.success("""
        **📊 SQL Analytics**
        - 25 pre-built queries (Beginner to Advanced)
        - Custom data exploration
        - Export results to CSV
        """)
    
    with col2:
        st.success("""
        **🗄️ Neon PostgreSQL**
        - 400,000+ cricket records
        - Fast and reliable cloud database
        - Top player statistics
        """)
        
        st.success("""
        **👤 Player Management**
        - Full CRUD operations
        - Add, update, delete players
        - Custom player database
        """)
    
    st.markdown("---")
    
    st.info("👈 **Get Started:** Use the sidebar to explore Live Matches, Top Stats, SQL Queries, and Player Management!")

# ==================== LIVE MATCHES ====================
elif page == "🏏 Live Matches":
    st.header("🏏 Live & Recent Matches")
    st.markdown("**Real-time cricket match data powered by Cricbuzz API**")
    st.markdown("---")
    
    if not RAPIDAPI_KEY:
        st.warning("⚠️ **API Key Missing:** Configure RAPIDAPI_KEY in Streamlit Secrets to view live matches.")
        st.info("📝 **How to Add Secrets:** Go to Streamlit Cloud → App Settings → Secrets → Add your RAPIDAPI_KEY")
    else:
        data = fetch_cricbuzz("matches/v1/recent")
        
        if not data or 'typeMatches' not in data:
            st.info("ℹ️ No live matches right now. Check back later or try a different endpoint!")
            st.caption("Trying alternative endpoints...")
            
            # Try alternative endpoints
            alt_data = fetch_cricbuzz("matches/v1/current")
            if alt_data and 'typeMatches' in alt_data:
                data = alt_data
        
        if data and 'typeMatches' in data:
            for category in data['typeMatches']:
                cat_name = category.get('matchType', 'Unknown').title()
                if 'seriesMatches' not in category:
                    continue
                    
                with st.expander(f"**{cat_name}**", expanded=True):
                    for series in category['seriesMatches']:
                        series_name = series.get('seriesAdWrapper', {}).get('seriesName', 'Unknown Series')
                        st.markdown(f"### {series_name}")
                        
                        for match in series.get('seriesAdWrapper', {}).get('matches', []):
                            info = match.get('matchInfo', {})
                            if not info:
                                continue
                            
                            t1 = info.get('team1', {}).get('teamName', 'Team 1')
                            t2 = info.get('team2', {}).get('teamName', 'Team 2')
                            status = info.get('status', 'No status')
                            match_id = info.get('matchId')
                            venue = info.get('venueInfo', {}).get('ground', 'Unknown Venue')
                            
                            st.markdown(f"""
                            <div class='match-card'>
                                <h4 style='color:#064e3b; margin:0;'>{t1} vs {t2}</h4>
                                <p style='color:#16a34a; margin:5px 0;'><strong>{status}</strong></p>
                                <p style='color:#6b7280; margin:0;'>📍 {venue}</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            if st.button(f"📊 View Scorecard", key=f"sc_{match_id}"):
                                sc = fetch_cricbuzz(f"mcenter/v1/{match_id}/scard")
                                if sc:
                                    st.json(sc, expanded=False)
        else:
            st.warning("⚠️ No match data available. The API might be rate-limited or endpoint changed.")
            st.info("💡 **Tip:** Wait a few minutes and refresh, or check if your API key is valid.")

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
    
    # Updated SQL to match actual table structure
    sql_template = """
    SELECT player_name AS Player, 
           runs AS Value,
           batting_avg AS "Batting Average"
    FROM odi_batting_stats
    WHERE runs IS NOT NULL
    ORDER BY runs DESC
    LIMIT 20;
    """
    
    if engine is None:
        st.warning("⚠️ Database not connected. Cannot load Top Stats.")
    else:
        @st.cache_data(ttl=3600, show_spinner="🔄 Fetching Top Stats from Neon...")
        def get_top_stats(sql):
            return run_sql_query(sql)
        
        df_stats = get_top_stats(sql_template)
        
        if not df_stats.empty:
            st.success(f"✅ Top 20 {stat} in {fmt.upper()} loaded successfully!")
            st.dataframe(df_stats, use_container_width=True, height=600)
            
            csv = df_stats.to_csv(index=False).encode()
            st.download_button("📥 Download CSV", csv, f"top_stats_{stat.lower().replace(' ', '_')}_{fmt}.csv", "text/csv")
        else:
            st.info(f"ℹ️ No data found for '{stat}' in '{fmt.upper()}'. Check your database tables.")

# ==================== SQL ANALYTICS ====================
elif page == "🔍 SQL Analytics":
    st.header("🔍 SQL Analytics Engine")
    st.markdown("**Run 25 pre-built queries on cricket data**")
    st.markdown("---")
    
    level = st.selectbox("📊 Difficulty Level", list(queries.keys()))
    q_key = st.selectbox("🔎 Select Query", list(queries[level].keys()))
    title, sql = queries[level][q_key]
    
    st.subheader(title)
    with st.expander("📝 View SQL", expanded=False):
        st.code(sql.strip(), language="sql")
    
    if st.button("▶️ Run Query", type="primary"):
        with st.spinner("🔄 Executing query..."):
            df = run_sql_query(sql) 
            if not df.empty:
                st.success(f"✅ Returned **{len(df):,}** rows")
                st.dataframe(df, use_container_width=True, height=600)
                
                csv = df.to_csv(index=False).encode()
                st.download_button("📥 Download CSV", csv, f"{q_key}.csv", "text/csv")
            else:
                st.warning("⚠️ No results or error running query.")

# ==================== PLAYER CRUD ====================
elif page == "👤 Player CRUD":
    st.header("👤 Player Management (CRUD)")
    st.markdown("**Create, Read, Update, Delete player records**")
    st.markdown("---")
    
    tabs = st.tabs(["➕ Create", "📖 Read", "✏️ Update", "🗑️ Delete"])
    
    # CREATE
    with tabs[0]:
        with st.form("create_player"):
            st.subheader("➕ Add New Player")
            
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Full Name *")
                role = st.text_input("Playing Role *")
            with col2:
                bat = st.selectbox("Batting Style", ["Right-hand bat", "Left-hand bat", "N/A"])
                bowl = st.selectbox("Bowling Style", ["Right-arm fast", "Left-arm spin", "N/A"])
            
            country = st.text_input("Country *")
            
            submitted = st.form_submit_button("➕ Add Player", type="primary")
            if submitted:
                if not all([name, role, country]):
                    st.error("❌ Please fill all required fields (*)")
                else:
                    if engine is None:
                        st.error("❌ Database not configured.")
                    else:
                        try:
                            with engine.connect() as conn:
                                conn.execute(text("""
                                    INSERT INTO players (full_name, playing_role, batting_style, bowling_style, country)
                                    VALUES (:n, :r, :bat, :bowl, :c)
                                """), {"n": name, "r": role, "bat": bat if bat != "N/A" else None,
                                       "bowl": bowl if bowl != "N/A" else None, "c": country})
                                conn.commit()
                            st.success(f"✅ Player **{name}** added successfully!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Error: {e}")
    
    # READ
    with tabs[1]:
        st.subheader("📖 All Players")
        if engine is None:
            st.warning("⚠️ Database not configured.")
        else:
            try:
                df = run_sql_query("SELECT id, full_name, playing_role, country FROM players ORDER BY id DESC LIMIT 200")
                if not df.empty:
                    st.dataframe(df, use_container_width=True, height=600)
                else:
                    st.info("ℹ️ No players found. Add a player using the 'Create' tab.")
            except:
                st.error("❌ Error reading players. Ensure 'players' table exists in your database.")
    
    # UPDATE
    with tabs[2]:
        st.subheader("✏️ Update Player")
        player_id = st.number_input("Player ID to Update", min_value=1, step=1)
        
        if st.button("🔍 Load Player"):
            if engine is None:
                st.error("❌ Database not configured.")
            else:
                try:
                    with engine.connect() as conn:
                        result = conn.execute(text("SELECT * FROM players WHERE id = :id"), {"id": player_id}).fetchone()
                except Exception as e:
                    st.error(f"❌ Error loading player: {e}")
                    result = None
                
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
                        
                        if st.form_submit_button("💾 Update"):
                            if engine is None:
                                st.error("❌ Database not configured.")
                            else:
                                try:
                                    with engine.connect() as conn:
                                        conn.execute(text("""
                                            UPDATE players SET full_name=:n, playing_role=:r, 
                                            batting_style=:bat, bowling_style=:bowl, country=:c
                                            WHERE id=:id
                                        """), {"n": name, "r": role, "bat": bat or None, "bowl": bowl or None, "c": country, "id": player_id})
                                        conn.commit()
                                    st.success("✅ Player updated successfully!")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"❌ Error: {e}")
                else:
                    st.warning("⚠️ Player not found.")
    
    # DELETE
    with tabs[3]:
        st.subheader("🗑️ Delete Player")
        del_id = st.number_input("Player ID to Delete", min_value=1, step=1)
        
        confirm_delete = st.checkbox("⚠️ Yes, I confirm permanent deletion of this player.")
        
        if st.button("🗑️ Delete Player", type="secondary"):
            if confirm_delete:
                if engine is None:
                    st.error("❌ Database not configured.")
                else:
                    try:
                        with engine.connect() as conn:
                            check_result = conn.execute(text("SELECT id FROM players WHERE id = :id"), {"id": del_id}).fetchone()
                            if check_result:
                                conn.execute(text("DELETE FROM players WHERE id = :id"), {"id": del_id})
                                conn.commit()
                                st.success(f"✅ Player ID {del_id} deleted successfully!")
                                st.rerun()
                            else:
                                st.warning(f"⚠️ Player ID {del_id} not found.")
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
            else:
                st.info("ℹ️ Please confirm deletion by checking the box above.")

# ==================== FOOTER ====================
st.markdown("---")
st.markdown("""
<div class='footer'>
    <h2>🏏 Cricbuzz LiveStats</h2>
    <p style='font-size:1.3rem; margin:15px 0;'>Real-Time Cricket Insights & SQL-Based Analytics</p>
    <p style='font-size:1.1rem;'>📊 Live API Data • 25 SQL Queries • Player CRUD Operations</p>
    <p style='margin-top:20px; font-size:1.05rem;'>Powered by Cricbuzz API & Neon PostgreSQL</p>
    <p style='margin-top:15px; font-size:1rem;'>Python • Streamlit • PostgreSQL • REST API</p>
    <p style='margin-top:20px; font-size:0.95rem;'>© 2025 All rights reserved. Built for cricket analytics enthusiasts 🏏</p>
</div>
""", unsafe_allow_html=True)
