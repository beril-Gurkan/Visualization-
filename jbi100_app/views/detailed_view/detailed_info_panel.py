from dash import html, dcc


def detailed_info_panel():
    """
    Panel that displays detailed information about a selected country.
    Includes key stats side-by-side with a radar chart comparing to global averages.
    """
    return html.Div(
        id="detailed-info-panel",
        className="panel",
        children=[
            html.H2("Country Details", className="panel-title"),
            html.Div(
                id="detailed-info-content",
                children=[
                    html.Div(
                        "Select a country from the ranking or scatterplot to view details.",
                        className="detailed-info-placeholder"
                    )
                ]
            )
        ]
    )
