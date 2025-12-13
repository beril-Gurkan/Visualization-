from dash import html
from jbi100_app.views.map_view import map_view
from jbi100_app.views.complex_metrics import complex_metrics
from jbi100_app.views.ranking_panel import ranking_panel
from jbi100_app.views.detailed_info import detailed_info

def detailed_layout():
    return html.Div(
        id="detailed-layout",
        className="layout",
        children=[
            html.H1("Selected Region"),
            html.Div(
                className="region-main-grid",
                children=[
                    html.Div(
                        className="left-column",
                        children=[
                            complex_metrics(),
                            html.Div("Main Metric Graph"),
                        ]
                    ),
                    html.Div(
                        className="center-column",
                        children=[
                            map_view(),
                            detailed_info()
                        ]
                    ),
                    html.Div(
                        ranking_panel(),
                        className="right-column"
                    )
                ]
            )
        ]
    )