from dash import html, dcc, callback, Input, Output, ctx
import pandas as pd
from jbi100_app.data import (
    available_skilled_workforce,
    industrial_energy_capacity,
    supply_chain_connectivity_score,
    wage_sustainability_index,
    economic_resilience_score,
    get_data,
)
from jbi100_app.views.scatterplot import Scatterplot


def ranking_panel():
    """Interactive ranking panel with customizable metrics, sort order, top N selection, and scatterplot."""
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
                style={"width": "100%", "height": "400px"},
            ),
            
            # Scatterplot container (text shows initially, replaced by scatterplot on click)
            html.Div(
                id="scatterplot-container",
                style={
                    "marginTop": "10px",
                    "width": "600px",
                    "boxSizing": "border-box"
                }
            ),
        ],
    )


# Scatterplot callback - shows scatterplot when country is clicked from ranking
@callback(
    Output("scatterplot-container", "children"),
    Input("ranking-bar", "clickData"),
    Input("metrics-econ", "value"),
    Input("metrics-demo", "value"),
    Input("metrics-sustain", "value"),
    Input("metrics-advanced", "value"),
    prevent_initial_call=False,
)
def show_scatterplot_for_country(click_data, econ_metrics, demo_metrics, sustain_metrics, advanced_metrics):
    """Display scatterplot when a country is clicked from the ranking bar chart."""
    if not click_data or not click_data.get("points"):
        return html.Div(
            "Click a bar to select a country.",
            style={"padding": "10px", "color": "#666", "fontSize": "0.95rem", "textAlign": "center"}
        )
    
    # Extract country name from click data
    # The bar chart stores the actual Country name (all caps) in customdata[0]
    point = click_data["points"][0]
    customdata = point.get("customdata")
    if customdata and len(customdata) > 0:
        selected_country = customdata[0]
    else:
        # Fallback to label/y/x if customdata not available
        selected_country = point.get("label") or point.get("y") or point.get("x")
    
    # Ensure country name is a string and strip any whitespace
    if selected_country:
        selected_country = str(selected_country).strip().upper()
    
    try:
        # Get the full dataset
        df = get_data()
        
        # Combine all selected metrics from different groups
        selected_metrics = []
        if econ_metrics:
            selected_metrics.extend(econ_metrics if isinstance(econ_metrics, list) else [econ_metrics])
        if demo_metrics:
            selected_metrics.extend(demo_metrics if isinstance(demo_metrics, list) else [demo_metrics])
        if sustain_metrics:
            selected_metrics.extend(sustain_metrics if isinstance(sustain_metrics, list) else [sustain_metrics])
        if advanced_metrics:
            selected_metrics.extend(advanced_metrics if isinstance(advanced_metrics, list) else [advanced_metrics])
        
        # Filter to available columns
        selected_metrics = [m for m in selected_metrics if m in df.columns]
        
        # Need at least 2 metrics for scatterplot
        if len(selected_metrics) < 2:
            # Fallback to available metrics
            available = [col for col in df.columns if col != 'Country']
            if len(available) >= 2:
                selected_metrics = available[:2]
            else:
                return html.Div("Not enough metrics available for scatterplot")
        
        # Use first two selected metrics as x and y axes
        x_metric = selected_metrics[0]
        y_metric = selected_metrics[1]
        
        # Create the scatterplot instance
        plot = Scatterplot(f"Country Comparison", x_metric, y_metric, df)
        
        # Highlight the selected country by building the figure with selected_data
        selected_data = {"points": [{"customdata": selected_country}]}
        fig = plot._build_figure({selected_country})  # Pass the country as a set for highlighting
        
        # Update the graph's figure
        plot.children[1].figure = fig
        
        # Wrap in container
        return html.Div(
            [
                html.H4(f"{selected_country} - highlighted in scatterplot", style={"fontSize": "1rem", "marginBottom": "8px", "marginTop": "0"}),
                plot
            ],
            style={
                "width": "100%",
                "maxWidth": "100%",
                "boxSizing": "border-box"
            }
        )
        
    except Exception as e:
        return html.Div(f"Error creating scatterplot: {e}", style={"color": "red", "fontSize": "0.95rem"})
