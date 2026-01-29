from dash import html, dcc


def scatterplot_panel():
    """
    Panel containing the scatterplot for comparing countries on complex metrics.
    """
    return html.Div(
        id="scatterplot-panel",
        className="panel",
        children=[
            html.H2("Complex Metrics Comparison", className="panel-title"),
            
            # Axis selection dropdowns
            html.Div(
                className="axis-controls",
                children=[
                    html.Div(
                        className="axis-control",
                        children=[
                            html.Label("X-Axis:", className="axis-label"),
                            dcc.Dropdown(
                                id="scatter-x-axis",
                                clearable=False,
                                value="ASF",
                                options=[
                                    {"label": "Skilled Workforce", "value": "ASF"},
                                    {"label": "Energy Capacity", "value": "IEC"},
                                    {"label": "Supply Chain", "value": "SCC"},
                                    {"label": "Wage Sustainability", "value": "WSI"},
                                    {"label": "Economic Resilience", "value": "ERS"},
                                ],
                            ),
                        ],
                    ),
                    html.Div(
                        className="axis-control",
                        children=[
                            html.Label("Y-Axis:", className="axis-label"),
                            dcc.Dropdown(
                                id="scatter-y-axis",
                                clearable=False,
                                value="IEC",
                                options=[
                                    {"label": "Skilled Workforce", "value": "ASF"},
                                    {"label": "Energy Capacity", "value": "IEC"},
                                    {"label": "Supply Chain", "value": "SCC"},
                                    {"label": "Wage Sustainability", "value": "WSI"},
                                    {"label": "Economic Resilience", "value": "ERS"},
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            
            # Dynamic subtitle
            html.P("Click on a point to select a country", className="scatterplot-hint"),
            html.Div(id="scatterplot-subtitle"),
            
            
            # Scatterplot graph
            dcc.Graph(
                id="detailed-scatterplot",
                config={"displayModeBar": True, "responsive": True},
                style={"flex": "1", "width": "100%"},
            ),
        ]
    )
