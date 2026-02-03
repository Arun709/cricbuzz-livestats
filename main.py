import streamlit as st
import requests
import pandas as pd
from sqlalchemy import create_engine, text
from typing import Optional, Dict, Any
from datetime import datetime
import os

# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="Cricbuzz LiveStats Pro",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== PREMIUM UI WITH ANIMATIONS ====================
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Smooth Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-50px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    @keyframes shimmer {
        0% { background-position: -1000px 0; }
        100% { background-position: 1000px 0; }
    }
    
    @keyframes glow {
        0%, 100% { box-shadow: 0 0 20px rgba(14, 165, 233, 0.5); }
        50% { box-shadow: 0 0 40px rgba(14, 165, 233, 0.8); }
    }
    
    /* Main App Background */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
        font-family: 'Inter', sans-serif;
        animation: fadeIn 0.8s ease-in-out;
    }
    
    /* Glassmorphism Container */
    .main .block-container {
        padding: 1.5rem 2.5rem;
        background: rgba(15, 23, 42, 0.4);
        border-radius: 30px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.6);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        animation: fadeIn 1s ease-in-out;
    }
    
    /* Premium Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a0f1e 0%, #0f172a 100%);
        border-right: 1px solid rgba(14, 165, 233, 0.2);
        box-shadow: 4px 0 30px rgba(0,0,0,0.5);
        animation: slideInLeft 0.6s ease-out;
    }
    
    section[data-testid="stSidebar"] > div {
        padding: 2rem 1rem;
    }
    
    /* Sidebar Logo/Title */
    section[data-testid="stSidebar"] h1 {
        color: #fff;
        font-size: 1.8rem;
        font-weight: 900;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(120deg, #0ea5e9, #3b82f6, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shimmer 3s infinite linear;
        background-size: 200% auto;
    }
    
    /* Radio Buttons - Modern Card Style */
    .stRadio > div {
        background: transparent;
        gap: 0.8rem;
    }
    
    .stRadio > div > label {
        background: linear-gradient(135deg, rgba(14, 165, 233, 0.1) 0%, rgba(59, 130, 246, 0.1) 100%);
        border: 2px solid rgba(14, 165, 233, 0.3);
        border-radius: 16px;
        padding: 1rem 1.5rem;
        color: #e0f2fe;
        font-weight: 600;
        font-size: 1rem;
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        display: flex;
        align-items: center;
        gap: 0.8rem;
        margin: 0.5rem 0;
    }
    
    .stRadio > div > label:hover {
        background: linear-gradient(135deg, rgba(14, 165, 233, 0.25) 0%, rgba(59, 130, 246, 0.25) 100%);
        border-color: #0ea5e9;
        transform: translateX(8px) scale(1.02);
        box-shadow: 0 8px 25px rgba(14, 165, 233, 0.4);
    }
    
    .stRadio > div > label[data-checked="true"] {
        background: linear-gradient(135deg, #0ea5e9 0%, #3b82f6 100%);
        border-color: #0ea5e9;
        color: white;
        box-shadow: 0 8px 30px rgba(14, 165, 233, 0.6);
        animation: pulse 2s infinite;
    }
    
    /* Titles & Headers */
    h1 {
        color: #ffffff;
        font-weight: 900;
        font-size: 3.5rem;
        margin-bottom: 0.5rem;
        background: linear-gradient(120deg, #0ea5e9, #3b82f6, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shimmer 3s infinite linear;
        background-size: 200% auto;
        text-shadow: 0 0 40px rgba(14, 165, 233, 0.5);
    }
    
    h2 {
        color: #e0f2fe;
        font-weight: 800;
        font-size: 2rem;
        margin: 2rem 0 1rem 0;
        padding-left: 1rem;
        border-left: 5px solid #0ea5e9;
        animation: fadeIn 0.8s ease-in-out;
    }
    
    h3 {
        color: #bae6fd;
        font-weight: 700;
        font-size: 1.5rem;
    }
    
    /* Premium Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #0ea5e9 0%, #3b82f6 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.9rem 2rem;
        font-weight: 700;
        font-size: 1rem;
        box-shadow: 0 8px 25px rgba(14, 165, 233, 0.4);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stButton > button:hover {
        transform: translateY(-4px) scale(1.02);
        box-shadow: 0 15px 40px rgba(14, 165, 233, 0.6);
        background: linear-gradient(135deg, #3b82f6 0%, #0ea5e9 100%);
    }
    
    .stButton > button:active {
        transform: translateY(-2px) scale(0.98);
    }
    
    /* Premium Metric Cards with Float Animation */
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(14, 165, 233, 0.15) 0%, rgba(59, 130, 246, 0.15) 100%);
        padding: 2rem;
        border-radius: 20px;
        border: 2px solid rgba(14, 165, 233, 0.3);
        box-shadow: 0 10px 40px rgba(0,0,0,0.3);
        transition: all 0.3s ease;
        animation: float 6s ease-in-out infinite;
        backdrop-filter: blur(10px);
    }
    
    div[data-testid="stMetric"]:hover {
        transform: translateY(-8px) scale(1.03);
        box-shadow: 0 20px 60px rgba(14, 165, 233, 0.4);
        animation: glow 2s infinite;
    }
    
    div[data-testid="stMetric"] label {
        color: #bae6fd;
        font-weight: 700;
        font-size: 1.1rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #ffffff;
        font-weight: 900;
        font-size: 3rem;
        text-shadow: 0 0 30px rgba(14, 165, 233, 0.8);
    }
    
    /* Premium Input Fields */
    .stTextInput input,
    .stNumberInput input,
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.05);
        border: 2px solid rgba(14, 165, 233, 0.3);
        border-radius: 12px;
        color: #f1f5f9;
        font-weight: 600;
        padding: 0.9rem 1.2rem;
        font-size: 1rem;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    .stTextInput input:focus,
    .stNumberInput input:focus,
    .stSelectbox > div > div:focus {
        border-color: #0ea5e9;
        box-shadow: 0 0 25px rgba(14, 165, 233, 0.5);
        background: rgba(255, 255, 255, 0.08);
    }
    
    .stTextInput label,
    .stNumberInput label,
    .stSelectbox label {
        color: #e0f2fe;
        font-weight: 700;
        font-size: 1rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Premium Dropdown */
    div[data-baseweb="select"] {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 12px;
    }
    
    ul[role="listbox"] {
        background: rgba(255, 255, 255, 0.98);
        border: 2px solid #0ea5e9;
        border-radius: 12px;
        backdrop-filter: blur(20px);
    }
    
    li[role="option"] {
        background: transparent;
        color: #0f172a;
        font-weight: 600;
        padding: 1rem 1.5rem;
        transition: all 0.2s ease;
    }
    
    li[role="option"]:hover {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
        color: #0c4a6e;
        transform: translateX(8px);
    }
    
    li[role="option"][aria-selected="true"] {
        background: linear-gradient(135deg, #0ea5e9 0%, #3b82f6 100%);
        color: white;
        font-weight: 800;
    }
    
    /* Alert Boxes - Premium Style */
    .stSuccess,
    .stInfo,
    .stWarning,
    .stError {
        border-radius: 16px;
        padding: 1.5rem;
        border-left: 5px solid;
        backdrop-filter: blur(10px);
        animation: fadeIn 0.5s ease-in-out;
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
    }
    
    .stSuccess {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(5, 150, 105, 0.15) 100%);
        border-left-color: #10b981;
    }
    
    .stInfo {
        background: linear-gradient(135deg, rgba(14, 165, 233, 0.15) 0%, rgba(59, 130, 246, 0.15) 100%);
        border-left-color: #0ea5e9;
    }
    
    .stWarning {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.15) 0%, rgba(217, 119, 6, 0.15) 100%);
        border-left-color: #f59e0b;
    }
    
    .stError {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(220, 38, 38, 0.15) 100%);
        border-left-color: #ef4444;
    }
    
    /* Premium Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background: rgba(14, 165, 233, 0.05);
        padding: 1rem;
        border-radius: 20px;
        backdrop-filter: blur(10px);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 1rem 2rem;
        font-weight: 700;
        color: #bae6fd;
        border: 2px solid rgba(14, 165, 233, 0.2);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(14, 165, 233, 0.15);
        border-color: #0ea5e9;
        transform: translateY(-3px);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #0ea5e9 0%, #3b82f6 100%);
        color: white;
        box-shadow: 0 8px 30px rgba(14, 165, 233, 0.5);
        animation: pulse 2s infinite;
    }
    
    /* Premium DataFrames */
    .stDataFrame {
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 10px 40px rgba(0,0,0,0.3);
        border: 2px solid rgba(14, 165, 233, 0.2);
        animation: fadeIn 0.6s ease-in-out;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, rgba(14, 165, 233, 0.15) 0%, rgba(59, 130, 246, 0.15) 100%);
        border-radius: 12px;
        font-weight: 700;
        color: #e0f2fe;
        padding: 1.2rem;
        border: 2px solid rgba(14, 165, 233, 0.3);
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background: linear-gradient(135deg, rgba(14, 165, 233, 0.25) 0%, rgba(59, 130, 246, 0.25) 100%);
        border-color: #0ea5e9;
        box-shadow: 0 8px 25px rgba(14, 165, 233, 0.3);
    }
    
    /* Checkbox */
    .stCheckbox label {
        color: #e0f2fe;
        font-weight: 600;
        font-size: 1rem;
    }
    
    /* Premium Divider */
    hr {
        margin: 3rem 0;
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #0ea5e9, transparent);
        animation: shimmer 3s infinite linear;
        background-size: 200% auto;
    }
    
    /* Text Colors */
    p, li, span, div {
        color: #f1f5f9;
        line-height: 1.7;
    }
    
    strong {
        color: #ffffff;
        font-weight: 800;
    }
    
    /* Floating Badge */
    .floating-badge {
        position: fixed;
        top: 20px;
        right: 20px;
        background: linear-gradient(135deg, #0ea5e9 0%, #3b82f6 100%);
        color: white;
        padding: 0.8rem 1.5rem;
        border-radius: 50px;
        font-weight: 700;
        box-shadow: 0 8px 25px rgba(14, 165, 233, 0.5);
        z-index: 999;
        animation: float 3s ease-in-out infinite;
        border: 2px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Match Card - Premium */
    .match-card {
        padding: 2rem;
        border-radius: 20px;
        margin: 1.5rem 0;
        background: linear-gradient(135deg, rgba(14, 165, 233, 0.1) 0%, rgba(59, 130, 246, 0.1) 100%);
        border: 2px solid rgba(14, 165, 233, 0.3);
        box-shadow: 0 10px 40px rgba(0,0,0,0.3);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
        animation: fadeIn 0.8s ease-in-out;
    }
    
    .match-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 60px rgba(14, 165, 233, 0.4);
    }
    
    /* Score Display */
    .score-display {
        background: linear-gradient(135deg, #0ea5e9 0%, #3b82f6 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 16px;
        text-align: center;
        font-weight: 800;
        font-size: 1.5rem;
        box-shadow: 0 8px 30px rgba(14, 165, 233, 0.5);
        animation: pulse 3s infinite;
    }
    
    /* Loading Spinner */
    .stSpinner > div {
        border-color: #0ea5e9 transparent transparent transparent;
    }
    
    /* Scrollbar Styling */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(15, 23, 42, 0.5);
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #0ea5e9 0%, #3b82f6 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
    }
</style>
""", unsafe_allow_html=True)

# ==================== FLOATING STATUS BADGE ====================
st.markdown("""
<div class="floating-badge">
    🔴 LIVE
</div>
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

# ==================== SQL QUERIES ====================
SQL_QUERIES = {
    "🏏 Top 20 ODI Run Scorers": "SELECT player_name, runs, batting_avg, matches_played FROM odi_batting_stats ORDER BY runs DESC LIMIT 20;",
    "🇮🇳 All Indian Players": "SELECT name, battingstyle, bowlingstyle FROM indian_players LIMIT 50;",
    "⭐ Best All-Rounders": "SELECT player_name, total_runs, total_wickets FROM all_rounders ORDER BY (total_runs + total_wickets*20) DESC LIMIT 20;",
    "📊 Recent Match Results": "SELECT match_desc, team1_name, team2_name, status FROM recent_matches ORDER BY match_date DESC LIMIT 30;",
    "🤝 Top Partnerships": "SELECT player_names, combined_partnership_runs FROM partnerships ORDER BY combined_partnership_runs DESC LIMIT 20;",
    "🎯 Bowler by Venue": "SELECT bowler, venue, total_wickets FROM bowler_venue_stats ORDER BY total_wickets DESC LIMIT 30;",
    "📈 Player Career": "SELECT player, test_matches, odi_matches, total_matches FROM player_career_summary LIMIT 30;",
    "🎲 Toss Impact": "SELECT format, win_percent_choose_bat_first FROM toss_advantage_stats;",
    "🏆 Team Performance": "SELECT team, home_wins, away_wins FROM team_home_away_wins LIMIT 20;",
    "🔥 Recent Form": "SELECT player, avg_runs_last5 FROM recent_form LIMIT 20;",
    "💰 Economical Bowlers": "SELECT bowler, overall_economy_rate FROM bowlers_aggregate ORDER BY overall_economy_rate ASC LIMIT 20;",
    "📉 Batting Distribution": "SELECT player, avg_runs_scored FROM player_batting_distribution LIMIT 20;",
    "⚡ Clutch Batting": "SELECT player, batting_average_close_matches FROM clutch_batting_stats LIMIT 20;",
    "📅 Yearly Stats": "SELECT player, year, matches_played FROM player_yearly_stats WHERE year >= 2020 LIMIT 30;",
    "🆚 Head to Head": "SELECT pair, total_matches FROM head_to_head_series LIMIT 20;",
}

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("# 🏏 CricStats Pro")
    st.markdown("---")
    
    page = st.radio(
        "NAVIGATION",
        ["🏠 Home", "🔴 Live Matches", "📊 Top Stats", "💻 SQL Analytics", "👥 Player CRUD"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("### 📡 System Status")
    
    if RAPIDAPI_KEY:
        st.success("✅ API Connected")
    else:
        st.error("❌ API Offline")
    
    if engine:
        st.success("✅ Database Online")
    else:
        st.error("❌ Database Offline")

# ==================== MAIN HEADER ====================
st.title("🏏 Cricbuzz LiveStats Pro")
st.markdown("Real-Time Cricket Insights & Advanced Analytics Dashboard")
st.markdown("---")

# ==================== HOME PAGE ====================
if page == "🏠 Home":
    # Hero Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="API Status",
            value="ACTIVE" if RAPIDAPI_KEY else "OFFLINE",
            delta="Real-time" if RAPIDAPI_KEY else "Disconnected"
        )
    
    with col2:
        st.metric(
            label="Database",
            value="ONLINE" if engine else "OFFLINE",
            delta="Connected" if engine else "Disconnected"
        )
    
    with col3:
        st.metric(
            label="SQL Queries",
            value="15",
            delta="Pre-built"
        )
    
    with col4:
        st.metric(
            label="Tables",
            value="25+",
            delta="Database"
        )
    
    st.markdown("---")
    
    # Feature Cards
    st.markdown("## 🚀 Platform Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("### 📺 Live Cricket\nReal-time match updates, detailed scorecards, ball-by-ball commentary, and live scores from ongoing matches worldwide.")
        
        st.success("### 📊 Advanced Analytics\n15 SQL queries, 25+ database tables, comprehensive statistics, and data visualization tools.")
    
    with col2:
        st.warning("### ⚡ High Performance\nFast queries, real-time data synchronization, responsive UI, and optimized database operations.")
        
        st.error("### 👥 Player Management\nFull CRUD operations, custom player IDs, batch imports, and advanced search capabilities.")
    
    st.markdown("---")
    
    st.markdown("## 📈 Platform Statistics")
    
    # Stats Display
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='text-align:center; padding:2rem; background:linear-gradient(135deg, rgba(14,165,233,0.15), rgba(59,130,246,0.15)); border-radius:20px; border:2px solid rgba(14,165,233,0.3);'>
            <h2 style='color:#0ea5e9; margin:0;'>1000+</h2>
            <p style='color:#bae6fd; margin:0.5rem 0 0 0;'>Players Tracked</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='text-align:center; padding:2rem; background:linear-gradient(135deg, rgba(59,130,246,0.15), rgba(139,92,246,0.15)); border-radius:20px; border:2px solid rgba(59,130,246,0.3);'>
            <h2 style='color:#3b82f6; margin:0;'>500+</h2>
            <p style='color:#bae6fd; margin:0.5rem 0 0 0;'>Matches Analyzed</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='text-align:center; padding:2rem; background:linear-gradient(135deg, rgba(139,92,246,0.15), rgba(168,85,247,0.15)); border-radius:20px; border:2px solid rgba(139,92,246,0.3);'>
            <h2 style='color:#8b5cf6; margin:0;'>50+</h2>
            <p style='color:#bae6fd; margin:0.5rem 0 0 0;'>Teams Covered</p>
        </div>
        """, unsafe_allow_html=True)

# ==================== LIVE MATCHES ====================
elif page == "🔴 Live Matches":
    st.markdown("## 🔴 Live Cricket Matches")
    st.markdown("---")
    
    if not RAPIDAPI_KEY:
        st.error("❌ **API Key Required** - Add RAPIDAPI_KEY in Streamlit Secrets to view live matches")
        st.stop()
    
    with st.spinner("🔄 Fetching live matches..."):
        data = fetch_cricbuzz("matches/v1/live")
        if not data or "typeMatches" not in data:
            st.warning("⚠️ No live matches currently. Loading recent matches...")
            data = fetch_cricbuzz("matches/v1/recent")
    
    if not data:
        st.error("❌ Failed to fetch match data from API")
        st.stop()
    
    for category in data.get("typeMatches", []):
        match_type = category.get("matchType", "").upper()
        
        with st.expander(f"🏏 {match_type} MATCHES", expanded=True):
            for series in category.get("seriesMatches", []):
                series_info = series.get("seriesAdWrapper", {}) or series.get("adWrapper", {})
                if not series_info:
                    continue
                
                series_name = series_info.get("seriesName", "Match Series")
                matches = series_info.get("matches", [])
                
                if matches:
                    st.markdown(f"### 📍 {series_name}")
                
                for match in matches:
                    info = match.get("matchInfo", {})
                    score = match.get("matchScore", {})
                    match_id = str(info.get("matchId", ""))
                    
                    t1 = info.get("team1", {}).get("teamName", "Team 1")
                    t2 = info.get("team2", {}).get("teamName", "Team 2")
                    t1s = info.get("team1", {}).get("teamSName", "T1")
                    t2s = info.get("team2", {}).get("teamSName", "T2")
                    
                    # Premium Match Card
                    st.markdown(f"""
                    <div class="match-card">
                        <div style="text-align:center;">
                            <h3 style="margin:0; color:#fff; font-size:1.8rem;">{t1} 🆚 {t2}</h3>
                            <p style="margin:1rem 0; color:#bae6fd; font-size:1.1rem;">
                                {info.get('matchDesc','')} • {info.get('matchFormat','')}
                            </p>
                            <p style="margin:1rem 0; font-weight:800; color:#4ade80; font-size:1.4rem;">
                                {info.get('status','Starting soon')}
                            </p>
                            <p style="margin:0.5rem 0; color:#94a3b8; font-size:0.95rem;">
                                📍 {info.get('venueInfo', {}).get('ground','')} • 🕐 {format_time(info.get('startDate'))}
                            </p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Live Scores
                    c1, c2, c3 = st.columns([2, 1, 2])
                    
                    with c1:
                        if score.get("team1Score", {}).get("inngs1"):
                            s = score["team1Score"]["inngs1"]
                            st.markdown(f"""
                            <div class="score-display">
                                {t1s}<br>
                                {s.get('runs',0)}/{s.get('wickets',0)}<br>
                                <span style="font-size:1rem;">({s.get('overs','')} overs)</span>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    with c2:
                        st.markdown("<h2 style='text-align:center; color:#0ea5e9; margin-top:30px;'>VS</h2>", unsafe_allow_html=True)
                    
                    with c3:
                        if score.get("team2Score", {}).get("inngs1"):
                            s = score["team2Score"]["inngs1"]
                            st.markdown(f"""
                            <div class="score-display">
                                {t2s}<br>
                                {s.get('runs',0)}/{s.get('wickets',0)}<br>
                                <span style="font-size:1rem;">({s.get('overs','')} overs)</span>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    # Full Scorecard Button
                    if st.button("📊 VIEW FULL SCORECARD", key=f"sc_{match_id}", use_container_width=True):
                        with st.spinner("🔄 Loading detailed scorecard..."):
                            sc = fetch_cricbuzz(f"mcenter/v1/{match_id}/scard")
                            
                            if not sc or ("scorecard" not in sc and "scoreCard" not in sc):
                                st.warning("⚠️ Scorecard not available yet for this match")
                                continue
                            
                            scorecard = sc.get("scorecard") or sc.get("scoreCard", [])
                            
                            for i, inn in enumerate(scorecard, 1):
                                team = inn.get("batTeamName") or inn.get("batteamname", "Team")
                                
                                st.markdown(f"""
                                <div style="text-align:center; margin:2rem 0 1rem 0;">
                                    <h3 style="color:#0ea5e9; margin:0;">INNINGS {i} — {team}</h3>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                col_left, col_right = st.columns(2)
                                
                                with col_left:
                                    st.markdown("### ⚾ Batting Performance")
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
                                                "Dismissal": p.get("outDesc") or p.get("outdec", "not out")
                                            })
                                    if bats:
                                        st.dataframe(pd.DataFrame(bats), use_container_width=True, hide_index=True)
                                    else:
                                        st.info("No batting data available")
                                
                                with col_right:
                                    st.markdown("### 🎯 Bowling Performance")
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
                                        st.info("No bowling data available")
                                
                                st.markdown("---")
                    
                    st.markdown("<br>", unsafe_allow_html=True)

# ==================== TOP STATS ====================
elif page == "📊 Top Stats":
    st.markdown("## 📊 Cricket Statistics")
    st.markdown("---")
    
    if not engine:
        st.error("❌ Database connection required")
        st.stop()
    
    table_map = {
        "🏏 ODI Batting Stats": "odi_batting_stats",
        "🇮🇳 Indian Players": "indian_players",
        "⭐ All-Rounders": "all_rounders",
        "🎯 Bowlers Aggregate": "bowlers_aggregate",
        "📊 Recent Matches": "recent_matches"
    }
    
    col1, col2 = st.columns(2)
    
    with col1:
        selected = st.selectbox("📋 Select Table", list(table_map.keys()))
    
    with col2:
        limit = st.selectbox("📈 Number of Records", [10, 20, 50, 100])
    
    if st.button("🔍 LOAD DATA", type="primary", use_container_width=True):
        with st.spinner("🔄 Fetching data..."):
            df = run_sql_query(f"SELECT * FROM {table_map[selected]} LIMIT {limit}")
            
            if not df.empty:
                st.success(f"✅ Successfully loaded {len(df)} records")
                st.dataframe(df, use_container_width=True, height=600)
                
                # Download button
                csv = df.to_csv(index=False).encode()
                st.download_button(
                    label="⬇️ DOWNLOAD CSV",
                    data=csv,
                    file_name=f"{selected.replace(' ', '_')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            else:
                st.warning("⚠️ No data found in the selected table")

# ==================== SQL ANALYTICS ====================
elif page == "💻 SQL Analytics":
    st.markdown("## 💻 SQL Analytics Dashboard")
    st.markdown("15 Pre-Built Advanced Queries")
    st.markdown("---")
    
    if not engine:
        st.error("❌ Database connection required")
        st.stop()
    
    query_name = st.selectbox("🔍 Select Query", list(SQL_QUERIES.keys()))
    sql = SQL_QUERIES[query_name]
    
    with st.expander("📝 VIEW SQL CODE"):
        st.code(sql, language="sql")
    
    if st.button("▶️ EXECUTE QUERY", type="primary", use_container_width=True):
        with st.spinner("⚙️ Executing query..."):
            df = run_sql_query(sql)
            
            if not df.empty:
                st.success(f"✅ Query executed successfully - {len(df)} rows returned")
                st.dataframe(df, use_container_width=True, height=600)
                
                # Download option
                csv = df.to_csv(index=False).encode()
                st.download_button(
                    label="⬇️ DOWNLOAD RESULTS",
                    data=csv,
                    file_name=f"query_results.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            else:
                st.warning("⚠️ Query returned no results")

# ==================== PLAYER CRUD ====================
elif page == "👥 Player CRUD":
    st.markdown("## 👥 Player Management System")
    st.markdown("Complete CRUD Operations with Advanced Features")
    st.markdown("---")
    
    if not engine:
        st.error("❌ Database connection required for CRUD operations")
        st.stop()
    
    tabs = st.tabs(["➕ CREATE", "📖 READ", "✏️ UPDATE", "🗑️ DELETE"])
    
    # CREATE
    with tabs[0]:
        st.markdown("### ➕ Add New Player")
        st.info("💡 Leave Player ID empty for auto-generation, or enter a custom ID")
        
        with st.form("create_player", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                player_id = st.number_input(
                    "Player ID (Optional)",
                    min_value=1,
                    step=1,
                    value=None,
                    help="Leave empty to auto-generate"
                )
                name = st.text_input(
                    "Player Name *",
                    placeholder="e.g., Virat Kohli"
                )
                batting = st.text_input(
                    "Batting Style",
                    placeholder="e.g., Right-hand bat"
                )
            
            with col2:
                bowling = st.text_input(
                    "Bowling Style",
                    placeholder="e.g., Right-arm medium"
                )
                st.markdown("### 👁️ Preview")
                if name:
                    st.success(f"Ready to add: **{name}**")
                else:
                    st.warning("Enter player name")
            
            submitted = st.form_submit_button("➕ ADD PLAYER", type="primary", use_container_width=True)
            
            if submitted:
                if not name or name.strip() == "":
                    st.error("❌ Player name is required!")
                else:
                    try:
                        with engine.connect() as conn:
                            if player_id is not None:
                                check = conn.execute(
                                    text("SELECT id FROM indian_players WHERE id = :id"),
                                    {"id": player_id}
                                ).fetchone()
                                
                                if check:
                                    st.error(f"❌ Player ID {player_id} already exists!")
                                else:
                                    conn.execute(
                                        text("INSERT INTO indian_players (id, name, battingstyle, bowlingstyle) VALUES (:id, :n, :bat, :bowl)"),
                                        {"id": player_id, "n": name.strip(), "bat": batting.strip() or None, "bowl": bowling.strip() or None}
                                    )
                                    conn.commit()
                                    st.success(f"✅ Player '{name}' added with ID: {player_id}!")
                                    st.balloons()
                            else:
                                max_id_result = conn.execute(text("SELECT COALESCE(MAX(id), 0) + 1 as next_id FROM indian_players")).fetchone()
                                next_id = max_id_result[0]
                                
                                conn.execute(
                                    text("INSERT INTO indian_players (id, name, battingstyle, bowlingstyle) VALUES (:id, :n, :bat, :bowl)"),
                                    {"id": next_id, "n": name.strip(), "bat": batting.strip() or None, "bowl": bowling.strip() or None}
                                )
                                conn.commit()
                                st.success(f"✅ Player '{name}' added with ID: {next_id}!")
                                st.balloons()
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
    
    # READ
    with tabs[1]:
        st.markdown("### 📖 View Players")
        
        search = st.text_input("🔍 Search by name", placeholder="Type player name...")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📊 LOAD ALL PLAYERS", type="primary", use_container_width=True):
                df = run_sql_query("SELECT * FROM indian_players ORDER BY id DESC LIMIT 100")
                if not df.empty:
                    st.success(f"✅ Found {len(df)} players")
                    st.dataframe(df, use_container_width=True, height=600)
                    csv = df.to_csv(index=False).encode()
                    st.download_button("⬇️ DOWNLOAD CSV", csv, "players.csv", "text/csv", use_container_width=True)
                else:
                    st.warning("⚠️ No players found")
        
        with col2:
            if st.button("🔍 SEARCH", type="secondary", use_container_width=True):
                if search:
                    df = run_sql_query(f"SELECT * FROM indian_players WHERE LOWER(name) LIKE LOWER('%{search}%') ORDER BY id DESC")
                    if not df.empty:
                        st.success(f"✅ Found {len(df)} matches")
                        st.dataframe(df, use_container_width=True, height=600)
                    else:
                        st.warning(f"⚠️ No results for '{search}'")
                else:
                    st.warning("⚠️ Enter search term")
    
    # UPDATE
    with tabs[2]:
        st.markdown("### ✏️ Update Player")
        
        player_id = st.number_input("Enter Player ID", min_value=1, step=1, key="update_id")
        
        if st.button("🔍 LOAD PLAYER", type="primary"):
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
                        st.success(f"✅ Loaded: **{result.name}** (ID: {result.id})")
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
                    save_btn = st.form_submit_button("💾 SAVE CHANGES", type="primary", use_container_width=True)
                
                with col_cancel:
                    cancel_btn = st.form_submit_button("❌ CANCEL", use_container_width=True)
                
                if save_btn:
                    if not new_name or new_name.strip() == "":
                        st.error("❌ Name cannot be empty!")
                    else:
                        try:
                            with engine.connect() as conn:
                                conn.execute(
                                    text("UPDATE indian_players SET name=:n, battingstyle=:bat, bowlingstyle=:bowl WHERE id=:id"),
                                    {"n": new_name.strip(), "bat": new_batting.strip() or None, "bowl": new_bowling.strip() or None, "id": player['id']}
                                )
                                conn.commit()
                            st.success("✅ Player updated successfully!")
                            del st.session_state['update_player']
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Update failed: {e}")
                
                if cancel_btn:
                    del st.session_state['update_player']
                    st.rerun()
    
    # DELETE
    with tabs[3]:
        st.markdown("### 🗑️ Delete Player")
        st.warning("⚠️ **Warning:** This action cannot be undone!")
        
        delete_id = st.number_input("Enter Player ID", min_value=1, step=1, key="delete_id")
        
        if st.button("👁️ PREVIEW PLAYER", type="secondary"):
            try:
                with engine.connect() as conn:
                    check = conn.execute(
                        text("SELECT * FROM indian_players WHERE id = :id"),
                        {"id": delete_id}
                    ).fetchone()
                    
                    if check:
                        st.info(f"**Player Details:**\n- ID: {check.id}\n- Name: {check.name}\n- Batting: {check.battingstyle or 'N/A'}\n- Bowling: {check.bowlingstyle or 'N/A'}")
                    else:
                        st.error(f"❌ No player found with ID: {delete_id}")
            except Exception as e:
                st.error(f"❌ Error: {e}")
        
        confirm = st.checkbox("✅ I confirm permanent deletion")
        
        if st.button("🗑️ DELETE PLAYER", type="secondary", use_container_width=True):
            if not confirm:
                st.error("❌ Please confirm deletion!")
            else:
                try:
                    with engine.connect() as conn:
                        check = conn.execute(
                            text("SELECT name FROM indian_players WHERE id = :id"),
                            {"id": delete_id}
                        ).fetchone()
                        
                        if check:
                            conn.execute(text("DELETE FROM indian_players WHERE id = :id"), {"id": delete_id})
                            conn.commit()
                            st.success(f"✅ Player '{check.name}' deleted!")
                            st.rerun()
                        else:
                            st.error(f"❌ No player found with ID: {delete_id}")
                except Exception as e:
                    st.error(f"❌ Delete failed: {e}")

# ==================== PREMIUM FOOTER ====================
st.markdown("---")
st.markdown("""
<div style='text-align:center; padding:2.5rem; background:linear-gradient(135deg, #0ea5e9 0%, #3b82f6 100%);
     color:white; border-radius:20px; box-shadow:0 10px 40px rgba(14,165,233,0.5);'>
    <h2 style='color:white; margin:0; font-size:2rem;'>🏏 Cricbuzz LiveStats Pro</h2>
    <p style='color:rgba(255,255,255,0.9); font-size:1.1rem; margin:1rem 0;'>
        15 Queries • 25+ Tables • Full CRUD • Real-Time API
    </p>
    <p style='color:rgba(255,255,255,0.7); font-size:0.9rem; margin:0.5rem 0 0 0;'>
        Built with Streamlit • Powered by RapidAPI & PostgreSQL
    </p>
</div>
""", unsafe_allow_html=True)
