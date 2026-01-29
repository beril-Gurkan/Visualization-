# Mini map panel - read-only world map showing selected countries highlighted
# Purpose: provides geographic context in detailed view without interaction
# Different from overview map: no clicking, just shows current selection in corner of detailed view

from dash import html, dcc

# Relates to the mini map panel in the corner of the detailed view.
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
