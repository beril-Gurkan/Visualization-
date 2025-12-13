# app.py
from jbi100_app.main import app
from jbi100_app.layouts.overview_layout import overview_layout
from jbi100_app.layouts.detailed_layout import detailed_layout

from dash import html, dcc, callback_context
from dash.dependencies import Input, Output


app.layout = html.Div(
    [
        dcc.Store(id="view-state", data=None),

        html.Button(
            id="btn-toggle-view",
            n_clicks=0
        ),

        html.Div(
            id="layout-container",
            children=[
                overview_layout(),
                detailed_layout()
            ]
        )
    ]
)


# Toggle view-state
@app.callback(
    Output("view-state", "data"),
    Input("btn-toggle-view", "n_clicks"),
    prevent_initial_call=True
)
def toggle_view(n_clicks):
    return "country" if n_clicks % 2 == 1 else None


# Update button label
@app.callback(
    Output("btn-toggle-view", "children"),
    Input("view-state", "data")
)
def update_button_label(view_state):
    if view_state:
        return "Back to global view"
    return "Select region"


# Toggle layout visibility
@app.callback(
    Output("overview-layout", "style"),
    Output("detailed-layout", "style"),
    Input("view-state", "data")
)
def toggle_layout_visibility(view_state):
    if view_state:
        return (
            {"display": "none"},
            {"display": "block"}
        )
    return (
        {"display": "block"},
        {"display": "none"}
    )


if __name__ == "__main__":
    app.run(debug=False, dev_tools_ui=False)