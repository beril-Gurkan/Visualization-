from dash import html


def selected_countries_bar():
    return html.Div(
        style={
            "margin": "0 0 10px 0",
            "padding": "10px 12px",
            "borderRadius": "12px",
            "border": "1px solid rgba(0,0,0,0.12)",
            "background": "white",
            "display": "flex",
            "alignItems": "center",
            "justifyContent": "space-between",
            "gap": "12px",
        },
        children=[
            html.Div(
                [
                    html.Div("Selected countries", style={"fontWeight": 700, "marginBottom": "4px"}),
                    html.Div(id="selected-countries-label", style={"opacity": 0.8}),
                ],
                style={"flex": "1"},
            ),
            html.Button(
                "Clear",
                id="clear-selected",
                n_clicks=0,
                style={
                    "border": "1px solid rgba(0,0,0,0.2)",
                    "background": "white",
                    "borderRadius": "10px",
                    "padding": "8px 12px",
                    "cursor": "pointer",
                    "fontWeight": 600,
                },
            ),
        ],
    )
