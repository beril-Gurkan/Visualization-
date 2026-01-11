from dash import html, dcc, callback, Input, Output, ctx, ALL
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
    """Panel showing ranked countries based on complex_metrics weights."""
    return html.Div([
        html.H2("Ranking Panel"),
        html.Div(id="ranked-countries-output", style={"margin-top": "20px"}),
        dcc.Store(id="selected-country-from-ranking", data=None),
        html.Div(id="scatterplot-container", style={"margin-top": "20px"}),
    ], className="panel")


@callback(
    Output("ranked-countries-output", "children"),
    Input("weight-asf", "value"),
    Input("weight-iec", "value"),
    Input("weight-scc", "value"),
    Input("weight-wsi", "value"),
    Input("weight-ers", "value"),
    prevent_initial_call=False,
)
def update_ranking_output(w_asf, w_iec, w_scc, w_wsi, w_ers):
    """Display ranked countries based on complex_metrics weights."""
    try:
        # Compute all metrics (functions use global data internally)
        asf = available_skilled_workforce()
        iec = industrial_energy_capacity()
        scc = supply_chain_connectivity_score()
        wsi = wage_sustainability_index()
        ers = economic_resilience_score()
        
        # Align all series by index
        all_metrics = pd.concat([asf, iec, scc, wsi, ers], axis=1).dropna()
        all_metrics.columns = ['ASF', 'IEC', 'SCC', 'WSI', 'ERS']
        
        # Normalize weights
        total_weight = w_asf + w_iec + w_scc + w_wsi + w_ers
        if total_weight == 0:
            return html.Div("Set at least one weight > 0")
        
        w_asf /= total_weight
        w_iec /= total_weight
        w_scc /= total_weight
        w_wsi /= total_weight
        w_ers /= total_weight
        
        # Compute weighted average
        combined = (
            all_metrics['ASF'] * w_asf +
            all_metrics['IEC'] * w_iec +
            all_metrics['SCC'] * w_scc +
            all_metrics['WSI'] * w_wsi +
            all_metrics['ERS'] * w_ers
        )
        
        top = combined.sort_values(ascending=False).head(10)
        
        # Create clickable country entries
        entries = []
        for country, score in top.items():
            entries.append(
                html.Button(
                    f"{country}: {score:.2f}",
                    id={"type": "country-rank-button", "index": country},
                    style={
                        "padding": "8px 12px",
                        "margin": "4px",
                        "width": "100%",
                        "textAlign": "left",
                        "backgroundColor": "#f0f0f0",
                        "border": "1px solid #ddd",
                        "borderRadius": "4px",
                        "cursor": "pointer",
                        ":hover": {"backgroundColor": "#e0e0e0"}
                    },
                    n_clicks=0
                )
            )
        
        return html.Div([html.H4("Top 10 Countries by Complex Metrics"), *entries])
    except Exception as e:
        return html.Div(f"Error: {e}")


@callback(
    Output("selected-country-from-ranking", "data"),
    Input({"type": "country-rank-button", "index": ALL}, "n_clicks"),
    prevent_initial_call=True,
)
def capture_country_click(n_clicks):
    """Capture which country button was clicked."""
    if not ctx.triggered_id:
        return None
    return ctx.triggered_id["index"]


@callback(
    Output("scatterplot-container", "children"),
    Input("selected-country-from-ranking", "data"),
    prevent_initial_call=False,
)
def show_scatterplot_for_country(selected_country):
    """Display scatterplot when a country is selected from ranking."""
    if selected_country is None:
        return html.Div("Click on a country to see the scatterplot", style={"padding": "10px", "color": "#666"})
    
    try:
        # Get the full dataset
        df = get_data()
        
        # Define available metrics for the scatterplot
        # Use economic and demographic metrics that are likely available
        metric_cols = [
            'Real_GDP_per_Capita_USD',
            'Unemployment_Rate_percent',
            'Total_Population',
            'Total_Literacy_Rate',
            'electricity_access_percent',
            'electricity_production_kWh',
        ]
        
        # Filter to only columns that exist in the dataframe
        available_metrics = [col for col in metric_cols if col in df.columns]
        
        if len(available_metrics) < 2:
            return html.Div("Not enough metrics available for scatterplot")
        
        # Default to first two available metrics
        x_metric = available_metrics[0]
        y_metric = available_metrics[1]
        
        # Create the scatterplot instance
        plot = Scatterplot(f"Metrics for {selected_country}", x_metric, y_metric, df)
        
        # Highlight the selected country
        selected_data = {"points": [{"customdata": selected_country}]}
        fig = plot.update(x_metric, y_metric, selected_data)
        plot.children[1].figure = fig
        
        return html.Div([
            html.H4(f"Country Comparison"),
            plot
        ])
        
    except Exception as e:
        return html.Div(f"Error creating scatterplot: {e}")