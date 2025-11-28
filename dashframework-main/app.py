from jbi100_app.main import app
from jbi100_app.views.menu import make_menu_layout
from jbi100_app.views.scatterplot import Scatterplot
from jbi100_app.views.globeplot import GlobePlot
from jbi100_app.views.metrics_panel import make_metrics_panel
from jbi100_app.data import get_data

from dash import html
from dash.dependencies import Input, Output


if __name__ == '__main__':
    # Load your data
    df = get_data()

    # Define metrics that can be selected (numeric columns only)
    available_metrics = [
        'Total_Population',
        'Population_Growth_Rate',
        'Birth_Rate',
        'Death_Rate',
        'Median_Age',
        'Total_Literacy_Rate',
        'Real_GDP_per_Capita_USD',
        'Real_GDP_PPP_billion_USD',
        'Real_GDP_Growth_Rate_percent',
        'Unemployment_Rate_percent',
        'Exports_billion_USD',
        'Imports_billion_USD',
        'electricity_access_percent',
        'internet_users_total',
        'mobile_cellular_subscriptions_total'
    ]

    # Instantiate custom views
    globe = GlobePlot("World Rankings", df)

    app.layout = html.Div(
        id="app-container",
        children=[
            # Main content area with globe
            html.Div(
                id="main-content",
                children=[
                    globe
                ],
            ),
            
            # Bottom-right metrics panel
            html.Div(
                id="metrics-panel-container",
                children=make_metrics_panel(available_metrics)
            ),
        ],
    )

    # Define interactions - update globe when metrics are toggled
    @app.callback(
        Output(globe.html_id, "figure"),
        Input("metrics-checklist", "value")
    )
    def update_globe(selected_metrics):
        return globe.update(selected_metrics)

    app.run(debug=True)