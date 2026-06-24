# ==========================================================
# SIDEBAR
# ==========================================================
import streamlit as st

def show_sidebar():
    with st.sidebar: st.markdown("""
    <h1 style='text-align:center;color:#FFD700;'>
    🏏 IPL Predictor
    </h1>
    <p style='text-align:center;color:gray;font-size:14px;'>
    AI Powered Match Winner Prediction
    </p>
    <hr>
    """, unsafe_allow_html=True)

    st.subheader("📋 Match Details")

    # ------------------------------------------------------
    # Season
    # ------------------------------------------------------

    from datetime import datetime

    current_year = datetime.now().year

    season = st.selectbox(
        "📅 Season",
        options=list(range(2008, current_year + 1)),
        index=current_year - 2008
    )

    # ------------------------------------------------------
    # Venue
    # Replace this list with your actual venue list
    # ------------------------------------------------------
    
    import pandas as pd

    # Load venues from CSV
    venue_df = pd.read_csv("data/venue.csv")

# Create sorted venue list
    venues = sorted(
        venue_df["venue"]
        .dropna()
        .astype(str)
        .str.strip()
        .unique()
        .tolist()
    )

    # Venue selector
    venue = st.selectbox(
        "🏟 Venue",
        options=venues
    )

    # ------------------------------------------------------
    # Teams
    # ------------------------------------------------------

    teams = sorted([
        "Chennai Super Kings",
        "Mumbai Indians",
        "Royal Challengers Bengaluru",
        "Kolkata Knight Riders",
        "Sunrisers Hyderabad",
        "Delhi Capitals",
        "Punjab Kings",
        "Rajasthan Royals",
        "Lucknow Super Giants",
        "Gujarat Titans"
    ])

    team1 = st.selectbox(
        "🟡 Team 1",
        teams
    )

    remaining_teams = [team for team in teams if team != team1]

    team2 = st.selectbox(
        "🔵 Team 2",
        remaining_teams
    )

    st.divider()

    # ------------------------------------------------------
    # Toss
    # ------------------------------------------------------

    st.subheader("🪙 Toss Details")

    toss_winner = st.radio(
        "Toss Winner",
        [team1, team2],
        horizontal=True
    )

    toss_decision = st.radio(
        "Toss Decision",
        ["Bat First", "Field First"],
        horizontal=True
    )

    st.divider()

    # ------------------------------------------------------
    # Playoff
    # ------------------------------------------------------

    playoff = st.toggle(
        "🏆 Playoff Match",
        value=False
    )

    st.divider()

    # ------------------------------------------------------
    # Match Summary
    # ------------------------------------------------------

    st.markdown("### 📄 Selected Match")

    st.info(
        f"""
**Season:** {season}

**Venue:** {venue}

**Match:** {team1} vs {team2}

**Toss Winner:** {toss_winner}

**Decision:** {toss_decision}

**Playoff:** {"Yes" if playoff else "No"}
"""
    )

    st.divider()

    # ------------------------------------------------------
    # Footer
    # ------------------------------------------------------

    st.caption("Version 1.0")

    st.caption("Built using ❤️ Streamlit + Machine Learning")
    return {
    "season": season,
    "venue": venue,
    "team1": team1,
    "team2": team2,
    "toss_winner": toss_winner,
    "toss_decision": toss_decision,
    "playoff": playoff
    }