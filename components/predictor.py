# ==========================================================
# predictor.py
# IPL Match Winner Predictor Backend
# ==========================================================

import joblib
import numpy as np
import pandas as pd
import streamlit as st

# ==========================================================
# LOAD MODEL
# ==========================================================

@st.cache_resource
def load_model():
    """Load trained model."""
    model_dict = joblib.load("saved_models/best_model.pkl")

    return (
        model_dict["model"],
        model_dict["features"],
        model_dict["name"]
    )


best_model, FEAT_COLS, MODEL_NAME = load_model()


# ==========================================================
# LOAD PRECOMPUTED STATS
# ==========================================================

@st.cache_resource
def load_stats():
    """Load all precomputed statistics."""

    stats = joblib.load("saved_models/precomputed_stats.pkl")

    return stats


stats = load_stats()

batting_stats = stats["batting_stats"]
bowling_stats = stats["bowling_stats"]
team_alltime = stats["team_alltime"]
season_wr = stats["season_wr"]
h2h = stats["h2h"]
venue_stats = stats["venue_stats"]


# ==========================================================
# LOOKUP TABLES
# ==========================================================

_wr_at = (
    team_alltime
    .set_index("team")["win_rate_alltime"]
    .to_dict()
)

_wr_rec = (
    season_wr
    .set_index(["team", "season_year"])["win_rate_rolling3"]
    .to_dict()
)

_h2h_wr = (
    h2h
    .set_index(["team_a", "team_b"])["h2h_win_rate"]
    .to_dict()
)

_h2h_pl = (
    h2h
    .set_index(["team_a", "team_b"])["played"]
    .to_dict()
)

_v_idx = venue_stats.set_index("venue")


# ==========================================================
# FALLBACK VALUES
# ==========================================================

BAT_AVG_FALLBACK = (
    batting_stats["batting_avg_venue"]
    .median()
)

BAT_SR_FALLBACK = (
    batting_stats["strike_rate_venue"]
    .median()
)

ECO_FALLBACK = (
    bowling_stats["economy_rate_venue"]
    .median()
)

BOWL_AVG_FALLBACK = (
    bowling_stats["bowling_avg_venue"]
    .replace(999.0, np.nan)
    .median()
)


# ==========================================================
# PLAYER LOOKUPS
# ==========================================================

_bat_idx = batting_stats.set_index(
    ["batter", "venue"]
)

_bowl_idx = bowling_stats.set_index(
    ["bowler", "venue"]
)


# ==========================================================
# TEAM NAME ALIASES
# ==========================================================

TEAM_ALIAS = {

    "Delhi Daredevils":
        "Delhi Capitals",

    "Kings XI Punjab":
        "Punjab Kings",

    "Rising Pune Supergiant":
        "Rising Pune Supergiants",

    "Gujarat Lions":
        "Gujarat Lions",

    "Deccan Chargers":
        "Deccan Chargers"

}


# ==========================================================
# VENUE NAME ALIASES
# ==========================================================

VENUE_ALIAS = {

    # Add aliases if required.
    # Leave empty if your dataset
    # already uses standardized venue names.

}


# ==========================================================
# CLEANING FUNCTIONS
# ==========================================================

def clean_team(name):
    """
    Standardize team names.
    """

    if pd.isna(name):
        return name

    return TEAM_ALIAS.get(
        str(name).strip(),
        str(name).strip()
    )


def clean_venue(name):
    """
    Standardize venue names.
    """

    if pd.isna(name):
        return name

    return VENUE_ALIAS.get(
        str(name).strip(),
        str(name).strip()
    )


print("✅ Predictor initialized successfully.")
print(f"Loaded Model : {MODEL_NAME}")
print(f"Features     : {len(FEAT_COLS)}")

# ==========================================================
# SQUAD FEATURE AGGREGATION
# ==========================================================

def aggregate_squad(
    squad,
    venue,
    top_bat=6,
    top_bowl=5
):
    """
    Calculate squad-level batting and bowling statistics
    for the selected Playing XI.
    """

    bat_avgs = []
    bat_srs = []

    ecos = []
    bowl_avgs = []

    # ------------------------------------------------------
    # BATTERS
    # ------------------------------------------------------

    for player in squad[:top_bat]:

        key = (player, venue)

        if key in _bat_idx.index:

            row = _bat_idx.loc[key]

            if isinstance(row, pd.DataFrame):
                row = row.iloc[0]

            bat_avgs.append(
                row["batting_avg_venue"]
            )

            bat_srs.append(
                row["strike_rate_venue"]
            )

        else:

            bat_avgs.append(
                BAT_AVG_FALLBACK
            )

            bat_srs.append(
                BAT_SR_FALLBACK
            )

    # ------------------------------------------------------
    # BOWLERS
    # ------------------------------------------------------

    for player in squad[top_bat:top_bat + top_bowl]:

        key = (player, venue)

        if key in _bowl_idx.index:

            row = _bowl_idx.loc[key]

            if isinstance(row, pd.DataFrame):
                row = row.iloc[0]

            ecos.append(
                row["economy_rate_venue"]
            )

            avg = row["bowling_avg_venue"]

            if avg >= 999:

                avg = BOWL_AVG_FALLBACK

            bowl_avgs.append(avg)

        else:

            ecos.append(ECO_FALLBACK)

            bowl_avgs.append(
                BOWL_AVG_FALLBACK
            )

    # ------------------------------------------------------
    # SAFETY CHECKS
    # ------------------------------------------------------

    if len(bat_avgs) == 0:
        bat_avgs = [BAT_AVG_FALLBACK]

    if len(bat_srs) == 0:
        bat_srs = [BAT_SR_FALLBACK]

    if len(ecos) == 0:
        ecos = [ECO_FALLBACK]

    if len(bowl_avgs) == 0:
        bowl_avgs = [BOWL_AVG_FALLBACK]

    # ------------------------------------------------------
    # RETURN FEATURES
    # ------------------------------------------------------

    return {

        "squad_avg_batting_avg":
            round(np.mean(bat_avgs), 2),

        "squad_avg_strike_rate":
            round(np.mean(bat_srs), 2),

        "squad_avg_economy":
            round(np.mean(ecos), 2),

        "squad_avg_bowling_avg":
            round(np.mean(bowl_avgs), 2),

        "squad_min_economy":
            round(np.min(ecos), 2),

        "squad_max_batting_avg":
            round(np.max(bat_avgs), 2)

    }
    
    # ==========================================================
# MATCH PREDICTION
# ==========================================================

def predict_match(

    team1,
    team2,

    team1_players,
    team2_players,

    venue,

    toss_winner,
    toss_decision,

    season_year,

    is_playoff

):
    """
    Predict IPL Match Winner.
    """

    # ------------------------------------------------------

    team1 = clean_team(team1)
    team2 = clean_team(team2)

    venue = clean_venue(venue)

    toss_winner = clean_team(toss_winner)

    # ------------------------------------------------------
    # TEAM STATS
    # ------------------------------------------------------

    t1_at = _wr_at.get(team1, 0.45)
    t2_at = _wr_at.get(team2, 0.45)

    t1_rec = _wr_rec.get(
        (team1, season_year),
        t1_at
    )

    t2_rec = _wr_rec.get(
        (team2, season_year),
        t2_at
    )

    h2h_rate = _h2h_wr.get(
        (team1, team2),
        0.50
    )

    h2h_games = _h2h_pl.get(
        (team1, team2),
        0
    )

    # ------------------------------------------------------
    # VENUE FEATURES
    # ------------------------------------------------------

    if venue in _v_idx.index:

        row = _v_idx.loc[venue]

        if isinstance(row, pd.DataFrame):
            row = row.iloc[0]

        bat_first_wr = row["bat_first_win_rate"]

        venue_matches = row["total_matches"]

        home_team = row.get(
            "venue_home_team",
            ""
        )

    else:

        bat_first_wr = 0.45

        venue_matches = 10

        home_team = ""

    # ------------------------------------------------------

    toss_team1 = int(
        toss_winner == team1
    )

    # ------------------------------------------------------
    # PLAYING XI FEATURES
    # ------------------------------------------------------

    team1_squad = aggregate_squad(
        team1_players,
        venue
    )

    team2_squad = aggregate_squad(
        team2_players,
        venue
    )

    # ------------------------------------------------------
    # FEATURE VECTOR
    # ------------------------------------------------------

    feat = {

        "t1_wr_alltime": t1_at,
        "t2_wr_alltime": t2_at,

        "wr_diff_alltime":
            round(t1_at - t2_at, 3),

        "t1_wr_recent": t1_rec,
        "t2_wr_recent": t2_rec,

        "wr_diff_recent":
            round(t1_rec - t2_rec, 3),

        "h2h_t1_vs_t2":
            h2h_rate,

        "h2h_games_played":
            h2h_games,

        "venue_bat_first_wr":
            bat_first_wr,

        "venue_total_matches":
            venue_matches,

        "t1_home_venue":
            int(team1 == home_team),

        "t2_home_venue":
            int(team2 == home_team),

        "toss_won_by_t1":
            toss_team1,

        "t1_chose_bat":
            int(
                toss_team1 and
                toss_decision == "bat"
            ),

        "t1_chose_field":
            int(
                toss_team1 and
                toss_decision == "field"
            ),

        "toss_decision_encoded":
            int(
                toss_decision == "field"
            ),

        "is_playoff":
            int(is_playoff),

        **{
            f"t1_{k}": v
            for k, v in team1_squad.items()
        },

        **{
            f"t2_{k}": v
            for k, v in team2_squad.items()
        }

    }

    # ------------------------------------------------------
    # FEATURE ORDER
    # ------------------------------------------------------

    X_pred = pd.DataFrame([
        {
            col: feat.get(col, 0)
            for col in FEAT_COLS
        }
    ])

    # ------------------------------------------------------
    # PREDICT
    # ------------------------------------------------------

    probability = best_model.predict_proba(
        X_pred
    )[0]

    team1_probability = float(
        probability[1] * 100
    )

    team2_probability = float(
        probability[0] * 100
    )

    winner = (
        team1
        if team1_probability >= 50
        else team2
    )

    # ------------------------------------------------------
    # CONFIDENCE
    # ------------------------------------------------------

    margin = abs(
        team1_probability -
        team2_probability
    )

    if margin < 15:

        confidence = "Low"

    elif margin < 35:

        confidence = "Medium"

    else:

        confidence = "High"

    # ------------------------------------------------------
    # RETURN
    # ------------------------------------------------------

    return {

        "winner":
            winner,

        "team1":
            team1,

        "team2":
            team2,

        "team1_probability":
            round(team1_probability, 2),

        "team2_probability":
            round(team2_probability, 2),

        "confidence":
            confidence,

        "model":
            MODEL_NAME

    }


print("✅ Predictor Ready")