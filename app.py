import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# ── Seed data ──────────────────────────────────────────────────────────────
np.random.seed(42)

teams = ["Lakers","Celtics","Warriors","Bulls","Heat","Nets","Suns","Nuggets",
         "Bucks","76ers","Clippers","Mavericks","Thunder","Spurs","Raptors","Knicks"]

conferences = {
    "Lakers":"West","Celtics":"East","Warriors":"West","Bulls":"East",
    "Heat":"East","Nets":"East","Suns":"West","Nuggets":"West",
    "Bucks":"East","76ers":"East","Clippers":"West","Mavericks":"West",
    "Thunder":"West","Spurs":"West","Raptors":"East","Knicks":"East"
}

seasons = ["2019-20","2020-21","2021-22","2022-23","2023-24"]

# Team season stats
rows = []
for team in teams:
    for season in seasons:
        rows.append({
            "Team": team,
            "Season": season,
            "Conference": conferences[team],
            "Wins": np.random.randint(20, 65),
            "PPG": round(np.random.uniform(105, 120), 1),
            "OppPPG": round(np.random.uniform(105, 118), 1),
            "3PT%": round(np.random.uniform(33, 42), 1),
            "FG%": round(np.random.uniform(44, 52), 1),
            "Assists": round(np.random.uniform(22, 30), 1),
            "Rebounds": round(np.random.uniform(40, 48), 1),
        })
df = pd.DataFrame(rows)
df["Net_Rating"] = (df["PPG"] - df["OppPPG"]).round(1)

# Top players
players_data = [
    {"Player":"LeBron James","Team":"Lakers","PPG":25.7,"APG":8.3,"RPG":7.3,"FG%":54.0,"Season":"2023-24"},
    {"Player":"Stephen Curry","Team":"Warriors","PPG":26.4,"APG":5.1,"RPG":4.5,"FG%":45.0,"Season":"2023-24"},
    {"Player":"Giannis Antetokounmpo","Team":"Bucks","PPG":30.4,"APG":6.5,"RPG":11.5,"FG%":61.0,"Season":"2023-24"},
    {"Player":"Nikola Jokic","Team":"Nuggets","PPG":26.4,"APG":9.0,"RPG":12.4,"FG%":58.3,"Season":"2023-24"},
    {"Player":"Luka Doncic","Team":"Mavericks","PPG":33.9,"APG":9.8,"RPG":9.2,"FG%":48.7,"Season":"2023-24"},
    {"Player":"Jayson Tatum","Team":"Celtics","PPG":26.9,"APG":4.9,"RPG":8.1,"FG%":47.1,"Season":"2023-24"},
    {"Player":"Joel Embiid","Team":"76ers","PPG":34.7,"APG":5.6,"RPG":11.0,"FG%":52.8,"Season":"2023-24"},
    {"Player":"Kevin Durant","Team":"Suns","PPG":27.1,"APG":5.0,"RPG":6.6,"FG%":52.0,"Season":"2023-24"},
    {"Player":"Devin Booker","Team":"Suns","PPG":27.8,"APG":6.9,"RPG":4.5,"FG%":49.3,"Season":"2023-24"},
    {"Player":"Damian Lillard","Team":"Bucks","PPG":24.3,"APG":7.6,"RPG":4.4,"FG%":44.2,"Season":"2023-24"},
    {"Player":"Anthony Davis","Team":"Lakers","PPG":24.7,"APG":3.5,"RPG":12.6,"FG%":55.7,"Season":"2023-24"},
    {"Player":"Kawhi Leonard","Team":"Clippers","PPG":23.7,"APG":3.6,"RPG":6.1,"FG%":52.1,"Season":"2023-24"},
]
df_players = pd.DataFrame(players_data)

# Monthly scoring trend (per team, fake monthly data)
months = ["Oct","Nov","Dec","Jan","Feb","Mar","Apr"]
trend_rows = []
for team in teams[:8]:
    base = np.random.uniform(108, 118)
    for month in months:
        trend_rows.append({"Team": team, "Month": month,
                           "PPG": round(base + np.random.uniform(-4, 4), 1)})
df_trend = pd.DataFrame(trend_rows)

# ── App ────────────────────────────────────────────────────────────────────
app = dash.Dash(__name__, title="NBA Analytics Dashboard")
server = app.server  # for Render

COLORS = {
    "bg": "#0f1117", "card": "#1a1d2e", "accent": "#f5a623",
    "blue": "#4a90d9", "green": "#50c878", "red": "#e05c5c",
    "text": "#e8e8e8", "muted": "#888"
}

card_style = {
    "background": COLORS["card"],
    "borderRadius": "12px",
    "padding": "20px",
    "marginBottom": "20px",
    "boxShadow": "0 4px 24px rgba(0,0,0,0.3)"
}

kpi_style = {
    **card_style,
    "textAlign": "center",
    "padding": "16px 12px",
    "marginBottom": "0"
}

app.layout = html.Div(style={"backgroundColor": COLORS["bg"], "minHeight": "100vh",
                              "fontFamily": "'Segoe UI', sans-serif", "padding": "24px"}, children=[

    # Header
    html.Div(style={"marginBottom": "28px", "borderBottom": f"2px solid {COLORS['accent']}",
                    "paddingBottom": "16px", "display": "flex", "alignItems": "center", "gap": "16px"}, children=[
        html.Div("🏀", style={"fontSize": "2.5rem"}),
        html.Div([
            html.H1("NBA Analytics Dashboard", style={"color": COLORS["accent"], "margin": "0",
                                                        "fontSize": "1.8rem", "fontWeight": "700"}),
            html.P("Team & Player Performance · 2019–2024",
                   style={"color": COLORS["muted"], "margin": "4px 0 0", "fontSize": "0.85rem"})
        ])
    ]),

    # Filters row
    html.Div(style={"display": "grid", "gridTemplateColumns": "1fr 1fr 1fr", "gap": "16px",
                    "marginBottom": "24px"}, children=[
        html.Div([
            html.Label("Season", style={"color": COLORS["muted"], "fontSize": "0.75rem",
                                         "textTransform": "uppercase", "letterSpacing": "0.1em"}),
            dcc.Dropdown(id="season-filter", options=[{"label": s, "value": s} for s in seasons],
                         value="2023-24", clearable=False,
                         style={"backgroundColor": COLORS["card"], "color": "#000", "border": "none"})
        ], style=card_style),
        html.Div([
            html.Label("Conference", style={"color": COLORS["muted"], "fontSize": "0.75rem",
                                             "textTransform": "uppercase", "letterSpacing": "0.1em"}),
            dcc.Dropdown(id="conf-filter",
                         options=[{"label": "All", "value": "All"},
                                  {"label": "East", "value": "East"},
                                  {"label": "West", "value": "West"}],
                         value="All", clearable=False,
                         style={"backgroundColor": COLORS["card"], "color": "#000", "border": "none"})
        ], style=card_style),
        html.Div([
            html.Label("Metric", style={"color": COLORS["muted"], "fontSize": "0.75rem",
                                         "textTransform": "uppercase", "letterSpacing": "0.1em"}),
            dcc.Dropdown(id="metric-filter",
                         options=[{"label": "Points Per Game", "value": "PPG"},
                                  {"label": "Wins", "value": "Wins"},
                                  {"label": "Net Rating", "value": "Net_Rating"},
                                  {"label": "3PT%", "value": "3PT%"},
                                  {"label": "Assists", "value": "Assists"}],
                         value="PPG", clearable=False,
                         style={"backgroundColor": COLORS["card"], "color": "#000", "border": "none"})
        ], style=card_style),
    ]),

    # KPI Cards
    html.Div(id="kpi-cards", style={"display": "grid",
                                     "gridTemplateColumns": "repeat(4, 1fr)",
                                     "gap": "16px", "marginBottom": "24px"}),

    # Row 1: Bar + Pie
    html.Div(style={"display": "grid", "gridTemplateColumns": "2fr 1fr", "gap": "16px",
                    "marginBottom": "20px"}, children=[
        html.Div(dcc.Graph(id="bar-chart", config={"displayModeBar": False}), style=card_style),
        html.Div(dcc.Graph(id="pie-chart", config={"displayModeBar": False}), style=card_style),
    ]),

    # Row 2: Line + Scatter
    html.Div(style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "16px",
                    "marginBottom": "20px"}, children=[
        html.Div(dcc.Graph(id="line-chart", config={"displayModeBar": False}), style=card_style),
        html.Div(dcc.Graph(id="scatter-chart", config={"displayModeBar": False}), style=card_style),
    ]),

    # Row 3: Player stats bar
    html.Div(dcc.Graph(id="player-chart", config={"displayModeBar": False}), style=card_style),

    # Footer
    html.P("Built with Plotly Dash · Data is illustrative · Sai Kiran Gopu",
           style={"color": COLORS["muted"], "textAlign": "center",
                  "fontSize": "0.78rem", "marginTop": "8px"})
])


def dark_layout(title):
    return dict(
        title=dict(text=title, font=dict(color=COLORS["text"], size=14), x=0.01),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=COLORS["text"], family="Segoe UI"),
        margin=dict(l=40, r=20, t=45, b=40),
        xaxis=dict(gridcolor="#2a2d3e", linecolor="#2a2d3e"),
        yaxis=dict(gridcolor="#2a2d3e", linecolor="#2a2d3e"),
    )


@app.callback(
    Output("kpi-cards", "children"),
    Output("bar-chart", "figure"),
    Output("pie-chart", "figure"),
    Output("line-chart", "figure"),
    Output("scatter-chart", "figure"),
    Output("player-chart", "figure"),
    Input("season-filter", "value"),
    Input("conf-filter", "value"),
    Input("metric-filter", "value"),
)
def update_all(season, conf, metric):
    dff = df[df["Season"] == season]
    if conf != "All":
        dff = dff[dff["Conference"] == conf]

    # ── KPI Cards ──
    avg_ppg = dff["PPG"].mean()
    avg_wins = dff["Wins"].mean()
    avg_net = dff["Net_Rating"].mean()
    top_team = dff.loc[dff[metric].idxmax(), "Team"]

    def kpi(label, value, color, suffix=""):
        return html.Div([
            html.P(label, style={"color": COLORS["muted"], "fontSize": "0.72rem",
                                  "textTransform": "uppercase", "letterSpacing": "0.1em", "margin": "0 0 6px"}),
            html.H2(f"{value}{suffix}", style={"color": color, "margin": "0", "fontSize": "1.8rem"}),
        ], style=kpi_style)

    kpis = [
        kpi("Avg PPG", round(avg_ppg, 1), COLORS["accent"]),
        kpi("Avg Wins", round(avg_wins, 1), COLORS["blue"]),
        kpi("Avg Net Rating", round(avg_net, 1), COLORS["green"] if avg_net > 0 else COLORS["red"]),
        kpi(f"Top Team ({metric})", top_team, COLORS["accent"]),
    ]

    # ── Bar Chart ──
    dff_sorted = dff.sort_values(metric, ascending=False)
    bar = px.bar(dff_sorted, x="Team", y=metric, color="Conference",
                 color_discrete_map={"East": COLORS["blue"], "West": COLORS["accent"]},
                 hover_data=["Wins", "PPG", "Net_Rating"])
    bar.update_layout(**dark_layout(f"Team {metric} — {season}"))
    bar.update_traces(marker_line_width=0)

    # ── Pie Chart ──
    conf_counts = dff.groupby("Conference")[metric].mean().reset_index()
    pie = px.pie(conf_counts, values=metric, names="Conference",
                 color_discrete_sequence=[COLORS["blue"], COLORS["accent"]],
                 hole=0.45)
    pie.update_layout(**dark_layout(f"Avg {metric} by Conference"))
    pie.update_traces(textfont_color=COLORS["text"])

    # ── Line Chart ── (scoring trend for top 5 teams by wins in selected season)
    top5 = dff.nlargest(5, "Wins")["Team"].tolist()
    dft = df_trend[df_trend["Team"].isin(top5)]
    line = px.line(dft, x="Month", y="PPG", color="Team",
                   markers=True,
                   color_discrete_sequence=px.colors.qualitative.Pastel)
    line.update_layout(**dark_layout("Monthly Scoring Trend — Top 5 Teams"))

    # ── Scatter Chart ──
    scatter = px.scatter(dff, x="PPG", y="Wins", size="Assists",
                         color="Conference", text="Team",
                         color_discrete_map={"East": COLORS["blue"], "West": COLORS["accent"]},
                         hover_data=["Net_Rating", "3PT%"])
    scatter.update_traces(textposition="top center", textfont=dict(size=9))
    scatter.update_layout(**dark_layout("PPG vs Wins (bubble = Assists)"))

    # ── Player Bar ──
    player_fig = go.Figure()
    for stat, color in [("PPG", COLORS["accent"]), ("APG", COLORS["blue"]), ("RPG", COLORS["green"])]:
        player_fig.add_trace(go.Bar(
            name=stat, x=df_players["Player"], y=df_players[stat],
            marker_color=color, marker_line_width=0
        ))
    player_fig.update_layout(**dark_layout("Top Player Stats — PPG / APG / RPG (2023-24)"),
                              barmode="group", legend=dict(orientation="h", y=1.1))

    return kpis, bar, pie, line, scatter, player_fig


if __name__ == "__main__":
    app.run(debug=True)
