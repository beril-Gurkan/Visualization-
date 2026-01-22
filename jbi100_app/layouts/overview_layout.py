from dash import html, dcc

from jbi100_app.views.global_overview_views.metrics_panel import metrics_panel
from jbi100_app.views.global_overview_views.selected_countries_bar import selected_countries_bar
from jbi100_app.views.global_overview_views.map_card import map_card
from jbi100_app.views.global_overview_views.ranking_panel import ranking_panel


def overview_layout():
    return html.Div(
        style={
            "display": "flex",
            "height": "100vh",
            "fontFamily": "Arial",
            "background": "#ffffff",
        },
        children=[
            metrics_panel(),

            # RIGHT PANEL
            html.Div(
                style={"flex": "1", "padding": "18px", "overflow": "hidden", "background": "#ffffff"},
                children=[
                    # Stores must be in the layout
                    dcc.Store(id="selected-countries", data=[]),

                    html.H1(
                        "Global Overview",
                        style={"textAlign": "center", "margin": "4px 0 8px 0", "fontSize": "54px", "fontWeight": "500"},
                    ),

                    selected_countries_bar(),
                    map_card(),
                    ranking_panel(),
                ],
            ),
        ],
    )