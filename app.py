from dash import dcc, html
from dash.dependencies import Input, Output

from jbi100_app.main import app

# layouts
from jbi100_app.layouts.overview_layout import overview_layout
from jbi100_app.layouts.detailed_layout import detailed_layout

# IMPORTANT: import callbacks so they register
import jbi100_app.callbacks.ranking_callbacks
import jbi100_app.callbacks.region_map_callbacks
import jbi100_app.callbacks.detail_callbacks
import jbi100_app.callbacks.global_map_hover
import jbi100_app.callbacks.resize_callbacks
import jbi100_app.callbacks.view_toggle   # <-- (we will create/use this next)

# App layout (single source of truth)
app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        dcc.Store(id="selected_region", storage_type="memory"),
        dcc.Store(id="selected_country", storage_type="memory"),
        html.Div(id="page-content"),
    ]
)

# URL-based routing (ONLY ONE callback owns page-content)
@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname"),
    Input("url", "search"),
)
def display_page(pathname, search):
    # Region / Detail page
    if pathname == "/detail":
        return detailed_layout()

    # Default: overview
    return overview_layout()


if __name__ == "__main__":
    app.run(debug=False)
