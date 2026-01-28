from dash import html, dcc


def selected_ranking_panel():
    """
    Panel that shows the ranking of all countries with selected ones highlighted.
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
            
            # Dynamic subtitle
            html.Div(id="ranking-subtitle"),
            
            # Ranking bar chart
            dcc.Graph(
                id="detailed-ranking-bar",
                config={"displayModeBar": False, "responsive": True},
                style={"flex": "1", "width": "100%"},
            ),
            
            # Selected country indicator
            html.Div(id="detailed-selected-country-indicator"),
        ]
    )
