from dash import html, dcc
import plotly.graph_objects as go
import pandas as pd
import numpy as np

from jbi100_app.data import get_data


def detailed_info(country_name: str | None):
    """
    Panel for selected country. If no country is selected, show a placeholder message.
    """
    # Placeholder when nothing is selected
    if not country_name:
        return html.Div(
            className="panel detailed-info",
            children=[
                html.Div(
                    [
                        html.H4("Country details", className="detail-title"),
                        html.Div(
                            "Please select a country from the rankings first.",
                            className="detail-subtitle",
                        ),
                    ],
                    className="detail-header",
                ),
            ],
        )

    try:
        df = get_data()
    except Exception:
        return html.Div("Data unavailable", className="panel detailed-info")

    if "Country" not in df.columns:
        return html.Div("Dataset has no Country column.", className="panel detailed-info")

    sel = df[df["Country"] == country_name]
    if sel.empty:
        return html.Div(f"Country '{country_name}' not found.", className="panel detailed-info")

    row = sel.iloc[0]

    key_metrics = [
        ("Total_Population", "Population", "{:,.0f}"),
        ("Real_GDP_per_Capita_USD", "GDP per Capita", "${:,.0f}"),
        ("Unemployment_Rate_percent", "Unemployment", "{:.1f}%"),
        ("Total_Literacy_Rate", "Literacy Rate", "{:.1f}%"),
        ("electricity_access_percent", "Electricity Access", "{:.1f}%"),
    ]

    stats_children = []
    for col, label, fmt in key_metrics:
        if col in df.columns:
            val = row.get(col)
            if pd.notna(val):
                non_null = df[col].dropna()
                if non_null.empty:
                    rank_info = ""
                else:
                    rank_val = int((non_null > val).sum()) + 1
                    count = non_null.shape[0]
                    rank_info = f" (Rank {rank_val}/{count})"

                stats_children.append(
                    html.Div(
                        [
                            html.Div(label, className="stat-label"),
                            html.Div(f"{fmt.format(val)}{rank_info}", className="stat-value"),
                        ],
                        className="stat-item",
                    )
                )

    # Optional small bar chart if score columns exist
    score_cols = [c for c in ["Economic_Score", "Demographic_Score", "Energy_Sustainability_Score"] if c in df.columns]
    chart = None
    if score_cols:
        labels, values = [], []
        for c in score_cols:
            v = row.get(c)
            if pd.notna(v):
                labels.append(c.replace("_", " "))
                values.append(v)

        if values:
            fig = go.Figure(go.Bar(x=values, y=labels, orientation="h"))
            fig.update_layout(
                margin=dict(l=90, r=20, t=10, b=20),
                height=150,
                xaxis_title="Score",
            )
            chart = dcc.Graph(
                figure=fig,
                config={"displayModeBar": False, "responsive": True},
                style={"width": "100%", "height": "160px"},
            )

    # Radar chart (normalized 0–1) – thinner lines, less fill to improve accuracy
    preferred = ["Economic_Score", "Demographic_Score", "Energy_Sustainability_Score"]
    if any(c in df.columns for c in preferred):
        radar_metrics = [c for c in preferred if c in df.columns]
    else:
        fallback = [
            "Total_Population",
            "Real_GDP_per_Capita_USD",
            "Total_Literacy_Rate",
            "electricity_access_percent",
            "Unemployment_Rate_percent",
        ]
        radar_metrics = [c for c in fallback if c in df.columns]

    radar = None
    if radar_metrics:
        label_map = {
            "Total_Population": "Population",
            "Real_GDP_per_Capita_USD": "GDP per Capita",
            "Total_Literacy_Rate": "Literacy Rate",
            "electricity_access_percent": "Electricity Access",
            "Unemployment_Rate_percent": "Unemployment",
        }

        def normalize_col(c):
            col = pd.to_numeric(df[c], errors="coerce")
            if c == "Total_Population":
                return np.log10(col + 1)
            return col

        r_vals, theta = [], []
        for c in radar_metrics:
            col_t = normalize_col(c)
            raw = row.get(c)
            raw_t = np.log10(raw + 1) if (c == "Total_Population" and pd.notna(raw)) else raw

            minv, maxv = col_t.min(), col_t.max()
            if pd.isna(raw_t) or pd.isna(minv) or pd.isna(maxv) or (maxv - minv) == 0:
                continue

            norm = (float(raw_t) - float(minv)) / float(maxv - minv)
            r_vals.append(norm)
            theta.append(label_map.get(c, c.replace("_", " ")))

        if r_vals:
            # close the loop
            r = r_vals + [r_vals[0]]
            th = theta + [theta[0]]

            # global average
            avg_vals = []
            for c in radar_metrics:
                col_t = normalize_col(c)
                minv, maxv = col_t.min(), col_t.max()
                if pd.isna(minv) or pd.isna(maxv) or (maxv - minv) == 0:
                    continue
                avg_raw = col_t.mean()
                avg_vals.append((float(avg_raw) - float(minv)) / float(maxv - minv))

            avg = avg_vals + [avg_vals[0]] if avg_vals else None

            radar_fig = go.Figure()

            if avg:
                radar_fig.add_trace(
                    go.Scatterpolar(
                        r=avg,
                        theta=th,
                        name="Global Average",
                        fill="toself",
                        opacity=0.18,
                        line=dict(width=2, dash="dot"),
                    )
                )

            radar_fig.add_trace(
                go.Scatterpolar(
                    r=r,
                    theta=th,
                    name=country_name,
                    fill="toself",
                    opacity=0.22,
                    line=dict(width=2),
                )
            )

            radar_fig.update_layout(
                polar=dict(
                    radialaxis=dict(range=[0, 1], showticklabels=True, tickfont=dict(size=9)),
                    angularaxis=dict(tickfont=dict(size=10)),
                ),
                showlegend=True,
                legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.15),
                margin=dict(l=10, r=10, t=10, b=60),
                height=280,
            )

            radar = dcc.Graph(
                figure=radar_fig,
                config={"displayModeBar": False, "responsive": True},
                style={"width": "100%", "height": "290px"},
            )

    return html.Div(
        className="panel detailed-info",
        children=[
            html.Div(
                [
                    html.H4(country_name, className="detail-title"),
                    html.Div("Quick summary for decision support", className="detail-subtitle"),
                ],
                className="detail-header",
            ),
            html.Div(
                [
                    html.Div(stats_children, className="stats-grid") if stats_children else html.Div("No key stats available."),
                    chart if chart is not None else html.Div(),
                    radar if radar is not None else html.Div(),
                ],
                className="detail-body",
            ),
        ],
    )
