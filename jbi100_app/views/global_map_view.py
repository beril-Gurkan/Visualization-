from __future__ import annotations

from dash import html, dcc
import plotly.graph_objects as go

from jbi100_app.data import get_data
from jbi100_app.utils.country_meta import attach_country_meta


REGION_ORDER = ["Africa", "Americas", "Asia", "Europe", "Oceania"]
REGION_COLORS = {
    "Africa": "#fed9a6",
    "Americas": "#fbb4ae",
    "Asia": "#e5f5b5",
    "Europe": "#decbe4",
    "Oceania": "#ccebc5",
}


def global_map_view():
    df = attach_country_meta(get_data())
    df = df.dropna(subset=["iso3", "region"]).copy()
    df = df[df["region"].isin(REGION_ORDER)].copy()

    fig = go.Figure()

    # one trace per region (lets us fade whole regions on hover without rebuilding geo)
    for region in REGION_ORDER:
        sub = df[df["region"] == region]
        fig.add_trace(
            go.Choropleth(
                name=region,
                locations=sub["iso3"],
                z=[1] * len(sub),  # dummy values (we color via a single-color colorscale)
                colorscale=[[0, REGION_COLORS[region]], [1, REGION_COLORS[region]]],
                showscale=False,
                showlegend=True,
                marker_line_color="#444",
                marker_line_width=0.6,
                marker_opacity=1.0,
                customdata=list(zip(sub["region"], sub["Country"], sub["country_display"])),
                hovertemplate="<b>%{customdata[0]}</b><extra></extra>",
            )
        )

    fig.update_geos(
        projection_type="natural earth",  # keep the “3D-ish” look
        showocean=True,
        oceancolor="#b9d9ff",
        showlakes=True,
        lakecolor="#b9d9ff",
        showland=True,
        landcolor="#eef2f7",
        showcountries=True,
        countrycolor="#444",
        showcoastlines=True,
        coastlinecolor="#444",
    )

    fig.update_layout(
        margin=dict(l=0, r=0, t=45, b=0),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            title_text="Region",
        ),
        uirevision="globe-map-stable",  # preserve view
        hoverlabel=dict(font_size=18, bgcolor="white"),
        dragmode = False,
    )

    return html.Div(
        className="panel",
        style={
            "justifyContent": "flex-start",
            "alignItems": "stretch",
            "gap": "8px",
            "fontSize": "1.2rem",
            "padding": "12px",
        },
        children=[
            html.Div("Click a country to drill down to its region", style={"fontWeight": "700"}),
            dcc.Graph(
                id="globe-map",
                figure=fig,
                clear_on_unhover=True,  # so hoverData becomes None when leaving the map
                config={
                    "displayModeBar": False,
                    "responsive": True,
                },
                style={"width": "100%", "height": "100%"},
            ),
        ],
    )
