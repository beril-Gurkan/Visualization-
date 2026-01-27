import pandas as pd
from jbi100_app.data import (
    available_skilled_workforce,
    industrial_energy_capacity,
    supply_chain_connectivity_score,
    wage_sustainability_index,
    economic_resilience_score,
)

def compute_complex_scores(
    w_asf, w_iec, w_scc, w_wsi, w_ers,
    t_asf, t_iec, t_scc, t_wsi, t_ers
) -> pd.DataFrame:
    scores = {}
    weights = {}

    if t_asf:
        scores["ASF"] = available_skilled_workforce()
        weights["ASF"] = w_asf
    if t_iec:
        scores["IEC"] = industrial_energy_capacity()
        weights["IEC"] = w_iec
    if t_scc:
        scores["SCC"] = supply_chain_connectivity_score()
        weights["SCC"] = w_scc
    if t_wsi:
        scores["WSI"] = wage_sustainability_index()
        weights["WSI"] = w_wsi
    if t_ers:
        scores["ERS"] = economic_resilience_score()
        weights["ERS"] = w_ers

    if not scores:
        return pd.DataFrame({"Country": [], "Complex_Score": []})

    result_df = None
    for name, series in scores.items():
        temp_df = pd.DataFrame({"Country": series.index, name: series.values})
        result_df = temp_df if result_df is None else result_df.merge(temp_df, on="Country", how="outer")

    total_weight = sum(weights.values()) or 1
    score_cols = list(scores.keys())
    result_df["Complex_Score"] = 0
    for col in score_cols:
        result_df["Complex_Score"] += (weights[col] / total_weight) * result_df[col].fillna(0)

    return result_df[["Country", "Complex_Score"] + score_cols]
