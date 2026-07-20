import pandas as pd
import os

base = "parquet"
for root, dirs, files in os.walk(base):
    for fn in files:
        if fn.endswith(".csv"):
            csv_path = os.path.join(root, fn)
            parquet_path = csv_path.replace(".csv", ".parquet")
            df = pd.read_csv(csv_path)
            df.to_parquet(parquet_path, index=False)
            print(f"  {csv_path} -> {parquet_path} ({len(df)} rows)")
