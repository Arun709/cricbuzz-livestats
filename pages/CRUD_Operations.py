import streamlit as st
from utils import run_sql_query, engine
from sqlalchemy import text

st.header("Player Management - Full CRUD Operations")
st.markdown("Create • Read • Update • Delete")
st.markdown("---")
tabs = st.tabs(["CREATE", "READ", "UPDATE", "DELETE"])


