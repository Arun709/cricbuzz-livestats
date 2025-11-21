import streamlit as st
from utils import SQL_QUERIES, run_sql_query

st.header("SQL Analytics")
st.markdown("25 Pre-Built Queries")
st.markdown("---")
query_name = st.selectbox("Select Query", list(SQL_QUERIES.keys()))
sql = SQL_QUERIES[query_name]
with st.expander("SQL Code"):
    st.code(sql, language="sql")
if st.button("Execute", type="primary"):
    df = run_sql_query(sql)
    if not df.empty:
        st.success(f"{len(df)} rows")
        st.dataframe(df, use_container_width=True, height=600)
