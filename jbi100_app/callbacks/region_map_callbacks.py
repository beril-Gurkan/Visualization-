import plotly.graph_objects as go
from dash.dependencies import Input, Output
from jbi100_app.main import app
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

def _blank(msg: str):
    fig = go.Figure()
    fig.update_layout(
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        annotations=[dict(text=msg, showarrow=False, x=0.5, y=0.5)],
    )
    return fig


@app.callback(
    Output("region-map-title", "children"),
    Output("region-map", "figure"),
    Input("selected_region", "data"),
    Input("selected_country", "data"),
)
def update_region_map(selected_region, selected_country):
    if not selected_region:
        return "Region Map", _blank("Select a region on the global map")

    df = attach_country_meta(get_data())
    df = df.dropna(subset=["iso3", "region"]).copy()
    df = df[df["region"] == selected_region].copy()

    if df.empty:
        return f"Region Map — {selected_region}", _blank(f"No mappable countries for: {selected_region}")

    region_color = REGION_COLORS.get(selected_region, "#ccebc5")
    grey_color = "#d9d9d9"

    fig = go.Figure()

    # If there is a valid selected country in this region:
    # draw everyone grey, then draw selected country in region color.
    sel_row = None
    if selected_country:
        sel_row = df[df["Country"] == selected_country]
        if sel_row.empty:
            sel_row = None

    if sel_row is not None:
        # 1) All countries grey
        fig.add_trace(
            go.Choropleth(
                locations=df["iso3"],
                z=[1] * len(df),
                colorscale=[[0, grey_color], [1, grey_color]],
                showscale=False,
                marker_line_color="#333",
                marker_line_width=1.0,
                customdata=list(zip(df["Country"], df["country_display"])),
                hovertemplate="%{customdata[1]}<extra></extra>",
            )
        )

        # 2) Selected country on top, region color (others remain grey)
        iso3 = sel_row.iloc[0]["iso3"]
        disp = sel_row.iloc[0]["country_display"]
        fig.add_trace(
            go.Choropleth(
                locations=[iso3],
                z=[1],
                colorscale=[[0, region_color], [1, region_color]],
                showscale=False,
                marker_line_color="#333",
                marker_line_width=1.0,
                customdata=[(selected_country, disp)],
                hovertemplate="%{customdata[1]}<extra></extra>",
            )
        )

    else:
        # No selection: show all countries in region color (same behavior as before)
        fig.add_trace(
            go.Choropleth(
                locations=df["iso3"],
                z=[1] * len(df),
                colorscale=[[0, region_color], [1, region_color]],
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
        # Hide all basemap layers so only your choropleth polygons are visible
        visible=False,
        bgcolor="white",
    )

    fig.update_layout(
        dragmode=False,
        margin=dict(l=0, r=0, t=0, b=0),
        uirevision=f"region-map-{selected_region}",
    )

    return f"Region Map — {selected_region}", fig
