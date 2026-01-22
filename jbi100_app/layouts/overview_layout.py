from dash import html, dcc


def overview_layout():
    return html.Div(
        style={
            "display": "flex",
            "height": "100vh",
            "fontFamily": "Arial",
            "background": "#ffffff",
        },
        children=[
            # LEFT PANEL
            html.Div(
                style={
                    "width": "360px",
                    "padding": "22px 18px",
                    "borderRight": "2px solid #1f1f1f",
                    "overflowY": "auto",
                    "background": "#ffffff",
                },
                children=[
                    html.H1(
                        "Global Metrics",
                        style={"margin": "0 0 18px 0", "fontSize": "44px", "fontWeight": "500"},
                    ),

                    html.H2("Economic", style={"fontSize": "34px", "margin": "14px 0 10px 0", "fontWeight": "500"}),
                    dcc.Checklist(
                        id="metric-checklist",
                        options=[
                            {"label": "Unemployment rate", "value": "unemployment"},
                            {"label": "GDP per capita", "value": "gdp_pc"},
                        ],
                        value=["unemployment", "gdp_pc"],
                        inputStyle={"marginRight": "10px"},
                        labelStyle={"display": "block", "marginBottom": "8px", "fontSize": "16px"},
                    ),
                    html.Div("Importance", style={"marginTop": "8px", "fontSize": "16px"}),
                    dcc.Slider(
                        id="w-unemployment", min=0, max=100, step=1, value=60,
                        marks={0: "0", 100: "100"},
                        tooltip={"placement": "bottom", "always_visible": True},
                    ),
                    html.Div(style={"height": "14px"}),
                    dcc.Slider(
                        id="w-gdp_pc", min=0, max=100, step=1, value=70,
                        marks={0: "0", 100: "100"},
                        tooltip={"placement": "bottom", "always_visible": True},
                    ),

                    html.Hr(style={"margin": "22px 0", "opacity": 0.3}),

                    html.H2("Demographic", style={"fontSize": "34px", "margin": "14px 0 10px 0", "fontWeight": "500"}),
                    dcc.Checklist(
                        id="metric-checklist-dem",
                        options=[
                            {"label": "Youth unemployment rate", "value": "youth_unemp"},
                            {"label": "Population growth rate", "value": "pop_growth"},
                        ],
                        value=["youth_unemp", "pop_growth"],
                        inputStyle={"marginRight": "10px"},
                        labelStyle={"display": "block", "marginBottom": "8px", "fontSize": "16px"},
                    ),
                    html.Div("Importance", style={"marginTop": "8px", "fontSize": "16px"}),
                    dcc.Slider(
                        id="w-youth_unemp", min=0, max=100, step=1, value=50,
                        marks={0: "0", 100: "100"},
                        tooltip={"placement": "bottom", "always_visible": True},
                    ),
                    html.Div(style={"height": "14px"}),
                    dcc.Slider(
                        id="w-pop_growth", min=0, max=100, step=1, value=40,
                        marks={0: "0", 100: "100"},
                        tooltip={"placement": "bottom", "always_visible": True},
                    ),

                    html.Hr(style={"margin": "22px 0", "opacity": 0.3}),

                    html.H2("Sustainability", style={"fontSize": "34px", "margin": "14px 0 10px 0", "fontWeight": "500"}),
                    dcc.Checklist(
                        id="metric-checklist-sus",
                        options=[
                            {"label": "Electricity access %", "value": "elec_access"},
                            {"label": "Electricity generating capacity (relative)", "value": "elec_capacity"},
                        ],
                        value=["elec_access", "elec_capacity"],
                        inputStyle={"marginRight": "10px"},
                        labelStyle={"display": "block", "marginBottom": "8px", "fontSize": "16px"},
                    ),
                    html.Div("Importance", style={"marginTop": "8px", "fontSize": "16px"}),
                    dcc.Slider(
                        id="w-elec_access", min=0, max=100, step=1, value=65,
                        marks={0: "0", 100: "100"},
                        tooltip={"placement": "bottom", "always_visible": True},
                    ),
                    html.Div(style={"height": "14px"}),
                    dcc.Slider(
                        id="w-elec_capacity", min=0, max=100, step=1, value=55,
                        marks={0: "0", 100: "100"},
                        tooltip={"placement": "bottom", "always_visible": True},
                    ),
                ],
            ),

            # RIGHT PANEL
            html.Div(
                style={"flex": "1", "padding": "18px", "overflow": "hidden", "background": "#ffffff"},
                children=[
                    # Stores must be in the layout
                    dcc.Store(id="selected-countries", data=[]),

                    html.H1(
                        "Global Overview",
                        style={"textAlign": "center", "margin": "4px 0 8px 0", "fontSize": "54px", "fontWeight": "500"},
                    ),

                    # Selected countries bar
                    html.Div(
                        style={
                            "margin": "0 0 10px 0",
                            "padding": "10px 12px",
                            "borderRadius": "12px",
                            "border": "1px solid rgba(0,0,0,0.12)",
                            "background": "white",
                            "display": "flex",
                            "alignItems": "center",
                            "justifyContent": "space-between",
                            "gap": "12px",
                        },
                        children=[
                            html.Div(
                                [
                                    html.Div("Selected countries", style={"fontWeight": 700, "marginBottom": "4px"}),
                                    html.Div(id="selected-countries-label", style={"opacity": 0.8}),
                                ],
                                style={"flex": "1"},
                            ),
                            html.Button(
                                "Clear",
                                id="clear-selected",
                                n_clicks=0,
                                style={
                                    "border": "1px solid rgba(0,0,0,0.2)",
                                    "background": "white",
                                    "borderRadius": "10px",
                                    "padding": "8px 12px",
                                    "cursor": "pointer",
                                    "fontWeight": 600,
                                },
                            ),
                        ],
                    ),

                    # MAP
                    html.Div(
                        style={
                            "borderRadius": "12px",
                            "border": "1px solid rgba(0,0,0,0.12)",
                            "overflow": "hidden",
                            "background": "white",
                        },
                        children=[
                            dcc.Graph(
                                id="globe-map",
                                style={"height": "62vh"},
                                config={
                                    "displayModeBar": True,
                                    "scrollZoom": True,
                                    "doubleClick": "reset",
                                    "showTips": False,
                                    "modeBarButtonsToRemove": ["lasso2d", "select2d"],
                                },
                            ),
                        ],
                    ),

                    # RANKING
                    html.Div(
                        style={
                            "marginTop": "12px",
                            "padding": "12px",
                            "borderRadius": "12px",
                            "border": "1px solid rgba(0,0,0,0.12)",
                            "background": "white",
                        },
                        children=[
                            html.Div(
                                style={"display": "flex", "gap": "10px", "alignItems": "center", "marginBottom": "10px"},
                                children=[
                                    dcc.Dropdown(
                                        id="topn-dropdown",
                                        options=[
                                            {"label": "Top 10", "value": 10},
                                            {"label": "Top 20", "value": 20},
                                            {"label": "Top 50", "value": 50},
                                            {"label": "All", "value": "all"},
                                        ],
                                        value=20,
                                        clearable=False,
                                        style={"width": "220px"},
                                    ),
                                ],
                            ),
                            html.Div(
                                id="ranking-container",
                                style={"maxHeight": "22vh", "overflowY": "auto", "paddingRight": "6px"},
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )