from dash import html, dcc


def make_metrics_panel(available_metrics, default_selected=None):
    """
    Metric selection panel (global + advanced).
    - available_metrics: list[str] columns that exist in df
    - default_selected: list[str] pre-selected metric columns
    """

    METRIC_GROUPS = {
        "Global — Economic": [
            ("GDP (normalized)", "GDP__norm"),
            ("Unemployment (lower is better)", "Unemployment__norm_inv"),
        ],
        "Global — Demographic": [
            ("Youth unemployment (lower is better)", "Youth_Unemp__norm_inv"),
            ("Population growth (normalized)", "Pop_Growth__norm"),
        ],
        "Global — Sustainability": [
            ("Electricity access (normalized)", "Elec_Access__norm"),
            ("Electricity capacity (normalized)", "Elec_Capacity__norm"),
        ],
        "Advanced — Region-specific (derived)": [
            ("Available Skilled Workforce", "Available_Skilled_Workforce__norm"),
            ("Industrial Energy Capacity", "Industrial_Energy_Capacity__norm"),
            ("Supply Chain Connectivity", "Supply_Chain_Connectivity_Score__norm"),
            ("Wage Sustainability Index", "Wage_Sustainability_Index__norm"),
            ("Economic Resilience Score", "Economic_Resilience_Score__norm"),
        ],
    }

    # Defaults: pick 2 (scatterplot needs x & y)
    if default_selected is None:
        default_selected = [
            c for c in ["GDP__norm", "Unemployment__norm_inv"] if c in available_metrics
        ]
        if len(default_selected) < 2:
            # fallback: first two available
            default_selected = available_metrics[:2]

    # Build ordered checklist options with disabled headers
    options = []
    for group, items in METRIC_GROUPS.items():
        # disabled header row (stays visible but not selectable)
        options.append(
            {
                "label": f"— {group} —",
                "value": f"__header__{group}",
                "disabled": True,
            }
        )

        for label, col in items:
            if col in available_metrics:
                options.append({"label": label, "value": col})

    return html.Section(
        id="metrics-panel",
        className="panel filters-panel",
        children=[
            # Panel header (matches prototype structure)
            html.Div(
                className="panel-header",
                children=[
                    html.Div(
                        className="panel-title-block",
                        children=[
                            html.H2("Filters", className="panel-title"),
                            html.P("Start with global metrics", className="panel-subtitle"),
                        ],
                    )
                ],
            ),

            # Panel body
            html.Div(
                className="panel-body filters-body",
                children=[
                    html.Div(
                        className="card metric-card",
                        children=[
                            html.H3("Metric selection", className="card-title"),

                            dcc.Checklist(
                                id="metrics-checklist",
                                options=options,
                                value=default_selected,
                                className="metrics-checklist",
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )