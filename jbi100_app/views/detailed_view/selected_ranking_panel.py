from dash import html
from jbi100_app.data import get_data
from jbi100_app.utils.country_meta import attach_country_meta


def get_iso3_to_country_map():
    """
    Create a mapping from ISO3 codes to country names.
    """
    df = attach_country_meta(get_data())
    # Create a dict mapping iso3 -> Country name
    iso3_map = df.dropna(subset=["iso3"]).set_index("iso3")["Country"].to_dict()
    return iso3_map


def order_countries(countries):
    """
    Order countries by a specific criterion.
    Currently: alphabetical ordering (placeholder for custom ordering)
    """
    if not countries:
        return []
    return sorted(countries)


def selected_ranking_panel_list(selected_countries=None):
    """
    Create the content for the ranking panel (title and list only).
    """
    if selected_countries is None:
        selected_countries = []
    
    ordered_countries = order_countries(selected_countries)
    
    # Map ISO3 codes to full country names
    iso3_map = get_iso3_to_country_map()
    
    country_items = [
        html.Div(
            iso3_map.get(country.upper(), country),  # Fallback to ISO3 if not found
            className="ranking-country-item",
        )
        for country in ordered_countries
    ]
    
    return [
        html.H3("Ranking", className="panel-title"),
        html.Div(
            className="ranking-country-list",
            children=country_items if country_items else html.P("No countries selected", className="empty-message"),
        ),
    ]


def selected_ranking_panel(selected_countries=None):
    """
    Create a ranking panel displaying selected countries.
    For backwards compatibility, returns the full div with content.
    """
    return html.Div(
        id="selected-ranking-panel",
        className="panel",
        children=selected_ranking_panel_list(selected_countries),
    )
