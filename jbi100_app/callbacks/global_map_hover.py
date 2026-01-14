from dash.dependencies import Input, Output, State
from jbi100_app.main import app

# Hover behaviour: grey out other region traces in-place (no figure updates)
app.clientside_callback(
    """
    function(hoverData, fig) {
        if (!fig || !fig.data || !window.Plotly) return "";

        const el = document.getElementById("global-map");
        if (!el) return "";

        // Dash versions differ:
        // Sometimes #global-map IS the plotly graph div (has class js-plotly-plot),
        // sometimes it's a wrapper that contains the plotly div.
        const gd = el.classList.contains("js-plotly-plot")
            ? el
            : el.querySelector(".js-plotly-plot");

        if (!gd) return "";

        const FULL = 1.0;
        const FADE = 0.20;

        // choropleth traces only (skip any non-map helper traces)
        const choroplethIdx = [];
        for (let i = 0; i < fig.data.length; i++) {
            if (fig.data[i].type === "choropleth") choroplethIdx.push(i);
        }

        // reset when not hovering
        if (!hoverData || !hoverData.points || hoverData.points.length === 0) {
            const op = choroplethIdx.map(_ => FULL);
            window.Plotly.restyle(gd, { "opacity": op }, choroplethIdx);
            return "";
        }

        const hoveredCurve = hoverData.points[0].curveNumber;

        // if hoveredCurve isn’t a choropleth trace, do nothing
        if (choroplethIdx.indexOf(hoveredCurve) === -1) return "";

        const op = choroplethIdx.map(idx => (idx === hoveredCurve ? FULL : FADE));
        window.Plotly.restyle(gd, { "opacity": op }, choroplethIdx);
        return "";
    }
    """,
    Output("hover-sentinel", "children"),
    Input("global-map", "hoverData"),
    State("global-map", "figure"),
)
