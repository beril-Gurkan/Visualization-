from dash.dependencies import Input, Output
from jbi100_app.app_instance import app
from jbi100_app.views.detailed_view.selected_ranking_panel import selected_ranking_panel_list


@app.callback(
    Output("selected-ranking-panel", "children"),
    Input("selected-countries", "data"),
)
def update_ranking_panel(selected_countries):
    """Update the ranking panel when selected countries change."""
    return selected_ranking_panel_list(selected_countries)
