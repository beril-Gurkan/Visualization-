"""
Main application entry point for the Global Expansion Evaluator.
Sets up the Dash app with two views: overview and detailed analysis.
"""

from dash import dcc, html
from dash.dependencies import Input, Output

from jbi100_app.app_instance import app
from jbi100_app.layouts.overview_layout import overview_layout
from jbi100_app.layouts.detailed_layout import detailed_layout

from jbi100_app.callbacks.register_callbacks import register_callbacks

# Register all interactive callbacks (map clicks, filters, brushing, etc.)
register_callbacks()

# Main layout: includes URL routing and shared data stores
# Stores allow data to be shared between callbacks without recomputation
app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        # Memory stores for cross-component state management
        dcc.Store(id="selected_country", storage_type="memory"),  # Currently clicked country
        dcc.Store(id="selected-countries", storage_type="memory"),  # Countries selected on map
        dcc.Store(id="metric-brush", storage_type="memory"),  # Brushed countries from metric cards
        dcc.Store(id="metric-brush-rev", storage_type="memory"),  # Revision counter for brush updates
        dcc.Store(id="expanded-metric", storage_type="memory"),  # Currently expanded metric card
        html.Div(id="layout-container"),
    ]
)

# URL-based routing between overview and detailed view
@app.callback(
    Output("layout-container", "children"),
    Input("url", "pathname"),
)
def display_page(pathname):
    """Switch between overview and detailed layouts based on URL."""
    if pathname == "/detailed":
        return detailed_layout()
    return overview_layout()


if __name__ == "__main__":
    app.run(debug=False)