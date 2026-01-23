from dash.dependencies import Input, Output, State
from dash import callback_context

from jbi100_app.app_instance import app


@app.callback(
    Output("selected-countries", "data"),
    Input("globe-map", "clickData"),
    Input("clear-selected", "n_clicks"),
    State("selected-countries", "data"),
    prevent_initial_call=True,
)
def toggle_selected(clickData, clear_clicks, selected):
    selected = selected or []

    ctx = callback_context
    trigger = ctx.triggered_id

    # Only clear if the button was actually clicked
    if trigger == "clear-selected" and clear_clicks:
        return []

    if trigger != "globe-map":
        return selected

    if not clickData or "points" not in clickData or not clickData["points"]:
        return selected

    iso3 = clickData["points"][0].get("location")
    if not iso3:
        return selected

    iso3 = iso3.upper().strip()
    s = {x.upper().strip() for x in selected if x}

    if iso3 in s:
        s.remove(iso3)
    else:
        s.add(iso3)

    return sorted(s)


@app.callback(
    Output("selected-countries-label", "children"),
    Input("selected-countries", "data"),
)
def label(selected):
    selected = selected or []
    if not selected:
        return "None"
    return ", ".join(selected[:10]) + (f" (+{len(selected)-10} more)" if len(selected) > 10 else "")