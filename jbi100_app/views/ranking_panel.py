from dash import html, dcc, callback, Input, Output
import pandas as pd
from jbi100_app.data import (
    available_skilled_workforce,
    industrial_energy_capacity,
    supply_chain_connectivity_score,
    wage_sustainability_index,
    economic_resilience_score,
)


def ranking_panel():
    """Panel showing ranked countries based on complex_metrics weights."""
    return html.Div([
        html.H2("Ranking Panel"),
        html.Div(id="ranked-countries-output", style={"margin-top": "20px"}),
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
        entries = [html.Div(f"{country}: {score:.2f}", style={"padding": "5px"}) for country, score in top.items()]
        
        return html.Div([html.H4("Top 10 Countries by Complex Metrics"), *entries])
    except Exception as e:
        return html.Div(f"Error: {e}")