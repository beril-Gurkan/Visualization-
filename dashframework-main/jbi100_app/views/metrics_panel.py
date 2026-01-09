from dash import html, dcc


def make_metrics_panel(available_metrics, default_selected=None):
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

    options = []
    for group, items in METRIC_GROUPS.items():
        options.append({"label": f"— {group} —", "value": f"__header__{group}", "disabled": True})
        for label, col in items:
            if col in available_metrics:
                options.append({"label": label, "value": col})

    if default_selected is None:
        default_selected = [c for c in ["GDP__norm", "Unemployment__norm_inv"] if c in available_metrics]
        if len(default_selected) < 2:
            default_selected = available_metrics[:2]

    return html.Div(
        id="metrics-panel",
        children=[
            html.Div(
                children=[
                    html.H3("Filters", style={"margin": "0 0 4px 0"}),
                    html.Div("Start with global metrics", style={"opacity": 0.75, "fontSize": "13px"}),
                ],
                style={"marginBottom": "12px"},
            ),
            html.Div(
                children=[
                    html.H4("Metric selection", style={"margin": "0 0 8px 0"}),
                    dcc.Checklist(
                        id="metrics-checklist",
                        options=options,
                        value=default_selected,
                        className="metrics-checklist",
                        labelStyle={"display": "block", "margin": "6px 0"},
                    ),
                ],
                style={
                    "background": "white",
                    "border": "1px solid rgba(0,0,0,0.08)",
                    "borderRadius": "12px",
                    "padding": "14px",
                },
            ),
        ],
        style={"width": "320px", "padding": "14px"},
    )