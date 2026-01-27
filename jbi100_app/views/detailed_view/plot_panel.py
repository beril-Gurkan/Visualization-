from dash import html, dcc


INFO_TEXT = (
    "What you see in each card:\n"
    "• Grey bars: all countries (distribution)\n"
    "• Grey dots: all countries (brushable rug)\n"
    "• Orange dots: selected in Global Overview\n"
    "• Green dots: selected in Detailed Overview\n"
    "• Dark outline: brushed selection\n"
    "• Dotted line: global median\n"
    "\n"
    "Interactions:\n"
    "• Brush (box select) on rug dots to highlight across views\n"
    "• Use ⤢ to expand a metric; use ↩︎ to return to overview\n"
    "• Clear brush resets linked selections\n"
)

METRIC_FULL = {
    "ASF": "Available Skilled Workforce",
    "IEC": "Industrial Energy Capacity",
    "SCC": "Supply Chain Connectivity",
    "WSI": "Wage Sustainability Index",
    "ERS": "Economic Resilience Score",
}


def _metric_header(short_label: str, expand_btn_id: str):
    full = METRIC_FULL.get(short_label, short_label)
    return html.Div(
        className="metric-card-header",
        children=[
            html.Div(
                className="metric-card-title-wrap",
                children=[
                    html.H3(short_label, className="metric-card-title"),
                    # Per-metric tooltip uses full name
                    html.Span("i", className="info-icon", title=full),
                ],
            ),
            html.Button(
                "⤢",
                id=expand_btn_id,
                className="expand-btn",
                title="Expand this metric",
                n_clicks=0,
                type="button",
            ),
        ],
    )


def plot_panel():
    return html.Div(
        id="plot-panel",
        className="panel",
        children=[
            html.Div(
                className="plot-panel-header",
                children=[
                    html.Div(
                        className="plot-panel-title-wrap",
                        children=[
                            html.H2("Complex Metrics Overview", className="panel-title"),
                            # Panel-level tooltip keeps INFO_TEXT
                            html.Span("i", className="info-icon", title=INFO_TEXT),
                        ],
                    ),
                    html.P(
                        "Brush within the rug of any card to highlight countries across views."
                        "Orange markers indicate countries selected in the Global Overview."
                        "Green markers indicate countries selection in the current, Detailed overview.",
                        className="panel-subtitle",
                    ),
                    html.Div(
                        className="plot-panel-title-wrap",
                        children=[
                            html.Button(
                                "↩︎ Back",
                                id="metric-expand-clear",
                                className="expand-clear-btn",
                                title="Return to small multiples grid",
                                n_clicks=0,
                                type="button",
                            ),
                            html.Button(
                                "🖌 Clear Brush",
                                id="metric-brush-clear",
                                className="expand-clear-btn",
                                title="Clear linked brushing selection",
                                n_clicks=0,
                                type="button",
                            ),
                        ],
                    ),
                ],
            ),
            html.Div(
                id="metric-cards-grid",
                className="metric-cards-grid",
                children=[
                    html.Div(
                        id="metric-card-wrap-asf",
                        className="metric-card",
                        children=[
                            _metric_header("ASF", "metric-expand-asf"),
                            dcc.Graph(
                                id="metric-card-asf",
                                className="graph-container",
                                config={"displayModeBar": True, "responsive": True},
                            ),
                        ],
                    ),
                    html.Div(
                        id="metric-card-wrap-iec",
                        className="metric-card",
                        children=[
                            _metric_header("IEC", "metric-expand-iec"),
                            dcc.Graph(
                                id="metric-card-iec",
                                className="graph-container",
                                config={"displayModeBar": True, "responsive": True},
                            ),
                        ],
                    ),
                    html.Div(
                        id="metric-card-wrap-scc",
                        className="metric-card",
                        children=[
                            _metric_header("SCC", "metric-expand-scc"),
                            dcc.Graph(
                                id="metric-card-scc",
                                className="graph-container",
                                config={"displayModeBar": True, "responsive": True},
                            ),
                        ],
                    ),
                    html.Div(
                        id="metric-card-wrap-wsi",
                        className="metric-card",
                        children=[
                            _metric_header("WSI", "metric-expand-wsi"),
                            dcc.Graph(
                                id="metric-card-wsi",
                                className="graph-container",
                                config={"displayModeBar": True, "responsive": True},
                            ),
                        ],
                    ),
                    html.Div(
                        id="metric-card-wrap-ers",
                        className="metric-card",
                        children=[
                            _metric_header("ERS", "metric-expand-ers"),
                            dcc.Graph(
                                id="metric-card-ers",
                                className="graph-container",
                                config={"displayModeBar": True, "responsive": True},
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )
