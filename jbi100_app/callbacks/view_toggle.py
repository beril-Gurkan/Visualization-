from urllib.parse import urlencode

from dash import callback_context, no_update
from dash.dependencies import Input, Output

from jbi100_app.app_instance import app
from jbi100_app.data import get_data
from jbi100_app.utils.country_meta import attach_country_meta


def _build_region_lookup():
    """Precompute ISO3/name -> region for fast click lookups."""
    df = attach_country_meta(get_data()).dropna(subset=["iso3", "region", "Country"])
    iso_map = dict(zip(df["iso3"].str.upper(), df["region"]))
    name_map = dict(zip(df["Country"].str.upper(), df["region"]))
    return iso_map, name_map


ISO_TO_REGION, NAME_TO_REGION = _build_region_lookup()


def _region_from_click(point: dict):
    """Pull region from clickData point using ISO3 first, then country name."""
    if not point:
        return None

    iso3 = point.get("location")
    if iso3:
        iso3 = str(iso3).upper()
    if iso3 and iso3 in ISO_TO_REGION:
        return ISO_TO_REGION[iso3]

    custom = point.get("customdata")
    if custom and isinstance(custom, (list, tuple)) and len(custom) > 0:
        cand = str(custom[0]).upper()
        if cand in ISO_TO_REGION:
            return ISO_TO_REGION[cand]

    name = point.get("hovertext") or point.get("text")
    if name:
        return NAME_TO_REGION.get(str(name).upper())

    return None


@app.callback(
    Output("url", "pathname"),
    Output("url", "search"),
    Input("globe-map", "clickData"),
    Input("region-map-button", "n_clicks"),
    prevent_initial_call=True,
)
def route_by_map_click(click_data, back_clicks):
    """
    - Clicking a country on the globe navigates to /detail?region=<region>.
    - Clicking the Back button returns to the global view.
    """
    ctx = callback_context
    trigger = ctx.triggered[0]["prop_id"].split(".")[0] if ctx.triggered else None

    if trigger == "region-map-button":
        return "/", ""

    if trigger == "globe-map":
        # Globe clicks are reserved for multi-country selection; do not navigate.
        return no_update, no_update

    return no_update, no_update
