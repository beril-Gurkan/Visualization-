from dash import html
from jbi100_app.views.detailed_view.complex_metrics_panel import complex_metrics_panel
from jbi100_app.views.detailed_view.plot_panel import plot_panel
from jbi100_app.views.detailed_view.detailed_info_panel import detailed_info_panel
from jbi100_app.views.detailed_view.mini_map_panel import mini_map_panel
from jbi100_app.views.detailed_view.selected_ranking_panel import selected_ranking_panel

def detailed_layout():
    return html.Div(
        id="detailed-layout",
        className="layout",
        children=[
            complex_metrics_panel(),
            plot_panel(),
            detailed_info_panel(),
            mini_map_panel(),
            selected_ranking_panel(),
        ]
    )