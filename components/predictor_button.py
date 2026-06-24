# ==========================================================
# components/predict_button.py
# ==========================================================

import streamlit as st


def show_predict_button():
    """
    Display the Predict Match button.

    Returns
    -------
    bool
        True if the button is clicked.
    """

    st.markdown("---")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        predict = st.button(
            "🚀 Predict Match Winner",
            type="primary",
            use_container_width=True
        )

    return predict