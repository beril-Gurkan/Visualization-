from dash import html, dcc


def mini_map_panel():
    return html.Div(
        id="mini-map-panel",
        className="panel",
        children=[
            dcc.Link(
                html.Button(
                    "Back to Overview",
                    style={"cursor": "pointer", "width": "100%", "padding": "10px"}
                ),
                href="/"
            )
        ]
    )
