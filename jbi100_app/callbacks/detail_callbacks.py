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

# Color constants
COLOR_DEFAULT = '#94a3b8'      # Gray for non-selected countries
COLOR_SELECTED = '#22c55e'     # Green for selected countries
COLOR_CLICKED = '#f97316'      # Orange for clicked/active country


def _compute_complex_scores(w_asf, w_iec, w_scc, w_wsi, w_ers,
                            t_asf, t_iec, t_scc, t_wsi, t_ers):
    """
    Compute complex metrics score based on weights and toggles.
    Weights are now 0-100 (consistent with global metrics panel).
    Returns a DataFrame with Country and Complex_Score columns.
    """
    # Get individual metric scores (these return Series indexed by Country)
    scores = {}
    weights = {}
    
    if t_asf:
        scores['ASF'] = available_skilled_workforce()
        weights['ASF'] = w_asf
    if t_iec:
        scores['IEC'] = industrial_energy_capacity()
        weights['IEC'] = w_iec
    if t_scc:
        scores['SCC'] = supply_chain_connectivity_score()
        weights['SCC'] = w_scc
    if t_wsi:
        scores['WSI'] = wage_sustainability_index()
        weights['WSI'] = w_wsi
    if t_ers:
        scores['ERS'] = economic_resilience_score()
        weights['ERS'] = w_ers
    
    if not scores:
        return pd.DataFrame({'Country': [], 'Complex_Score': []})
    
    # Create a combined dataframe
    result_df = None
    for name, series in scores.items():
        temp_df = pd.DataFrame({
            'Country': series.index,
            name: series.values
        })
        if result_df is None:
            result_df = temp_df
        else:
            result_df = result_df.merge(temp_df, on='Country', how='outer')
    
    # Normalize weights (already 0-100 scale)
    total_weight = sum(weights.values())
    if total_weight == 0:
        total_weight = 1
    
    # Calculate weighted score
    score_cols = list(scores.keys())
    result_df['Complex_Score'] = 0
    for col in score_cols:
        w = weights[col] / total_weight
        result_df['Complex_Score'] += w * result_df[col].fillna(0)
    
    return result_df[['Country', 'Complex_Score'] + score_cols]


# ===== DETAILED RANKING BAR CHART =====
@app.callback(
    Output("detailed-ranking-bar", "figure"),
    Input("selected-countries", "data"),
    Input("detailed-ranking-metric", "value"),
    Input("detailed-ranking-order", "value"),
    Input("detailed-ranking-bar", "clickData"),
    Input("detailed-scatterplot", "clickData"),
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
    selected_countries, metric, order, ranking_click, scatter_click,
    w_asf, w_iec, w_scc, w_wsi, w_ers,
    t_asf, t_iec, t_scc, t_wsi, t_ers
):
    """
    Update the ranking bar chart showing relevant countries:
    - Selected countries are highlighted in green
    - Clicked country is highlighted in orange
    - Shows neighboring countries for context
    - Indicates when countries are skipped
    """
    selected_countries = selected_countries or []
    
    # Convert toggles to booleans
    t_asf = bool(t_asf)
    t_iec = bool(t_iec)
    t_scc = bool(t_scc)
    t_wsi = bool(t_wsi)
    t_ers = bool(t_ers)
    
    # Get ALL data
    df = attach_country_meta(get_data())
    
    if df.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=13, color="#888")
        )
        fig.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=200)
        return fig
    
    # Build selected set for highlighting
    selected_set = {str(x).upper().strip() for x in selected_countries if x}
    
    # Determine clicked country
    clicked_country = None
    ctx = callback_context
    if ctx.triggered:
        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if trigger_id == 'detailed-scatterplot' and scatter_click:
            points = scatter_click.get("points", [])
            if points:
                clicked_country = str(points[0].get("customdata", "")).upper().strip()
        elif trigger_id == 'detailed-ranking-bar' and ranking_click:
            points = ranking_click.get("points", [])
            if points:
                customdata = points[0].get("customdata")
                if customdata and len(customdata) > 0:
                    clicked_country = str(customdata[0]).upper().strip()
    
    # Handle Complex_Metrics
    if metric == "Complex_Metrics":
        scores_df = _compute_complex_scores(w_asf, w_iec, w_scc, w_wsi, w_ers,
                                            t_asf, t_iec, t_scc, t_wsi, t_ers)
        df = df.merge(
            scores_df[['Country', 'Complex_Score']], 
            on='Country', 
            how='left'
        )
        metric_col = 'Complex_Score'
        metric_label = "Complex Score"
    else:
        metric_col = metric
        metric_label = metric.replace("_", " ")
    
    # Drop rows with missing values
    df_all = df.dropna(subset=[metric_col]).copy()
    
    if df_all.empty:
        fig = go.Figure()
        fig.add_annotation(
            text=f"No {metric_label} data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=13, color="#888")
        )
        fig.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=200)
        return fig
    
    # Sort ALL countries
    ascending = (order == "asc")
    df_all = df_all.sort_values(by=metric_col, ascending=ascending).reset_index(drop=True)
    df_all['rank'] = range(1, len(df_all) + 1)
    
    # Identify countries of interest (selected + clicked)
    countries_of_interest_indices = set()
    
    # Add selected countries
    for idx, row in df_all.iterrows():
        country_upper = row['Country'].upper()
        iso3_upper = row['iso3'].upper() if pd.notna(row.get('iso3')) else ""
        if country_upper in selected_set or iso3_upper in selected_set:
            countries_of_interest_indices.add(idx)
    
    # Add clicked country
    if clicked_country:
        for idx, row in df_all.iterrows():
            country_upper = row['Country'].upper()
            iso3_upper = row['iso3'].upper() if pd.notna(row.get('iso3')) else ""
            if country_upper == clicked_country or iso3_upper == clicked_country:
                countries_of_interest_indices.add(idx)
                break
    
    # Always aim for ~15 countries in the ranking
    target_count = 15
    indices_to_show = set()
    
    if not countries_of_interest_indices:
        # No selection - just show top 15
        indices_to_show = set(range(min(target_count, len(df_all))))
        show_skipped = len(df_all) > target_count
    else:
        # Include all countries of interest
        indices_to_show.update(countries_of_interest_indices)
        
        # Calculate how many more we can fit
        remaining_slots = target_count - len(countries_of_interest_indices)
        
        if remaining_slots > 0:
            # Fill with top-ranked countries that aren't already included
            for idx in range(len(df_all)):
                if idx not in indices_to_show:
                    indices_to_show.add(idx)
                    remaining_slots -= 1
                    if remaining_slots <= 0:
                        break
        
        show_skipped = len(indices_to_show) < len(df_all)
    
    # Sort indices for display
    sorted_indices = sorted(indices_to_show)
    df_plot = df_all.loc[sorted_indices].copy().reset_index(drop=True)
    
    # Determine colors and create data for plot
    countries_list = []
    values_list = []
    colors_list = []
    customdata_list = []
    hovertext_list = []
    
    for _, row in df_plot.iterrows():
        country_upper = row['Country'].upper()
        iso3_upper = row['iso3'].upper() if pd.notna(row.get('iso3')) else ""
        
        countries_list.append(row['Country'])
        values_list.append(row[metric_col])
        customdata_list.append([row['Country'], row.get('iso3', ''), row.get('rank', '')])
        
        # Check if this country is clicked or selected
        is_clicked = clicked_country and (country_upper == clicked_country or iso3_upper == clicked_country)
        is_selected = country_upper in selected_set or iso3_upper in selected_set
        
        # Determine color: clicked > selected > default
        if is_clicked:
            colors_list.append(COLOR_CLICKED)
            hovertext_list.append(f"<b>{row['Country']}</b><br>{metric_label}: {row[metric_col]:.3f}<br>Rank: #{row['rank']}<br><i>Currently viewing</i>")
        elif is_selected:
            colors_list.append(COLOR_SELECTED)
            hovertext_list.append(f"<b>{row['Country']}</b><br>{metric_label}: {row[metric_col]:.3f}<br>Rank: #{row['rank']}<br><i>Selected on map</i>")
        else:
            colors_list.append(COLOR_DEFAULT)
            hovertext_list.append(f"<b>{row['Country']}</b><br>{metric_label}: {row[metric_col]:.3f}<br>Rank: #{row['rank']}")
    
    # Create horizontal bar chart
    fig = go.Figure(
        go.Bar(
            x=values_list,
            y=countries_list,
            orientation='h',
            marker_color=colors_list,
            marker_line_width=0,
            customdata=customdata_list,
            hovertext=hovertext_list,
            hovertemplate="%{hovertext}<extra></extra>",
        )
    )
    
    # Add title annotation if showing subset
    title_text = metric_label
    if show_skipped:
        total_countries = len(df_all)
        shown_countries = len(countries_list)
        title_text += f" (showing {shown_countries} of {total_countries} countries)"
    
    fig.update_layout(
        margin=dict(l=5, r=10, t=30, b=25),
        xaxis_title=metric_label,
        xaxis_title_font_size=10,
        yaxis=dict(automargin=True, tickfont=dict(size=9)),
        clickmode='event+select',
        hovermode='closest',
        height=400,
        bargap=0.12,
        title=dict(text=title_text, font=dict(size=11), x=0.5, xanchor='center'),
    )
    
    return fig


# ===== SCATTERPLOT =====
@app.callback(
    Output("detailed-scatterplot", "figure"),
    Input("selected-countries", "data"),
    Input("detailed-ranking-bar", "clickData"),
    Input("detailed-scatterplot", "clickData"),
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
    selected_countries, ranking_click, scatter_click,
    x_axis, y_axis,
    w_asf, w_iec, w_scc, w_wsi, w_ers,
    t_asf, t_iec, t_scc, t_wsi, t_ers
):
    """
    Update scatterplot showing ALL countries.
    - Selected countries are highlighted in green
    - Clicked country is highlighted in orange
    """
    selected_countries = selected_countries or []
    
    # Axis label mapping
    axis_labels = {
        'ASF': 'Skilled Workforce',
        'IEC': 'Energy Capacity',
        'SCC': 'Supply Chain',
        'WSI': 'Wage Sustainability',
        'ERS': 'Economic Resilience',
    }
    
    x_label = axis_labels.get(x_axis, x_axis)
    y_label = axis_labels.get(y_axis, y_axis)
    
    # Get scores (compute all metrics for scatterplot)
    scores_df = _compute_complex_scores(w_asf, w_iec, w_scc, w_wsi, w_ers,
                                        True, True, True, True, True)
    
    if scores_df.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=12, color="#888")
        )
        fig.update_layout(margin=dict(l=20, r=20, t=20, b=20))
        return fig
    
    # Get ALL data with country meta
    df = attach_country_meta(get_data())
    
    # Merge scores with ALL countries
    df_plot = df.merge(scores_df, on='Country', how='left')
    
    # Check if selected axes exist
    if x_axis not in df_plot.columns or y_axis not in df_plot.columns:
        fig = go.Figure()
        fig.add_annotation(
            text="Selected metrics not available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=12, color="#888")
        )
        fig.update_layout(margin=dict(l=20, r=20, t=20, b=20))
        return fig
    
    df_plot = df_plot.dropna(subset=[x_axis, y_axis])
    
    if df_plot.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No data for selected metrics",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=12, color="#888")
        )
        fig.update_layout(margin=dict(l=20, r=20, t=20, b=20))
        return fig
    
    # Build selected set for highlighting
    selected_set = {str(x).upper().strip() for x in selected_countries if x}
    
    # Determine clicked country
    clicked_country = None
    ctx = callback_context
    if ctx.triggered:
        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if trigger_id == 'detailed-scatterplot' and scatter_click:
            points = scatter_click.get("points", [])
            if points:
                clicked_country = str(points[0].get("customdata", "")).upper().strip()
        elif trigger_id == 'detailed-ranking-bar' and ranking_click:
            points = ranking_click.get("points", [])
            if points:
                customdata = points[0].get("customdata")
                if customdata and len(customdata) > 0:
                    clicked_country = str(customdata[0]).upper().strip()
    
    # Create marker properties: clicked > selected > default
    marker_colors = []
    marker_sizes = []
    marker_opacities = []
    marker_line_widths = []
    
    for _, row in df_plot.iterrows():
        country_upper = row['Country'].upper()
        iso3_upper = row['iso3'].upper() if pd.notna(row.get('iso3')) else ""
        
        # Check if this country is the clicked one
        is_clicked = clicked_country and (country_upper == clicked_country or iso3_upper == clicked_country)
        # Check if this country is in the selected set (from map)
        is_selected = country_upper in selected_set or iso3_upper in selected_set
        
        if is_clicked:
            # Clicked country gets orange highlight (highest priority)
            marker_colors.append(COLOR_CLICKED)
            marker_sizes.append(14)
            marker_opacities.append(1.0)
            marker_line_widths.append(2)
        elif is_selected:
            # Selected countries from map get green highlight
            marker_colors.append(COLOR_SELECTED)
            marker_sizes.append(11)
            marker_opacities.append(0.9)
            marker_line_widths.append(1)
        else:
            # All other countries are gray and smaller
            marker_colors.append(COLOR_DEFAULT)
            marker_sizes.append(7)
            marker_opacities.append(0.5)
            marker_line_widths.append(0)
    
    # Create scatterplot
    fig = go.Figure(
        go.Scatter(
            x=df_plot[x_axis],
            y=df_plot[y_axis],
            mode='markers',
            marker=dict(
                size=marker_sizes,
                opacity=marker_opacities,
                color=marker_colors,
                line=dict(width=marker_line_widths, color='#1f2937')
            ),
            text=df_plot['Country'],
            customdata=df_plot['Country'],
            hovertemplate="<b>%{text}</b><br>" +
                          f"{x_label}: %{{x:.3f}}<br>" +
                          f"{y_label}: %{{y:.3f}}<extra></extra>",
        )
    )
    
    fig.update_layout(
        margin=dict(l=50, r=15, t=15, b=45),
        xaxis_title=x_label,
        yaxis_title=y_label,
        xaxis_title_font_size=11,
        yaxis_title_font_size=11,
        hovermode='closest',
        clickmode='event',
    )
    
    return fig


# ===== PLOT PANEL (Empty - Reserved for future) =====
# Note: The radar chart has been moved to the detailed info panel


# ===== DETAILED INFO PANEL (Stats + Radar side by side) =====
@app.callback(
    Output("detailed-info-content", "children"),
    Input("detailed-ranking-bar", "clickData"),
    Input("detailed-scatterplot", "clickData"),
    Input("selected-countries", "data"),
)
def update_detailed_info(ranking_click, scatter_click, selected_countries):
    """Update detailed info panel with key statistics and radar chart side by side."""
    # Determine which country was clicked
    country_name = None
    
    ctx = callback_context
    if ctx.triggered:
        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if trigger_id == 'detailed-scatterplot' and scatter_click:
            points = scatter_click.get("points", [])
            if points:
                country_name = points[0].get("customdata")
        elif trigger_id == 'detailed-ranking-bar' and ranking_click:
            points = ranking_click.get("points", [])
            if points:
                customdata = points[0].get("customdata")
                if customdata and len(customdata) > 0:
                    country_name = customdata[0]
    
    if not country_name and ranking_click:
        points = ranking_click.get("points", [])
        if points:
            customdata = points[0].get("customdata")
            if customdata and len(customdata) > 0:
                country_name = customdata[0]
    
    if not country_name:
        return html.Div(
            "Click a country in the ranking or scatterplot to view details.",
            className="detailed-info-placeholder"
        )
    
    # Get data
    try:
        df = get_data()
    except Exception:
        return html.Div("Data unavailable", className="detailed-info-placeholder")
    
    sel = df[df["Country"].str.upper() == country_name.upper()]
    if sel.empty:
        return html.Div(f"Country '{country_name}' not found.", className="detailed-info-placeholder")
    
    row = sel.iloc[0]
    country_display = row["Country"]
    
    # ===== BUILD STATS SECTION =====
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
                except:
                    formatted_val = str(val)
                
                # Calculate rank
                non_null = df[col].dropna()
                rank_info = ""
                if not non_null.empty:
                    if "Unemployment" in col:
                        rank_val = int((non_null < val).sum()) + 1
                    else:
                        rank_val = int((non_null > val).sum()) + 1
                    count = non_null.shape[0]
                    rank_info = f"#{rank_val}/{count}"
                
                stats_children.append(
                    html.Div(
                        className="stat-item",
                        children=[
                            html.Div(label, className="stat-label"),
                            html.Div(formatted_val, className="stat-value"),
                            html.Div(rank_info, className="stat-rank"),
                        ]
                    )
                )
    
    # ===== BUILD RADAR CHART =====
    metrics_data = []
    
    try:
        asf = available_skilled_workforce()
        if country_display in asf.index:
            metrics_data.append(('Workforce', asf[country_display], asf.mean()))
    except: pass
    
    try:
        iec = industrial_energy_capacity()
        if country_display in iec.index:
            metrics_data.append(('Energy', iec[country_display], iec.mean()))
    except: pass
    
    try:
        scc = supply_chain_connectivity_score()
        if country_display in scc.index:
            metrics_data.append(('Supply Chain', scc[country_display], scc.mean()))
    except: pass
    
    try:
        wsi = wage_sustainability_index()
        if country_display in wsi.index:
            metrics_data.append(('Wage Sust.', wsi[country_display], wsi.mean()))
    except: pass
    
    try:
        ers = economic_resilience_score()
        if country_display in ers.index:
            metrics_data.append(('Resilience', ers[country_display], ers.mean()))
    except: pass
    
    radar_element = html.Div("No complex metrics available", className="radar-placeholder")
    
    if metrics_data:
        labels = [m[0] for m in metrics_data]
        country_vals = [m[1] for m in metrics_data]
        avg_vals = [m[2] for m in metrics_data]
        
        # Close the loop
        labels_closed = labels + [labels[0]]
        country_closed = country_vals + [country_vals[0]]
        avg_closed = avg_vals + [avg_vals[0]]
        
        radar_fig = go.Figure()
        
        # Global average trace
        radar_fig.add_trace(
            go.Scatterpolar(
                r=avg_closed,
                theta=labels_closed,
                name="Avg",
                fill="toself",
                fillcolor="rgba(156, 163, 175, 0.12)",
                line=dict(color="#9ca3af", width=1.5, dash="dot"),
                hovertemplate="%{theta}: %{r:.3f}<extra>Global Avg</extra>"
            )
        )
        
        # Country trace
        radar_fig.add_trace(
            go.Scatterpolar(
                r=country_closed,
                theta=labels_closed,
                name=country_display[:10],
                fill="toself",
                fillcolor="rgba(59, 130, 246, 0.2)",
                line=dict(color="#3b82f6", width=2),
                hovertemplate="%{theta}: %{r:.3f}<extra>" + country_display + "</extra>"
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
                font=dict(size=9)
            ),
            margin=dict(l=30, r=30, t=20, b=50),
            height=330,
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
                html.H3(country_display, className="detail-title"),
                html.P("Key Statistics & Complex Metrics", className="detail-subtitle"),
            ]
        ),
        
        # Two-column layout
        html.Div(
            className="detail-content",
            children=[
                # Left: Stats
                html.Div(stats_children, className="stats-column"),
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
    """Show which country is currently selected."""
    country_name = None
    
    ctx = callback_context
    if ctx.triggered:
        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if trigger_id == 'detailed-scatterplot' and scatter_click:
            points = scatter_click.get("points", [])
            if points:
                country_name = points[0].get("customdata")
        elif trigger_id == 'detailed-ranking-bar' and ranking_click:
            points = ranking_click.get("points", [])
            if points:
                customdata = points[0].get("customdata")
                if customdata and len(customdata) > 0:
                    country_name = customdata[0]
    
    if not country_name and ranking_click:
        points = ranking_click.get("points", [])
        if points:
            customdata = points[0].get("customdata")
            if customdata and len(customdata) > 0:
                country_name = customdata[0]
    
    if country_name:
        return html.Span([
            "Selected: ",
            html.Strong(country_name)
        ])
    
    return "Click a bar or point to select a country"
