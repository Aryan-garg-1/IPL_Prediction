import streamlit as st
from datetime import datetime


def show_footer():
    """
    Displays the application footer.
    """

    current_year = datetime.now().year

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.markdown(
        """
        <style>

        .footer {
            margin-top:40px;
            padding:20px;
            text-align:center;
            color:#94A3B8;
            font-size:14px;
            border-top:1px solid rgba(255,255,255,0.08);
        }

        .footer-title{
            color:black;
            font-size:18px;
            font-weight:600;
            margin-bottom:8px;
        }

        .footer-small{
            color:#64748B;
            font-size:13px;
            margin-top:6px;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="footer">

        <div class="footer-title">
            🏏 IPL Match Winner Predictor
        </div>

        <div>
                Powered by Machine Learning • Streamlit • Plotly
        </div>

        <div class="footer-small">
                Model Version : <b>v1.0</b>
        </div>

        <div class="footer-small">
                © {current_year} IPL Match Winner Predictor
        </div>

        </div>
        """,
        unsafe_allow_html=True,
    )