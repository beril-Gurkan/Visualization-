# Global metrics panel - allows users to select and weight metrics for map coloring
# Contains checkboxes and sliders for 6 metrics across economic, social, and infrastructure categories
# Selected metrics are used to compute composite score displayed on the world map

from dash import html, dcc


def metrics_panel():
    return html.Div(
        className="panel", id="global-metrics-panel",
        children=[
            html.H2("Global Metrics", className="panel-title"),
            html.Div(
                className="global-metric",
                children=[
                    html.H2("Economic"),
                    
                    # Unemployment rate checkbox + slider
                    dcc.Checklist(
                        id="metric-checklist-unemployment",
                        options=[
                            {"label": "Unemployment rate", "value": "unemployment"},
                        ],
                        value=["unemployment"],
                        className="metric-checklist",
                    ),
                    html.Div("weight", className="importance-label"),
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
                    
                    # GDP per capita checkbox + slider
                    dcc.Checklist(
                        id="metric-checklist-gdp",
                        options=[
                            {"label": "GDP per capita", "value": "gdp_pc"},
                        ],
                        className="metric-checklist",
                        value=["gdp_pc"],
                    ),
                    html.Div("weight", className="importance-label"),
                    dcc.Slider(
                        id="w-gdp_pc",
                        min=0,
                        max=100,
                        step=1,
                        value=70,
                        marks={0: "0", 100: "100"},
                        tooltip={"placement": "bottom", "always_visible": True},
                    ),
                ],
            ),
            html.Div(
                className="global-metric",
                children=[
                    html.H2("Demographic"),
                    
                    # Youth unemployment rate checkbox + slider
                    dcc.Checklist(
                        id="metric-checklist-youth-unemp",
                        options=[
                            {"label": "Youth unemployment rate", "value": "youth_unemp"},
                        ],
                        className="metric-checklist",
                        value=["youth_unemp"],
                    ),
                    html.Div("weight", className="importance-label"),
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
                    
                    # Population growth rate checkbox + slider
                    dcc.Checklist(
                        id="metric-checklist-pop-growth",
                        options=[
                            {"label": "Population growth rate", "value": "pop_growth"},
                        ],
                        value=["pop_growth"],
                        className="metric-checklist",
                    ),
                    html.Div("weight", className="importance-label"),
                    dcc.Slider(
                        id="w-pop_growth",
                        min=0,
                        max=100,
                        step=1,
                        value=40,
                        marks={0: "0", 100: "100"},
                        tooltip={"placement": "bottom", "always_visible": True},
                    ),
                ],
            ),
            html.Div(
                className="global-metric",
                children=[
                    html.H2("Sustainability"),
                    
                    # Electricity access checkbox + slider
                    dcc.Checklist(
                        id="metric-checklist-elec-access",
                        options=[
                            {"label": "Electricity access %", "value": "elec_access"},
                        ],
                        value=["elec_access"],
                        className="metric-checklist",
                    ),
                    html.Div("weight", className="importance-label"),
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
                    
                    # Electricity generating capacity checkbox + slider
                    dcc.Checklist(
                        id="metric-checklist-elec-capacity",
                        options=[
                            {"label": "Electricity generating capacity (relative)", "value": "elec_capacity"},
                        ],
                        value=["elec_capacity"],
                        className="metric-checklist",
                    ),
                    html.Div("weight", className="importance-label"),
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
