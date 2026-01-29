# Overview layout - main landing page with global map and country selection
# Contains: title bar, selected countries display, metric cards, and interactive world map

from dash import html, dcc

from jbi100_app.views.global_overview.metrics_panel import metrics_panel
from jbi100_app.views.global_overview.selected_countries_bar import selected_countries_bar
from jbi100_app.views.global_overview.map_panel import map_panel


def overview_layout():
    return html.Div(
        id="overview-layout",
        children=[
            # Title panel
            html.Div(
                id="title-panel",
                children=[html.H1("GLOBAL OVERVIEW")],
            ),

            # Components
            selected_countries_bar(),
            metrics_panel(),
            map_panel(),
        ],
    )