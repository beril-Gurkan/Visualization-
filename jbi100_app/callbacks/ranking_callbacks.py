import pandas as pd
from dash import ctx
from dash.dependencies import Input, Output, State

from jbi100_app.main import app
from jbi100_app.data import get_data
from jbi100_app.utils.country_meta import attach_country_meta


def _compute_complex_metrics_scores(w_asf, w_iec, w_scc, w_wsi, w_ers):
    """Compute weighted complex metrics scores for all countries (0–100)."""
    from jbi100_app.data import (
        available_skilled_workforce,
        industrial_energy_capacity,
        supply_chain_connectivity_score,
        wage_sustainability_index,
        economic_resilience_score,
    )

    total = (w_asf or 0) + (w_iec or 0) + (w_scc or 0) + (w_wsi or 0) + (w_ers or 0)
    if total == 0:
        w_asf = w_iec = w_scc = w_wsi = w_ers = 0.2
    else:
        w_asf, w_iec, w_scc, w_wsi, w_ers = (
            w_asf / total,
            w_iec / total,
            w_scc / total,
            w_wsi / total,
            w_ers / total,
        )

    metrics = {
        "ASF": available_skilled_workforce(),
        "IEC": industrial_energy_capacity(),
        "SCC": supply_chain_connectivity_score(),
        "WSI": wage_sustainability_index(),
        "ERS": economic_resilience_score(),
    }

    all_countries = set().union(*[s.index for s in metrics.values()])
    scores = pd.Series(index=sorted(all_countries), dtype=float)

    for c in scores.index:
        scores.loc[c] = (
            metrics["ASF"].get(c, 0) * w_asf
            + metrics["IEC"].get(c, 0) * w_iec
            + metrics["SCC"].get(c, 0) * w_scc
            + metrics["WSI"].get(c, 0) * w_wsi
            + metrics["ERS"].get(c, 0) * w_ers
        )

    if len(scores) > 0 and scores.max() > scores.min():
        scores = (scores - scores.min()) / (scores.max() - scores.min()) * 100.0
    return scores


@app.callback(
    Output("ranking-title", "children"),
    Output("ranking-table", "data"),
    Output("ranking-table", "columns"),
    Output("ranking-table", "style_data_conditional"),
    Output("ranking-hint", "children"),
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
def update_ranking_table(selected_region, metric, order, top_n, selected_country, w_asf, w_iec, w_scc, w_wsi, w_ers):
    title = "Rankings"
    zebra = [{"if": {"row_index": "odd"}, "backgroundColor": "rgba(0,0,0,0.02)"}]

    if not selected_region:
        return title, [], [], zebra, "Select a region on the global map to populate rankings."

    selected_region = str(selected_region).strip()

    try:
        df = attach_country_meta(get_data())
    except Exception as e:
        return title, [], [], zebra, f"Error loading data: {e}"

    df = df[df["region"] == selected_region].copy()
    if df.empty:
        return title, [], [], zebra, f"No countries found for region '{selected_region}'."

    if metric == "Complex_Metrics":
        scores = _compute_complex_metrics_scores(w_asf, w_iec, w_scc, w_wsi, w_ers)
        df["value"] = df["Country"].map(scores)
        value_label = "Complex Metrics (0–100)"
    else:
        if metric not in df.columns:
            return title, [], [], zebra, f"Metric '{metric}' not found in data."
        df["value"] = pd.to_numeric(df[metric], errors="coerce")
        value_label = metric.replace("_", " ")

    df = df.dropna(subset=["value"]).copy()
    if df.empty:
        return title, [], [], zebra, f"No non-missing values for '{value_label}' in '{selected_region}'."

    ascending = (order == "asc")
    df = df.sort_values("value", ascending=ascending)

    if top_n != "all":
        df = df.head(int(top_n))

    df = df.reset_index(drop=True)
    df["Rank"] = range(1, len(df) + 1)

    rows = []
    for i in range(len(df)):
        rows.append(
            {
                "Rank": int(df.loc[i, "Rank"]),
                "Country": df.loc[i, "country_display"],
                "Value": df.loc[i, "value"],
                "__country_raw__": df.loc[i, "Country"],
            }
        )

    columns = [
        {"name": "Rank", "id": "Rank"},
        {"name": "Country", "id": "Country"},
        {"name": value_label, "id": "Value"},
    ]

    # purely visual highlight (selection still comes from map / clear button)
    style_cond = list(zebra)
    if selected_country:
        idxs = df.index[df["Country"] == selected_country].tolist()
        if idxs:
            style_cond.append(
                {
                    "if": {"row_index": int(idxs[0])},
                    "backgroundColor": "rgba(239, 85, 59, 0.15)",
                    "fontWeight": "700",
                }
            )

    hint = f"Showing {len(rows)} countries in {selected_region} ranked by '{value_label}'. Selection is done via the map (not the table)."
    return title, rows, columns, style_cond, hint


@app.callback(
    Output("selected_country", "data"),
    Input("region-map", "clickData"),
    Input("btn-clear-country", "n_clicks"),
    Input("selected_region", "data"),
    State("selected_country", "data"),
    prevent_initial_call=True,
)
def update_selected_country(region_map_click, clear_clicks, selected_region, current_country):
    # region change clears selection
    if ctx.triggered_id == "selected_region":
        return None

    # clear button
    if ctx.triggered_id == "btn-clear-country":
        return None

    # map click toggles selection
    if ctx.triggered_id == "region-map" and region_map_click and region_map_click.get("points"):
        cd = region_map_click["points"][0].get("customdata", [None, None])
        country = cd[0] if isinstance(cd, (list, tuple)) and len(cd) > 0 else None
        if not country:
            return current_country
        return None if country == current_country else country

    return current_country
