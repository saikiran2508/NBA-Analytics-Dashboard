# 🏀 NBA Analytics Dashboard

An interactive NBA team & player analytics dashboard built with Plotly Dash.

## Features
- 📊 Bar chart — Team performance by selected metric
- 🥧 Pie chart — Conference comparison
- 📈 Line chart — Monthly scoring trends
- 🔵 Scatter plot — PPG vs Wins (bubble = Assists)
- 👤 Player stats — Top player PPG/APG/RPG breakdown
- 🔽 Filters — Season, Conference, Metric

## Run Locally
```bash
pip install -r requirements.txt
python app.py
```
Visit: http://localhost:8050

## Deploy on Render

1. Push this folder to a GitHub repo
2. Go to https://render.com and sign in
3. Click **New → Web Service**
4. Connect your GitHub repo
5. Set:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:server`
   - **Environment:** Python 3
6. Click **Deploy** — live in ~2 minutes!

## Built By
Sai Kiran Gopu · MS Data Science, RIT
