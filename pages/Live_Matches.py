import streamlit as st
import pandas as pd
from utils import fetch_cricbuzz, format_time

st.header("Live Cricket Matches")
st.markdown("---")

data = fetch_cricbuzz("matches/v1/live")
if not data or "typeMatches" not in data:
    st.warning("No live matches. Showing recent...")
    data = fetch_cricbuzz("matches/v1/recent")

if not data:
    st.error("Failed to fetch matches")
    st.stop()

for category in data.get("typeMatches", []):
    match_type = category.get("matchType", "").upper()
    with st.expander(f"{match_type} Matches", expanded=True):
        for series in category.get("seriesMatches", []):
            series_info = series.get("seriesAdWrapper", {}) or series.get("adWrapper", {})
            if not series_info: continue
            series_name = series_info.get("seriesName", "Match")
            matches = series_info.get("matches", [])
            if matches:
                st.subheader(f"{series_name}")

            for match in matches:
                info = match.get("matchInfo", {})
                score = match.get("matchScore", {})
                match_id = str(info.get("matchId", ""))

                t1 = info.get("team1", {}).get("teamName", "Team 1")
                t2 = info.get("team2", {}).get("teamName", "Team 2")
                t1s = info.get("team1", {}).get("teamSName", "T1")
                t2s = info.get("team2", {}).get("teamSName", "T2")

                st.markdown(f"""<div style="text-align:center; padding:20px; background:linear-gradient(135deg,#0ea5e9,#2563eb); border-radius:15px; color:white; margin:20px 0;">
                    <h3 style="margin:0;">{t1} vs {t2}</h3>
                    <p style="margin:8px 0; font-size:1.1rem;">{info.get('matchDesc','')} • {info.get('matchFormat','')}</p>
                    <p style="margin:8px 0; font-weight:bold; color:#86efac; font-size:1.3rem;">{info.get('status','Starting soon')}</p>
                    <p style="margin:5px 0; font-size:0.95rem;">Venue: {info.get('venueInfo', {}).get('ground','')} • Start: {format_time(info.get('startDate'))}</p>
                </div>""", unsafe_allow_html=True)

                c1, c2, c3 = st.columns([2, 2, 2])
                with c1:
                    if score.get("team1Score", {}).get("inngs1"):
                        s = score["team1Score"]["inngs1"]
                        st.markdown(f"<div style='text-align:center; background:#0ea5e9; color:white; padding:15px; border-radius:12px; font-weight:bold;'>{t1s}<br>{s.get('runs',0)}/{s.get('wickets',0)} ({s.get('overs','')})</div>", unsafe_allow_html=True)
                with c2:
                    st.markdown("<h2 style='text-align:center; color:#0ea5e9; margin-top:20px;'>VS</h2>", unsafe_allow_html=True)
                with c3:
                    if score.get("team2Score", {}).get("inngs1"):
                        s = score["team2Score"]["inngs1"]
                        st.markdown(f"<div style='text-align:center; background:#0ea5e9; color:white; padding:15px; border-radius:12px; font-weight:bold;'>{t2s}<br>{s.get('runs',0)}/{s.get('wickets',0)} ({s.get('overs','')})</div>", unsafe_allow_html=True)

                if st.button("Full Scorecard", key=f"sc_{match_id}", use_container_width=True):
                    with st.spinner("Loading scorecard..."):
                        sc = fetch_cricbuzz(f"mcenter/v1/{match_id}/scard")
                        if not sc or ("scorecard" not in sc and "scoreCard" not in sc):
                            st.warning("Scorecard not available yet")
                            continue

                        scorecard = sc.get("scorecard") or sc.get("scoreCard", [])
                        for i, inn in enumerate(scorecard, 1):
                            team = inn.get("batTeamName") or inn.get("batteamname", "Team")

                            # Centered header with just the team name
                            st.markdown(f"""
                            <div style="text-align:center; margin:30px 0 20px 0;">
                                <h3 style="color:#0ea5e9; margin:0;">{team}</h3>
                            </div>
                            """, unsafe_allow_html=True)

                            # Batting Data
                            bats_data = inn.get("batsmenData") or inn.get("batsman") or {}
                            if isinstance(bats_data, dict):
                                bats_iter = bats_data.values()
                            else:
                                bats_iter = bats_data
                            bats = [
                                {
                                    "Batsman": p.get("batName") or p.get("name", "—"),
                                    "R": p.get("runs", 0),
                                    "B": p.get("balls", 0),
                                    "4s": p.get("fours", 0),
                                    "6s": p.get("sixes", 0),
                                    "SR": p.get("strikeRate") or p.get("strkrate", "0"),
                                    "Out": p.get("outDesc") or p.get("outdec", "not out"),
                                }
                                for p in bats_iter
                            ]

                            # Bowling Data
                            bowl_data = inn.get("bowlersData") or inn.get("bowler") or {}
                            if isinstance(bowl_data, dict):
                                bowl_iter = bowl_data.values()
                            else:
                                bowl_iter = bowl_data
                            bowls = [
                                {
                                    "Bowler": p.get("bowlName") or p.get("name", "—"),
                                    "O": p.get("overs", "0"),
                                    "M": p.get("maidens", 0),
                                    "R": p.get("runs", 0),
                                    "W": p.get("wickets", 0),
                                    "Econ": p.get("economy") or "0.0",
                                }
                                for p in bowl_iter
                            ]

                            # Centered two columns
                            sc_col1, sc_col2 = st.columns(2)
                            sc_col1.write(f"Batting ({team})")
                            if bats:
                                sc_col1.dataframe(pd.DataFrame(bats), use_container_width=True, hide_index=True)
                            else:
                                sc_col1.info("No batting data")
                            sc_col2.write(f"Bowling ({team})")
                            if bowls:
                                sc_col2.dataframe(pd.DataFrame(bowls), use_container_width=True, hide_index=True)
                            else:
                                sc_col2.info("No bowling data")
                        st.markdown("---")

                st.markdown("<hr style='border:2px solid #0ea5e9; margin:50px 0;'>", unsafe_allow_html=True)
