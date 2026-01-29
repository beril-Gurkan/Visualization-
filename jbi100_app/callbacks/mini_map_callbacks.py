# Mini-map callback - shows zoomed-in view of selected countries in detailed view
# Highlights selected countries (orange) and currently clicked country (green)
# Read-only map - no interaction, just visualization of current state

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
    Input("selected_country", "data"),
)
def update_mini_map(selected_countries, clicked_country):
    """Display a read-only map highlighting selected countries (orange) and clicked country (green)."""
    selected_countries = selected_countries or []
    selected_set = {str(x).upper().strip() for x in selected_countries if x}
    
    # Get data with country metadata (iso3 codes)
    df = attach_country_meta(get_data()).dropna(subset=["iso3"]).copy()
    
    # Convert clicked country name to ISO3 code
    clicked_iso3 = None
    if clicked_country:
        clicked_country_upper = str(clicked_country).upper().strip()
        # Try to find matching country by name or iso3
        match = df[
            (df["Country"].str.upper() == clicked_country_upper) | 
            (df["iso3"].str.upper() == clicked_country_upper)
        ]
        if not match.empty:
            clicked_iso3 = match.iloc[0]["iso3"]
            # Remove from selected set to avoid double-rendering
            selected_set.discard(clicked_country_upper)
            selected_set.discard(clicked_iso3)
    
    # Create base figure with all countries in light gray
    fig = go.Figure()
    
    # Add all countries as base layer (unselected)
    all_countries = sorted(df["iso3"].dropna().unique())
    unselected = [c for c in all_countries if c not in selected_set and c != clicked_iso3]
    
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
    
    # Add selected countries on top (highlighted in orange)
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
    
    # Add clicked country on top (highlighted in green)
    if clicked_iso3:
        fig.add_trace(
            go.Choropleth(
                locations=[clicked_iso3],
                z=[2],
                showscale=False,
                colorscale=[[0, "#22c55e"], [1, "#22c55e"]],
                marker_line_color="#15803d",
                marker_line_width=2.0,
                marker_opacity=1.0,
                hovertemplate="<b>%{hovertext}</b><br><i>Active</i><extra></extra>",
                customdata=[clicked_iso3],
                hovertext=[clicked_iso3],
                name="Active",
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
