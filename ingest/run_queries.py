import duckdb
import os

con = duckdb.connect()
sql_dir = "sql"
for fn in sorted(os.listdir(sql_dir)):
    if fn.endswith(".sql"):
        sql = open(os.path.join(sql_dir, fn)).read()
        print(f"=== {fn} ===")
        df = con.execute(sql).fetchdf()
        print(df.to_string(index=False))
        print()
