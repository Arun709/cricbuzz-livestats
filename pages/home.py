import streamlit as st
from utils import load_css

st.set_page_config(page_title="Cricbuzz LiveStats", page_icon="🏏", layout="wide", initial_sidebar_state="expanded")
load_css()

st.sidebar.title("Navigation")
st.sidebar.markdown("---")
st.sidebar.success("API")
st.sidebar.success("DB")

st.markdown("---")
st.markdown("""
<div style='text-align:center; padding:30px; background:linear-gradient(135deg, #0ea5e9, #2563eb);
     color:white; border-radius:15px;'>
    <h2 style='color:white !important;'>Cricbuzz LiveStats</h2>
    <p style='color:white !important;'>25 Queries • 25+ Tables • Full CRUD • Real-Time API</p>
</div>
""", unsafe_allow_html=True)
