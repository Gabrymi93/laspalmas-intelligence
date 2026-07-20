"""
Ingest: GTFS stop coordinates via OSM Overpass API.
Matches our 844 stop_ids from stop_times with OSM bus_stop ref tags.
Output: parquet/movilidad/gtfs_stops.parquet
"""
import json, os, time, urllib.request, urllib.parse, pandas as pd, duckdb

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "parquet", "movilidad")
os.makedirs(OUT, exist_ok=True)

con = duckdb.connect()
our_ids = set(r[0] for r in con.sql(f"SELECT DISTINCT stop_id FROM '{OUT}/gtfs_stop_times.parquet'").fetchall())
con.close()
print(f"GTFS stop_ids: {len(our_ids)}")

query = '''
[out:json][timeout:120];
area["name"="Las Palmas de Gran Canaria"]["admin_level"=8];
node["highway"="bus_stop"](area);
out body 1000;
'''
data = urllib.parse.urlencode({"data": query}).encode()
for attempt in range(3):
    try:
        req = urllib.request.Request(
            "https://overpass-api.de/api/interpreter", data=data,
            headers={"User-Agent": "laspalmas-intelligence/1.0", "Content-Type": "application/x-www-form-urlencoded"}
        )
        resp = urllib.request.urlopen(req, timeout=120)
        result = json.loads(resp.read())
        break
    except Exception as e:
        print(f"  attempt {attempt+1} failed: {e}")
        if attempt < 2:
            time.sleep(30)
        else:
            print("  giving up")
            exit(1)

stops = []
for e in result["elements"]:
    tags = e.get("tags", {})
    ref = tags.get("ref", "")
    if ref and ref.isdigit() and len(ref) <= 4:
        sid = int(ref)
        if sid in our_ids:
            stops.append({"stop_id": sid, "stop_name": tags.get("name", ""),
                          "stop_lat": e["lat"], "stop_lon": e["lon"]})

df = pd.DataFrame(stops)
df.to_parquet(os.path.join(OUT, "gtfs_stops.parquet"), index=False)
print(f"Saved: {len(df)} stops ({(len(df)/len(our_ids)*100):.0f}% of GTFS stop_ids)")
