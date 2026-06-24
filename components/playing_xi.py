# ==========================================================
# components/playing_xi.py
# ==========================================================

import streamlit as st
import pandas as pd


# ==========================================================
# LOAD PLAYERS
# ==========================================================

@st.cache_data
def load_players():

    players = pd.read_csv("data/players.csv")   # Change filename if needed

    players.columns = players.columns.str.strip().str.lower()

    players["player"] = (
        players["player"]
        .astype(str)
        .str.strip()
    )

    players = players.drop_duplicates(subset="player")

    return sorted(players["player"].tolist())


# ==========================================================
# PLAYING XI
# ==========================================================

def show_playing_xi(team1, team2):

    all_players = load_players()

    st.markdown("---")
    st.subheader("🏏 Playing XI")

    st.caption("Search and select exactly 11 players for each team.")

    col1, col2 = st.columns(2)

    # ======================================================
    # TEAM 1
    # ======================================================

    with col1:

        st.markdown(f"## 🟡 {team1}")

        team1_players = st.multiselect(

            "Search & Select Players",

            options=all_players,

            default=st.session_state.get("team1_players", []),

            max_selections=11,

            key="team1_players"

        )

        st.progress(len(team1_players) / 11)

        st.caption(f"{len(team1_players)} / 11 Players Selected")

    # ======================================================
    # TEAM 2
    # ======================================================

    with col2:

        st.markdown(f"## 🔵 {team2}")

        # Prevent selecting players already chosen in Team 1
        available_players = [
            p for p in all_players
            if p not in team1_players
        ]

        previous_selection = [
            p for p in st.session_state.get("team2_players", [])
            if p in available_players
        ]

        team2_players = st.multiselect(

            "Search & Select Players",

            options=available_players,

            default=previous_selection,

            max_selections=11,

            key="team2_players"

        )

        st.progress(len(team2_players) / 11)

        st.caption(f"{len(team2_players)} / 11 Players Selected")

    # ======================================================
    # VALIDATION
    # ======================================================

    st.markdown("---")

    if len(team1_players) != 11:

        st.warning(f"⚠️ {team1}: Select exactly 11 players.")

    if len(team2_players) != 11:

        st.warning(f"⚠️ {team2}: Select exactly 11 players.")

    if len(team1_players) == 11 and len(team2_players) == 11:

        st.success("✅ Playing XI Completed")

    return team1_players, team2_players