from dash import html, dcc
import plotly.graph_objects as go
import pandas as pd
import numpy as np

from jbi100_app.data import get_data


def detailed_info(country_name: str = None):
    """
    Return an overview panel for 'country_name' summarizing key indicators.
    """
    try:
        df = get_data()
    except Exception:
        return html.Div("Data unavailable", className="panel")

    if country_name is None:
        # Default to the first country in the dataset if none provided
        if 'Country' in df.columns and not df['Country'].dropna().empty:
            country_name = str(df['Country'].dropna().iloc[0])
        else:
            return html.Div("No country selected and dataset has no countries.", className="panel")

    # Exact match on the country name
    mask = df['Country'] == country_name
    sel = df[mask]
    if sel.empty:
        return html.Div(f"Country '{country_name}' not found.", className='panel')

    row = sel.iloc[0]

    # Define the key metrics to show (column_name, label, format)
    key_metrics = [
        ('Total_Population', 'Population', '{:,.0f}'),
        ('Real_GDP_per_Capita_USD', 'GDP per Capita', '${:,.0f}'),
        ('Unemployment_Rate_percent', 'Unemployment', '{:.1f}%'),
        ('Total_Literacy_Rate', 'Literacy Rate', '{:.1f}%'),
        ('electricity_access_percent', 'Electricity Access', '{:.1f}%')
    ]

    stats_children = []
    for col, label, fmt in key_metrics:
        if col in df.columns:
            val = row.get(col)
            if pd.notna(val):
                # compute rank among non-null values (higher value => better rank 1)
                non_null = df[col].dropna()
                if non_null.empty:
                    rank_info = ""
                else:
                    greater_count = (non_null > val).sum()
                    rank_val = int(greater_count) + 1
                    count = non_null.shape[0]
                    rank_info = f" (Rank {rank_val}/{count})"

                stats_children.append(
                    html.Div([
                        html.Div(label, className="stat-label", style={"fontSize": "12px", "color": "#666"}),
                        html.Div(f"{fmt.format(val)}{rank_info}", className="stat-value", style={"fontSize": "13px", "fontWeight": "600"})
                    ], className="stat-item", style={"padding": "4px"})
                )

    # Small bar chart for available score-like metrics (if present)
    score_cols = [c for c in ['Economic_Score', 'Demographic_Score', 'Energy_Sustainability_Score'] if c in df.columns]
    chart = None
    if score_cols:
        values = []
        labels = []
        for c in score_cols:
            v = row.get(c)
            if pd.notna(v):
                labels.append(c.replace('_', ' '))
                values.append(v)

            if values:
                fig = go.Figure(go.Bar(x=values, y=labels, orientation='h', marker_color='#2c8cff'))
                fig.update_layout(margin=dict(l=80, r=20, t=24, b=30), height=140, xaxis_title='Score')
            chart = dcc.Graph(
                figure=fig,
                config={'displayModeBar': False, 'responsive': True},
                className='detail-chart',
                style={'width': '80%', 'height': '140px', 'minHeight': '120px', 'margin': '0 auto', 'display': 'block'}
            )

    # Radar chart showing normalized values (0-1).
    # Prefer `Economic_Score`/`Demographic_Score`/`Energy_Sustainability_Score` if present,
    # otherwise fall back to a small set of common numeric indicators.
    radar = None
    preferred = ['Economic_Score', 'Demographic_Score', 'Energy_Sustainability_Score']
    if any(c in df.columns for c in preferred):
        radar_metrics = [c for c in preferred if c in df.columns]
    else:
        fallback = ['Total_Population', 'Real_GDP_per_Capita_USD', 'Total_Literacy_Rate', 'electricity_access_percent', 'Unemployment_Rate_percent']
        radar_metrics = [c for c in fallback if c in df.columns]

    if radar_metrics:
        # display names for radar axes
        label_map = {
            'Total_Population': 'Population',
            'Real_GDP_per_Capita_USD': 'GDP per Capita',
            'Total_Literacy_Rate': 'Literacy Rate',
            'electricity_access_percent': 'Electricity Access',
            'Unemployment_Rate_percent': 'Unemployment'
        }
        norm_vals = []
        labels = []
        for c in radar_metrics:
            col = pd.to_numeric(df[c], errors='coerce')
            raw = row.get(c)
            # apply log10 transform for population to keep scale comparable
            if c == 'Total_Population':
                col_t = np.log10(col + 1)
                raw_t = np.log10(raw + 1) if pd.notna(raw) else np.nan
            else:
                col_t = col
                raw_t = raw

            minv = col_t.min()
            maxv = col_t.max()
            if pd.isna(raw_t) or pd.isna(minv) or pd.isna(maxv) or (maxv - minv) == 0:
                norm = None
            else:
                norm = (float(raw_t) - float(minv)) / float(maxv - minv)
            if norm is not None:
                norm_vals.append(norm)
                labels.append(label_map.get(c, c.replace('_', ' ')))

        if norm_vals:
            r = norm_vals[:]
            r.append(r[0])
            theta = labels[:]
            theta.append(theta[0])

            # compute normalized global average for the same metrics
            avg_vals = []
            for c in radar_metrics:
                col = pd.to_numeric(df[c], errors='coerce')
                # apply same transform for population
                if c == 'Total_Population':
                    col_t = np.log10(col + 1)
                else:
                    col_t = col

                minv = col_t.min()
                maxv = col_t.max()
                if pd.isna(minv) or pd.isna(maxv) or (maxv - minv) == 0:
                    avg_norm = None
                else:
                    avg_raw = col_t.mean()
                    avg_norm = (float(avg_raw) - float(minv)) / float(maxv - minv)
                if avg_norm is not None:
                    avg_vals.append(avg_norm)
            if avg_vals:
                avg = avg_vals[:]
                avg.append(avg[0])

                radar_fig = go.Figure()
                radar_fig.add_trace(go.Scatterpolar(
                    r=avg,
                    theta=theta,
                    fill='toself',
                    name='Global Average',
                    line=dict(color='#1f6f2e', width=10),
                    opacity=0.95
                ))

                radar_fig.add_trace(go.Scatterpolar(
                    r=r,
                    theta=theta,
                    fill='toself',
                    name=row.get('Country') or 'Country',
                    line=dict(color='#06a3d9', width=6),
                    opacity=0.9
                ))

                radar_fig.update_layout(
                    polar=dict(radialaxis=dict(range=[0, 1], visible=True, tickfont=dict(size=9), showticklabels=False),
                        angularaxis=dict(tickfont=dict(size=10), rotation=90, direction='clockwise'),
                        gridshape='linear'
                    ),
                    showlegend=True,
                    legend=dict(
                        orientation='h',
                        x=0.5,
                        xanchor='center',
                        y=-0.12,
                        yanchor='top',
                        font=dict(size=10)
                    ),
                    margin=dict(l=8, r=8, t=20, b=70),
                    height=300
                )
                radar = dcc.Graph(
                    figure=radar_fig,
                    config={'displayModeBar': False, 'responsive': True},
                    className='detail-radar',
                    style={'width': '50%', 'height': '300px', 'minHeight': '260px', 'margin': '0 auto', 'display': 'block'}
                )

    header = html.Div([
        html.H4(country_name, className='detail-title', style={"fontSize": "14px", "margin": "0", "color": "#111"}),
        html.Div('Quick summary for decision support', className='detail-subtitle', style={"fontSize": "12px", "color": "#333", "margin": "0"})
    ], className='detail-header', style={
        'position': 'static',
        'top': 'auto',
        'zIndex': '0',
        'backgroundColor': 'transparent',
        'padding': '6px 8px',
        'borderBottom': '1px solid #e6e6e6',
        'display': 'block'
    })

    body_children = [
        html.Div(stats_children, className='stats-grid', style={
            'maxHeight': '220px', 'overflowY': 'auto',
            'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '8px', 'width': '100%'
        }) if stats_children else html.Div('No key stats available.'),
    ]
    if chart is not None:
        body_children.append(chart)
    if radar is not None:
        body_children.append(radar)

    return html.Div([
        header,
        html.Div(body_children, className='detail-body', style={'width': '100%'} )
    ], className='panel detailed-info', style={'maxHeight': '600px', 'width': '100%', 'overflowY': 'auto'})
