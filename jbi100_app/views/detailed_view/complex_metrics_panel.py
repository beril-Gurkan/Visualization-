from dash import html, dcc

# Panel displaying the 5 complex metrics as toggleable options.
def complex_metrics_panel():
    return html.Div(
        id="complex-metrics-panel",
        className="panel",
        children=[
            html.H2("Complex Metrics", className="panel-title"),
            
            # Available Skilled Workforce
            html.Div(
                className="complex-metric",
                children=[
                    html.Div(
                        [
                            html.H2("Available Skilled Workforce"),
                            dcc.Checklist(
                                id="toggle-asf",
                                options=[{"label": "", "value": "enabled"}],
                                value=["enabled"],
                                className="metric-checklist",
                            ),
                        ],
                        className="metric-header",
                    ),
                    html.Div("Literacy × Unemployment × Population scale", 
                             className="metric-description"),
                    html.Div("weight", className="importance-label"),
                    dcc.Slider(
                        id="weight-asf",
                        min=0,
                        max=100,
                        step=1,
                        value=20,
                        marks={0: "0", 100: "100"},
                        tooltip={"placement": "bottom", "always_visible": True},
                    ),
                    html.Div(className="slider-spacer"),
                ],
            ),
            
            # Industrial Energy Capacity
            html.Div(
                className="complex-metric",
                children=[
                    html.Div(
                        [
                            html.H2("Industrial Energy Capacity"),
                            dcc.Checklist(
                                id="toggle-iec",
                                options=[{"label": "", "value": "enabled"}],
                                value=["enabled"],
                                className="metric-checklist",
                            ),
                        ],
                        className="metric-header",
                    ),
                    html.Div("Per-capita capacity × Grid scale", 
                             className="metric-description"),
                    html.Div("weight", className="importance-label"),
                    dcc.Slider(
                        id="weight-iec",
                        min=0,
                        max=100,
                        step=1,
                        value=20,
                        marks={0: "0", 100: "100"},
                        tooltip={"placement": "bottom", "always_visible": True},
                    ),
                    html.Div(className="slider-spacer"),
                ],
            ),
            
            # Supply Chain Connectivity
            html.Div(
                className="complex-metric",
                children=[
                    html.Div(
                        [
                            html.H2("Supply Chain Connectivity"),
                            dcc.Checklist(
                                id="toggle-scc",
                                options=[{"label": "", "value": "enabled"}],
                                value=["enabled"],
                                className="metric-checklist",
                            ),
                        ],
                        className="metric-header",
                    ),
                    html.Div("Airport + Rail + Waterway density", 
                             className="metric-description"),
                    html.Div("weight", className="importance-label"),
                    dcc.Slider(
                        id="weight-scc",
                        min=0,
                        max=100,
                        step=1,
                        value=20,
                        marks={0: "0", 100: "100"},
                        tooltip={"placement": "bottom", "always_visible": True},
                    ),
                    html.Div(className="slider-spacer"),
                ],
            ),
            
            # Wage Sustainability Index
            html.Div(
                className="complex-metric",
                children=[
                    html.Div(
                        [
                            html.H2("Wage Sustainability Index"),
                            dcc.Checklist(
                                id="toggle-wsi",
                                options=[{"label": "", "value": "enabled"}],
                                value=["enabled"],
                                className="metric-checklist",
                            ),
                        ],
                        className="metric-header",
                    ),
                    html.Div("GDP/capita adjusted for fiscal risk", 
                             className="metric-description"),
                    html.Div("weight", className="importance-label"),
                    dcc.Slider(
                        id="weight-wsi",
                        min=0,
                        max=100,
                        step=1,
                        value=20,
                        marks={0: "0", 100: "100"},
                        tooltip={"placement": "bottom", "always_visible": True},
                    ),
                    html.Div(className="slider-spacer"),
                ],
            ),
            
            # Economic Resilience
            html.Div(
                className="complex-metric",
                children=[
                    html.Div(
                        [
                            html.H2("Economic Resilience"),
                            dcc.Checklist(
                                id="toggle-ers",
                                options=[{"label": "", "value": "enabled"}],
                                value=["enabled"],
                                className="metric-checklist",
                            ),
                        ],
                        className="metric-header",
                    ),
                    html.Div("GDP growth + Budget stability + Debt management", 
                             className="metric-description"),
                    html.Div("weight", className="importance-label"),
                    dcc.Slider(
                        id="weight-ers",
                        min=0,
                        max=100,
                        step=1,
                        value=20,
                        marks={0: "0", 100: "100"},
                        tooltip={"placement": "bottom", "always_visible": True},
                    ),
                ],
            ),
        ]
    )

