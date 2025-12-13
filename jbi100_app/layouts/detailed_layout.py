from dash import html
from jbi100_app.views.region_map_view import region_map_view
from jbi100_app.views.complex_metrics import complex_metrics
from jbi100_app.views.ranking_panel import ranking_panel
from jbi100_app.views.detailed_info import detailed_info

def detailed_layout():
    return html.Div(
        id="detailed-layout",
        className="layout",
        children=[
            html.Div(complex_metrics(), id="complex-metrics-wrapper"),
            html.Div(region_map_view(), id="region-map-wrapper"),
            html.Div(detailed_info(), id="detailed-info-wrapper"),
            html.Div(ranking_panel(), id="ranking-wrapper",)
        ]
    )