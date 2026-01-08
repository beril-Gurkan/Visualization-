from dash import html, dcc

def complex_metrics():
    """Panel with sliders for metric weights."""
    return html.Div([
        html.H3("Complex Metrics"),
        html.Div([
            html.Label("Available Skilled Workforce"),
            dcc.Slider(id="weight-asf", min=0, max=1, step=0.01, value=0.2, marks={0: "0", 1: "1"}),
        ], style={"margin-bottom": "15px"}),
        html.Div([
            html.Label("Industrial Energy Capacity"),
            dcc.Slider(id="weight-iec", min=0, max=1, step=0.01, value=0.2, marks={0: "0", 1: "1"}),
        ], style={"margin-bottom": "15px"}),
        html.Div([
            html.Label("Supply Chain Connectivity"),
            dcc.Slider(id="weight-scc", min=0, max=1, step=0.01, value=0.2, marks={0: "0", 1: "1"}),
        ], style={"margin-bottom": "15px"}),
        html.Div([
            html.Label("Wage Sustainability Index"),
            dcc.Slider(id="weight-wsi", min=0, max=1, step=0.01, value=0.2, marks={0: "0", 1: "1"}),
        ], style={"margin-bottom": "15px"}),
        html.Div([
            html.Label("Economic Resilience"),
            dcc.Slider(id="weight-ers", min=0, max=1, step=0.01, value=0.2, marks={0: "0", 1: "1"}),
        ], style={"margin-bottom": "15px"}),
    ], className="panel")