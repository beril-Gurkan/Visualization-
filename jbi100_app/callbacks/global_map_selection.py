# jbi100_app/callbacks/global_map_selection.py
from typing import Optional
from dash import callback_context, no_update
from dash.dependencies import Input, Output, State
from jbi100_app.app_instance import app


def _iso_from_click(click_data) -> Optional[str]:
    if not click_data or not click_data.get("points"):
        return None
    pt = (click_data.get("points") or [None])[0] or {}
    iso = pt.get("location")
    return str(iso).strip().upper() if iso else None


@app.callback(
    Output("selected-countries", "data"),
    Input("globe-map", "clickData"),
    Input("clear-selected", "n_clicks"),
    State("selected-countries", "data"),
    prevent_initial_call=True,
)
def toggle_selected_countries(click_data, clear_clicks, selected):
    trigger = callback_context.triggered[0]["prop_id"].split(".")[0] if callback_context.triggered else None
    selected = selected or []

    if trigger == "clear-selected":
        return []

    if trigger == "globe-map":
        iso3 = _iso_from_click(click_data)
        if not iso3:
            return selected

        s = {str(x).strip().upper() for x in selected if x}
        if iso3 in s:
            s.remove(iso3)
        else:
            s.add(iso3)
        return sorted(s)

    return no_update