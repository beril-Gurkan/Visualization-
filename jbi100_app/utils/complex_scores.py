"""
Complex metric calculation module.
Computes weighted composite scores from individual metrics based on user-selected
weights and toggles from the detailed view panel.
"""

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
    """
    Calculate weighted composite scores from enabled metrics.
    
    Args:
        w_asf, w_iec, w_scc, w_wsi, w_ers: Weights (0-100) for each metric
        t_asf, t_iec, t_scc, t_wsi, t_ers: Toggles (True/False) for each metric
    
    Returns:
        DataFrame with Country, individual metric columns, and Complex_Score
    """
    scores = {}
    weights = {}

    # Only include metrics that are toggled on
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

    # Return empty if no metrics are enabled
    if not scores:
        return pd.DataFrame({"Country": [], "Complex_Score": []})

    # Merge all enabled metrics into a single DataFrame
    result_df = None
    for name, series in scores.items():
        temp_df = pd.DataFrame({"Country": series.index, name: series.values})
        result_df = temp_df if result_df is None else result_df.merge(temp_df, on="Country", how="outer")

    # Calculate weighted average of enabled metrics
    total_weight = sum(weights.values()) or 1
    score_cols = list(scores.keys())
    result_df["Complex_Score"] = 0
    for col in score_cols:
        # Normalize by total weight and add to composite score
        result_df["Complex_Score"] += (weights[col] / total_weight) * result_df[col].fillna(0)

    return result_df[["Country", "Complex_Score"] + score_cols]
