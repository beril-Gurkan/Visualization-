from dash import dcc, html


def ranking_panel():
    return html.Div(
        style={
            "marginTop": "12px",
            "padding": "12px",
            "borderRadius": "12px",
            "border": "1px solid rgba(0,0,0,0.12)",
            "background": "white",
        },
        children=[
            html.Div(
                style={"display": "flex", "gap": "10px", "alignItems": "center", "marginBottom": "10px"},
                children=[
                    dcc.Dropdown(
                        id="topn-dropdown",
                        options=[
                            {"label": "Top 10", "value": 10},
                            {"label": "Top 20", "value": 20},
                            {"label": "Top 50", "value": 50},
                            {"label": "All", "value": "all"},
                        ],
                        value=20,
                        clearable=False,
                        style={"width": "220px"},
                    ),
                ],
            ),
            html.Div(
                id="ranking-container",
                style={"maxHeight": "22vh", "overflowY": "auto", "paddingRight": "6px"},
            ),
        ],
    )
