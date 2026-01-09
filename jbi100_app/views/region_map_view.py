from dash import html, dcc

def region_map_view():
    return html.Div(
        className="panel",
        style={
            "justifyContent": "flex-start",
            "alignItems": "stretch",
            "gap": "8px",
            "fontSize": "1.2rem",
            "padding": "12px",
        },
        children=[
            html.Div(id="region-map-title", style={"fontWeight": "700"}, children="Region Map View"),
            dcc.Graph(
                id="region-map",
                config={"displayModeBar": False, "responsive": True},
                style={"width": "100%", "height": "100%"},
            ),
            html.Button("Back to global view", id="region-map-button"),
        ],
    )