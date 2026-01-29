"""
Callbacks for the detailed view panels:
- Complex Metrics Panel (toggleable metrics with weights)
- Ranking Panel (bar chart + scatterplot)
- Plot Panel (radar chart and country profile)
- Detailed Info Panel (key statistics)
"""

import pandas as pd
import plotly.graph_objects as go

from dash.dependencies import Input, Output
from dash import html, dcc, callback_context

from jbi100_app.app_instance import app
from jbi100_app.data import (
    get_data,
    available_skilled_workforce,
    industrial_energy_capacity,
    supply_chain_connectivity_score,
    wage_sustainability_index,
    economic_resilience_score,
)
from jbi100_app.utils.country_meta import attach_country_meta
from jbi100_app.views.detailed_view.scatterplot import Scatterplot
from jbi100_app.utils.complex_scores import compute_complex_scores

# Color constants
COLOR_DEFAULT = "#94a3b8"   # Gray for non-selected countries
COLOR_SELECTED = "#f97316"  # Orange for selected countries
COLOR_CLICKED = "#22c55e"   # Green for clicked/active country


def _compute_complex_scores(
    w_asf, w_iec, w_scc, w_wsi, w_ers,
    t_asf, t_iec, t_scc, t_wsi, t_ers
):
    return compute_complex_scores(
        w_asf, w_iec, w_scc, w_wsi, w_ers,
        t_asf, t_iec, t_scc, t_wsi, t_ers
    )


def _extract_country_iso3_from_click(clickData):
    """
    Returns (country_name, iso3) if possible.
    - scatterplot customdata is expected: [Country, iso3]
    - ranking bar customdata is expected: [Country, iso3, rank]
    """
    if not clickData:
        return None, None
    pts = clickData.get("points") or []
    if not pts:
        return None, None

    cd = pts[0].get("customdata")
    if isinstance(cd, (list, tuple)) and len(cd) >= 2:
        return str(cd[0]), str(cd[1])
    if isinstance(cd, (list, tuple)) and len(cd) >= 1:
        return str(cd[0]), (str(cd[1]) if len(cd) >= 2 else None)
    if isinstance(cd, str):
        return cd, None
    return None, None


# ===== DETAILED RANKING BAR CHART =====
@app.callback(
    Output("detailed-ranking-bar", "figure"),
    Input("selected-countries", "data"),
    Input("selected_country", "data"),
    Input("detailed-ranking-metric", "value"),
    Input("weight-asf", "value"),
    Input("weight-iec", "value"),
    Input("weight-scc", "value"),
    Input("weight-wsi", "value"),
    Input("weight-ers", "value"),
    Input("toggle-asf", "value"),
    Input("toggle-iec", "value"),
    Input("toggle-scc", "value"),
    Input("toggle-wsi", "value"),
    Input("toggle-ers", "value"),
)
def update_detailed_ranking(
    selected_countries, clicked_country, metric,
    w_asf, w_iec, w_scc, w_wsi, w_ers,
    t_asf, t_iec, t_scc, t_wsi, t_ers
):
    selected_countries = selected_countries or []

    t_asf = bool(t_asf)
    t_iec = bool(t_iec)
    t_scc = bool(t_scc)
    t_wsi = bool(t_wsi)
    t_ers = bool(t_ers)

    df = attach_country_meta(get_data())

    if df.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=13, color="#888"),
        )
        fig.update_layout(margin=dict(l=10, r=10, t=10, b=10))
        return fig

    selected_set = {str(x).upper().strip() for x in selected_countries if x}

    if clicked_country:
        clicked_country = str(clicked_country).upper().strip()

    if metric == "Complex_Metrics":
        scores_df = _compute_complex_scores(
            w_asf, w_iec, w_scc, w_wsi, w_ers,
            t_asf, t_iec, t_scc, t_wsi, t_ers,
        )
        df = df.merge(scores_df[["Country", "Complex_Score"]], on="Country", how="left")
        metric_col = "Complex_Score"
        metric_label = "Complex Score"
    else:
        metric_col = metric
        metric_label = metric.replace("_", " ")

    df_all = df.dropna(subset=[metric_col]).copy()

    if df_all.empty:
        fig = go.Figure()
        fig.add_annotation(
            text=f"No {metric_label} data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=13, color="#888"),
        )
        fig.update_layout(margin=dict(l=10, r=10, t=10, b=10))
        return fig

    df_all = df_all.sort_values(by=metric_col, ascending=False).reset_index(drop=True)
    df_all["rank"] = range(1, len(df_all) + 1)

    highlighted_indices = set()

    for idx, row in df_all.iterrows():
        country_upper = str(row["Country"]).upper()
        iso3_upper = str(row.get("iso3", "")).upper() if pd.notna(row.get("iso3")) else ""
        if country_upper in selected_set or iso3_upper in selected_set:
            highlighted_indices.add(idx)

    if clicked_country:
        for idx, row in df_all.iterrows():
            country_upper = str(row["Country"]).upper()
            iso3_upper = str(row.get("iso3", "")).upper() if pd.notna(row.get("iso3")) else ""
            if country_upper == clicked_country or iso3_upper == clicked_country:
                highlighted_indices.add(idx)
                break

    target_count = 15

    if not highlighted_indices:
        indices_to_show = list(range(min(target_count, len(df_all))))
    else:
        sorted_highlighted = sorted(highlighted_indices)
        indices_to_show = list(sorted_highlighted)

        remaining_slots = target_count - len(sorted_highlighted)
        filler_indices = []
        for idx in range(len(df_all)):
            if idx not in highlighted_indices:
                filler_indices.append(idx)
                if len(filler_indices) >= remaining_slots:
                    break

        indices_to_show = sorted(set(indices_to_show + filler_indices))

        if len(indices_to_show) > target_count:
            final_indices = list(sorted_highlighted)
            for idx in filler_indices:
                if len(final_indices) >= target_count:
                    break
                final_indices.append(idx)
            indices_to_show = sorted(final_indices)

    skip_positions = []
    for i in range(1, len(indices_to_show)):
        if indices_to_show[i] - indices_to_show[i - 1] > 1:
            skip_positions.append(i)
    if indices_to_show and indices_to_show[-1] < len(df_all) - 1:
        skip_positions.append(len(indices_to_show))

    countries_list = []
    values_list = []
    colors_list = []
    customdata_list = []
    hovertext_list = []

    skip_set = set(skip_positions)

    for i, idx in enumerate(indices_to_show):
        if i in skip_set:
            if i > 0:
                skipped_count = indices_to_show[i] - indices_to_show[i - 1] - 1
            else:
                skipped_count = indices_to_show[i]
            if skipped_count > 0:
                countries_list.append(f"... ({skipped_count} skipped)")
                values_list.append(0)
                colors_list.append("#e5e5e5")
                customdata_list.append(["", "", ""])
                hovertext_list.append(f"{skipped_count} countries not shown")

        row = df_all.loc[idx]
        country = row["Country"]
        country_upper = str(country).upper()
        iso3_upper = str(row.get("iso3", "")).upper() if pd.notna(row.get("iso3")) else ""

        countries_list.append(country)
        values_list.append(row[metric_col])
        customdata_list.append([country, row.get("iso3", ""), row.get("rank", "")])

        is_clicked = clicked_country and (country_upper == clicked_country or iso3_upper == clicked_country)
        is_selected = (country_upper in selected_set) or (iso3_upper in selected_set)

        if is_clicked:
            colors_list.append(COLOR_CLICKED)
            hovertext_list.append(
                f"<b>{country}</b><br>{metric_label}: {row[metric_col]:.3f}<br>"
                f"Rank: #{row['rank']}<br><i>Currently viewing</i>"
            )
        elif is_selected:
            colors_list.append(COLOR_SELECTED)
            hovertext_list.append(
                f"<b>{country}</b><br>{metric_label}: {row[metric_col]:.3f}<br>"
                f"Rank: #{row['rank']}<br><i>Selected on map</i>"
            )
        else:
            colors_list.append(COLOR_DEFAULT)
            hovertext_list.append(
                f"<b>{country}</b><br>{metric_label}: {row[metric_col]:.3f}<br>Rank: #{row['rank']}"
            )

    if len(indices_to_show) in skip_set and indices_to_show:
        skipped_count = len(df_all) - 1 - indices_to_show[-1]
        if skipped_count > 0:
            countries_list.append(f"... ({skipped_count} more)")
            values_list.append(0)
            colors_list.append("#e5e5e5")
            customdata_list.append(["", "", ""])
            hovertext_list.append(f"{skipped_count} more countries not shown")

    countries_list = countries_list[::-1]
    values_list = values_list[::-1]
    colors_list = colors_list[::-1]
    customdata_list = customdata_list[::-1]
    hovertext_list = hovertext_list[::-1]

    fig = go.Figure(
        go.Bar(
            x=values_list,
            y=countries_list,
            orientation="h",
            marker_color=colors_list,
            marker_line_width=0,
            customdata=customdata_list,
            hovertext=hovertext_list,
            hovertemplate="%{hovertext}<extra></extra>",
        )
    )

    title_text = metric_label
    total_countries = len(df_all)
    num_actual_countries = len(indices_to_show)
    if num_actual_countries < total_countries:
        title_text += f" ({num_actual_countries} of {total_countries} countries)"

    fig.update_layout(
        margin=dict(l=5, r=10, t=30, b=25),
        height=450,
        xaxis_title=metric_label,
        xaxis_title_font_size=10,
        yaxis=dict(automargin=True, tickfont=dict(size=9), fixedrange=True),
        clickmode="event+select",
        hovermode="closest",
        bargap=0.12,
        title=dict(text=title_text, font=dict(size=11), x=0.5, xanchor="center"),
    )

    return fig


# ===== SCATTERPLOT (built on Scatterplot component) =====
@app.callback(
    Output("detailed-scatterplot", "figure"),
    Output("scatterplot-subtitle", "children"),
    Input("selected-countries", "data"),
    Input("selected_country", "data"),
    Input("metric-brush", "data"),
    Input("metric-brush-rev", "data"),
    Input("scatter-x-axis", "value"),
    Input("scatter-y-axis", "value"),
    Input("weight-asf", "value"),
    Input("weight-iec", "value"),
    Input("weight-scc", "value"),
    Input("weight-wsi", "value"),
    Input("weight-ers", "value"),
    Input("toggle-asf", "value"),
    Input("toggle-iec", "value"),
    Input("toggle-scc", "value"),
    Input("toggle-wsi", "value"),
    Input("toggle-ers", "value"),
)
def update_detailed_scatterplot(
    selected_countries, clicked_country, brushed_iso3, brush_rev,
    x_axis, y_axis,
    w_asf, w_iec, w_scc, w_wsi, w_ers,
    t_asf, t_iec, t_scc, t_wsi, t_ers
):
    selected_countries = selected_countries or []
    brushed_set = {str(x).upper().strip() for x in (brushed_iso3 or []) if x}
    has_brush = len(brushed_set) > 0

    axis_labels = {
        "ASF": "Skilled Workforce",
        "IEC": "Energy Capacity",
        "SCC": "Supply Chain",
        "WSI": "Wage Sustainability",
        "ERS": "Economic Resilience",
    }
    x_label = axis_labels.get(x_axis, x_axis)
    y_label = axis_labels.get(y_axis, y_axis)

    scores_df = _compute_complex_scores(
        w_asf, w_iec, w_scc, w_wsi, w_ers,
        bool(t_asf), bool(t_iec), bool(t_scc), bool(t_wsi), bool(t_ers)
    )

    if scores_df.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=12, color="#888"),
        )
        fig.update_layout(margin=dict(l=20, r=20, t=0, b=20))
        return fig, ""

    df = attach_country_meta(get_data())
    df_plot = df.merge(scores_df, on="Country", how="left")

    if x_axis not in df_plot.columns or y_axis not in df_plot.columns:
        fig = go.Figure()
        fig.add_annotation(
            text="Selected metrics not available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=12, color="#888"),
        )
        fig.update_layout(margin=dict(l=20, r=20, t=0, b=20))
        return fig, ""

    df_plot = df_plot.dropna(subset=[x_axis, y_axis, "iso3"]).copy()
    if df_plot.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No data for selected metrics",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=12, color="#888"),
        )
        fig.update_layout(margin=dict(l=20, r=20, t=0, b=20))
        return fig, ""

    selected_set = {str(x).upper().strip() for x in selected_countries if x}

    active_iso3 = None
    if clicked_country:
        cc = str(clicked_country).upper().strip()
        if (df_plot["iso3"].astype(str).str.upper() == cc).any():
            active_iso3 = cc
        else:
            m = df_plot[df_plot["Country"].astype(str).str.upper() == cc]
            if not m.empty:
                active_iso3 = str(m.iloc[0]["iso3"]).upper().strip()

    country_upper = df_plot["Country"].astype(str).str.upper()
    iso_upper = df_plot["iso3"].astype(str).str.upper()

    selected_country_names = set(df_plot.loc[country_upper.isin(selected_set), "Country"].astype(str))
    selected_country_names |= set(df_plot.loc[iso_upper.isin(selected_set), "Country"].astype(str))

    if x_axis == y_axis:
        base_df = df_plot[["Country", x_axis, "iso3"]].copy()
    else:
        base_df = df_plot[["Country", x_axis, y_axis, "iso3"]].copy()

    # Build base figure via Scatterplot component (unchanged file), then enhance it
    sp = Scatterplot("Detailed Scatterplot", x_axis, y_axis, base_df)
    fig = sp._build_figure(selected_country_names)

    countries = base_df["Country"].astype(str).tolist()
    iso3s = base_df["iso3"].astype(str).str.upper().tolist()

    marker_colors = []
    marker_sizes = []
    marker_opacities = []
    marker_line_widths = []

    for c, iso in zip(countries, iso3s):
        is_clicked = (active_iso3 == iso) if active_iso3 else False
        is_selected = (c.upper() in selected_set) or (iso in selected_set)
        is_brushed = iso in brushed_set

        if is_clicked:
            marker_colors.append(COLOR_CLICKED)
            marker_sizes.append(14)
            marker_opacities.append(1.0)
            marker_line_widths.append(2)
        elif is_selected:
            marker_colors.append(COLOR_SELECTED)
            marker_sizes.append(11)
            marker_opacities.append(0.9)
            marker_line_widths.append(1)
        elif is_brushed:
            marker_colors.append(COLOR_DEFAULT)
            marker_sizes.append(10)
            marker_opacities.append(0.9)
            marker_line_widths.append(1)
        else:
            marker_colors.append(COLOR_DEFAULT)
            marker_sizes.append(7)
            marker_opacities.append(0.15 if has_brush else 0.5)
            marker_line_widths.append(0)

    if fig.data:
        fig.data[0].customdata = list(zip(countries, iso3s))
        fig.data[0].marker = dict(
            size=marker_sizes,
            opacity=marker_opacities,
            color=marker_colors,
            line=dict(width=marker_line_widths, color="#1f2937"),
        )
        fig.data[0].hovertemplate = (
            "<b>%{customdata[0]}</b><br>"
            f"{x_label}: %{{x:.3f}}<br>"
            f"{y_label}: %{{y:.3f}}<extra></extra>"
        )

    # Use brush revision to allow selection state to reset after brushing
    ui_rev = f"scatter-{brush_rev}" if brush_rev else "scatter-default"
    
    fig.update_layout(
        margin=dict(l=55, r=15, t=0, b=60),
        xaxis=dict(
            title=x_label,
            title_font_size=11,
            title_standoff=10,
            range=[-0.02, 1.02],
        ),
        yaxis=dict(
            title=y_label,
            title_font_size=11,
            title_standoff=10,
            range=[-0.02, 1.02],
        ),
        hovermode="closest",
        clickmode="event",
        dragmode="select",
        uirevision=ui_rev,
        selections=[],  # Clear any existing selection boxes
        transition=dict(
            duration=300,
            easing="cubic-in-out",
        ),
    )

    fig.update_traces(
        marker=dict(
            sizemode="diameter",
        ),
    )
    
    subtitle = f"{x_label} vs {y_label}"
    return fig, subtitle


# ===== DETAILED INFO PANEL (Stats + Radar side by side) =====
@app.callback(
    Output("detailed-info-content", "children"),
    Input("detailed-ranking-bar", "clickData"),
    Input("detailed-scatterplot", "clickData"),
    Input("selected-countries", "data"),
)
def update_detailed_info(ranking_click, scatter_click, selected_countries):
    country_name = None

    ctx = callback_context
    if ctx.triggered:
        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if trigger_id == "detailed-scatterplot":
            country_name, _ = _extract_country_iso3_from_click(scatter_click)
        elif trigger_id == "detailed-ranking-bar":
            country_name, _ = _extract_country_iso3_from_click(ranking_click)

    if not country_name:
        country_name, _ = _extract_country_iso3_from_click(ranking_click)
    if not country_name:
        country_name, _ = _extract_country_iso3_from_click(scatter_click)

    if not country_name:
        return html.Div(
            "Click a country in the ranking or scatterplot to view details.",
            className="detailed-info-placeholder",
        )

    try:
        df = get_data()
    except Exception:
        return html.Div("Data unavailable", className="detailed-info-placeholder")

    sel = df[df["Country"].astype(str).str.upper() == str(country_name).upper()]
    if sel.empty:
        return html.Div(f"Country '{country_name}' not found.", className="detailed-info-placeholder")

    row = sel.iloc[0]
    country_display = row["Country"]

    key_metrics = [
        ("Total_Population", "Population", "{:,.0f}"),
        ("Real_GDP_per_Capita_USD", "GDP/Capita", "${:,.0f}"),
        ("Unemployment_Rate_percent", "Unemployment", "{:.1f}%"),
        ("Total_Literacy_Rate", "Literacy", "{:.1f}%"),
        ("electricity_access_percent", "Elec. Access", "{:.1f}%"),
        ("Real_GDP_Growth_Rate_percent", "GDP Growth", "{:+.1f}%"),
        ("Median_Age", "Median Age", "{:.0f} yrs"),
    ]

    stats_children = []
    for col, label, fmt in key_metrics:
        if col in df.columns:
            val = row.get(col)
            if pd.notna(val):
                try:
                    formatted_val = fmt.format(val)
                except Exception:
                    formatted_val = str(val)

                non_null = df[col].dropna()
                rank_info = ""
                if not non_null.empty:
                    if "Unemployment" in col:
                        rank_val = int((non_null < val).sum()) + 1
                    else:
                        rank_val = int((non_null > val).sum()) + 1
                    rank_info = f"#{rank_val}/{non_null.shape[0]}"

                stats_children.append(
                    html.Div(
                        className="stat-item",
                        children=[
                            html.Div(label, className="stat-label"),
                            html.Div(
                                className="stat-value-row",
                                children=[
                                    html.Div(formatted_val, className="stat-value"),
                                    html.Div(rank_info, className="stat-rank"),
                                ]
                            ),
                        ]
                    )
                )

    metrics_data = []

    try:
        asf = available_skilled_workforce()
        if country_display in asf.index:
            metrics_data.append(("Workforce", asf[country_display], asf.mean()))
    except Exception:
        pass

    try:
        iec = industrial_energy_capacity()
        if country_display in iec.index:
            metrics_data.append(("Energy", iec[country_display], iec.mean()))
    except Exception:
        pass

    try:
        scc = supply_chain_connectivity_score()
        if country_display in scc.index:
            metrics_data.append(("Supply Chain", scc[country_display], scc.mean()))
    except Exception:
        pass

    try:
        wsi = wage_sustainability_index()
        if country_display in wsi.index:
            metrics_data.append(("Wage Sust.", wsi[country_display], wsi.mean()))
    except Exception:
        pass

    try:
        ers = economic_resilience_score()
        if country_display in ers.index:
            metrics_data.append(("Resilience", ers[country_display], ers.mean()))
    except Exception:
        pass

    radar_element = html.Div("No complex metrics available", className="radar-placeholder")

    if metrics_data:
        labels = [m[0] for m in metrics_data]
        country_vals = [m[1] for m in metrics_data]
        avg_vals = [m[2] for m in metrics_data]

        labels_closed = labels + [labels[0]]
        country_closed = country_vals + [country_vals[0]]
        avg_closed = avg_vals + [avg_vals[0]]

        radar_fig = go.Figure()
        radar_fig.add_trace(
            go.Scatterpolar(
                r=avg_closed,
                theta=labels_closed,
                name="Avg",
                fill="toself",
                fillcolor="rgba(156, 163, 175, 0.12)",
                line=dict(color="#9ca3af", width=1.5, dash="dot"),
                hovertemplate="%{theta}: %{r:.3f}<extra>Global Avg</extra>",
            )
        )
        radar_fig.add_trace(
            go.Scatterpolar(
                r=country_closed,
                theta=labels_closed,
                name=country_display[:10],
                fill="toself",
                fillcolor="rgba(59, 130, 246, 0.2)",
                line=dict(color="#3b82f6", width=2),
                hovertemplate="%{theta}: %{r:.3f}<extra>" + country_display + "</extra>",
            )
        )

        radar_fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1],
                    showticklabels=False,
                    gridcolor="rgba(0,0,0,0.06)",
                ),
                angularaxis=dict(
                    tickfont=dict(size=9, color="#555"),
                    gridcolor="rgba(0,0,0,0.06)",
                ),
                bgcolor="white",
            ),
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.25,
                xanchor="center",
                x=0.5,
                font=dict(size=9),
            ),
            margin=dict(l=30, r=30, t=20, b=50),
            paper_bgcolor="white",
        )

        radar_element = dcc.Graph(
            figure=radar_fig,
            config={"displayModeBar": False, "responsive": True},
        )
    
    # ===== COMBINE STATS AND RADAR SIDE BY SIDE =====
    return html.Div([
        # Header
        html.Div(
            className="detail-header",
            children=[
                html.Div(
                    className="detail-title-wrapper",
                    children=[
                        html.H3(country_display, className="detail-title"),
                        html.Div(
                            className="stats-wrapper",
                            children=[
                                html.Button("i", className="info-button", title="Hover for stats"),
                                html.Div(stats_children, className="stats-column-hidden"),
                            ]
                        ),
                    ]
                ),
            ]
        ),
        
        # Two-column layout
        html.Div(
            className="detail-content",
            children=[
                # Right: Radar
                html.Div(
                    className="radar-column",
                    children=[
                        html.Div("Complex Metrics Profile", className="radar-title"),
                        radar_element,
                    ]
                ),
            ]
        ),
    ])


# ===== SELECTED COUNTRY INDICATOR =====
@app.callback(
    Output("detailed-selected-country-indicator", "children"),
    Input("detailed-ranking-bar", "clickData"),
    Input("detailed-scatterplot", "clickData"),
)
def update_selected_indicator(ranking_click, scatter_click):
    country_name = None

    ctx = callback_context
    if ctx.triggered:
        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if trigger_id == "detailed-scatterplot":
            country_name, _ = _extract_country_iso3_from_click(scatter_click)
        elif trigger_id == "detailed-ranking-bar":
            country_name, _ = _extract_country_iso3_from_click(ranking_click)

    if not country_name:
        country_name, _ = _extract_country_iso3_from_click(ranking_click)
    if not country_name:
        country_name, _ = _extract_country_iso3_from_click(scatter_click)

    if country_name:
        return html.Span(["Selected: ", html.Strong(country_name)])

    return "Click a bar or point to select a country"


# ===== TRACK CLICKED COUNTRY =====
@app.callback(
    Output("selected_country", "data"),
    Input("detailed-ranking-bar", "clickData"),
    Input("detailed-scatterplot", "clickData"),
)
def update_selected_country(ranking_click, scatter_click):
    clicked_country = None

    ctx = callback_context
    if ctx.triggered:
        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if trigger_id == "detailed-scatterplot" and scatter_click:
            country_name, iso3 = _extract_country_iso3_from_click(scatter_click)
            clicked_country = (iso3 or country_name or "").upper().strip()
        elif trigger_id == "detailed-ranking-bar" and ranking_click:
            country_name, iso3 = _extract_country_iso3_from_click(ranking_click)
            clicked_country = (iso3 or country_name or "").upper().strip()

    return clicked_country
