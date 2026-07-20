import duckdb
import os
import sys

sql_dir = "sql"

con = duckdb.connect()
con.execute("INSTALL spatial; LOAD spatial;")

errors = 0
for fn in sorted(os.listdir(sql_dir)):
    if not fn.endswith(".sql"):
        continue
    filepath = os.path.join(sql_dir, fn)
    sql = open(filepath).read()
    print(f"\n=== {fn} ===")
    
    # Split by ; and execute each statement separately
    statements = [s.strip() for s in sql.split(";") if s.strip()]
    
    for stmt in statements:
        try:
            # Check if it's a SELECT query (produces results)
            is_select = stmt.upper().lstrip().startswith("SELECT")
            
            if is_select:
                result = con.execute(stmt)
                rows = result.fetchall()
                if rows:
                    desc = result.description
                    headers = [d[0] for d in desc]
                    # Print header
                    print("  " + " | ".join(str(h) for h in headers))
                    print("  " + "-" * (sum(len(str(h)) + 3 for h in headers)))
                    # Print rows (limit to 50 for display)
                    for row in rows[:50]:
                        print("  " + " | ".join(str(v) if v is not None else "NULL" for v in row))
                    if len(rows) > 50:
                        print(f"  ... ({len(rows)} rows total, showing first 50)")
                    print(f"  → {len(rows)} rows")
                else:
                    print("  (empty result)")
            else:
                # Non-SELECT: just execute
                con.execute(stmt)
                print("  ✓")
                
        except Exception as e:
            print(f"  ✗ ERROR: {e}")
            errors += 1

print(f"\n{'='*50}")
print(f"Queries ejecutadas: {len([f for f in os.listdir(sql_dir) if f.endswith('.sql')])}")
print(f"Errores: {errors}")
con.close()
sys.exit(0 if errors == 0 else 1)
