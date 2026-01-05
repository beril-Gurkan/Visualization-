from jbi100_app.main import app
from jbi100_app.views.scatterplot import Scatterplot
from jbi100_app.views.metrics_panel import make_metrics_panel

from dash import html
from dash.dependencies import Input, Output
import pandas as pd



# Processed data path

DATA_PATH = "data_sets/processed/countries_processed.csv"
df = pd.read_csv(DATA_PATH)

if "Country" not in df.columns:
    raise ValueError("countries_processed.csv must contain a 'Country' column.")


#Metrics chosen for scatterplot
METRIC_COLUMNS = [
    "GDP__norm",
    "Unemployment__norm_inv",
    "Youth_Unemp__norm_inv",
    "Pop_Growth__norm",
    "Elec_Access__norm",
    "Elec_Capacity__norm",
    "Available_Skilled_Workforce__norm",
    "Industrial_Energy_Capacity__norm",
    "Supply_Chain_Connectivity_Score__norm",
    "Wage_Sustainability_Index__norm",
    "Economic_Resilience_Score__norm",
]

available_metrics = [m for m in METRIC_COLUMNS if m in df.columns]
if len(available_metrics) < 2:
    raise ValueError("Need at least TWO metric columns in the dataset to make a scatterplot.")

default_selected = [m for m in ["GDP__norm", "Unemployment__norm_inv"] if m in available_metrics]
if len(default_selected) < 2:
    default_selected = available_metrics[:2]

x0, y0 = default_selected[0], default_selected[1]

plot = Scatterplot("Country Comparison", x0, y0, df)
plot.children[1].figure = plot.update(x0, y0, None)



# Layout

app.layout = html.Div(
    id="app-container",
    children=[
        html.Div(id="main-content", children=[plot]),
        html.Div(
            id="metrics-panel-container",
            children=make_metrics_panel(
                available_metrics=available_metrics,
                default_selected=default_selected
            ),
        ),
    ],
)



# Callback: update plot when metrics change or selection changes

@app.callback(
    Output(plot.html_id, "figure"),
    Input("metrics-checklist", "value"),
    Input(plot.html_id, "selectedData"),
)
def update_plot(selected_metrics, selected_data):
    if not selected_metrics:
        selected_metrics = default_selected

    selected_metrics = [m for m in selected_metrics if m in df.columns]
    selected_metrics = [m for m in selected_metrics if not str(m).startswith("__header__")]

    if len(selected_metrics) >= 2:
        x, y = selected_metrics[0], selected_metrics[1]
    elif len(selected_metrics) == 1:
        x, y = selected_metrics[0], y0
    else:
        x, y = x0, y0

    return plot.update(x, y, selected_data)


if __name__ == "__main__":
    app.run(debug=True)
