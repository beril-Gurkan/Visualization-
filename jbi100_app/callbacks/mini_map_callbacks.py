from dash.dependencies import Input
from dash import Output
import plotly.graph_objects as go
import pandas as pd

from jbi100_app.app_instance import app
from jbi100_app.data import get_data
from jbi100_app.utils.country_meta import attach_country_meta


@app.callback(
    Output("mini-map", "figure"),
    Input("selected-countries", "data"),
)
def update_mini_map(selected_countries):
    """Display a read-only map highlighting selected countries."""
    selected_countries = selected_countries or []
    selected_set = {str(x).upper().strip() for x in selected_countries if x}
    
    # Get data with country metadata (iso3 codes)
    df = attach_country_meta(get_data()).dropna(subset=["iso3"]).copy()
    
    # Create base figure with all countries in light gray
    fig = go.Figure()
    
    # Add all countries as base layer (unselected)
    all_countries = sorted(df["iso3"].dropna().unique())
    unselected = [c for c in all_countries if c not in selected_set]
    
    if unselected:
        fig.add_trace(
            go.Choropleth(
                locations=unselected,
                z=[0] * len(unselected),
                showscale=False,
                colorscale=[[0, "#e5e7eb"], [1, "#e5e7eb"]],
                marker_line_color="rgba(0,0,0,0.15)",
                marker_line_width=0.5,
                marker_opacity=1.0,
                hoverinfo="skip",
                name="Unselected",
            )
        )
    
    # Add selected countries on top (highlighted)
    if selected_set:
        fig.add_trace(
            go.Choropleth(
                locations=sorted(selected_set),
                z=[1] * len(selected_set),
                showscale=False,
                colorscale=[[0, "#fb923c"], [1, "#fb923c"]],
                marker_line_color="#c2410c",
                marker_line_width=1.5,
                marker_opacity=1.0,
                hovertemplate="<b>%{hovertext}</b><extra></extra>",
                customdata=sorted(selected_set),
                hovertext=sorted(selected_set),
                name="Selected",
            )
        )
    
    # Update layout
    fig.update_geos(
        projection_type="natural earth",
        showframe=False,
        showcountries=True,
        countrycolor="rgba(0,0,0,0.15)",
        showcoastlines=True,
        coastlinecolor="rgba(0,0,0,0.15)",
        showocean=True,
        oceancolor="white",
        showland=True,
        landcolor="rgb(245,245,245)",
        bgcolor="white",
    )
    
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        hovermode="closest",
        dragmode=False,  # Disable interactions
        clickmode="none",  # Disable click events
    )
    
    return fig
