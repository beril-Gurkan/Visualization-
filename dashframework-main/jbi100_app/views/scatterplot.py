from dash import dcc, html
import plotly.graph_objects as go


class Scatterplot(html.Div):
    def __init__(self, name, feature_x, feature_y, df):
        self.html_id = name.lower().replace(" ", "-")
        self.df = df
        self.feature_x = feature_x
        self.feature_y = feature_y

        super().__init__(
            className="graph_card",
            children=[
                html.H6(name),
                dcc.Graph(
                    id=self.html_id,
                    clear_on_unhover=True,
                    config={"displayModeBar": True},
                ),
            ],
        )

    def update(self, feature_x, feature_y, selected_data=None):
        """
        Returns a Plotly figure for the selected x/y metrics.
        selected_data comes from dcc.Graph(selectedData) and may be None.
        """
        self.feature_x = feature_x
        self.feature_y = feature_y

        # --- Handle no selection safely ---
        points = []
        if isinstance(selected_data, dict):
            points = selected_data.get("points") or []

        # Try to detect selected countries from customdata (preferred)
        selected_countries = set()
        for p in points:
            cd = p.get("customdata")
            if isinstance(cd, (list, tuple)) and len(cd) > 0:
                selected_countries.add(cd[0])
            elif isinstance(cd, str):
                selected_countries.add(cd)

        # Build figure
        return self._build_figure(selected_countries)

    def _build_figure(self, selected_countries):
        """
        Build the scatterplot figure.
        - x: feature_x column
        - y: feature_y column
        - hover: country name
        - selection: if selected_countries not empty, highlight them
        """
        xcol = self.feature_x
        ycol = self.feature_y

        # Basic guards
        if xcol not in self.df.columns or ycol not in self.df.columns:
            fig = go.Figure()
            fig.update_layout(
                title="Invalid metric selection",
                xaxis_title=xcol,
                yaxis_title=ycol,
            )
            return fig

        # Ensure numeric (Plotly will misbehave if strings)
        df_plot = self.df.copy()
        df_plot[xcol] = df_plot[xcol].astype(float)
        df_plot[ycol] = df_plot[ycol].astype(float)

        countries = df_plot["Country"].astype(str)

        # Decide styling: highlight selected
        if selected_countries:
            is_sel = countries.isin(selected_countries)
            marker_opacity = [1.0 if s else 0.2 for s in is_sel]
            marker_size = [10 if s else 7 for s in is_sel]
        else:
            marker_opacity = 0.85
            marker_size = 8

        fig = go.Figure(
            data=[
                go.Scatter(
                    x=df_plot[xcol],
                    y=df_plot[ycol],
                    mode="markers",
                    customdata=countries,  # so selection returns Country
                    text=countries,
                    hovertemplate="<b>%{text}</b><br>"
                                  + f"{xcol}: %{{x:.3f}}<br>"
                                  + f"{ycol}: %{{y:.3f}}<extra></extra>",
                    marker=dict(
                        size=marker_size,
                        opacity=marker_opacity,
                    ),
                )
            ]
        )

        fig.update_layout(
            margin=dict(l=40, r=20, t=30, b=40),
            xaxis_title=xcol,
            yaxis_title=ycol,
        )

        return fig
