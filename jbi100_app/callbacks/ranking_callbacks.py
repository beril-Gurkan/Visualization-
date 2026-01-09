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


def _compute_complex_metrics_scores(w_asf, w_iec, w_scc, w_wsi, w_ers):
    """Compute weighted complex metrics scores for all countries."""
    from jbi100_app.data import (
        available_skilled_workforce,
        industrial_energy_capacity,
        supply_chain_connectivity_score,
        wage_sustainability_index,
        economic_resilience_score,
    )
    
    # Normalize weights
    total = w_asf + w_iec + w_scc + w_wsi + w_ers
    if total == 0:
        w_asf = w_iec = w_scc = w_wsi = w_ers = 0.2
    else:
        w_asf, w_iec, w_scc, w_wsi, w_ers = w_asf/total, w_iec/total, w_scc/total, w_wsi/total, w_ers/total
    
    # Compute each metric
    metrics = {
        'ASF': available_skilled_workforce(),
        'IEC': industrial_energy_capacity(),
        'SCC': supply_chain_connectivity_score(),
        'WSI': wage_sustainability_index(),
        'ERS': economic_resilience_score(),
    }
    
    # Combine into weighted score
    scores = pd.Series(dtype=float)
    for country in set().union(*[s.index for s in metrics.values()]):
        score = (
            metrics['ASF'].get(country, 0) * w_asf +
            metrics['IEC'].get(country, 0) * w_iec +
            metrics['SCC'].get(country, 0) * w_scc +
            metrics['WSI'].get(country, 0) * w_wsi +
            metrics['ERS'].get(country, 0) * w_ers
        )
        scores[country] = score
    
    # Scale to 0-100
    if len(scores) > 0 and scores.max() > scores.min():
        scores = (scores - scores.min()) / (scores.max() - scores.min()) * 100
    
    return scores


@app.callback(
    Output("ranking-title", "children"),
    Output("ranking-bar", "figure"),
    Input("selected_region", "data"),
    Input("ranking-metric", "value"),
    Input("ranking-order", "value"),
    Input("ranking-top-n", "value"),
    Input("selected_country", "data"),
    Input("weight-asf", "value"),
    Input("weight-iec", "value"),
    Input("weight-scc", "value"),
    Input("weight-wsi", "value"),
    Input("weight-ers", "value"),
)
def update_ranking(selected_region, metric, order, top_n, selected_country, w_asf, w_iec, w_scc, w_wsi, w_ers):
    """Update ranking bar chart based on selected metric and weights."""
    
    # Empty state
    if not selected_region:
        fig = go.Figure()
        fig.update_layout(
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            annotations=[dict(text="Select a region on the global map", showarrow=False, x=0.5, y=0.5)],
        )
        return "Ranking (select a region)", fig

    # Get data for selected region
    df = attach_country_meta(get_data())
    df = df[df["region"] == selected_region].copy()

    if df.empty:
        fig = go.Figure()
        fig.update_layout(
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            annotations=[dict(text=f"No countries in {selected_region}", showarrow=False, x=0.5, y=0.5)],
        )
        return f"Ranking — {selected_region}", fig

    # Compute values based on selected metric
    if metric == "Complex_Metrics":
        # Compute complex metrics with current slider weights
        scores = _compute_complex_metrics_scores(w_asf, w_iec, w_scc, w_wsi, w_ers)
        df["value"] = df["Country"].map(scores)
        x_title = "Complex Metrics (0–100)"
        
    else:
        # Standard metric from dataframe
        df["value"] = pd.to_numeric(df.get(metric, pd.Series(dtype=float)), errors="coerce")
        x_title = metric.replace("_", " ")

    # Filter out NaN values
    df = df.dropna(subset=["value"]).copy()
    
    if df.empty:
        fig = go.Figure()
        fig.update_layout(
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            annotations=[dict(text="No data for this metric", showarrow=False, x=0.5, y=0.5)],
        )
        return f"Ranking — {selected_region}", fig

    # Sort and limit to top N
    ascending = (order == "asc")
    df = df.sort_values("value", ascending=ascending).head(int(top_n))
    
    # Reverse the order for display (so highest is at top of chart)
    df = df.iloc[::-1]

    # Highlight selected country
    colors = ["#636EFA" if not selected_country or c != selected_country else "#EF553B" 
              for c in df["Country"]]

    # Create bar chart
    fig = go.Figure(
        go.Bar(
            x=df["value"],
            y=df["country_display"],
            orientation="h",
            customdata=df["Country"].values.reshape(-1, 1),
            hovertemplate="%{y}: %{x:.2f}<extra></extra>",
            marker=dict(color=colors),
        )
    )
    
    fig.update_layout(
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis_title=x_title,
        yaxis_title="",
        height=520,
        showlegend=False,
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
