# ==========================================================
# IPL MATCH WINNER PREDICTOR
# app.py
# ==========================================================

import streamlit as st

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="🏏 IPL Match Winner Predictor",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# IMPORT COMPONENTS
# ==========================================================

from components.header import show_header
from components.sidebar import show_sidebar
from components.playing_xi import show_playing_xi
from components.predictor_button import show_predict_button
from components.result_card import show_result_card
from components.probability_chart import show_probability_chart
from components.match_summary import show_match_summary
from components.footer import show_footer

from components.predictor import predict_match

# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown("""
<style>

.block-container{
    padding-top:2rem;
    padding-bottom:2rem;
}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# SIDEBAR
# ==========================================================

sidebar_data = show_sidebar()

season = sidebar_data["season"]
venue = sidebar_data["venue"]
team1 = sidebar_data["team1"]
team2 = sidebar_data["team2"]
toss_winner = sidebar_data["toss_winner"]
toss_decision = sidebar_data["toss_decision"]
playoff = sidebar_data["playoff"]

# ==========================================================
# HEADER
# ==========================================================

show_header(
    season=season,
    venue=venue,
    team1=team1,
    team2=team2,
    playoff=playoff
)

# ==========================================================
# PLAYING XI
# ==========================================================

team1_players, team2_players = show_playing_xi(
    team1,
    team2
)

# ==========================================================
# PREDICT BUTTON
# ==========================================================

predict_clicked = show_predict_button()

# ==========================================================
# PREDICTION
# ==========================================================

if predict_clicked:

    # ------------------------------------------------------
    # Validation
    # ------------------------------------------------------

    if team1 == team2:
        st.error("❌ Team 1 and Team 2 cannot be the same.")
        st.stop()

    if len(team1_players) != 11:
        st.error(f"❌ Please select exactly 11 players for {team1}.")
        st.stop()

    if len(team2_players) != 11:
        st.error(f"❌ Please select exactly 11 players for {team2}.")
        st.stop()

    # ------------------------------------------------------
    # Prediction
    # ------------------------------------------------------

    with st.spinner("🤖 AI is analyzing match conditions..."):

        prediction = predict_match(

            team1=team1,
            team2=team2,

            team1_players=team1_players,
            team2_players=team2_players,

            venue=venue,

            toss_winner=toss_winner,
            toss_decision=toss_decision,

            season_year=season,

            is_playoff=playoff

        )

    st.success("✅ Prediction Generated Successfully!")

    # ======================================================
    # RESULT CARD
    # ======================================================

    show_result_card(

        winner=prediction["winner"],

        team1=prediction["team1"],

        team2=prediction["team2"],

        team1_probability=prediction["team1_probability"],

        team2_probability=prediction["team2_probability"],

        confidence=prediction["confidence"]

    )

    # ======================================================
    # PROBABILITY CHART
    # ======================================================

    show_probability_chart(

        team1=prediction["team1"],

        team2=prediction["team2"],

        team1_probability=prediction["team1_probability"],

        team2_probability=prediction["team2_probability"]

    )

    # ======================================================
    # MATCH SUMMARY
    # ======================================================

    show_match_summary(

        season=season,

        venue=venue,

        team1=prediction["team1"],

        team2=prediction["team2"],

        toss_winner=toss_winner,

        toss_decision=toss_decision,

        playoff=playoff,

        winner=prediction["winner"],

        team1_probability=prediction["team1_probability"],

        team2_probability=prediction["team2_probability"],

        confidence=prediction["confidence"]

    )

# ==========================================================
# FOOTER
# ==========================================================

show_footer()