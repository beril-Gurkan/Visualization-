from dash import ctx
from dash.dependencies import Input, Output, State
from jbi100_app.main import app

@app.callback(
    Output("overview-layout", "style"),
    Output("detailed-layout", "style"),
    Input("selected_region", "data")
)
def toggle_layout_visibility(view_state):
    if view_state:
        return {"display": "none"}, {"display": "block"}
    return {"display": "block"}, {"display": "none"}

@app.callback(
    Output("selected_region", "data"),
    Input("global-map-button", "n_clicks"),
    Input("region-map-button", "n_clicks"),
    State("selected_region", "data"),
    prevent_initial_call=True
)
def update_selected_region(global_clicks, region_clicks, current_state):
    if ctx.triggered_id == "global-map-button":
        return "selected_region"
    elif ctx.triggered_id == "region-map-button":
        return None
    return current_state