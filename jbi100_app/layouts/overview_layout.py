from dash import html
from jbi100_app.views.global_map_view import global_map_view
from jbi100_app.views.global_metrics import global_metrics

def overview_layout():
    return html.Div(
        id="overview-layout",
        className="layout",
        children=[
            html.H1("Global Overview"),
            html.Div(
                className="overview-content",
                children=[
                    html.Div(global_metrics(), id="global-metrics-wrapper"),
                    html.Div(global_map_view(), id="global-map-wrapper"),
                ]
            )
        ]
    )