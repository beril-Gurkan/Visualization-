from urllib.parse import parse_qs

from dash.dependencies import Input, Output

from jbi100_app.app_instance import app
from jbi100_app.data import get_data
from jbi100_app.utils.country_meta import attach_country_meta


# Keep a simple set of valid regions to ignore junk query params
VALID_REGIONS = set(
    attach_country_meta(get_data())
    .dropna(subset=["region"])["region"]
    .unique()
)


@app.callback(
    Output("selected_region", "data"),
    Input("url", "pathname"),
    Input("url", "search"),
)
def sync_region_store(pathname, search):
    """
    Push ?region=<...> from the URL into the selected_region store when on /detail.
    Clears the store when navigating away.
    """
    if pathname != "/detail":
        return None

    query = parse_qs(search.lstrip("?") if search else "")
    region = query.get("region", [None])[0]
    return region if region in VALID_REGIONS else None
