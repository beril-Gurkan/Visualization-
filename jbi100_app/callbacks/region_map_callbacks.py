import numpy as np
import pandas as pd
import plotly.graph_objects as go

from dash.dependencies import Input, Output
from jbi100_app.app_instance import app
from jbi100_app.data import get_data
from jbi100_app.utils.country_meta import attach_country_meta


REGION_COLORS = {
    "Africa": "#fed9a6",
    "Americas": "#fbb4ae",
    "Asia": "#b2df8a",      # green (doesn’t blend with ocean)
    "Europe": "#decbe4",
    "Oceania": "#ccebc5",
}

# Hard crop bounds (lon, lat) for each region (good-enough world atlas style)
REGION_BOUNDS = {
    "Africa":   {"lon": [-25,  60], "lat": [-40,  40]},
    "Americas": {"lon": [-170, -30], "lat": [-60,  75]},
    "Asia":     {"lon": [  25, 180], "lat": [ -10,  80]},
    "Europe":   {"lon": [ -30,  70], "lat": [  30,  75]},
    "Oceania":  {"lon": [ 110, 180], "lat": [ -50,  15]},
}


# --- Map your UI metric keys to dataframe columns
# If you already have normalized columns in countries_processed.csv (like GDP__norm),
# you can swap the "col" values to those and set normalize=False in compute_scores below.
METRICS = {
    "unemployment": {
        "label": "Unemployment rate",
        "col": "Unemployment_Rate_percent",
        "higher_is_better": False,
    },
    "gdp_pc": {
        "label": "GDP per capita",
        "col": "Real_GDP_per_Capita_USD",
        "higher_is_better": True,
    },
    "youth_unemp": {
        "label": "Youth unemployment rate",
        "col": "Youth_Unemployment_Rate_percent",
        "higher_is_better": False,
    },
    "pop_growth": {
        "label": "Population growth rate",
        "col": "Population_Growth_Rate",
        "higher_is_better": True,
    },
    "elec_access": {
        "label": "Electricity access %",
        "col": "electricity_access_percent",
        "higher_is_better": True,
    },
    "elec_capacity": {
        "label": "Electricity generation capacity (relative)",
        "col": "electricity_generating_capacity_kW",
        "higher_is_better": True,
    },
}


def _blank(msg: str):
    fig = go.Figure()
    fig.update_layout(
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        annotations=[dict(text=msg, showarrow=False, x=0.5, y=0.5)],
    )
    return fig


def _minmax(series: pd.Series, higher_is_better: bool) -> pd.Series:
    s = pd.to_numeric(series, errors="coerce")
    mn, mx = s.min(), s.max()
    if pd.isna(mn) or pd.isna(mx) or mn == mx:
        return pd.Series(np.nan, index=s.index)
    norm = (s - mn) / (mx - mn)
    return norm if higher_is_better else (1 - norm)


def compute_scores(df: pd.DataFrame, selected_keys: list[str], weights: dict[str, float]):
    """
    Strict missing-data policy:
      - drop countries missing any selected metric
    Returns:
      scored_df with columns: Country, iso3, country_display, score
      note: coverage text
    """
    cols = [METRICS[k]["col"] for k in selected_keys]

    work = df[["Country", "iso3", "country_display"] + cols].copy()

    total = len(work)
    work = work.dropna(subset=cols)
    kept = len(work)

    if kept == 0:
        return None, "No countries have complete data for the selected metrics."

    # Normalize each metric within the current filtered set
    for k in selected_keys:
        c = METRICS[k]["col"]
        work[c + "__normtmp"] = _minmax(work[c], METRICS[k]["higher_is_better"])

    # Normalize weights so they sum to 1
    w = np.array([max(0.0, float(weights.get(k, 0.0))) for k in selected_keys], dtype=float)
    if w.sum() == 0:
        w = np.ones(len(selected_keys), dtype=float)
    w = w / w.sum()

    norm_cols = [METRICS[k]["col"] + "__normtmp" for k in selected_keys]
    work["score"] = (work[norm_cols].values * w).sum(axis=1)

    note = f"Included {kept}/{total} countries (excluded {total-kept} due to missing data)."
    return work[["Country", "iso3", "country_display", "score"]], note


# ------------------------------------------------------------------
# IMPORTANT: Adjust the Inputs below if your IDs are named differently
# ------------------------------------------------------------------
@app.callback(
    Output("region-map-title", "children"),
    Output("region-map", "figure"),

    # region/country selection (already in your code)
    Input("selected_region", "data"),
    Input("selected_country", "data"),

    # metric selections (ASSUMED IDs)
    Input("metric-checklist", "value"),       # Economic selections
    Input("metric-checklist-dem", "value"),   # Demographic selections
    Input("metric-checklist-sus", "value"),   # Sustainability selections

    # weights (ASSUMED IDs)
    Input("w-unemployment", "value"),
    Input("w-gdp_pc", "value"),
    Input("w-youth_unemp", "value"),
    Input("w-pop_growth", "value"),
    Input("w-elec_access", "value"),
    Input("w-elec_capacity", "value"),
)
def update_region_map(
    selected_region,
    selected_country,
    econ_sel,
    dem_sel,
    sus_sel,
    w_unemployment,
    w_gdp_pc,
    w_youth_unemp,
    w_pop_growth,
    w_elec_access,
    w_elec_capacity
):
    if not selected_region:
        return "Region Map", _blank("Select a region on the global map")

    df = attach_country_meta(get_data())
    df = df.dropna(subset=["iso3", "region"]).copy()
    df = df[df["region"] == selected_region].copy()

    if df.empty:
        return f"Region Map — {selected_region}", _blank(f"No mappable countries for: {selected_region}")

    # Selected metrics = union of the three checklist groups
    econ_sel = econ_sel or []
    dem_sel = dem_sel or []
    sus_sel = sus_sel or []
    selected_keys = econ_sel + dem_sel + sus_sel

    # Build weights dict
    weights = {
        "unemployment": w_unemployment or 0,
        "gdp_pc": w_gdp_pc or 0,
        "youth_unemp": w_youth_unemp or 0,
        "pop_growth": w_pop_growth or 0,
        "elec_access": w_elec_access or 0,
        "elec_capacity": w_elec_capacity or 0,
    }

    # If no metric selected, fall back to old behavior (static region fill)
    if not selected_keys:
        color = REGION_COLORS.get(selected_region, "#ccebc5")
        fig = go.Figure()
        fig.add_trace(
            go.Choropleth(
                locations=df["iso3"],
                z=[1] * len(df),
                colorscale=[[0, color], [1, color]],
                showscale=False,
                marker_line_color="#333",
                marker_line_width=1.0,
                customdata=list(zip(df["Country"], df["country_display"])),
                hovertemplate="%{customdata[1]}<extra></extra>",
            )
        )
        bounds = REGION_BOUNDS.get(selected_region, {"lon": [-180, 180], "lat": [-60, 85]})
        fig.update_geos(
            projection_type="equirectangular",
            lonaxis=dict(range=bounds["lon"]),
            lataxis=dict(range=bounds["lat"]),
            visible=False,
            bgcolor="white",
        )
        fig.update_layout(dragmode=False, margin=dict(l=0, r=0, t=0, b=0), uirevision=f"region-map-{selected_region}")
        return f"Region Map — {selected_region}", fig

    # Compute weighted scores
    scored, note = compute_scores(df, selected_keys, weights)
    if scored is None:
        return f"Region Map — {selected_region}", _blank(note)

    # Choropleth colored by score
    fig = go.Figure()
    fig.add_trace(
        go.Choropleth(
            locations=scored["iso3"],
            z=scored["score"],
            zmin=0,
            zmax=1,
            colorscale="Blues",
            showscale=True,
            colorbar=dict(title="Score", len=0.6),
            marker_line_color="#333",
            marker_line_width=1.0,
            customdata=list(zip(scored["Country"], scored["country_display"], scored["score"])),
            hovertemplate=(
                "%{customdata[1]}<br>"
                "Score: %{customdata[2]:.3f}"
                "<extra></extra>"
            ),
        )
    )

    # highlight selected country (outline)
    if selected_country:
        row = scored[scored["Country"] == selected_country]
        if not row.empty:
            iso3 = row.iloc[0]["iso3"]
            fig.add_trace(
                go.Choropleth(
                    locations=[iso3],
                    z=[1],
                    colorscale=[[0, "rgba(0,0,0,0)"], [1, "rgba(0,0,0,0)"]],
                    showscale=False,
                    marker_line_color="#000",
                    marker_line_width=3.0,
                    hoverinfo="skip",
                )
            )

    bounds = REGION_BOUNDS.get(selected_region, {"lon": [-180, 180], "lat": [-60, 85]})
    fig.update_geos(
        projection_type="equirectangular",
        lonaxis=dict(range=bounds["lon"]),
        lataxis=dict(range=bounds["lat"]),
        visible=False,
        bgcolor="white",
    )

    fig.update_layout(
        dragmode=False,
        margin=dict(l=0, r=0, t=0, b=0),
        uirevision=f"region-map-{selected_region}",
    )

    title = f"Region Map — {selected_region} (Weighted Score) · {note}"
    return title, fig
