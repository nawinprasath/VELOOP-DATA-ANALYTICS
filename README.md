
# VELOOP – Rewards Analytics Platform

An interactive data analytics platform built using Python, Pandas, and Streamlit to analyze simulated user engagement, sessions, task performance, feature usage, and data quality for the VELOOP Rewards platform.

## Live Dashboard

[Open VELOOP Rewards Analytics Dashboard](https://veloop-rewards-analytics.streamlit.app/)

## Project Overview

This project focuses on transforming raw simulated user behavior data into structured datasets and meaningful business insights through data preprocessing, exploratory analysis, data quality validation, and interactive visualization.

## Key Features

- Executive Overview – Platform performance metrics.
- User Engagement – Daily and weekly user activity trends.
- Task Performance – Task status distribution and failure analysis.
- Feature Usage – Feature adoption and usage comparisons.
- Data Quality – Missing values and data validation findings.

## Technology Stack

- Python
- Pandas
- NumPy
- Streamlit
- Matplotlib
- Jupyter Notebook
- GitHub

## Project Structure

```text
VELOOP-DATA-ANALYTICS/
│
├── dashboard/
│   └── app.py
│
├── data/
│   └── processed/
│       ├── daily_activity.csv
│       ├── feature_events.csv
│       ├── feature_usage.csv
│       ├── milestones.csv
│       ├── sessions.csv
│       ├── task_activity.csv
│       └── users.csv
│
├── notebooks/
│   └── VELOOP_Data_Pipeline.ipynb
│
├── requirements.txt
└── README.md
```

## Installation and Local Execution

1. Clone the repository:

```bash
git clone https://github.com/nawinprasath/VELOOP-DATA-ANALYTICS.git
```

2. Navigate to the project directory:

```bash
cd VELOOP-DATA-ANALYTICS
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the Streamlit dashboard:

```bash
streamlit run dashboard/app.py
```

## Data Sources

The project uses simulated datasets containing user, session, task activity, feature event, feature usage, milestone, and daily activity information.

**Note:** The dashboard is based on simulated datasets and does not represent verified production customer data. Rewards, wallet, withdrawals, and referral analytics remain pending because their datasets are unavailable.

## Deployment

The interactive dashboard is deployed using Streamlit Community Cloud.

**Live URL:** https://veloop-rewards-analytics.streamlit.app/

## Project Status

- Data preprocessing: Completed
- Data quality analysis: Completed
- Interactive dashboard: Completed
- GitHub repository: Available
- Cloud deployment: Successful

## Author

Nawin Prasath

GitHub: https://github.com/nawinprasath
