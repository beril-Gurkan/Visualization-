from jbi100_app.main import app
from jbi100_app.layouts.overview_layout import overview_layout
from jbi100_app.layouts.detailed_layout import detailed_layout

from dash import html, dcc

# Import callbacks
import jbi100_app.callbacks.view_toggle


app.layout = html.Div(
    [
        dcc.Store(id="selected_region", data=None),

        html.Button(id="btn-toggle-view", n_clicks=0),

        html.Div(
            id="layout-container",
            children=[
                overview_layout(),
                detailed_layout()
            ]
        )
    ]
)

if __name__ == "__main__":
    app.run(debug=False, dev_tools_ui=False)