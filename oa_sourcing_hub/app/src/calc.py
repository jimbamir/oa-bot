
import pandas as pd

def default_fee_model():
    return {"referral_pct": 0.15, "fba_fee_fixed": 3.00, "closing_fee": 0.0}

def compute_metrics(df: pd.DataFrame, fee_model: dict):
    df = df.copy()
    for col in ["amazon_price","buy_price"]:
        df[col] = pd.to_numeric(df.get(col, 0), errors="coerce").fillna(0.0)
    ref = fee_model.get("referral_pct", 0.15)
    fba = fee_model.get("fba_fee_fixed", 3.0)
    closing = fee_model.get("closing_fee", 0.0)
    df["amazon_fees"] = df["amazon_price"] * ref + fba + closing
    df["net_revenue"] = df["amazon_price"] - df["amazon_fees"]
    df["profit"] = df["net_revenue"] - df["buy_price"]
    df["roi"] = df["profit"] / df["buy_price"].replace(0, pd.NA)
    df["margin"] = df["profit"] / df["amazon_price"].replace(0, pd.NA)
    df["breakeven_price"] = (df["buy_price"] + fba + closing) / (1 - ref).replace(0, pd.NA)
    if "is_profitable" not in df.columns: df["is_profitable"] = df["profit"] > 0
    needed = ["title","ean","asin","shop_url","buy_price","amazon_price","amazon_fees","net_revenue","profit","roi","margin","breakeven_price","is_profitable","bsr","category","amazon_seller"]
    for c in needed:
        if c not in df.columns: df[c] = pd.NA
    return df[needed]
