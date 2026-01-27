from dash import dcc, html


def map_panel():
    return html.Div(
        className="panel", id="map-panel",
        children=[
            html.H2("Global Map", className="panel-title"),
            html.Div(id="map-subtitle",),
            dcc.Graph(
                id="globe-map",
                className="graph-container",
                config={
                    "displayModeBar": True,
                    "scrollZoom": True,
                    "doubleClick": "reset",
                    "showTips": False,
                    "modeBarButtonsToRemove": ["lasso2d", "select2d"],
                },
            ),
        ],
    )
