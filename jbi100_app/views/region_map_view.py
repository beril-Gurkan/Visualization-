from dash import html, dcc

def region_map_view():
    return html.Div(
        className="panel",
        children=[
            html.Div(
                style={"display": "flex", "justifyContent": "space-between", "width": "100%"},
                children=[html.H3("Region Map View", className="panel-title", id="region-map-title"), html.Button("Back to global view", className="btn-reset-filters", id="region-map-button"),]
            ),
            dcc.Graph(
                id="region-map",
                config={"displayModeBar": False, "responsive": True},
                style={"width": "100%", "height": "100%"},
            ),
        ],
    )