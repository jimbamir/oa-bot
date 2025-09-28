
import pandas as pd
def apply_filters(df: pd.DataFrame, min_roi: float, min_margin: float, exclude_amazon: bool):
    out = df.copy()
    if min_roi: out = out[out["roi"].fillna(0) >= min_roi]
    if min_margin: out = out[out["margin"].fillna(0) >= min_margin]
    if exclude_amazon: out = out[out["amazon_seller"].fillna("") != "Amazon"]
    return out.sort_values(by=["roi","margin","profit"], ascending=[False, False, False])
