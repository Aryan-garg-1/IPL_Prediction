import plotly.graph_objects as go
import streamlit as st


def show_probability_chart(
    team1: str,
    team2: str,
    team1_probability: float,
    team2_probability: float
):
    """
    Displays an interactive probability comparison chart.

    Parameters
    ----------
    team1 : str
        First team.

    team2 : str
        Second team.

    team1_probability : float
        Winning probability of Team 1.

    team2_probability : float
        Winning probability of Team 2.
    """

    st.markdown("## 📊 Winning Probability")

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            name=team1,
            x=[team1_probability],
            y=[team1],
            orientation="h",
            text=[f"{team1_probability:.2f}%"],
            textposition="inside",
            marker=dict(
                color="#2563EB",
                line=dict(color="white", width=1)
            ),
            hovertemplate="%{y}<br>%{x:.2f}%<extra></extra>"
        )
    )

    fig.add_trace(
        go.Bar(
            name=team2,
            x=[team2_probability],
            y=[team2],
            orientation="h",
            text=[f"{team2_probability:.2f}%"],
            textposition="inside",
            marker=dict(
                color="#F97316",
                line=dict(color="white", width=1)
            ),
            hovertemplate="%{y}<br>%{x:.2f}%<extra></extra>"
        )
    )

    fig.update_layout(

        barmode="group",
        
        bargap=0.8,

        height=320,

        template="plotly_dark",

        title=dict(
            text="Match Win Probability",
            x=0.5,
            font=dict(size=20)
        ),

        xaxis=dict(
            title="Winning Probability (%)",
            range=[0, 100],
            ticksuffix="%",
            showgrid=True,
            gridcolor="rgba(255,255,255,0.1)"
        ),

        yaxis=dict(
            title=""
        ),

        font=dict(size=15),

        margin=dict(
            l=30,
            r=30,
            t=60,
            b=30
        ),

        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.05,
            xanchor="center",
            x=0.5
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": False,
            "responsive": True
        }
    )