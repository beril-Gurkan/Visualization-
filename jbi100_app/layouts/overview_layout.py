from dash import html, dcc
from dash import dcc

dcc.Store(id="selected_region", storage_type="memory")

def overview_layout():
    return html.Div(
        style={
            "display": "flex",
            "height": "100vh",
            "fontFamily": "Arial",
            "background": "#ffffff",
            "overflow": "hidden",
        },
        children=[
            # LEFT PANEL
            html.Div(
                style={
                    "width": "360px",
                    "padding": "20px",
                    "borderRight": "2px solid #222",
                    "overflowY": "auto",
                    "background": "#ffffff",
                },
                children=[
                    html.H2("Global Metrics", style={"marginTop": "0"}),

                    html.H3("Economic"),
                    dcc.Checklist(
                        id="metric-checklist",
                        options=[
                            {"label": "Unemployment rate", "value": "unemployment"},
                            {"label": "GDP per capita", "value": "gdp_pc"},
                        ],
                        value=["unemployment", "gdp_pc"],
                    ),
                    html.Div("Importance"),
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

                    html.Hr(),

                    html.H3("Demographic"),
                    dcc.Checklist(
                        id="metric-checklist-dem",
                        options=[
                            {"label": "Youth unemployment rate", "value": "youth_unemp"},
                            {"label": "Population growth rate", "value": "pop_growth"},
                        ],
                        value=["youth_unemp", "pop_growth"],
                    ),
                    html.Div("Importance"),
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

                    html.Hr(),

                    html.H3("Sustainability"),
                    dcc.Checklist(
                        id="metric-checklist-sus",
                        options=[
                            {"label": "Electricity access %", "value": "elec_access"},
                            {"label": "Electricity generation capacity (relative)", "value": "elec_capacity"},
                        ],
                        value=["elec_access", "elec_capacity"],
                    ),
                    html.Div("Importance"),
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

            # RIGHT SIDE: use a grid (map on top, ranking on bottom)
            html.Div(
                style={
                    "flex": "1",
                    "display": "grid",
                    "gridTemplateRows": "auto 1fr",
                    "gap": "10px",
                    "padding": "16px 18px",
                    "height": "100vh",
                    "overflow": "hidden",
                },
                children=[
                    # TOP: title + map
                    html.Div(
                        style={"minHeight": 0},
                        children=[
                            html.H1(
                                "Global Overview",
                                style={
                                    "margin": "0 0 8px 0",
                                    "fontWeight": "400",
                                    "textAlign": "center",
                                },
                            ),
                            dcc.Graph(
                                id="globe-map",
                                style={"height": "58vh"},  # slightly smaller
                                config={
                                    "scrollZoom": False,
                                    "displayModeBar": False,
                                    "doubleClick": "reset",
                                    "staticPlot": False,
                                },
                            ),
                            html.Div(
                                id="click-debug",
                                style={"padding": "6px", "fontSize": "12px", "opacity": 0.7},
                            ),
                        ],
                    ),

                    # BOTTOM: ranking fills remaining space
                    html.Div(
                        style={
                            "minHeight": 0,
                            "overflow": "hidden",
                            "display": "flex",
                            "flexDirection": "column",
                            "gap": "8px",
                        },
                        children=[
                            dcc.Dropdown(
                                id="topn-dropdown",
                                options=[
                                    {"label": "Top 10", "value": 10},
                                    {"label": "Top 20", "value": 20},
                                    {"label": "Top 50", "value": 50},
                                    {"label": "Top 100", "value": 100},
                                    {"label": "All countries", "value": "all"},
                                ],
                                value=20,
                                clearable=False,
                                style={"maxWidth": "220px"},
                            ),
                            html.Div(
                                id="ranking-container",
                                style={"minHeight": 0, "overflow": "hidden"},
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )
