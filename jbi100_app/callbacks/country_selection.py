# Country selection callback - handles map clicks and selection state
# Maintains a list of selected countries (up to 10)
# Supports toggling selection on/off and clearing all selections

from dash.dependencies import Input, Output, State
from dash import callback_context

from jbi100_app.app_instance import app

# Limit to 10 countries to keep visualizations readable
MAX_SELECTED_COUNTRIES = 10


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
        # Cap the number of selected countries to MAX_SELECTED_COUNTRIES
        if len(s) >= MAX_SELECTED_COUNTRIES:
            return sorted(s)  # Don't add more if already at limit
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
    label_text = ", ".join(selected)
    if len(selected) >= MAX_SELECTED_COUNTRIES:
        label_text += f" (max {MAX_SELECTED_COUNTRIES})"
    return label_text