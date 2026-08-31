"""
Fetch atestados from Wayback Machine (ODS format).
Missing years: 2000-2001, 2006-2011, 2015-2016
"""
import os
import requests
import pandas as pd
from odf.opendocument import load
from odf.table import Table, TableRow, TableCell
from odf.text import P
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from http_utils import get_csv_df

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "parquet", "movilidad")

def read_ods_table(url, timeout=30):
    """Download ODS from Wayback Machine and read as DataFrame."""
    r = requests.get(url, timeout=timeout)
    if r.status_code != 200:
        return None
    
    # Save temp file
    tmp = "/tmp/wayback_temp.ods"
    with open(tmp, 'wb') as f:
        f.write(r.content)
    
    # Read ODS
    doc = load(tmp)
    for table in doc.spreadsheet.getElementsByType(Table):
        rows = table.getElementsByType(TableRow)
        data = []
        for row in rows:
            cells = row.getElementsByType(TableCell)
            row_data = []
            for cell in cells:
                repeat = cell.getAttribute('numbercolumnsrepeated')
                texts = cell.getElementsByType(P)
                value = ''.join([str(t) for t in texts])
                if repeat and int(repeat) > 1:
                    row_data.extend([value] * int(repeat))
                else:
                    row_data.append(value)
            data.append(row_data)
        
        if len(data) > 1:
            columns = data[0]
            return pd.DataFrame(data[1:], columns=columns)
    return None

# Years to recover from Wayback Machine
WAYBACK_YEARS = [2000, 2001, 2006, 2007, 2008, 2009, 2010, 2011, 2015, 2016]

# Existing CSV years (from original source)
CSV_YEARS = [1998, 1999, 2002, 2003, 2004, 2005, 2012, 2013, 2014]

for tipo in ["ACC", "HER", "VEH"]:
    print(f"\n=== {tipo} ===")
    dfs = []
    
    # Load existing CSV data
    for year in CSV_YEARS:
        url = f"http://datosabiertos.laspalmasgc.es/repositorio/policia/atestados/DB_{tipo}_{year}.csv"
        try:
            df = get_csv_df(url, encoding="latin1")
            df["year"] = year
            dfs.append(df)
            print(f"  {year} (CSV): {len(df)} rows")
        except:
            pass
    
    # Load Wayback Machine data
    for year in WAYBACK_YEARS:
        # Try multiple timestamps
        timestamps = [
            "20200926140747",
            "20191207191800",
            "20201022150530",
            "20191211030645",
            "20211024030509",
        ]
        loaded = False
        for ts in timestamps:
            url = f"https://web.archive.org/web/{ts}/http://datosabiertos.laspalmasgc.es/repositorio/policia/atestados/DB_{tipo}_{year}.ods"
            try:
                df = read_ods_table(url)
                if df is not None and len(df) > 0:
                    df["year"] = year
                    dfs.append(df)
                    print(f"  {year} (Wayback {ts}): {len(df)} rows")
                    loaded = True
                    break
            except:
                pass
        if not loaded:
            print(f"  {year}: NOT FOUND")
    
    if dfs:
        combined = pd.concat(dfs, ignore_index=True)
        outfile = f"atestados_{tipo.lower()}.parquet" if tipo != "ACC" else "atestados_acc.parquet"
        if tipo == "HER":
            outfile = "atestados_her.parquet"
        elif tipo == "VEH":
            outfile = "atestados_veh.parquet"
        combined.to_parquet(os.path.join(OUT, outfile), index=False)
        print(f"  Total: {len(combined)} rows -> {outfile}")

print("\nDone.")
