from dash import html
from dash.dependencies import Input, Output
from jbi100_app.main import app

def global_map_view():
    return html.Div(
        children=[
            html.Div("Global Map View"),
            html.Button("Select region", id="global-map-button")
        ],
        className="panel"
    )

