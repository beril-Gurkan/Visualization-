from dash import html, dcc


def multiview_panel():
    """
    Framework panel for multiple coordinated views.
    Tab 1 contains the scatterplot (existing functionality).
    Other tabs are placeholders for future small multiples / distributions etc.
    """
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
            html.Div("Multiple Views", style={"fontWeight": "800"}),

            dcc.Tabs(
                id="multiview-tabs",
                value="tab-scatter",
                children=[
                    dcc.Tab(
                        label="Scatterplot (relationships)",
                        value="tab-scatter",
                        children=[
                            html.Div(
                                id="scatterplot-container",
                                style={"marginTop": "10px"},
                            )
                        ],
                    ),
                    dcc.Tab(
                        label="Small multiples (placeholder)",
                        value="tab-smallmultiples",
                        children=[
                            html.Div(
                                "Placeholder: small multiples grid will go here (compare countries across metrics).",
                                style={"padding": "10px", "opacity": 0.75},
                            )
                        ],
                    ),
                    dcc.Tab(
                        label="Distributions (placeholder)",
                        value="tab-distributions",
                        children=[
                            html.Div(
                                "Placeholder: distribution / percentile view will go here.",
                                style={"padding": "10px", "opacity": 0.75},
                            )
                        ],
                    ),
                ],
            ),
        ],
    )
