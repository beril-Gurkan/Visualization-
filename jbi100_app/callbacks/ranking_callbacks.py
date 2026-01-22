import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from dash import html
from dash.dependencies import Input, Output

from jbi100_app.app_instance import app
from jbi100_app.data import get_data
from jbi100_app.utils.country_meta import attach_country_meta


METRICS = {
    "unemployment": {"label": "Unemployment rate (%)", "col": "Unemployment_Rate_percent", "higher_is_better": False},
    "gdp_pc": {"label": "GDP per capita (USD)", "col": "Real_GDP_per_Capita_USD", "higher_is_better": True},
    "youth_unemp": {"label": "Youth unemployment (%)", "col": "Youth_Unemployment_Rate_percent", "higher_is_better": False},
    "pop_growth": {"label": "Population growth (%)", "col": "Population_Growth_Rate", "higher_is_better": True},
    "elec_access": {"label": "Electricity access (%)", "col": "electricity_access_percent", "higher_is_better": True},
    "elec_capacity": {"label": "Electricity capacity (kW)", "col": "electricity_generating_capacity_kW", "higher_is_better": True},
}


def _minmax(series: pd.Series, higher_is_better: bool) -> pd.Series:
    s = pd.to_numeric(series, errors="coerce")
    mn, mx = s.min(), s.max()
    if pd.isna(mn) or pd.isna(mx) or mn == mx:
        return pd.Series(np.nan, index=s.index)
    norm = (s - mn) / (mx - mn)
    return norm if higher_is_better else (1 - norm)


def compute_scores(df: pd.DataFrame, selected_keys: list[str], weights: dict[str, float]):
    cols = [METRICS[k]["col"] for k in selected_keys]
    work = df[["Country", "iso3"] + cols].copy()
    total = len(work)

    work = work.dropna(subset=cols)
    kept = len(work)
    if kept == 0:
        return None, "No countries have complete data for the selected metrics."

    for k in selected_keys:
        c = METRICS[k]["col"]
        work[c + "__norm"] = _minmax(work[c], METRICS[k]["higher_is_better"])

    w = np.array([max(0.0, float(weights.get(k, 0.0))) for k in selected_keys], dtype=float)
    if w.sum() == 0:
        w = np.ones(len(selected_keys), dtype=float)
    w = w / w.sum()

    norm_cols = [METRICS[k]["col"] + "__norm" for k in selected_keys]
    work["score"] = (work[norm_cols].values * w).sum(axis=1)

    note = f"Included {kept}/{total} countries (excluded {total-kept} due to missing data)."
    return work[["Country", "iso3", "score"] + cols], note


def _ranking_panel(top: pd.DataFrame, note: str):
    smin, smax = top["score"].min(), top["score"].max()
    denom = (smax - smin) if smax != smin else 1.0

    rows = []
    for i, row in enumerate(top.itertuples(index=False), start=1):
        width_pct = int(100 * ((row.score - smin) / denom))
        rows.append(
            html.Div(
                style={
                    "display": "grid",
                    "gridTemplateColumns": "50px 1fr 90px 140px",
                    "gap": "10px",
                    "alignItems": "center",
                    "padding": "8px 10px",
                    "borderBottom": "1px solid rgba(0,0,0,0.06)",
                },
                children=[
                    html.Div(f"{i}.", style={"opacity": 0.65}),
                    html.Div(row.Country, style={"fontWeight": 700}),
                    html.Div(f"{row.score:.3f}", style={"fontVariantNumeric": "tabular-nums", "opacity": 0.85}),
                    html.Div(
                        style={
                            "height": "10px",
                            "background": "rgba(0,0,0,0.08)",
                            "borderRadius": "999px",
                            "overflow": "hidden",
                        },
                        children=[
                            html.Div(
                                style={
                                    "height": "10px",
                                    "width": f"{width_pct}%",
                                    "background": "#3b82f6",
                                    "borderRadius": "999px",
                                }
                            )
                        ],
                    ),
                ],
            )
        )

    return html.Div(
        style={
            "background": "white",
            "border": "1px solid rgba(0,0,0,0.10)",
            "borderRadius": "12px",
            "padding": "10px 12px",
        },
        children=[
            html.Div(note, style={"opacity": 0.70, "fontSize": "13px", "marginBottom": "8px"}),
            html.Div(rows, style={"overflowY": "auto", "paddingRight": "6px"}),
        ],
    )


@app.callback(
    Output("globe-map", "figure"),
    Output("ranking-container", "children"),
    Input("metric-checklist", "value"),
    Input("metric-checklist-dem", "value"),
    Input("metric-checklist-sus", "value"),
    Input("w-unemployment", "value"),
    Input("w-gdp_pc", "value"),
    Input("w-youth_unemp", "value"),
    Input("w-pop_growth", "value"),
    Input("w-elec_access", "value"),
    Input("w-elec_capacity", "value"),
    Input("topn-dropdown", "value"),
    Input("selected-countries", "data"),
    Input("clear-selected", "n_clicks"),  # ✅ added
)
def update_global_map_and_ranking(
    econ_sel, dem_sel, sus_sel,
    w_unemp, w_gdp, w_youth, w_pop, w_access, w_cap,
    topn_value, selected_countries, clear_clicks
):
    econ_sel = econ_sel or []
    dem_sel = dem_sel or []
    sus_sel = sus_sel or []
    selected_metric_keys = econ_sel + dem_sel + sus_sel

    df = attach_country_meta(get_data()).dropna(subset=["iso3"]).copy()

    if not selected_metric_keys:
        fig = px.choropleth(pd.DataFrame({"iso3": [], "score": []}), locations="iso3", color="score")
        fig.update_geos(projection_type="natural earth", showframe=False, showcoastlines=False, bgcolor="white")
        fig.update_layout(title="Select at least one metric to compute a score.", margin=dict(l=0, r=0, t=60, b=0))
        return fig, html.Div("Select at least one metric to see ranking.", style={"opacity": 0.8})

    weights = {
        "unemployment": w_unemp or 0,
        "gdp_pc": w_gdp or 0,
        "youth_unemp": w_youth or 0,
        "pop_growth": w_pop or 0,
        "elec_access": w_access or 0,
        "elec_capacity": w_cap or 0,
    }

    scored, note = compute_scores(df, selected_metric_keys, weights)
    if scored is None:
        fig = px.choropleth(pd.DataFrame({"iso3": [], "score": []}), locations="iso3", color="score")
        fig.update_layout(title=note, margin=dict(l=0, r=0, t=60, b=0))
        return fig, html.Div(note)

    selected_set = {str(x).strip().upper() for x in (selected_countries or []) if x}
    available = set(scored["iso3"].astype(str).str.upper())
    selected_set = {x for x in selected_set if x in available}

    metric_cols = [METRICS[k]["col"] for k in selected_metric_keys]

    fig = px.choropleth(
        scored,
        locations="iso3",
        color="score",
        hover_name="Country",
        custom_data=metric_cols,
        color_continuous_scale="Blues",
        range_color=(0, 1),
    )

    hover_lines = [f"{METRICS[k]['label']}: %{{customdata[{i}]}}" for i, k in enumerate(selected_metric_keys)]
    hovertemplate = "<b>%{hovertext}</b><br>" + "<br>".join(hover_lines) + "<br><b>Score</b>: %{z:.3f}<extra></extra>"
    fig.update_traces(
        hovertemplate=hovertemplate,
        marker=dict(line=dict(color="rgba(0,0,0,0.28)", width=0.6)),
    )

    # ✅ when nothing selected: full opacity
    base_opacity = 0.9 if not selected_set else 0.35
    fig.update_traces(marker_opacity=base_opacity)

    # ✅ overlay ONLY when selected
    if selected_set:
        fig.add_trace(
            go.Choropleth(
                name="Selected",
                locations=sorted(selected_set),
                z=[1] * len(selected_set),
                showscale=False,
                colorscale=[[0, "#fb923c"], [1, "#fb923c"]],
                marker_line_color="#c2410c",
                marker_line_width=2.2,
                marker_opacity=1.0,
                hoverinfo="skip",
            )
        )

    fig.update_geos(
        projection_type="natural earth",
        showframe=False,
        showcountries=True,
        countrycolor="rgba(0,0,0,0.25)",
        showcoastlines=True,
        coastlinecolor="rgba(0,0,0,0.25)",
        showocean=True,
        oceancolor="white",
        showland=True,
        landcolor="rgb(245,245,245)",
        bgcolor="white",
    )

    # ✅ THIS is the fix: clicking Clear bumps uirevision -> resets plot interaction state
    clear_clicks = clear_clicks or 0

    fig.update_layout(
        title=f"Global Composite Score (weighted) — {note}",
        margin=dict(l=0, r=0, t=60, b=0),
        dragmode="pan",
        hovermode="closest",
        clickmode="event+select",
        uirevision=f"globe-map-clear-{clear_clicks}",
    )

    top = scored.sort_values("score", ascending=False)
    if topn_value != "all":
        top = top.head(int(topn_value) if topn_value else 20)

    return fig, _ranking_panel(top, note)