# Selected countries bar - displays currently selected countries with remove buttons
# Shows: list of selected countries with × buttons to deselect individual countries
# Updates: when countries are clicked on map or selected via dropdown

from dash import html

# Build the selection display bar
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
