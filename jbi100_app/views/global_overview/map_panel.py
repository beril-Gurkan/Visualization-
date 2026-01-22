from dash import dcc, html


def map_panel():
    return html.Div(
        className="panel", id="map-panel",
        children=[
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
