from dash import html, dcc


def metrics_panel():
    return html.Div(
        className="panel", id="global-metrics-panel",
        children=[
            html.H1("Global Metrics"),
            html.Div(
                className="global-metric",
                children=[
                    html.H2("Economic"),
                    dcc.Checklist(
                        id="metric-checklist",
                        options=[
                            {"label": "Unemployment rate", "value": "unemployment"},
                            {"label": "GDP per capita", "value": "gdp_pc"},
                        ],
                        value=["unemployment", "gdp_pc"],
                    ),
                    html.Div("Importance", className="importance-label"),
                    dcc.Slider(
                        id="w-unemployment",
                        min=0,
                        max=100,
                        step=1,
                        value=60,
                        marks={0: "0", 100: "100"},
                        tooltip={"placement": "bottom", "always_visible": True},
                    ),
                    html.Div(className="slider-spacer"),
                    dcc.Slider(
                        id="w-gdp_pc",
                        min=0,
                        max=100,
                        step=1,
                        value=70,
                        marks={0: "0", 100: "100"},
                        tooltip={"placement": "bottom", "always_visible": True},
                    ),
                    html.Hr(),
                ],
            ),
            html.Div(
                className="global-metric",
                children=[
                    html.H2("Demographic"),
                    dcc.Checklist(
                        id="metric-checklist-dem",
                        options=[
                            {"label": "Youth unemployment rate", "value": "youth_unemp"},
                            {"label": "Population growth rate", "value": "pop_growth"},
                        ],
                        value=["youth_unemp", "pop_growth"],
                    ),
                    html.Div("Importance", className="importance-label"),
                    dcc.Slider(
                        id="w-youth_unemp",
                        min=0,
                        max=100,
                        step=1,
                        value=50,
                        marks={0: "0", 100: "100"},
                        tooltip={"placement": "bottom", "always_visible": True},
                    ),
                    html.Div(className="slider-spacer"),
                    dcc.Slider(
                        id="w-pop_growth",
                        min=0,
                        max=100,
                        step=1,
                        value=40,
                        marks={0: "0", 100: "100"},
                        tooltip={"placement": "bottom", "always_visible": True},
                    ),
                    html.Hr(),
                ],
            ),
            html.Div(
                className="global-metric",
                children=[
                    html.H2("Sustainability"),
                    dcc.Checklist(
                        id="metric-checklist-sus",
                        options=[
                            {"label": "Electricity access %", "value": "elec_access"},
                            {"label": "Electricity generating capacity (relative)", "value": "elec_capacity"},
                        ],
                        value=["elec_access", "elec_capacity"],
                    ),
                    html.Div("Importance", className="importance-label"),
                    dcc.Slider(
                        id="w-elec_access",
                        min=0,
                        max=100,
                        step=1,
                        value=65,
                        marks={0: "0", 100: "100"},
                        tooltip={"placement": "bottom", "always_visible": True},
                    ),
                    html.Div(className="slider-spacer"),
                    dcc.Slider(
                        id="w-elec_capacity",
                        min=0,
                        max=100,
                        step=1,
                        value=55,
                        marks={0: "0", 100: "100"},
                        tooltip={"placement": "bottom", "always_visible": True},
                    ),
                ],
            ),
        ],
    )
