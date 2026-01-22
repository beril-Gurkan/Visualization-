from dash import dcc, html


def map_card():
    return html.Div(
        style={
            "borderRadius": "12px",
            "border": "1px solid rgba(0,0,0,0.12)",
            "overflow": "hidden",
            "background": "white",
        },
        children=[
            dcc.Graph(
                id="globe-map",
                style={"height": "62vh"},
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
