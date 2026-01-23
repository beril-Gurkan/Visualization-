from dash import html, dcc


def complex_metrics_panel():
    """
    Panel displaying the 5 complex metrics as toggleable options.
    Consistent with the global metrics_panel.py structure.
    """
    return html.Div(
        id="complex-metrics-panel",
        className="panel",
        children=[
            html.H1("Complex Metrics"),
            
            # Available Skilled Workforce
            html.Div(
                className="complex-metric",
                children=[
                    html.H2("Available Skilled Workforce"),
                    dcc.Checklist(
                        id="toggle-asf",
                        options=[{"label": "Enabled", "value": "enabled"}],
                        value=["enabled"],
                    ),
                    html.Div("Literacy × Unemployment × Population scale", 
                             className="metric-description"),
                    html.Div("Importance", className="importance-label"),
                    dcc.Slider(
                        id="weight-asf",
                        min=0,
                        max=100,
                        step=1,
                        value=20,
                        marks={0: "0", 100: "100"},
                        tooltip={"placement": "bottom", "always_visible": True},
                    ),
                    html.Hr(),
                ],
            ),
            
            # Industrial Energy Capacity
            html.Div(
                className="complex-metric",
                children=[
                    html.H2("Industrial Energy Capacity"),
                    dcc.Checklist(
                        id="toggle-iec",
                        options=[{"label": "Enabled", "value": "enabled"}],
                        value=["enabled"],
                    ),
                    html.Div("Per-capita capacity × Grid scale", 
                             className="metric-description"),
                    html.Div("Importance", className="importance-label"),
                    dcc.Slider(
                        id="weight-iec",
                        min=0,
                        max=100,
                        step=1,
                        value=20,
                        marks={0: "0", 100: "100"},
                        tooltip={"placement": "bottom", "always_visible": True},
                    ),
                    html.Hr(),
                ],
            ),
            
            # Supply Chain Connectivity
            html.Div(
                className="complex-metric",
                children=[
                    html.H2("Supply Chain Connectivity"),
                    dcc.Checklist(
                        id="toggle-scc",
                        options=[{"label": "Enabled", "value": "enabled"}],
                        value=["enabled"],
                    ),
                    html.Div("Airport + Rail + Waterway density", 
                             className="metric-description"),
                    html.Div("Importance", className="importance-label"),
                    dcc.Slider(
                        id="weight-scc",
                        min=0,
                        max=100,
                        step=1,
                        value=20,
                        marks={0: "0", 100: "100"},
                        tooltip={"placement": "bottom", "always_visible": True},
                    ),
                    html.Hr(),
                ],
            ),
            
            # Wage Sustainability Index
            html.Div(
                className="complex-metric",
                children=[
                    html.H2("Wage Sustainability Index"),
                    dcc.Checklist(
                        id="toggle-wsi",
                        options=[{"label": "Enabled", "value": "enabled"}],
                        value=["enabled"],
                    ),
                    html.Div("GDP/capita adjusted for fiscal risk", 
                             className="metric-description"),
                    html.Div("Importance", className="importance-label"),
                    dcc.Slider(
                        id="weight-wsi",
                        min=0,
                        max=100,
                        step=1,
                        value=20,
                        marks={0: "0", 100: "100"},
                        tooltip={"placement": "bottom", "always_visible": True},
                    ),
                    html.Hr(),
                ],
            ),
            
            # Economic Resilience
            html.Div(
                className="complex-metric",
                children=[
                    html.H2("Economic Resilience"),
                    dcc.Checklist(
                        id="toggle-ers",
                        options=[{"label": "Enabled", "value": "enabled"}],
                        value=["enabled"],
                    ),
                    html.Div("GDP growth + Budget stability + Debt management", 
                             className="metric-description"),
                    html.Div("Importance", className="importance-label"),
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

