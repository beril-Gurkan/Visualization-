# Metric cards callbacks - manage the expandable metric visualization cards in detailed view
# Features: histogram + rug plot for each of 5 complex metrics (ASF, IEC, SCC, WSI, ERS)
# Supports: brushing/selection on rug plots, expand/collapse individual cards,
# linked highlighting across cards and scatterplot

from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.graph_objects as go

from dash.dependencies import Input, Output, State
from dash import callback_context

from jbi100_app.app_instance import app
from jbi100_app.data import get_data
from jbi100_app.utils.country_meta import attach_country_meta

# Reuse complex score computation from shared utility
from jbi100_app.utils.complex_scores import compute_complex_scores

# Five complex metrics displayed in cards
METRIC_KEYS = ["ASF", "IEC", "SCC", "WSI", "ERS"]

# Build dataset with all 5 metrics for visualization
def _build_all_metrics_df() -> pd.DataFrame:
    scores_df = compute_complex_scores(
        1, 1, 1, 1, 1,   # dummy equal weights
        True, True, True, True, True
    )

    base = attach_country_meta(get_data()).copy()
    base = base.dropna(subset=["iso3"]).copy()
    base["Country"] = base["Country"].astype(str)
    base["iso3"] = base["iso3"].astype(str).str.upper().str.strip()

    out = base[["Country", "iso3"]].drop_duplicates().merge(scores_df, on="Country", how="inner")
    out = out.dropna(subset=METRIC_KEYS).copy()
    return out


def _empty_fig(message: str) -> go.Figure:
    fig = go.Figure()
    fig.update_layout(
        margin=dict(l=8, r=8, t=10, b=10),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        annotations=[
            dict(
                text=message,
                x=0.5,
                y=0.5,
                xref="paper",
                yref="paper",
                showarrow=False,
                font=dict(size=12),
                opacity=0.85,
            )
        ],
    )
    return fig


def _stable_jitter_from_codes(codes: np.ndarray, scale: float) -> np.ndarray:
    h = np.array([(abs(hash(str(c))) % 1000) / 1000.0 for c in codes], dtype=float)
    return (h - 0.5) * 2.0 * scale


def _metric_card_fig(
    df_all: pd.DataFrame,
    metric_key: str,
    selected_iso3: set[str],
    brushed_iso3: set[str],
    active_iso3: str | None,
    collapsed: bool = False,
    brush_rev: int = 0,
) -> go.Figure:
    if df_all.empty or metric_key not in df_all.columns:
        return _empty_fig("No data available.")

    brushed_iso3 = {str(x).upper().strip() for x in (brushed_iso3 or set()) if x}
    selected_iso3 = {str(x).upper().strip() for x in (selected_iso3 or set()) if x}
    active_iso3 = (str(active_iso3).upper().strip() if active_iso3 else None)

    x_all = df_all[metric_key].to_numpy(dtype=float)
    iso_all = df_all["iso3"].to_numpy()
    country_all = df_all["Country"].to_numpy()

    # Histogram bins over [0,1]
    bins = np.linspace(0, 1, 21)  # 20 bins
    counts, edges = np.histogram(x_all, bins=bins)
    centers = (edges[:-1] + edges[1:]) / 2.0
    bin_w = (edges[1] - edges[0]) * 0.95
    max_count = int(counts.max()) if counts.size else 1

    fig = go.Figure()

    # Base histogram
    fig.add_trace(
        go.Bar(
            x=centers,
            y=counts,
            width=bin_w,
            marker=dict(color="rgba(148,163,184,0.55)"),
            hovertemplate=f"{metric_key}: %{{x:.2f}}<br>Count: %{{y}}<extra></extra>",
            name="All countries",
        )
    )

    # Highlight bins containing selected countries
    if selected_iso3:
        sel_mask = np.isin(iso_all, list(selected_iso3))
        x_sel_for_bins = x_all[sel_mask]
        if x_sel_for_bins.size > 0:
            idx = np.digitize(x_sel_for_bins, bins) - 1
            idx = np.clip(idx, 0, len(centers) - 1)
            selected_bins = np.zeros_like(counts, dtype=bool)
            selected_bins[np.unique(idx)] = True

            fig.add_trace(
                go.Bar(
                    x=centers[selected_bins],
                    y=counts[selected_bins],
                    width=bin_w,
                    marker=dict(color="rgba(251,146,60,0.35)"),
                    hoverinfo="skip",
                    name="Selected bins",
                )
            )

    # Highlight bin containing ACTIVE (clicked) country (green)
    if active_iso3:
        act_row = df_all[df_all["iso3"] == active_iso3]
        if not act_row.empty:
            x_act = float(act_row.iloc[0][metric_key])
            act_idx = np.digitize([x_act], bins) - 1
            act_idx = int(np.clip(act_idx[0], 0, len(centers) - 1))

            fig.add_trace(
                go.Bar(
                    x=[centers[act_idx]],
                    y=[counts[act_idx]],
                    width=bin_w,
                    marker=dict(color="rgba(34,197,94,0.45)"),
                    hoverinfo="skip",
                    name="Active bin",
                )
            )

    # Median line
    global_median = float(np.nanmedian(x_all))
    fig.add_vline(
        x=global_median,
        line_width=2,
        line_dash="dot",
        line_color="rgba(0,0,0,0.55)",
    )

    # Collapsed: histogram only
    if collapsed:
        fig.update_layout(
            margin=dict(l=2, r=2, t=2, b=2),
            showlegend=False,
            hovermode="closest",
            dragmode=False,
            barmode="overlay",
            xaxis=dict(
                range=[0, 1],
                showticklabels=False,
                ticks="",
                title="",
                showgrid=False,
                zeroline=False,
            ),
            yaxis=dict(
                range=[0, max_count * 1.10],
                showticklabels=False,
                title="",
                showgrid=False,
                zeroline=False,
            ),
            uirevision=f"{metric_key}-collapsed-{brush_rev}",
        )
        return fig

    # Expanded: add rug + brushing visuals
    x_jit_all = _stable_jitter_from_codes(iso_all, scale=0.006)
    y_all = _stable_jitter_from_codes(iso_all, scale=0.30)

    sel_mask = np.isin(iso_all, list(selected_iso3))
    x_sel_raw = x_all[sel_mask]
    iso_sel = iso_all[sel_mask]
    country_sel = country_all[sel_mask]
    x_jit_sel = _stable_jitter_from_codes(iso_sel, scale=0.004)
    y_sel = _stable_jitter_from_codes(iso_sel, scale=0.22)

    has_brush = len(brushed_iso3) > 0
    brushed_mask_all = np.isin(iso_all, list(brushed_iso3))
    brushed_mask_sel = np.isin(iso_sel, list(brushed_iso3))

    active_mask_all = (iso_all == active_iso3) if active_iso3 else np.zeros(len(iso_all), dtype=bool)
    active_mask_sel = (iso_sel == active_iso3) if active_iso3 else np.zeros(len(iso_sel), dtype=bool)

    base_op_all = np.where(brushed_mask_all, 0.85, 0.25 if has_brush else 0.25)
    base_sz_all = np.where(brushed_mask_all, 9, 6)
    base_lw_all = np.where(brushed_mask_all, 2.2, 0.4)

    base_op_sel = np.where(brushed_mask_sel, 0.95, 0.15 if has_brush else 0.70)
    base_sz_sel = np.where(brushed_mask_sel, 12, 9)
    base_lw_sel = np.where(brushed_mask_sel, 3.0, 1.0)

    colors_all = np.array(["rgba(100,116,139,0.55)"] * len(iso_all), dtype=object)
    colors_sel = np.array(["#fb923c"] * len(iso_sel), dtype=object)

    if active_iso3:
        colors_all[active_mask_all] = "#22c55e"
        colors_sel[active_mask_sel] = "#22c55e"

        base_op_all[active_mask_all] = 0.5
        base_sz_all[active_mask_all] = 12
        base_lw_all[active_mask_all] = 1

        base_op_sel[active_mask_sel] = 0.5
        base_sz_sel[active_mask_sel] = 14
        base_lw_sel[active_mask_sel] = 1

    # Rug: all
    fig.add_trace(
        go.Scatter(
            x=np.clip(x_all + x_jit_all, 0, 1),
            y=y_all,
            mode="markers",
            customdata=np.stack([country_all, iso_all], axis=1),
            hovertemplate=(
                "<b>%{customdata[0]}</b><br>"
                "ISO3: %{customdata[1]}<br>"
                f"{metric_key}: %{{x:.2f}}<extra></extra>"
            ),
            marker=dict(
                color=colors_all,
                size=base_sz_all,
                opacity=base_op_all,
                line=dict(color="rgba(0,0,0,0.45)", width=base_lw_all),
            ),
            name="All (rug)",
            yaxis="y2",
        )
    )

    # Rug: selected countries
    fig.add_trace(
        go.Scatter(
            x=np.clip(x_sel_raw + x_jit_sel, 0, 1),
            y=y_sel,
            mode="markers",
            customdata=np.stack([country_sel, iso_sel], axis=1),
            hovertemplate=(
                "<b>%{customdata[0]}</b><br>"
                "ISO3: %{customdata[1]}<br>"
                f"{metric_key}: %{{x:.2f}}<extra></extra>"
            ),
            marker=dict(
                color=colors_sel,
                size=base_sz_sel,
                opacity=base_op_sel,
                line=dict(color="rgba(0,0,0,0.75)", width=base_lw_sel),
            ),
            name="Selected",
            yaxis="y2",
        )
    )

    fig.update_layout(
        margin=dict(l=2, r=2, t=2, b=2),
        dragmode="select",
        showlegend=False,
        hovermode="closest",
        xaxis=dict(range=[0, 1], tickfont=dict(size=10), title=""),
        yaxis=dict(
            domain=[0.25, 1.0],
            range=[0, max_count * 1.10],
            showticklabels=False,
            zeroline=False,
            title="",
            showgrid=True,
        ),
        yaxis2=dict(
            domain=[0.0, 0.20],
            range=[-1.0, 1.0],
            showticklabels=False,
            zeroline=False,
            title="",
            showgrid=False,
        ),
        barmode="overlay",
        uirevision=f"{metric_key}-expanded-{brush_rev}",
    )

    return fig


# Brush revision
@app.callback(
    Output("metric-brush-rev", "data"),
    Input("metric-brush", "data"),
    State("metric-brush-rev", "data"),
)
def bump_brush_revision(_brush, rev):
    """Increment revision any time brush changes so plotly clears selection artifacts."""
    rev = int(rev or 0)
    return rev + 1


# Metric cards figures
@app.callback(
    Output("metric-card-asf", "figure"),
    Output("metric-card-iec", "figure"),
    Output("metric-card-scc", "figure"),
    Output("metric-card-wsi", "figure"),
    Output("metric-card-ers", "figure"),
    Input("selected-countries", "data"),
    Input("metric-brush", "data"),
    Input("metric-brush-rev", "data"),
    Input("expanded-metric", "data"),
    Input("selected_country", "data"),
)
def update_metric_cards(selected_countries, brushed, brush_rev, expanded_metric, clicked_country):
    df_all = _build_all_metrics_df()

    selected_set = {str(x).upper().strip() for x in (selected_countries or []) if x}
    brushed_set = {str(x).upper().strip() for x in (brushed or []) if x}

    active_iso3 = None
    if clicked_country:
        cc = str(clicked_country).upper().strip()
        if "iso3" in df_all.columns and (df_all["iso3"] == cc).any():
            active_iso3 = cc
        else:
            m = df_all[df_all["Country"].astype(str).str.upper() == cc]
            if not m.empty:
                active_iso3 = str(m.iloc[0]["iso3"]).upper().strip()

    expanded_metric = (expanded_metric or "").strip().upper()

    def is_collapsed(key: str) -> bool:
        return bool(expanded_metric) and expanded_metric != key

    brush_rev = int(brush_rev or 0)

    return (
        _metric_card_fig(df_all, "ASF", selected_set, brushed_set, active_iso3, collapsed=is_collapsed("ASF"), brush_rev=brush_rev),
        _metric_card_fig(df_all, "IEC", selected_set, brushed_set, active_iso3, collapsed=is_collapsed("IEC"), brush_rev=brush_rev),
        _metric_card_fig(df_all, "SCC", selected_set, brushed_set, active_iso3, collapsed=is_collapsed("SCC"), brush_rev=brush_rev),
        _metric_card_fig(df_all, "WSI", selected_set, brushed_set, active_iso3, collapsed=is_collapsed("WSI"), brush_rev=brush_rev),
        _metric_card_fig(df_all, "ERS", selected_set, brushed_set, active_iso3, collapsed=is_collapsed("ERS"), brush_rev=brush_rev),
    )


# Brush store: metric cards OR detailed scatterplot
@app.callback(
    Output("metric-brush", "data"),
    Input("metric-card-asf", "selectedData"),
    Input("metric-card-iec", "selectedData"),
    Input("metric-card-scc", "selectedData"),
    Input("metric-card-wsi", "selectedData"),
    Input("metric-card-ers", "selectedData"),
    Input("detailed-scatterplot", "selectedData"),
    Input("detailed-scatterplot", "relayoutData"),  # detect double-click reset
    Input("metric-brush-clear", "n_clicks"),
    State("metric-brush", "data"),
    prevent_initial_call=True,
)
def store_metric_brush(
    sel_asf, sel_iec, sel_scc, sel_wsi, sel_ers,
    sel_scatter, scatter_relayout, clear_clicks, current_brush
):
    """
    Stores the brushed ISO3s from *rug/scatter point* selection.

    Rules:
    - Histogram bar-only selections produce selectedData with no [Country, ISO3] customdata: keep current brush.
    - Clear button resets brush to [].
    - Double-click reset in scatterplot (relayoutData autorange) resets brush to [].
    """
    trig = callback_context.triggered_id
    current_brush = current_brush or []

    if trig == "metric-brush-clear" and clear_clicks:
        return []

    if trig == "detailed-scatterplot" and isinstance(scatter_relayout, dict):
        if scatter_relayout.get("xaxis.autorange") or scatter_relayout.get("yaxis.autorange"):
            return []

    selectedData = None
    if trig == "metric-card-asf":
        selectedData = sel_asf
    elif trig == "metric-card-iec":
        selectedData = sel_iec
    elif trig == "metric-card-scc":
        selectedData = sel_scc
    elif trig == "metric-card-wsi":
        selectedData = sel_wsi
    elif trig == "metric-card-ers":
        selectedData = sel_ers
    elif trig == "detailed-scatterplot":
        selectedData = sel_scatter

    if not selectedData or "points" not in selectedData:
        return current_brush

    iso3s: list[str] = []
    for p in selectedData["points"]:
        cd = p.get("customdata")
        if isinstance(cd, (list, tuple)) and len(cd) >= 2:
            iso3s.append(str(cd[1]).upper().strip())

    iso3s = [x for x in iso3s if x]
    if not iso3s:
        return current_brush

    return sorted(set(iso3s))
