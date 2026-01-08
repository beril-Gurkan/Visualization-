import numpy as np
import pandas as pd
import plotly.graph_objects as go

from dash import ctx
from dash.dependencies import Input, Output, State
from jbi100_app.main import app
from jbi100_app.data import get_data
from jbi100_app.utils.country_meta import attach_country_meta


def _winsorize(s: pd.Series, lower=0.05, upper=0.95) -> pd.Series:
    s = pd.to_numeric(s, errors="coerce")
    lo = s.quantile(lower)
    hi = s.quantile(upper)
    return s.clip(lo, hi)


def _zscore(s: pd.Series) -> pd.Series:
    s = s.astype(float)
    mu = s.mean()
    sd = s.std(ddof=0)
    if sd == 0 or np.isnan(sd):
        return s * 0.0
    return (s - mu) / sd


def _composite_score(df: pd.DataFrame) -> pd.Series:
    # Outlier-robust composite: winsorize + z-score + average, rescaled to 0..100.
    # Higher better: GDPpc, literacy, electricity
    # Lower better: unemployment, debt
    components = [
        ("Real_GDP_per_Capita_USD", +1, True),
        ("Total_Literacy_Rate", +1, False),
        ("electricity_access_percent", +1, False),
        ("Unemployment_Rate_percent", -1, False),
        ("Public_Debt_percent_of_GDP", -1, False),
    ]

    zs = []
    for col, direction, log1p in components:
        if col not in df.columns:
            continue
        base = pd.to_numeric(df[col], errors="coerce")
        if log1p:
            base = np.log1p(base)
        base = _winsorize(base)
        zs.append(_zscore(base) * direction)

    if not zs:
        return pd.Series(np.nan, index=df.index)

    score = pd.concat(zs, axis=1).mean(axis=1)
    mn, mx = score.min(), score.max()
    if pd.isna(mn) or pd.isna(mx) or mx == mn:
        return pd.Series(50.0, index=df.index)
    return (score - mn) / (mx - mn) * 100.0


@app.callback(
    Output("ranking-title", "children"),
    Output("ranking-bar", "figure"),
    Input("selected_region", "data"),
    Input("ranking-metric", "value"),
    Input("ranking-order", "value"),
    Input("ranking-top-n", "value"),
    Input("selected_country", "data"),
)
def update_ranking(selected_region, metric, order, top_n, selected_country):
    if not selected_region:
        fig = go.Figure()
        fig.update_layout(
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            annotations=[dict(text="Select a region on the global map", showarrow=False, x=0.5, y=0.5)],
        )
        return "Ranking (select a region)", fig

    df = attach_country_meta(get_data())
    df = df[df["region"] == selected_region].copy()

    if df.empty:
        fig = go.Figure()
        fig.update_layout(
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            annotations=[dict(text=f"No countries for region: {selected_region}", showarrow=False, x=0.5, y=0.5)],
        )
        return f"Ranking — {selected_region}", fig

    if metric == "Composite_Score":
        df["value"] = _composite_score(df)
        x_title = "Composite Score (0–100)"
    else:
        if metric not in df.columns:
            df["value"] = np.nan
        else:
            df["value"] = pd.to_numeric(df[metric], errors="coerce")
        x_title = metric.replace("_", " ")

    df = df.dropna(subset=["value"]).copy()
    if df.empty:
        fig = go.Figure()
        fig.update_layout(
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            annotations=[dict(text="No values for this metric in this region.", showarrow=False, x=0.5, y=0.5)],
        )
        return f"Ranking — {selected_region}", fig

    ascending = (order == "asc")
    df = df.sort_values("value", ascending=ascending).head(int(top_n))

    line_width = [3 if (selected_country and c == selected_country) else 0 for c in df["Country"]]

    fig = go.Figure(
        go.Bar(
            x=df["value"],
            y=df["country_display"],
            orientation="h",
            customdata=np.stack([df["Country"]], axis=-1),
            hovertemplate="%{y}<br>%{x}<extra></extra>",
            marker=dict(line=dict(width=line_width)),
        )
    )
    fig.update_layout(
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis_title=x_title,
        yaxis_title="",
        height=520,
    )

    return f"Ranking — {selected_region}", fig


@app.callback(
    Output("selected_country", "data"),
    Input("ranking-bar", "clickData"),
    Input("selected_region", "data"),
    State("selected_country", "data"),
    prevent_initial_call=True,
)
def update_selected_country(ranking_click, selected_region, current_country):
    if ctx.triggered_id == "selected_region":
        return None

    if ctx.triggered_id == "ranking-bar" and ranking_click and ranking_click.get("points"):
        country = ranking_click["points"][0].get("customdata", [None])[0]
        return country or current_country

    return current_country
