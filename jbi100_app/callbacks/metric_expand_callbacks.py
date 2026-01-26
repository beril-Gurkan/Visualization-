from dash.dependencies import Input, Output, State
from dash import callback_context

from jbi100_app.app_instance import app


CARD_IDS = ["asf", "iec", "scc", "wsi", "ers"]
KEY_MAP = {"asf": "ASF", "iec": "IEC", "scc": "SCC", "wsi": "WSI", "ers": "ERS"}


def _enabled_map(t_asf, t_iec, t_scc, t_wsi, t_ers):
    return {
        "asf": bool(t_asf),
        "iec": bool(t_iec),
        "scc": bool(t_scc),
        "wsi": bool(t_wsi),
        "ers": bool(t_ers),
    }


@app.callback(
    Output("expanded-metric", "data"),
    Input("metric-expand-asf", "n_clicks"),
    Input("metric-expand-iec", "n_clicks"),
    Input("metric-expand-scc", "n_clicks"),
    Input("metric-expand-wsi", "n_clicks"),
    Input("metric-expand-ers", "n_clicks"),
    Input("metric-expand-clear", "n_clicks"),
    # also respond when toggles change (to auto-clear invalid expanded state)
    Input("toggle-asf", "value"),
    Input("toggle-iec", "value"),
    Input("toggle-scc", "value"),
    Input("toggle-wsi", "value"),
    Input("toggle-ers", "value"),
    State("expanded-metric", "data"),
    prevent_initial_call=True,
)
def toggle_expanded(_a, _b, _c, _d, _e, _clear, t_asf, t_iec, t_scc, t_wsi, t_ers, expanded):
    trig = callback_context.triggered_id
    enabled = _enabled_map(t_asf, t_iec, t_scc, t_wsi, t_ers)

    expanded = (expanded or "").strip().lower() or None

    # If a toggle changed and the currently expanded metric is now disabled -> clear it
    if trig and str(trig).startswith("toggle-") and expanded:
        if expanded in enabled and not enabled[expanded]:
            return None
        return expanded

    if trig == "metric-expand-clear":
        return None

    if not trig or not str(trig).startswith("metric-expand-"):
        return expanded

    clicked = str(trig).replace("metric-expand-", "").strip().lower()
    if clicked not in CARD_IDS:
        return expanded

    # If clicked metric is disabled, do nothing
    if not enabled.get(clicked, True):
        return expanded

    # toggle off if re-clicking the same one
    if expanded == clicked:
        return None

    return clicked


@app.callback(
    Output("metric-cards-grid", "className"),
    Output("metric-card-wrap-asf", "className"),
    Output("metric-card-wrap-iec", "className"),
    Output("metric-card-wrap-scc", "className"),
    Output("metric-card-wrap-wsi", "className"),
    Output("metric-card-wrap-ers", "className"),
    # ✅ styles to actually hide/show cards
    Output("metric-card-wrap-asf", "style"),
    Output("metric-card-wrap-iec", "style"),
    Output("metric-card-wrap-scc", "style"),
    Output("metric-card-wrap-wsi", "style"),
    Output("metric-card-wrap-ers", "style"),
    Input("expanded-metric", "data"),
    Input("toggle-asf", "value"),
    Input("toggle-iec", "value"),
    Input("toggle-scc", "value"),
    Input("toggle-wsi", "value"),
    Input("toggle-ers", "value"),
)
def apply_expand_classes(expanded, t_asf, t_iec, t_scc, t_wsi, t_ers):
    expanded = (expanded or "").strip().lower()
    enabled = _enabled_map(t_asf, t_iec, t_scc, t_wsi, t_ers)

    base = "metric-card"
    grid_base = "metric-cards-grid"

    # style helper
    def vis(card_id: str):
        return {"display": "flex"} if enabled.get(card_id, True) else {"display": "none"}

    # If expanded is currently disabled, behave like no expanded
    if expanded and not enabled.get(expanded, True):
        expanded = ""

    # no expand → default small-multiples grid
    if not expanded:
        return (
            grid_base,
            base, base, base, base, base,
            vis("asf"), vis("iec"), vis("scc"), vis("wsi"), vis("ers"),
        )

    # expanded-mode → sidebar + main detail
    def cls(card):
        if card == expanded:
            return f"{base} expanded"
        return f"{base} collapsed"

    return (
        f"{grid_base} expanded-mode",
        cls("asf"),
        cls("iec"),
        cls("scc"),
        cls("wsi"),
        cls("ers"),
        vis("asf"), vis("iec"), vis("scc"), vis("wsi"), vis("ers"),
    )
