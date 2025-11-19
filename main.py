# app.py - Cricbuzz LiveStats (COMPLETE FINAL VERSION)
# All Database Tables • Full CRUD • Working Scorecard • Readable UI

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

# ==================== ULTRA READABLE CSS ====================
st.markdown("""
<style>
    /* White Background */
    .stApp {
        background: #ffffff;
    }
    
    .main .block-container {
        padding: 2rem 3rem;
        background: #ffffff;
    }
    
    /* Headers - Dark Blue */
    h1, h2, h3, h4 {
        color: #0c4a6e !important;
        font-weight: 800 !important;
    }
    
    /* All Text - Black */
    p, li, span, div, label, td, th {
        color: #000000 !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
    }
    
    /* Buttons - BRIGHT BLUE */
    .stButton > button {
        background: #0ea5e9 !important;
        color: #ffffff !important;
        border: 2px solid #0369a1 !important;
        border-radius: 8px !important;
        padding: 12px 24px !important;
        font-weight: 800 !important;
        font-size: 1.1rem !important;
        text-transform: uppercase !important;
    }
    
    .stButton > button:hover {
        background: #0284c7 !important;
        border-color: #0c4a6e !important;
    }
    
    /* Sidebar - WHITE */
    section[data-testid="stSidebar"] {
        background: #ffffff !important;
        border-right: 2px solid #e5e7eb !important;
    }
    
    section[data-testid="stSidebar"] * {
        color: #000000 !important;
        font-weight: 700 !important;
    }
    
    /* Selectbox - WHITE WITH BLACK TEXT */
    .stSelectbox label {
        color: #000000 !important;
        font-weight: 800 !important;
        font-size: 1.2rem !important;
    }
    
    .stSelectbox > div > div {
        background: #ffffff !important;
        color: #000000 !important;
        border: 2px solid #0ea5e9 !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
    }
    
    /* Input Fields */
    .stTextInput label, .stNumberInput label {
        color: #000000 !important;
        font-weight: 800 !important;
        font-size: 1.1rem !important;
    }
    
    .stTextInput input, .stNumberInput input {
        border: 2px solid #0ea5e9 !important;
        font-weight: 600 !important;
    }
    
    /* Metrics */
    div[data-testid="stMetric"] {
        background: #dbeafe !important;
        padding: 20px !important;
        border-radius: 10px !important;
        border: 2px solid #0ea5e9 !important;
    }
    
    div[data-testid="stMetric"] label {
        color: #0c4a6e !important;
        font-weight: 800 !important;
        font-size: 1.2rem !important;
    }
    
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #0c4a6e !important;
        font-weight: 900 !important;
        font-size: 2.5rem !important;
    }
    
    /* Alerts */
    .stSuccess, .stInfo, .stWarning, .stError {
        border-radius: 8px !important;
        padding: 1rem !important;
        font-weight: 700 !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab"] {
        color: #000000 !important;
        font-weight: 800 !important;
        font-size: 1.1rem !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: #0ea5e9 !important;
        color: #ffffff !important;
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
    """Display scorecard or show completed match info"""
    sc = fetch_cricbuzz(f"mcenter/v1/{match_id}/scard")
    
    if not sc or 'scoreCard' not in sc or not sc['scoreCard']:
        # Try to get match info instead
        match_info = fetch_cricbuzz(f"mcenter/v1/{match_id}")
        
        if match_info:
            st.info("📊 **Match Summary**")
            
            # Extract match details
            match_header = match_info.get('matchHeader', {})
            team1 = match_header.get('team1', {}).get('name', 'Team 1')
            team2 = match_header.get('team2', {}).get('name', 'Team 2')
            status = match_header.get('status', 'Status unavailable')
            result = match_header.get('result', {}).get('resultType', '')
            
            st.markdown(f"""
            ### {team1} vs {team2}
            **Status:** {status}
            **Result:** {result}
            """)
        else:
            st.warning("⚠️ Scorecard not available - Match may not have started yet")
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
        <div style='background:#0ea5e9; color:white; padding:20px; border-radius:10px; text-align:center; margin:15px 0;'>
            <h3 style='color:white !important;'>Innings {inning_idx + 1}: {team}</h3>
            <h2 style='color:white !important; font-size:2.5rem;'>{runs}/{wickets}</h2>
            <p style='color:white !important; font-size:1.2rem;'>Overs: {overs}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Batting
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
        
        # Bowling
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
st.subheader("Real-Time Cricket Analytics & Database Management")
st.markdown("---")

# ==================== SIDEBAR ====================
st.sidebar.title("🏏 NAVIGATION")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Select Page",
    ["🏠 Home", "🏏 Live Matches", "📊 Top Stats", "🔍 SQL Analytics", "👤 Player CRUD"],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.markdown("**System Status**")
st.sidebar.success("✅ API Active" if RAPIDAPI_KEY else "❌ API Disabled")
st.sidebar.success("✅ DB Connected" if engine else "❌ DB Disabled")

# ==================== HOME ====================
if page == "🏠 Home":
    st.header("Welcome to Cricbuzz LiveStats!")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("🏏 API Status", "Active" if RAPIDAPI_KEY else "Disabled")
    col2.metric("🗄️ Database", "Connected" if engine else "Disabled")
    col3.metric("📊 Tables", "25")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success("""
        **✨ Live Cricket Features**
        - Real-time match updates
        - Detailed scorecards
        - Completed match history
        - Player statistics
        """)
    
    with col2:
        st.info("""
        **📊 Database Features**
        - 25 cricket data tables
        - Advanced SQL analytics
        - Full CRUD operations
        - CSV data export
        """)

# ==================== LIVE MATCHES ====================
elif page == "🏏 Live Matches":
    st.header("🏏 Live & Recent Matches")
    st.markdown("---")
    
    if not RAPIDAPI_KEY:
        st.error("❌ API Key Required - Add RAPIDAPI_KEY in Streamlit Secrets")
    else:
        # Fetch live matches
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
                            <div style='background:#ffffff; border:3px solid #0ea5e9; border-radius:10px; padding:20px; margin:10px 0;'>
                                <h3 style='color:#0c4a6e; margin:0;'>🏏 {t1} vs {t2}</h3>
                                <p style='color:#0284c7; font-weight:700; margin:5px 0;'>{status}</p>
                                <p style='color:#64748b; margin:0;'>📍 {venue} • {match_format}</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            if st.button(f"📊 VIEW SCORECARD", key=f"sc_{match_id}"):
                                st.markdown("---")
                                display_scorecard(match_id)
            
            if not has_live:
                st.info("ℹ️ **No Live Matches Currently**")
                st.markdown("### 📋 Recent Completed Matches")
                
                # Show recent completed matches from database
                if engine:
                    completed = run_sql_query("""
                        SELECT match_desc, team1_name, team2_name, winner_sname, venue_name 
                        FROM recent_matches 
                        ORDER BY match_date DESC 
                        LIMIT 10
                    """)
                    
                    if not completed.empty:
                        st.dataframe(completed, use_container_width=True, hide_index=True)
                    else:
                        st.warning("No completed matches in database")
        else:
            st.warning("⚠️ Unable to fetch match data from API")

# ==================== TOP STATS (ALL TABLES) ====================
elif page == "📊 Top Stats":
    st.header("📊 Top Player Statistics")
    st.markdown("---")
    
    # Table selection based on your database
    table_map = {
        "ODI Batting Stats": "odi_batting_stats",
        "Indian Players": "indian_players",
        "All-Rounders": "all_rounders",
        "Bowlers Aggregate": "bowlers_aggregate",
        "Player Career Summary": "player_career_summary",
        "Recent Form": "recent_form",
        "Top Scorers (All Formats)": "top_scorers_in_every_format",
        "Partnerships": "partnerships",
        "Clutch Batting": "clutch_batting_stats",
        "Player Roles": "player_roles"
    }
    
    col1, col2 = st.columns(2)
    
    with col1:
        selected_table = st.selectbox("📊 Select Data Table", list(table_map.keys()))
    
    with col2:
        limit = st.selectbox("📈 Show Top", [10, 20, 50, 100])
    
    if engine and st.button("🔍 LOAD DATA", type="primary"):
        table_name = table_map[selected_table]
        
        with st.spinner(f"Loading {selected_table}..."):
            df = run_sql_query(f"SELECT * FROM {table_name} LIMIT {limit}")
        
        if not df.empty:
            st.success(f"✅ Loaded {len(df)} records from {selected_table}")
            st.dataframe(df, use_container_width=True, height=600)
            
            csv = df.to_csv(index=False).encode()
            st.download_button("📥 DOWNLOAD CSV", csv, f"{table_name}.csv", "text/csv")
        else:
            st.warning(f"⚠️ No data in {selected_table}")
    else:
        st.info("👆 Select a table and click 'Load Data' to view statistics")

# ==================== SQL ANALYTICS ====================
elif page == "🔍 SQL Analytics":
    st.header("🔍 SQL Query Analytics")
    st.markdown("---")
    
    st.markdown("### 🎯 Pre-Built Queries")
    
    queries = {
        "Top Run Scorers (ODI)": "SELECT player_name, runs, batting_avg FROM odi_batting_stats ORDER BY runs DESC LIMIT 20;",
        "All Indian Players": "SELECT name, playing_role, batting_style FROM indian_players LIMIT 50;",
        "All-Rounders Stats": "SELECT player_name, total_runs, total_wickets FROM all_rounders ORDER BY total_runs DESC LIMIT 20;",
        "Recent Matches": "SELECT match_desc, team1_name, team2_name, winner_sname FROM recent_matches LIMIT 30;",
        "Top Partnerships": "SELECT player_names, combined_partnership_runs, match_context FROM partnerships ORDER BY combined_partnership_runs DESC LIMIT 20;",
        "Bowler Venue Stats": "SELECT bowler, venue, total_wickets, average_economy_rate FROM bowler_venue_stats LIMIT 30;",
        "Player Career Summary": "SELECT player, test_matches, odi_matches, t20i_matches, total_matches FROM player_career_summary LIMIT 30;",
        "Toss Advantage": "SELECT format, win_percent_choose_bat_first, win_percent_choose_field_first FROM toss_advantage_stats;",
        "Team Home/Away Wins": "SELECT team, format, home_wins, away_wins FROM team_home_away_wins LIMIT 20;",
        "Recent Player Form": "SELECT player, avg_runs_last5, avg_runs_last10, form_category FROM recent_form LIMIT 20;"
    }
    
    query_name = st.selectbox("🔎 Select Query", list(queries.keys()))
    sql = queries[query_name]
    
    with st.expander("📝 View SQL Code"):
        st.code(sql, language="sql")
    
    if st.button("▶️ RUN QUERY", type="primary"):
        with st.spinner("Executing query..."):
            df = run_sql_query(sql)
        
        if not df.empty:
            st.success(f"✅ Query returned {len(df):,} rows")
            st.dataframe(df, use_container_width=True, height=600)
            
            csv = df.to_csv(index=False).encode()
            st.download_button("📥 DOWNLOAD CSV", csv, f"{query_name}.csv", "text/csv")
        else:
            st.warning("⚠️ Query returned no results")

# ==================== FULL CRUD OPERATIONS ====================
elif page == "👤 Player CRUD":
    st.header("👤 Player Management - Full CRUD Operations")
    st.markdown("---")
    
    tabs = st.tabs(["➕ CREATE", "📖 READ", "✏️ UPDATE", "🗑️ DELETE"])
    
    # CREATE
    with tabs[0]:
        st.subheader("➕ Add New Player")
        
        with st.form("create_player"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Full Name *")
                role = st.text_input("Playing Role *")
                batting = st.text_input("Batting Style")
            
            with col2:
                bowling = st.text_input("Bowling Style")
                country = st.text_input("Country *")
            
            submitted = st.form_submit_button("➕ ADD PLAYER", type="primary")
            
            if submitted:
                if not all([name, role, country]):
                    st.error("❌ Please fill all required fields (*)")
                elif not engine:
                    st.error("❌ Database not connected")
                else:
                    try:
                        with engine.connect() as conn:
                            conn.execute(text("""
                                INSERT INTO players (full_name, playing_role, batting_style, bowling_style, country)
                                VALUES (:n, :r, :bat, :bowl, :c)
                            """), {"n": name, "r": role, "bat": batting or None, "bowl": bowling or None, "c": country})
                            conn.commit()
                        st.success(f"✅ Player '{name}' added successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
    
    # READ
    with tabs[1]:
        st.subheader("📖 View All Players")
        
        if not engine:
            st.error("❌ Database not connected")
        else:
            search = st.text_input("🔍 Search by name", "")
            
            if search:
                sql = f"SELECT * FROM players WHERE LOWER(full_name) LIKE LOWER('%{search}%') LIMIT 100"
            else:
                sql = "SELECT * FROM players ORDER BY id DESC LIMIT 100"
            
            df = run_sql_query(sql)
            
            if not df.empty:
                st.success(f"✅ Found {len(df)} players")
                st.dataframe(df, use_container_width=True, height=600)
                
                csv = df.to_csv(index=False).encode()
                st.download_button("📥 DOWNLOAD CSV", csv, "players.csv", "text/csv")
            else:
                st.info("ℹ️ No players found. Add players using the CREATE tab.")
    
    # UPDATE
    with tabs[2]:
        st.subheader("✏️ Update Player Information")
        
        player_id = st.number_input("Enter Player ID to Update", min_value=1, step=1)
        
        if st.button("🔍 LOAD PLAYER DATA"):
            if not engine:
                st.error("❌ Database not connected")
            else:
                try:
                    with engine.connect() as conn:
                        result = conn.execute(text("SELECT * FROM players WHERE id = :id"), {"id": player_id}).fetchone()
                    
                    if result:
                        st.session_state['update_player'] = result
                        st.success(f"✅ Loaded player: {result.full_name}")
                    else:
                        st.warning(f"⚠️ No player found with ID {player_id}")
                except Exception as e:
                    st.error(f"❌ Error: {e}")
        
        if 'update_player' in st.session_state:
            player = st.session_state['update_player']
            
            with st.form("update_player"):
                col1, col2 = st.columns(2)
                
                with col1:
                    new_name = st.text_input("Full Name", value=player.full_name)
                    new_role = st.text_input("Playing Role", value=player.playing_role)
                    new_batting = st.text_input("Batting Style", value=player.batting_style or "")
                
                with col2:
                    new_bowling = st.text_input("Bowling Style", value=player.bowling_style or "")
                    new_country = st.text_input("Country", value=player.country)
                
                update_submitted = st.form_submit_button("💾 UPDATE PLAYER", type="primary")
                
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
                        st.success(f"✅ Player ID {player_id} updated successfully!")
                        del st.session_state['update_player']
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
    
    # DELETE
    with tabs[3]:
        st.subheader("🗑️ Delete Player")
        st.warning("⚠️ **Warning:** This action cannot be undone!")
        
        delete_id = st.number_input("Enter Player ID to Delete", min_value=1, step=1, key="delete_id")
        
        confirm = st.checkbox("I confirm I want to permanently delete this player")
        
        if st.button("🗑️ DELETE PLAYER", type="secondary"):
            if not confirm:
                st.error("❌ Please confirm deletion by checking the box")
            elif not engine:
                st.error("❌ Database not connected")
            else:
                try:
                    with engine.connect() as conn:
                        # Check if player exists
                        check = conn.execute(text("SELECT full_name FROM players WHERE id = :id"), {"id": delete_id}).fetchone()
                        
                        if check:
                            conn.execute(text("DELETE FROM players WHERE id = :id"), {"id": delete_id})
                            conn.commit()
                            st.success(f"✅ Player '{check.full_name}' (ID: {delete_id}) deleted successfully!")
                            st.rerun()
                        else:
                            st.warning(f"⚠️ No player found with ID {delete_id}")
                except Exception as e:
                    st.error(f"❌ Error: {e}")

# ==================== FOOTER ====================
st.markdown("---")
st.markdown("**🏏 Cricbuzz LiveStats** | Powered by Cricbuzz API & Neon PostgreSQL | Built with Streamlit")
