from jbi100_app.main import app
from jbi100_app.layouts.overview_layout import overview_layout
from jbi100_app.layouts.detailed_layout import detailed_layout

from dash import html, dcc

# callbacks (must be imported so Dash registers them)
import jbi100_app.callbacks.view_toggle
import jbi100_app.callbacks.ranking_callbacks
import jbi100_app.callbacks.detail_callbacks
import jbi100_app.callbacks.region_map_callbacks
import jbi100_app.callbacks.resize_callbacks

# ✅ new: multi-view (scatterplot) callback module
import jbi100_app.callbacks.multiview_callbacks


app.layout = html.Div(
    [
        dcc.Store(id="selected_region", data=None),
        dcc.Store(id="selected_country", data=None),

        html.Div(id="resize-sentinel", style={"display": "none"}),

        html.Div(
            id="layout-container",
            children=[
                html.H1("Global Overview", id="title"),
                overview_layout(),
                detailed_layout(),
            ],
        ),
    ]
)

if __name__ == "__main__":
    app.run(debug=True, dev_tools_ui=False)