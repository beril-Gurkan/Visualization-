# jbi100_app/callbacks/selected_label.py
from dash.dependencies import Input, Output
from jbi100_app.app_instance import app

@app.callback(
    Output("selected-countries-label", "children"),
    Input("selected-countries", "data"),
)
def update_label(selected):
    if not selected:
        return "None"
    selected = list(selected)
    if len(selected) <= 10:
        return ", ".join(selected)
    return ", ".join(selected[:10]) + f" +{len(selected)-10} more"