
import os, pandas as pd

def load_shops_config(path: str = "src/config/shops.csv"):
    if not os.path.exists(path):
        return pd.DataFrame(columns=["name","type","base_url","selector_config"])
    return pd.read_csv(path)
