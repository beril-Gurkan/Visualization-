from dash.dependencies import Input, Output, State
from jbi100_app.app_instance import app

# Hover behaviour: grey out other region traces in-place (no figure updates)
app.clientside_callback(
    """
    function(hoverData, fig) {
        if (!fig || !fig.data || !window.Plotly) return "";

        const el = document.getElementById("globe-map");
        if (!el) return "";

        const gd = el.querySelector(".js-plotly-plot");
        if (!gd) return "";

        const FULL = 1.0;
        const FADE = 0.20;

        // choropleth traces only (skip legend helper traces if any)
        const choroplethIdx = [];
        for (let i = 0; i < fig.data.length; i++) {
            const trace = fig.data[i];
            if (trace.type !== "choropleth") continue;
            if (trace.name && trace.name.toLowerCase().includes("selected")) continue;
            choroplethIdx.push(i);
        }
        if (choroplethIdx.length === 0) return "";

        // reset when not hovering
        if (!hoverData || !hoverData.points || hoverData.points.length === 0) {
            const op = choroplethIdx.map(_ => FULL);
            window.Plotly.restyle(gd, {"marker.opacity": [op]}, choroplethIdx);
            return "";
        }

        const hoveredCurve = hoverData.points[0].curveNumber;

        // if hoveredCurve isn’t a choropleth trace, do nothing
        if (choroplethIdx.indexOf(hoveredCurve) === -1) return "";

        const op = choroplethIdx.map(idx => (idx === hoveredCurve ? FULL : FADE));
        window.Plotly.restyle(gd, {"marker.opacity": [op]}, choroplethIdx);
        return "";
    }
    """,
    Output("hover-sentinel", "children"),
    Input("globe-map", "hoverData"),
    State("globe-map", "figure"),
)
