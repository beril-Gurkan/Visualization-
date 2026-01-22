from dash.dependencies import Input, Output

from jbi100_app.app_instance import app


@app.callback(
    Output("url", "pathname"),
    Input("go-to-detail-button", "n_clicks"),
    prevent_initial_call=True,
)
def navigate_to_detail(n_clicks):
    """
    Navigate to the detailed view when the 'Go to Detail' button is clicked.
    """
    return "/detailed"
