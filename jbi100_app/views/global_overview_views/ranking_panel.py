from dash import dcc, html


def ranking_panel():
    return html.Div(
        id="ranking-panel",
        children=[
            html.Div(
                className="ranking-header",
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
                    ),
                ],
            ),
            html.Div(id="ranking-container"),
        ],
    )
