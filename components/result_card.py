import streamlit as st


def show_result_card(
    winner: str,
    team1: str,
    team2: str,
    team1_probability: float,
    team2_probability: float,
    confidence: str
):
    """
    Displays the prediction result card.

    Parameters
    ----------
    winner : str
        Predicted winning team.

    team1 : str
        First team.

    team2 : str
        Second team.

    team1_probability : float
        Winning probability of Team 1.

    team2_probability : float
        Winning probability of Team 2.

    confidence : str
        Prediction confidence.
    """

    if winner == team1:
        winner_color = "#22C55E"      # Green
        loser = team2
        winner_prob = team1_probability
        loser_prob = team2_probability
    else:
        winner_color = "#3B82F6"      # Blue
        loser = team1
        winner_prob = team2_probability
        loser_prob = team1_probability

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        f"""
        <style>

        .winner-card {{
            background: linear-gradient(135deg,#111827,#1E3A8A);
            padding:30px;
            border-radius:18px;
            border-left:8px solid {winner_color};
            box-shadow:0px 10px 25px rgba(0,0,0,0.35);
            margin-top:20px;
            margin-bottom:20px;
        }}

        .winner-title {{
            color:#E5E7EB;
            font-size:18px;
            text-transform:uppercase;
            letter-spacing:1px;
        }}

        .winner-team {{
            color:white;
            font-size:38px;
            font-weight:700;
            margin-top:10px;
        }}

        .winner-prob {{
            color:{winner_color};
            font-size:60px;
            font-weight:bold;
            margin-top:15px;
        }}

        .confidence {{
            display:inline-block;
            background:{winner_color};
            color:white;
            padding:8px 18px;
            border-radius:20px;
            font-size:16px;
            font-weight:bold;
            margin-top:20px;
        }}

        .summary {{
            color:#CBD5E1;
            font-size:18px;
            margin-top:20px;
            line-height:1.8;
        }}

        </style>

        <div class="winner-card">
        <div class="winner-title">
                🏆 Predicted Winner
        </div>

         <div class="winner-team">
                {winner}
        </div>

        <div class="winner-prob">
                {winner_prob:.2f}%
        </div>

        <div class="confidence">
                {confidence} Confidence
        </div>

        <div class="summary">

        <b>{winner}</b> is predicted to defeat
        <b>{loser}</b>.

        <br>
        <br>

        <b>   Winning Chances
        </b>

        <br>
        <b>
            • {team1}: 
        {team1_probability:.2f}%
        </b>

        <br>
        <b>
            • {team2}: 
        {team2_probability:.2f}%
        </b>

        </div>

        </div>

        """,
        unsafe_allow_html=True,
    )