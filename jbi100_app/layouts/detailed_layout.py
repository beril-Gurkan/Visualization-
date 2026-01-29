# Detailed analysis layout - accessed via 'Back' button from overview
# Grid-based layout with 6 main panels:
# - Complex metrics (left sidebar with toggleable weights)
# - Plot panel (metric card visualizations with expand functionality)
# - Country details (radar chart and stats for clicked country)
# - Scatterplot (2D comparison of complex metrics with brushing)
# - Mini map (focused view of selected countries)
# - Ranking panel (sortable bar chart of countries by selected metric)

from dash import html
from jbi100_app.views.detailed_view.complex_metrics_panel import complex_metrics_panel
from jbi100_app.views.detailed_view.plot_panel import plot_panel
from jbi100_app.views.detailed_view.detailed_info_panel import detailed_info_panel
from jbi100_app.views.detailed_view.scatterplot_panel import scatterplot_panel
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
            scatterplot_panel(),
            mini_map_panel(),
            selected_ranking_panel(),
        ]
    )