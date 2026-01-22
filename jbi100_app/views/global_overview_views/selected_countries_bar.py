from dash import html


def selected_countries_bar():
    return html.Div(
        className="panel", id="selected-countries-bar-panel",
        children=[
            html.Div(
                [
                    html.Div(
                        [
                            html.Div("Selected countries", className="countries-label"),
                            html.Div(id="selected-countries-label"),
                        ],
                        className="countries-info",
                    ),
                    html.Button(
                        "Clear",
                        id="clear-selected",
                        n_clicks=0,
                    ),
                ],
                className="wrapper"
            )
        ],
    )
