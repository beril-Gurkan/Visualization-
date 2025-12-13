from dash.dependencies import Input, Output
from jbi100_app.main import app


@app.callback(
    Output("selected_region", "data"),
    Input("btn-toggle-view", "n_clicks"),
    prevent_initial_call=True
)
def toggle_view(n_clicks):
    return "this region" if n_clicks % 2 == 1 else None


@app.callback(
    Output("btn-toggle-view", "children"),
    Input("selected_region", "data")
)
def update_button_label(view_state):
    if view_state:
        return "Back to global view"
    return "Select region"


@app.callback(
    Output("overview-layout", "style"),
    Output("detailed-layout", "style"),
    Input("selected_region", "data")
)
def toggle_layout_visibility(view_state):
    if view_state:
        return {"display": "none"}, {"display": "block"}
    return {"display": "block"}, {"display": "none"}