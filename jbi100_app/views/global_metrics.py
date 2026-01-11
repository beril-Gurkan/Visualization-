from dash import html, dcc, callback, Input, Output


def global_metrics():
    """Filter panel for Economic, Demographic, and Sustainability metrics."""
    return html.Div([
        html.H3("Global Metrics", className="panel-title"),
        
        # Economic section
        html.Div([
            html.H4("Economic"),
            html.Div([
                dcc.Checklist(
                    id="check-unemployment",
                    options=[{"label": " Unemployment rate", "value": "unemployment"}],
                    value=[],
                    className="metrics-checklist",
                ),
                html.Div([
                    html.Label("Importance", className="metrics-label"),
                    dcc.Slider(
                        id="slider-unemployment",
                        min=0,
                        max=100,
                        step=1,
                        value=60,
                        marks={0: "0", 100: "100"},
                        tooltip={"placement": "bottom", "always_visible": True},
                        className="metrics-slider",
                    ),
                ], className="metrics-slider-wrapper"),
            ], className="metrics-subsection"),
            html.Div([
                dcc.Checklist(
                    id="check-gdp",
                    options=[{"label": " GDP per capita", "value": "gdp"}],
                    value=[],
                    className="metrics-checklist",
                ),
                html.Div([
                    html.Label("Importance", className="metrics-label"),
                    dcc.Slider(
                        id="slider-gdp",
                        min=0,
                        max=100,
                        step=1,
                        value=70,
                        marks={0: "0", 100: "100"},
                        tooltip={"placement": "bottom", "always_visible": True},
                        className="metrics-slider",
                    ),
                ], className="metrics-slider-wrapper"),
            ], className="metrics-subsection"),
        ], className="metrics-section"),
        
        # Demographic section
        html.Div([
            html.H4("Demographic"),
            html.Div([
                dcc.Checklist(
                    id="check-youth-unemp",
                    options=[{"label": " Youth unemployment rate", "value": "youth_unemployment"}],
                    value=[],
                    className="metrics-checklist",
                ),
                html.Div([
                    html.Label("Importance", className="metrics-label"),
                    dcc.Slider(
                        id="slider-youth-unemp",
                        min=0,
                        max=100,
                        step=1,
                        value=50,
                        marks={0: "0", 100: "100"},
                        tooltip={"placement": "bottom", "always_visible": True},
                        className="metrics-slider",
                    ),
                ], className="metrics-slider-wrapper"),
            ], className="metrics-subsection"),
            html.Div([
                dcc.Checklist(
                    id="check-pop-growth",
                    options=[{"label": " Population growth rate", "value": "pop_growth"}],
                    value=[],
                    className="metrics-checklist",
                ),
                html.Div([
                    html.Label("Importance", className="metrics-label"),
                    dcc.Slider(
                        id="slider-pop-growth",
                        min=0,
                        max=100,
                        step=1,
                        value=40,
                        marks={0: "0", 100: "100"},
                        tooltip={"placement": "bottom", "always_visible": True},
                        className="metrics-slider",
                    ),
                ], className="metrics-slider-wrapper"),
            ], className="metrics-subsection"),
        ], className="metrics-section"),
        
        # Sustainability section
        html.Div([
            html.H4("Sustainability"),
            html.Div([
                dcc.Checklist(
                    id="check-elec-access",
                    options=[{"label": " Electricity access %", "value": "elec_access"}],
                    value=[],
                    className="metrics-checklist",
                ),
                html.Div([
                    html.Label("Importance", className="metrics-label"),
                    dcc.Slider(
                        id="slider-elec-access",
                        min=0,
                        max=100,
                        step=1,
                        value=65,
                        marks={0: "0", 100: "100"},
                        tooltip={"placement": "bottom", "always_visible": True},
                        className="metrics-slider",
                    ),
                ], className="metrics-slider-wrapper"),
            ], className="metrics-subsection"),
            html.Div([
                dcc.Checklist(
                    id="check-elec-capacity",
                    options=[{"label": " Electricity generating capacity", "value": "elec_capacity"}],
                    value=[],
                    className="metrics-checklist",
                ),
                html.Div([
                    html.Label("Importance", className="metrics-label"),
                    dcc.Slider(
                        id="slider-elec-capacity",
                        min=0,
                        max=100,
                        step=1,
                        value=55,
                        marks={0: "0", 100: "100"},
                        tooltip={"placement": "bottom", "always_visible": True},
                        className="metrics-slider",
                    ),
                ], className="metrics-slider-wrapper"),
            ], className="metrics-subsection"),
        ], className="metrics-section"),
        
        # Buttons
        html.Div([
            html.Button("Apply filters", id="btn-apply-filters", n_clicks=0, className="btn-apply-filters"),
            html.Button("Reset", id="btn-reset-filters", n_clicks=0, className="btn-reset-filters"),
        ], className="metrics-buttons"),
    ], className="panel")


@callback(
    Output("check-unemployment", "value"),
    Output("slider-unemployment", "value"),
    Output("check-gdp", "value"),
    Output("slider-gdp", "value"),
    Output("check-youth-unemp", "value"),
    Output("slider-youth-unemp", "value"),
    Output("check-pop-growth", "value"),
    Output("slider-pop-growth", "value"),
    Output("check-elec-access", "value"),
    Output("slider-elec-access", "value"),
    Output("check-elec-capacity", "value"),
    Output("slider-elec-capacity", "value"),
    Input("btn-reset-filters", "n_clicks"),
    prevent_initial_call=True,
)
def reset_filters(n_clicks):
    """Reset all filters to default values."""
    return [], 60, [], 70, [], 50, [], 40, [], 65, [], 55

