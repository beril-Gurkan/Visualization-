from dash import html, dcc


def selected_countries_bar():
    return html.Div(
        className="panel", id="selected-countries-bar-panel",
        children=[
            html.Div(
                [
                    html.Div(
                        [
                            html.H2("Selected countries", className="panel-title"),
                            html.Div(id="selected-countries-label"),
                        ],
                        className="countries-info",
                    ),
                    html.Div(
                        [
                            html.Button(
                                "Clear",
                                id="clear-selected",
                                n_clicks=0,
                            ),
                            dcc.Link(
                                html.Button(
                                    "Continue",
                                ),
                                href="/detailed"
                            ),
                        ],
                        className="buttons-group",
                    ),
                ],
                className="wrapper"
            )
        ],
    )
