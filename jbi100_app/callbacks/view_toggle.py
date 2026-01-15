from urllib.parse import urlencode, parse_qs

from dash import callback_context, no_update
from dash.dependencies import Input, Output

from jbi100_app.main import app
from jbi100_app.data import get_data
from jbi100_app.utils.country_meta import attach_country_meta


@app.callback(
    Output("url", "pathname"),
    Output("url", "search"),
    Input("globe-map", "clickData"),
    Input("region-map-button", "n_clicks"),
    prevent_initial_call=True,
)
def route_by_map_click(clickData, back_clicks):
    """
    - Clicking a country on the globe navigates to /detail?region=<region>.
    - Clicking the Back button returns to the global view.
    """
    triggered = callback_context.triggered_id

    if triggered == "region-map-button":
        return "/", ""

    if triggered == "globe-map":
        if not clickData or "points" not in clickData:
            return no_update, no_update

        point = clickData["points"][0]
        df = attach_country_meta(get_data()).dropna(subset=["iso3", "region", "Country"])

        # Try iso3 first (most reliable)
        iso3 = point.get("location")
        if iso3:
            row = df[df["iso3"] == iso3]
            if not row.empty:
                region = row.iloc[0]["region"]
                return "/detail", "?" + urlencode({"region": region})

        # Fallback: try country name
        name = point.get("hovertext") or point.get("text")
        if name:
            row = df[df["Country"].str.upper() == str(name).upper()]
            if not row.empty:
                region = row.iloc[0]["region"]
                return "/detail", "?" + urlencode({"region": region})

    return no_update, no_update


@app.callback(
    Output("selected_region", "data"),
    Input("url", "pathname"),
    Input("url", "search"),
)
def sync_region_store(pathname, search):
    """
    Read the region from the URL when on /detail and push it into the store.
    Clears the store when leaving the detail view.
    """
    if pathname != "/detail":
        return None

    query = parse_qs(search.lstrip("?") if search else "")
    region = query.get("region", [None])[0]
    return region
