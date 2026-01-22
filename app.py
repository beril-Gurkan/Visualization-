from dash import dcc, html
from dash.dependencies import Input, Output

from jbi100_app.app_instance import app
from jbi100_app.layouts.overview_layout import overview_layout
from jbi100_app.layouts.detailed_layout import detailed_layout

from jbi100_app.callbacks.register_callbacks import register_callbacks

# Register all callbacks
register_callbacks()

# Single source of truth layout
app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        dcc.Store(id="selected_country", storage_type="memory"),
        html.Div(id="page-content"),
    ]
)

# Simple routing
@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname"),
)
def display_page(pathname):
    if pathname == "/detailed":
        return detailed_layout()
    return overview_layout()


if __name__ == "__main__":
    app.run(debug=True)