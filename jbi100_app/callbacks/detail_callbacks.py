from dash.dependencies import Input, Output
from jbi100_app.app_instance import app
from jbi100_app.views.detailed_info import detailed_info


@app.callback(
    Output("detailed-info-wrapper", "children"),
    Input("selected_country", "data"),
)
def render_country_detail(selected_country):
    return detailed_info(selected_country)
