import streamlit as st
import requests
import pandas as pd
from sqlalchemy import create_engine, text
from datetime import datetime
import os

def load_css():
    st.markdown(open("styles.css").read(), unsafe_allow_html=True)

def format_time(ms):
    if not ms: return "N/A"
    try:
        return datetime.fromtimestamp(int(ms)/1000).strftime("%d %b %Y, %I:%M %p")
    except:
        return "N/A"

DATABASE_URL = st.secrets.get("DATABASE_URL") or os.environ.get("DATABASE_URL")
RAPIDAPI_KEY = st.secrets.get("RAPIDAPI_KEY") or os.environ.get("RAPIDAPI_KEY")
engine = create_engine(DATABASE_URL) if DATABASE_URL else None

def fetch_cricbuzz(endpoint):
    if not RAPIDAPI_KEY: return None
    try:
        r = requests.get(
            f"https://cricbuzz-cricket.p.rapidapi.com/{endpoint}",
            headers={
                "X-RapidAPI-Key": RAPIDAPI_KEY,
                "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com"
            },
            timeout=15)
        return r.json() if r.status_code == 200 else None
    except:
        return None

def run_sql_query(sql):
    if not engine: return pd.DataFrame()
    try:
        with engine.connect() as conn:
            return pd.read_sql_query(text(sql), conn)
    except Exception as e:
        st.error(f"SQL Error: {e}")
        return pd.DataFrame()
