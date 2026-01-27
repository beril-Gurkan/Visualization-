from dash import html, dcc


def mini_map_panel():
    return html.Div(
        id="mini-map-panel",
        className="panel",
        children=[
            dcc.Graph(
                id="mini-map",
                className="graph-container",
                config={
                    "displayModeBar": False,
                    "scrollZoom": False,
                    "doubleClick": "reset",
                    "showTips": False,
                },
                style={"height": "100%", "width": "100%"}
            ),
            dcc.Link(
                html.Div(
                    className="mini-map-overlay",
                    children=[
                        html.P("Click here to go back to Global Overview"),
                    ]
                ),
                href="/"
            ),
        ]
    )
