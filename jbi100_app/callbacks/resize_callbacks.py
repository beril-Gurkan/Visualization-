from dash.dependencies import Input, Output
from jbi100_app.app_instance import app

# Force Plotly to resize graphs after view switching (display:none -> display:grid)
app.clientside_callback(
    """
    function(selected_region) {
        function doResize() {
            if (!window.Plotly) return;

            const ids = ["globe-map", "ranking-bar", "region-map"];
            ids.forEach(id => {
                const el = document.getElementById(id);
                if (!el) return;

                // Plotly graph div is inside dcc.Graph container
                const gd = el.querySelector(".js-plotly-plot");
                if (gd) {
                    try { window.Plotly.Plots.resize(gd); } catch(e) {}
                }
            });
        }

        // run a few times to catch the moment when the grid becomes visible
        setTimeout(doResize, 100);
        setTimeout(doResize, 250);
        setTimeout(doResize, 500);

        return "";
    }
    """,
    Output("resize-sentinel", "children"),
    Input("selected_region", "data"),
)
