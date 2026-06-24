import streamlit as st


def show_match_summary(
    season: int,
    venue: str,
    team1: str,
    team2: str,
    toss_winner: str,
    toss_decision: str,
    playoff: bool,
    winner: str,
    team1_probability: float,
    team2_probability: float,
    confidence: str,
):
    """
    Displays a professional match summary card.

    Parameters
    ----------
    season : int
    venue : str
    team1 : str
    team2 : str
    toss_winner : str
    toss_decision : str
    playoff : bool
    winner : str
    team1_probability : float
    team2_probability : float
    confidence : str
    """

    match_type = "Playoff" if playoff else "League Stage"

    st.markdown("## 📋 Match Summary")

    st.markdown(
        f"""
        <style>

        .summary-card {{
            background: linear-gradient(135deg,#111827,#1F2937);
            padding:25px;
            border-radius:18px;
            border:1px solid rgba(255,255,255,0.10);
            box-shadow:0px 8px 20px rgba(0,0,0,0.35);
            margin-top:10px;
        }}

        .summary-title {{
            color:white;
            font-size:28px;
            font-weight:700;
            margin-bottom:20px;
        }}

        .summary-table {{
            width:100%;
            border-collapse:collapse;
        }}

        .summary-table td {{
            padding:12px;
            border-bottom:1px solid rgba(255,255,255,0.08);
            color:#E5E7EB;
            font-size:17px;
        }}

        .summary-table td:first-child {{
            font-weight:bold;
            color:#93C5FD;
            width:35%;
        }}

        </style>

        <div class="summary-card">

        <div class="summary-title">
        🏏 Match Information
        </div>

        <table class="summary-table">

        <tr>
            <td>Season</td>
            <td>{season}</td>
        </tr>

        <tr>
            <td>Venue</td>
            <td>{venue}</td>
        </tr>

        <tr>
            <td>Match</td>
            <td>{team1} vs {team2}</td>
        </tr>

        <tr>
            <td>Toss Winner</td>
            <td>{toss_winner}</td>
        </tr>

        <tr>
            <td>Toss Decision</td>
            <td>{toss_decision}</td>
        </tr>

        <tr>
            <td>Match Type</td>
            <td>{match_type}</td>
        </tr>

        <tr>
            <td>Predicted Winner</td>
            <td><b>{winner}</b></td>
        </tr>

        <tr>
            <td>{team1} Win Probability</td>
            <td>{team1_probability:.2f}%</td>
        </tr>

        <tr>
            <td>{team2} Win Probability</td>
            <td>{team2_probability:.2f}%</td>
        </tr>

        <tr>
            <td>Prediction Confidence</td>
            <td>{confidence}</td>
        </tr>

        </table>

        </div>
        """,
        unsafe_allow_html=True,
    )