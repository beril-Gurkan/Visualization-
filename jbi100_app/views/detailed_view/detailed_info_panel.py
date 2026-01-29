# Detailed info panel - displays country-specific metadata and key statistics
# Shows: flag, name, region, population, GDP, area, energy consumption, etc.
# Updates when: user clicks country on map/scatterplot or selects from dropdown
# Also includes: radar chart comparing country to global averages

from dash import html, dcc

# Panel that displays detailed information about a selected country.
# Includes key stats upon hovering and info button, along with a radar chart comparing to global averages.
def detailed_info_panel():
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
