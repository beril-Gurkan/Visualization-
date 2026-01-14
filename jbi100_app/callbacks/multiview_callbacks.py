from dash import html, callback, Input, Output
from jbi100_app.data import get_data
from jbi100_app.views.scatterplot import Scatterplot


@callback(
    Output("scatterplot-container", "children"),
    Input("selected_country", "data"),
    Input("metrics-econ", "value"),
    Input("metrics-demo", "value"),
    Input("metrics-sustain", "value"),
    Input("metrics-advanced", "value"),
    prevent_initial_call=False,
)
def show_scatterplot_for_country(selected_country_store, econ_metrics, demo_metrics, sustain_metrics, advanced_metrics):
    """
    Scatterplot stays as a relationship/outlier view.
    It updates whenever a country is selected (map or ranking table).
    """
    if not selected_country_store:
        return html.Div(
            "Select a country (map or ranking) to highlight it here.",
            style={"padding": "10px", "color": "#666", "fontSize": "0.95rem", "textAlign": "center"},
        )

    selected_country = str(selected_country_store).strip().upper()

    try:
        df = get_data()

        # Combine selected metrics
        selected_metrics = []
        for group in [econ_metrics, demo_metrics, sustain_metrics, advanced_metrics]:
            if group:
                selected_metrics.extend(group if isinstance(group, list) else [group])

        selected_metrics = [m for m in selected_metrics if m in df.columns and m != "Country"]

        # Need at least 2 metrics
        if len(selected_metrics) < 2:
            available = [c for c in df.columns if c != "Country"]
            if len(available) >= 2:
                selected_metrics = available[:2]
            else:
                return html.Div("Not enough metrics available for scatterplot")

        x_metric, y_metric = selected_metrics[0], selected_metrics[1]
        plot = Scatterplot("Country Comparison", x_metric, y_metric, df)

        fig = plot._build_figure({selected_country})
        plot.children[1].figure = fig

        return html.Div(
            [
                html.Div(
                    f"Highlighted: {selected_country}",
                    style={"fontSize": "12px", "fontWeight": "700", "marginBottom": "6px"},
                ),
                plot,
            ]
        )

    except Exception as e:
        return html.Div(f"Error creating scatterplot: {e}", style={"color": "red", "fontSize": "0.95rem"})
