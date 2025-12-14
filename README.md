# EPL Match Outcome & League Winner Prediction

## Project Overview
This project applies machine learning techniques to predict match outcomes in the English Premier League (EPL) and uses those predictions to simulate full seasons in order to estimate league winner probabilities.  

Rather than directly predicting the league champion, the model forecasts individual match outcomes probabilistically and aggregates them through Monte Carlo season simulations.

The primary goal of this project is to demonstrate an end-to-end, time-aware machine learning pipeline using real-world sports data, with an emphasis on feature engineering, probabilistic modeling, and realistic evaluation. This project is designed as a portfolio piece for data science, machine learning, and analytics-focused roles.

---

## Why the Premier League
The English Premier League was chosen for this project because it provides:

- High-quality, publicly available historical match data
- A long and consistent season history
- Strong competitive balance, making prediction non-trivial
- High relevance to real-world sports analytics and forecasting problems

Focusing on a single league allows for cleaner modeling assumptions and deeper feature engineering while avoiding inconsistencies across leagues.

---

## Problem Formulation

### Task Definition
- **Primary task:** Predict match outcomes (Home Win / Draw / Away Win)
- **Secondary task:** Simulate full EPL seasons to estimate title-winning probabilities

### Motivation
Directly predicting the league winner yields extremely limited training data (one winner per season). By modeling individual matches instead, this project:

- Substantially increases the amount of training data
- Enables probabilistic forecasts instead of deterministic predictions
- Allows realistic season-level simulations

---

## Data Sources

### Match Results
- Historical EPL match data from [Football-Data.co.uk](https://www.football-data.co.uk/)
- Includes:
  - Match dates
  - Home and away teams
  - Goals scored
  - Match results
  - Betting odds

### Team Strength
- **Club ELO ratings** are used as a dynamic representation of team strength
- ELO ratings are merged with matches by date to prevent future data leakage

---

## Data Coverage
- **Seasons included:** 2005–06 to the most recent completed EPL season

This range provides:
- Approximately 7,000+ matches
- Coverage across multiple tactical eras and managerial cycles
- Sufficient data for time-based training, validation, and testing

Earlier seasons are excluded to reduce noise from structural and tactical differences that are less representative of modern football.

---

## Feature Engineering
All features are computed using only information available **prior to each match** to prevent data leakage.

Key engineered features include:

- Rolling points over the last *N* matches
- Rolling goals scored, conceded, and goal difference
- Home vs away performance splits
- ELO rating difference between teams
- Recent form indicators

Feature engineering is implemented using time-aware rolling windows to ensure realistic model training.

---

## Modeling Approach

### Baseline Model
- Multinomial Logistic Regression

### Primary Model
- Gradient Boosted Decision Trees (XGBoost)

### Target Variable Encoding
- `0` — Away Win  
- `1` — Draw  
- `2` — Home Win  

Models are trained using time-based splits rather than random sampling to reflect real-world forecasting conditions.

---

## Evaluation Metrics

### Match-Level Evaluation
- Log Loss
- Brier Score
- Accuracy (used as a secondary metric)

### Season-Level Evaluation
- League winner probability distributions
- Rank correlation between predicted and actual league tables

---

## Season Simulation
- Match outcome probabilities are generated for every EPL fixture
- Seasons are simulated thousands of times using Monte Carlo methods
- Points are accumulated using standard league rules (3–1–0)
- Final league tables are generated for each simulation

The final output is a probability distribution over league winners, mirroring techniques used in professional sports analytics.

---

## Results
The project outputs include:

- Match prediction performance metrics
- Feature importance analysis
- League winner probability tables

All generated artifacts are stored in the `results/` directory.

---

## Limitations
- Injuries, suspensions, and transfers are not fully modeled
- Managerial changes are only partially captured
- Betting markets are highly efficient, limiting achievable predictive edge
- Draw outcomes remain inherently difficult to predict

---

## Future Work
- Incorporate expected goals (xG) data
- Add squad market value and transfer-based features
- Extend the framework to additional European leagues
- Build a lightweight web dashboard for interactive visualization
