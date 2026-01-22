import json

from dash.dependencies import Input, Output

from jbi100_app.app_instance import app


@app.callback(
    Output("debug-click", "children"),
    Input("globe-map", "clickData"),
)
def show_click(clickData):
    return json.dumps(clickData, indent=2)
