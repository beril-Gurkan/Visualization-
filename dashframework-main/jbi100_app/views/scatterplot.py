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
        self.feature_x = feature_x
        self.feature_y = feature_y

        points = []
        if isinstance(selected_data, dict):
            points = selected_data.get("points") or []

        selected_countries = set()
        for p in points:
            cd = p.get("customdata")
            if isinstance(cd, (list, tuple)) and len(cd) > 0:
                selected_countries.add(cd[0])
            elif isinstance(cd, str):
                selected_countries.add(cd)

        return self._build_figure(selected_countries)

    def _build_figure(self, selected_countries):
        xcol = self.feature_x
        ycol = self.feature_y

        if xcol not in self.df.columns or ycol not in self.df.columns:
            fig = go.Figure()
            fig.update_layout(title="Invalid metric selection", xaxis_title=xcol, yaxis_title=ycol)
            return fig

        df_plot = self.df.copy()
        df_plot[xcol] = df_plot[xcol].astype(float)
        df_plot[ycol] = df_plot[ycol].astype(float)

        countries = df_plot["Country"].astype(str)

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
                    customdata=countries,
                    text=countries,
                    hovertemplate="<b>%{text}</b><br>"
                                  + f"{xcol}: %{{x:.3f}}<br>"
                                  + f"{ycol}: %{{y:.3f}}<extra></extra>",
                    marker=dict(size=marker_size, opacity=marker_opacity),
                )
            ]
        )

        fig.update_layout(
            title=f"{xcol} vs {ycol}",
            margin=dict(l=40, r=20, t=40, b=40),
            xaxis_title=xcol,
            yaxis_title=ycol,
        )
        return fig