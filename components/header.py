# ==========================================================
# HEADER SECTION
# ==========================================================

import streamlit as st

def show_header(season, venue, team1, team2, playoff):
    
    st.markdown("""
<style>

/* Hide Streamlit default menu and footer */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Header Card */
.header-container{
    background: linear-gradient(135deg,#0F172A,#1E3A8A,#2563EB);
    padding:30px;
    border-radius:18px;
    border:1px solid rgba(255,255,255,0.12);
    box-shadow:0px 8px 30px rgba(0,0,0,0.35);
    margin-bottom:20px;
}

/* Title */
.main-title{
    font-size:42px;
    font-weight:800;
    color:white;
    text-align:center;
    margin-bottom:8px;
}

/* Subtitle */
.subtitle{
    font-size:18px;
    color:#E2E8F0;
    text-align:center;
    margin-bottom:20px;
}

/* Info Boxes */
.info-box{
    background:rgba(255,255,255,0.08);
    border-radius:12px;
    padding:15px;
    text-align:center;
    border:1px solid rgba(255,255,255,0.08);
}

.info-title{
    color:#CBD5E1;
    font-size:14px;
}

.info-value{
    color:white;
    font-size:22px;
    font-weight:bold;
}

</style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
<div class="header-container">

<div class="main-title">
🏏 IPL Match Winner Predictor
</div>

<div class="subtitle">
AI-Powered Cricket Analytics Dashboard
</div>

</div>
    """, unsafe_allow_html=True)

# ----------------------------------------------------------
# HEADER INFORMATION CARDS
# ----------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
    <div class="info-box">
        <div class="info-title">📅 Season</div>
        <div class="info-value">{season}</div>
    </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
    <div class="info-box">
        <div class="info-title">🏟 Venue</div>
        <div class="info-value" style="font-size:16px;">{venue}</div>
    </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
    <div class="info-box">
        <div class="info-title">⚔ Match</div>
        <div class="info-value" style="font-size:18px;">
        {team1} <br> VS <br> {team2}
        </div>
    </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
    <div class="info-box">
        <div class="info-title">🏆 Match Type</div>
        <div class="info-value">
        {"Playoff" if playoff else "League"}
        </div>
    </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)