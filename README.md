# 🏏 IPL Match Winner Predictor

> AI-powered cricket analytics dashboard that predicts IPL match outcomes using machine learning — built with Python, Scikit-learn, LightGBM, CatBoost, and Streamlit.

![Python](https://img.shields.io/badge/Python-3.10+-blue) ![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red) ![License](https://img.shields.io/badge/License-MIT-green)

---

## What it does

Enter two IPL teams, their playing XI, venue, toss result and toss decision — and the model predicts the match winner with a win probability percentage and confidence level (High / Medium / Low).

The prediction is driven by a trained ensemble model that factors in:

- Head-to-head win rates between the two teams
- All-time win rates per team
- Venue-specific batting and bowling statistics
- Squad batting average and bowling economy for the selected players
- Toss decision and venue bat-first win rates
- Playoff vs league stage match type

---

## Tech stack

| Layer | Tools |
|---|---|
| Data processing | Pandas, NumPy |
| Machine learning | Scikit-learn, LightGBM, CatBoost |
| Model selection | StratifiedKFold cross-validation, ROC-AUC, Brier Score |
| Visualisation | Plotly, Matplotlib, Seaborn |
| Frontend | Streamlit |
| Notebook | Google Colab |

---

## Data sources

Three Kaggle datasets covering IPL 2008–2026:

- [IPL Dataset 2008–2025](https://www.kaggle.com/datasets/chaitu20/ipl-dataset2008-2025) — ball-by-ball and match metadata
- [IPL Complete Dataset 2008–2024](https://www.kaggle.com/datasets/patrickb1912/ipl-complete-dataset-20082020) — match summaries and deliveries
- [IPL Dataset 2008–2026](https://www.kaggle.com/datasets/maratheabhishek/ipl-dataset-2008-to-2025) — player details, team aliases, venue data

Raw data sourced from [Cricsheet](https://cricsheet.org/) and enriched with ESPN Cricinfo and IPL official stats.

---

## How the model works

### Feature engineering
- **Head-to-head win rate** — historical win % between the two teams (strongest single feature)
- **Squad batting average** — average batting avg of the 11 selected players at that venue
- **Squad bowling economy** — average economy rate of selected bowlers at that venue
- **Venue bat-first win rate** — % of matches won batting first at that ground
- **Toss advantage** — whether toss decision aligns with venue tendency
- **Playoff flag** — knockout matches have different pressure dynamics

### Model selection
Five models were trained and compared using 5-fold stratified cross-validation:

| Model | CV Accuracy | ROC-AUC |
|---|---|---|
| Logistic Regression | baseline | — |
| Random Forest | ✓ | ✓ |
| Gradient Boosting | ✓ | ✓ |
| LightGBM | ✓ | ✓ |
| CatBoost | ✓ | ✓ |

The best performing model was saved as `best_model.pkl` and loaded by the Streamlit app.

### Confidence levels
| Probability | Confidence |
|---|---|
| > 70% | High |
| 55–70% | Medium |
| < 55% | Low |

---

## How to run locally

```bash
# 1. Clone the repo
git clone https://github.com/your-username/ipl-match-predictor.git
cd ipl-match-predictor

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## Project structure

```
ipl-match-predictor/
├── app.py                  # Streamlit frontend
├── IPL_predictor.py        # Full ML pipeline (data → model)
├── models/
│   └── best_model.pkl      # Trained model
├── data/
│   └── (Kaggle CSVs)       # Not included — download from links above
├── requirements.txt
└── README.md
```

---

## Known limitations

- Squad economy and batting average are computed from historical data — current form is not factored in
- Venue sample sizes vary — predictions at less frequently used venues may be less reliable
- Player injuries, last-minute XI changes, and pitch conditions are not modelled
- Model trained on data up to 2026 season

---

## Author

**Aryan Garg** — Data Scientist & iOS Developer  
[LinkedIn](https://linkedin.com/in/aryan-garg-029b41233) · [GitHub](https://github.com/Aryan-garg-1) · [Portfolio](https://aryangarg.in)

---

## License

MIT — free to use, modify, and distribute with attribution.
