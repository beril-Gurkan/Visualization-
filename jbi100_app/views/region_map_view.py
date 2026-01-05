from dash import html
from dash.dependencies import Input, Output
from jbi100_app.main import app

def region_map_view():
    return html.Div(
        children=[
            html.Div("Region Map View"),
            html.Button("Back to global view", id="region-map-button")
        ],
        className="panel"
    )