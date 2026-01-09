from dash import html, dcc


def ranking_panel():
    """Interactive ranking panel with customizable metrics, sort order, and top N selection."""
    return html.Div(
        className="panel",
        style={
            "justifyContent": "flex-start",
            "alignItems": "stretch",
            "gap": "10px",
            "fontSize": "1.2rem",
            "padding": "12px",
        },
        children=[
            html.Div(id="ranking-title", style={"fontWeight": "800"}, children="Ranking (select a region)"),

            dcc.Dropdown(
                id="ranking-metric",
                clearable=False,
                value="Complex_Metrics",
                options=[
                    {"label": "Complex Metrics (Custom Weights)", "value": "Complex_Metrics"},
                    {"label": "GDP per Capita (USD)", "value": "Real_GDP_per_Capita_USD"},
                    {"label": "Literacy Rate (%)", "value": "Total_Literacy_Rate"},
                    {"label": "Electricity Access (%)", "value": "electricity_access_percent"},
                    {"label": "Unemployment (%)", "value": "Unemployment_Rate_percent"},
                    {"label": "Public Debt (% of GDP)", "value": "Public_Debt_percent_of_GDP"},
                ],
            ),

            dcc.RadioItems(
                id="ranking-order",
                value="desc",
                options=[
                    {"label": "High → Low", "value": "desc"},
                    {"label": "Low → High", "value": "asc"},
                ],
                inline=True,
            ),

            dcc.Slider(
                id="ranking-top-n",
                min=5,
                max=30,
                step=1,
                value=15,
                marks={5: "5", 10: "10", 15: "15", 20: "20", 25: "25", 30: "30"},
            ),

            dcc.Graph(
                id="ranking-bar",
                config={"displayModeBar": False, "responsive": True},
                style={"flex": "1 1 auto", "width": "100%"},
            ),

            html.Div(
                "Click a bar to select a country.",
                style={"fontSize": "0.95rem", "opacity": 0.9},
            ),
        ],
    )
