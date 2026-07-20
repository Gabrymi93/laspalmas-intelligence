import duckdb
import os

con = duckdb.connect()
con.execute("INSTALL spatial; LOAD spatial;")
sql_dir = "sql"
for fn in sorted(os.listdir(sql_dir)):
    if fn.endswith(".sql"):
        sql = open(os.path.join(sql_dir, fn)).read()
        print(f"=== {fn} ===")
        try:
            df = con.execute(sql).fetchdf()
            print(df.to_string(index=False))
        except Exception as e:
            print(f"  x {e}")
        print()
