from dash import html, dcc
from jbi100_app.data import get_data

def complex_metrics():
    """Panel with sliders for metric weights and metric selection."""
    # Get available columns from the dataset
    try:
        df = get_data()
        available_cols = df.columns.tolist()
    except Exception:
        available_cols = []
    
    # Define metric groups based on actual available columns
    METRIC_GROUPS = {
        "Global — Economic": [
            ("GDP per Capita (USD)", "Real_GDP_per_Capita_USD"),
            ("Unemployment Rate (%)", "Unemployment_Rate_percent"),
        ],
        "Global — Demographic": [
            ("Youth Unemployment (%)", "Youth_Unemployment_Rate_percent"),
            ("Population Growth Rate (%)", "Population_Growth_Rate"),
        ],
        "Global — Sustainability": [
            ("Electricity Access (%)", "electricity_access_percent"),
            ("Electricity Capacity (kW)", "electricity_generating_capacity_kW"),
        ],
        "Advanced — Development Indicators": [
            ("Total Population", "Total_Population"),
            ("Literacy Rate (%)", "Total_Literacy_Rate"),
            ("Median Age (years)", "Median_Age"),
            ("Exports (billion USD)", "Exports_billion_USD"),
            ("Imports (billion USD)", "Imports_billion_USD"),
        ],
    }

    # Build options list, filtering to available columns (exclude headers)
    options = []
    for group, items in METRIC_GROUPS.items():
        for label, col in items:
            if col in available_cols:
                options.append({"label": label, "value": col})
    
    # Set default selected metrics
    default_selected = [col for col in ["Real_GDP_per_Capita_USD", "Unemployment_Rate_percent"] 
                        if col in available_cols]
    if len(default_selected) < 2 and options:
        default_selected = [opt["value"] for opt in options][:2]
    
    # Build the checklist with group headers as plain text
    checklist_children = []
    group_ids = {
        "Global — Economic": "metrics-econ",
        "Global — Demographic": "metrics-demo",
        "Global — Sustainability": "metrics-sustain",
        "Advanced — Development Indicators": "metrics-advanced",
    }
    
    for group, items in METRIC_GROUPS.items():
        # Add group header as plain text, not a checkbox
        checklist_children.append(
            html.Div(group, style={"fontWeight": "bold", "marginTop": "12px", "marginBottom": "8px", "fontSize": "14px"})
        )
        # Add items for this group
        group_items = []
        for label, col in items:
            if col in available_cols:
                group_items.append({"label": label, "value": col})
        
        if group_items:
            checklist_children.append(
                dcc.Checklist(
                    options=group_items,
                    value=[opt["value"] for opt in group_items if opt["value"] in default_selected],
                    id=group_ids[group],
                    labelStyle={"display": "block", "margin": "6px 0", "fontSize": "14px"},
                    style={"marginBottom": "8px"}
                )
            )
    
    return html.Div([
        html.H3("Complex Metrics", className="panel-title"),
        html.Div([
            html.Label("Available Skilled Workforce"),
            dcc.Slider(id="weight-asf", min=0, max=1, step=0.01, value=0.2, marks={0: "0", 1: "1"}),
        ], style={"margin-bottom": "15px"}),
        html.Div([
            html.Label("Industrial Energy Capacity"),
            dcc.Slider(id="weight-iec", min=0, max=1, step=0.01, value=0.2, marks={0: "0", 1: "1"}),
        ], style={"margin-bottom": "15px"}),
        html.Div([
            html.Label("Supply Chain Connectivity"),
            dcc.Slider(id="weight-scc", min=0, max=1, step=0.01, value=0.2, marks={0: "0", 1: "1"}),
        ], style={"margin-bottom": "15px"}),
        html.Div([
            html.Label("Wage Sustainability Index"),
            dcc.Slider(id="weight-wsi", min=0, max=1, step=0.01, value=0.2, marks={0: "0", 1: "1"}),
        ], style={"margin-bottom": "15px"}),
        html.Div([
            html.Label("Economic Resilience"),
            dcc.Slider(id="weight-ers", min=0, max=1, step=0.01, value=0.2, marks={0: "0", 1: "1"}),
        ], style={"margin-bottom": "20px"}),
        
        # Scatterplot Metrics Selection Panel
        html.Div([
            html.H4("Metric selection", style={"margin": "0 0 8px 0", "fontSize": "16px"}),
            html.Div("Start with global metrics", style={"opacity": 0.75, "fontSize": "12px", "marginBottom": "12px"}),
            html.Div(checklist_children),
        ], style={
            "backgroundColor": "white",
            "border": "1px solid rgba(0,0,0,0.08)",
            "borderRadius": "6px",
            "padding": "14px",
            "marginTop": "15px",
        }),
    ], className="panel")