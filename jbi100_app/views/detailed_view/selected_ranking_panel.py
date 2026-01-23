from dash import html, dcc


def selected_ranking_panel():
    """
    Panel that shows the ranking of all countries with selected ones highlighted,
    and a scatterplot below for comparing countries on complex metrics.
    """
    return html.Div(
        id="selected-ranking-panel",
        className="panel",
        children=[
            html.H2("Country Rankings", className="panel-title"),
            
            # Ranking controls
            html.Div(
                className="ranking-controls",
                children=[
                    # Metric selection dropdown
                    html.Div(
                        className="control-group",
                        children=[
                            html.Label("Rank by:", className="control-label"),
                            dcc.Dropdown(
                                id="detailed-ranking-metric",
                                clearable=False,
                                value="Complex_Metrics",
                                options=[
                                    {"label": "Complex Metrics (Weighted)", "value": "Complex_Metrics"},
                                    {"label": "GDP per Capita (USD)", "value": "Real_GDP_per_Capita_USD"},
                                    {"label": "Literacy Rate (%)", "value": "Total_Literacy_Rate"},
                                    {"label": "Electricity Access (%)", "value": "electricity_access_percent"},
                                    {"label": "Unemployment (%)", "value": "Unemployment_Rate_percent"},
                                ],
                            ),
                        ],
                    ),
                    dcc.Store(id="detailed-ranking-order", data="desc"),
                ],
            ),
            
            # Ranking bar chart
            dcc.Graph(
                id="detailed-ranking-bar",
                config={"displayModeBar": False, "responsive": True},
                style={"height": "400px", "marginBottom": "0px", "paddingBottom": "0px"},
            ),
            
            # Scatterplot section
            html.Div(
                className="scatterplot-section",
                children=[
                    html.H3("Metric Comparison"),
                    
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
                    
                    html.P("Click a point to select a country", className="scatterplot-hint"),
                    
                    # Scatterplot graph
                    dcc.Graph(
                        id="detailed-scatterplot",
                        config={"displayModeBar": True, "responsive": True},
                    ),
                ],
            ),
            
            # Selected country indicator
            html.Div(id="detailed-selected-country-indicator"),
        ]
    )
