import streamlit as st
from utils import run_sql_query, engine

st.header("Top Statistics")
st.markdown("---")
table_map = {
    "ODI Batting Stats": "odi_batting_stats",
    "Indian Players": "indian_players",
    "All-Rounders": "all_rounders",
    "Bowlers Aggregate": "bowlers_aggregate",
    "Recent Matches": "recent_matches"
}
col1, col2 = st.columns(2)
with col1:
    selected = st.selectbox("Select Table", list(table_map.keys()))
with col2:
    limit = st.selectbox("Records", [10, 20, 50, 100])
if engine and st.button("Load", type="primary"):
    df = run_sql_query(f"SELECT * FROM {table_map[selected]} LIMIT {limit}")
    if not df.empty:
        st.success(f"{len(df)} records")
        st.dataframe(df, use_container_width=True, height=600)
