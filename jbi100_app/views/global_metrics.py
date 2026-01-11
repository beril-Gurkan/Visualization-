from dash import html, dcc, callback, Input, Output


def global_metrics():
    """Filter panel for Economic, Demographic, and Sustainability metrics."""
    return html.Div([
        html.H3("Global Metrics", className="panel-title"),
        
        # Economic section
        html.Div([
            html.H4("Economic", style={"margin-top": "15px", "margin-bottom": "10px"}),
            html.Div([
                dcc.Checklist(id="check-unemployment", options=[{"label": " Unemployment rate", "value": "unemployment"}], value=[]),
                html.Div([
                    html.Label("Importance", style={"display": "inline-block", "width": "70px"}),
                    dcc.Slider(id="slider-unemployment", min=0, max=100, step=1, value=60, marks={0: "0", 100: "100"}, tooltip={"placement": "bottom", "always_visible": True}),
                ], style={"margin-top": "8px", "margin-bottom": "15px"}),
            ]),
            html.Div([
                dcc.Checklist(id="check-gdp", options=[{"label": " GDP per capita", "value": "gdp"}], value=[]),
                html.Div([
                    html.Label("Importance", style={"display": "inline-block", "width": "70px"}),
                    dcc.Slider(id="slider-gdp", min=0, max=100, step=1, value=70, marks={0: "0", 100: "100"}, tooltip={"placement": "bottom", "always_visible": True}),
                ], style={"margin-top": "8px", "margin-bottom": "15px"}),
            ]),
        ]),
        
        # Demographic section
        html.Div([
            html.H4("Demographic", style={"margin-top": "15px", "margin-bottom": "10px"}),
            html.Div([
                dcc.Checklist(id="check-youth-unemp", options=[{"label": " Youth unemployment rate", "value": "youth_unemployment"}], value=[]),
                html.Div([
                    html.Label("Importance", style={"display": "inline-block", "width": "70px"}),
                    dcc.Slider(id="slider-youth-unemp", min=0, max=100, step=1, value=50, marks={0: "0", 100: "100"}, tooltip={"placement": "bottom", "always_visible": True}),
                ], style={"margin-top": "8px", "margin-bottom": "15px"}),
            ]),
            html.Div([
                dcc.Checklist(id="check-pop-growth", options=[{"label": " Population growth rate", "value": "pop_growth"}], value=[]),
                html.Div([
                    html.Label("Importance", style={"display": "inline-block", "width": "70px"}),
                    dcc.Slider(id="slider-pop-growth", min=0, max=100, step=1, value=40, marks={0: "0", 100: "100"}, tooltip={"placement": "bottom", "always_visible": True}),
                ], style={"margin-top": "8px", "margin-bottom": "15px"}),
            ]),
        ]),
        
        # Sustainability section
        html.Div([
            html.H4("Sustainability", style={"margin-top": "15px", "margin-bottom": "10px"}),
            html.Div([
                dcc.Checklist(id="check-elec-access", options=[{"label": " Electricity access %", "value": "elec_access"}], value=[]),
                html.Div([
                    html.Label("Importance", style={"display": "inline-block", "width": "70px"}),
                    dcc.Slider(id="slider-elec-access", min=0, max=100, step=1, value=65, marks={0: "0", 100: "100"}, tooltip={"placement": "bottom", "always_visible": True}),
                ], style={"margin-top": "8px", "margin-bottom": "15px"}),
            ]),
            html.Div([
                dcc.Checklist(id="check-elec-capacity", options=[{"label": " Electricity generating capacity", "value": "elec_capacity"}], value=[]),
                html.Div([
                    html.Label("Importance", style={"display": "inline-block", "width": "70px"}),
                    dcc.Slider(id="slider-elec-capacity", min=0, max=100, step=1, value=55, marks={0: "0", 100: "100"}, tooltip={"placement": "bottom", "always_visible": True}),
                ], style={"margin-top": "8px", "margin-bottom": "15px"}),
            ]),
        ]),
        
        # Buttons
        html.Div([
            html.Button("Apply filters", id="btn-apply-filters", n_clicks=0, style={"background-color": "#0056cc", "color": "white", "padding": "10px 20px", "border": "none", "border-radius": "5px", "margin-right": "10px", "cursor": "pointer"}),
            html.Button("Reset", id="btn-reset-filters", n_clicks=0, style={"background-color": "#f0f0f0", "color": "#333", "padding": "10px 20px", "border": "1px solid #ccc", "border-radius": "5px", "cursor": "pointer"}),
        ], style={"margin-top": "20px"}),
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

