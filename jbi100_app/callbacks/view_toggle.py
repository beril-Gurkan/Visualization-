from dash import ctx
from dash.dependencies import Input, Output, State
from jbi100_app.main import app


@app.callback(
    Output("overview-layout", "style"),
    Output("detailed-layout", "style"),
    Output("title", "children"),
    Input("selected_region", "data")
)
def toggle_layout_visibility(view_state):
    if view_state:
        return {"display": "none"}, {"display": "grid"}, "Business Expander - Regional Overview"
    return {"display": "grid"}, {"display": "none"}, "Business Expander - Global Overview"


@app.callback(
    Output("selected_region", "data"),
    Input("global-map", "clickData"),
    Input("region-map-button", "n_clicks"),
    State("selected_region", "data"),
    prevent_initial_call=True
)
def update_selected_region(map_click, back_clicks, current_state):
    if ctx.triggered_id == "region-map-button":
        return None

    if ctx.triggered_id == "global-map" and map_click and map_click.get("points"):
        # region stored as custom_data[0]
        region = map_click["points"][0].get("customdata", [None])[0]
        return region or current_state

    return current_state
