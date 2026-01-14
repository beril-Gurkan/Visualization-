from dash import html, dcc
from dash import dash_table


def ranking_panel():
    """Compact ranking panel: metric dropdown + order + top-N + numbered ranking table (non-interactive)."""
    return html.Div(
        className="panel",
        style={
            "justifyContent": "flex-start",
            "alignItems": "stretch",
            "gap": "10px",
            "fontSize": "1.2rem",
            "padding": "12px",
        },
        children=[
            html.Div(id="ranking-title", style={"fontWeight": "800"}, children="Rankings"),

            dcc.Dropdown(
                id="ranking-metric",
                clearable=False,
                value="Complex_Metrics",
                options=[
                    {"label": "Complex Metrics (Custom Weights)", "value": "Complex_Metrics"},
                    {"label": "GDP per Capita (USD)", "value": "Real_GDP_per_Capita_USD"},
                    {"label": "Literacy Rate (%)", "value": "Total_Literacy_Rate"},
                    {"label": "Electricity Access (%)", "value": "electricity_access_percent"},
                    {"label": "Unemployment (%)", "value": "Unemployment_Rate_percent"},
                    {"label": "Public Debt (% of GDP)", "value": "Public_Debt_percent_of_GDP"},
                ],
            ),

            dcc.RadioItems(
                id="ranking-order",
                value="desc",
                options=[
                    {"label": "High → Low", "value": "desc"},
                    {"label": "Low → High", "value": "asc"},
                ],
                inline=True,
            ),

            html.Div(
                style={"display": "flex", "gap": "10px", "alignItems": "center"},
                children=[
                    html.Div("Show:", style={"fontWeight": "700"}),
                    dcc.Dropdown(
                        id="ranking-top-n",
                        clearable=False,
                        searchable=False,
                        value="10",
                        style={"width": "140px"},
                        options=[
                            {"label": "Top 5", "value": "5"},
                            {"label": "Top 10", "value": "10"},
                            {"label": "Top 25", "value": "25"},
                            {"label": "All", "value": "all"},
                        ],
                    ),
                    html.Button(
                        "Clear selection",
                        id="btn-clear-country",
                        n_clicks=0,
                        style={
                            "marginLeft": "auto",
                            "padding": "6px 10px",
                            "borderRadius": "6px",
                            "border": "1px solid rgba(0,0,0,0.2)",
                            "backgroundColor": "#f5f5f5",
                            "cursor": "pointer",
                            "fontSize": "12px",
                        },
                    ),
                ],
            ),

            # ✅ IMPORTANT: no row_selectable, no selected_rows => removes radio-circle column
            dash_table.DataTable(
                id="ranking-table",
                data=[],
                columns=[],
                page_action="none",
                sort_action="none",
                style_as_list_view=True,

                # ✅ removes the “active cell” selection behaviour
                cell_selectable=False,

                style_table={
                    "height": "260px",
                    "overflowY": "auto",
                    "border": "1px solid rgba(0,0,0,0.10)",
                    "borderRadius": "8px",
                },
                style_cell={
                    "padding": "8px 10px",
                    "fontFamily": "inherit",
                    "fontSize": "13px",
                    "whiteSpace": "nowrap",
                    "overflow": "hidden",
                    "textOverflow": "ellipsis",
                },
                style_header={
                    "fontWeight": "700",
                    "backgroundColor": "rgba(0,0,0,0.03)",
                    "borderBottom": "1px solid rgba(0,0,0,0.10)",
                },
                style_data_conditional=[],
            ),

            html.Div(
                id="ranking-hint",
                children="Selection is done via the map (not the table).",
                style={"opacity": 0.7, "fontSize": "12px"},
            ),
        ],
    )
