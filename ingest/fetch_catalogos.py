"""
Ingest: catálogos completos de las fuentes de datos.

Produce dos parquet indexados en meta/catalogos/:
  1. laspalmasgc_catalogo.parquet — Ayuntamiento LPGC (DCAT RDF, ~100 datasets)
  2. istac_catalogo.parquet — ISTAT CKAN (API REST, ~22k datasets)

Uso: consultar qué datasets existen sin hacer requests individuales.
"""
import os, sys, json, re
import requests
import pandas as pd
import xml.etree.ElementTree as ET

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "meta", "catalogos")
os.makedirs(OUT, exist_ok=True)

# ---------- 1. Ayuntamiento LPGC (DCAT RDF) ----------
print("\n=== Catálogo Ayuntamiento LPGC ===")
try:
    resp = requests.get(
        "http://datosabiertos.laspalmasgc.es/proxyFileCKAN.php"
        "?catalog=http://datosabiertos.laspalmasgc.es/catalog.rdf",
        timeout=60
    )
    resp.raise_for_status()
    
    # Parse with namespace-aware XPath
    ns = {
        'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
        'dcat': 'http://www.w3.org/ns/dcat#',
        'dct': 'http://purl.org/dc/terms/',
    }
    root = ET.fromstring(resp.content)
    
    rows = []
    for ds in root.findall('.//dcat:Dataset', ns):
        title_el = ds.find('dct:title', ns)
        ident_el = ds.find('dct:identifier', ns)
        desc_el = ds.find('dct:description', ns)
        issued_el = ds.find('dct:issued', ns)
        modified_el = ds.find('dct:modified', ns)
        keywords_el = ds.findall('dcat:keyword', ns)
        keywords = [kw.text for kw in keywords_el if kw.text]
        
        resources = []
        for dist in ds.findall('dcat:distribution', ns):
            d_title = dist.find('dct:title', ns)
            d_url = dist.find('dcat:accessURL', ns)
            d_format = dist.find('dct:format', ns)
            resources.append({
                "name": d_title.text.strip() if d_title is not None and d_title.text else None,
                "url": d_url.text.strip() if d_url is not None and d_url.text else None,
                "format": d_format.text.strip() if d_format is not None and d_format.text else None,
            })
        
        rows.append({
            "id": ident_el.text.strip() if ident_el is not None and ident_el.text else None,
            "title": title_el.text.strip() if title_el is not None and title_el.text else None,
            "description": desc_el.text.strip()[:200] if desc_el is not None and desc_el.text else None,
            "issued": issued_el.text.strip() if issued_el is not None and issued_el.text else None,
            "modified": modified_el.text.strip() if modified_el is not None and modified_el.text else None,
            "keywords": ", ".join(keywords) if keywords else None,
            "n_resources": len(resources),
            "resources": json.dumps(resources, ensure_ascii=False),
            "formats": ", ".join(sorted(set(r["format"] for r in resources if r.get("format")))),
            "fuente": "laspalmasgc",
        })
    
    df = pd.DataFrame(rows)
    out_path = os.path.join(OUT, "laspalmasgc_catalogo.parquet")
    df.to_parquet(out_path, index=False)
    print(f"  {len(df)} datasets -> {out_path}")
    
except Exception as e:
    print(f"  x Error: {e}")

# ---------- 2. ISTAT CKAN (via package_search) ----------
print("\n=== Catálogo ISTAT CKAN ===")
try:
    rows = []
    start = 0
    limit = 500
    
    while True:
        resp = requests.get(
            "https://datos.canarias.es/catalogos/estadisticas/api/3/action/package_search",
            params={"rows": limit, "start": start},
            timeout=30
        )
        data = resp.json()
        result = data.get("result", {})
        datasets = result.get("results", [])
        total = result.get("count", 0)
        
        for ds in datasets:
            resources = ds.get("resources", [])
            rows.append({
                "id": ds.get("id"),
                "name": ds.get("name"),
                "title": ds.get("title"),
                "notes": ds.get("notes", "")[:200] if ds.get("notes") else None,
                "organization": ds.get("organization", {}).get("title") if ds.get("organization") else None,
                "tags": ", ".join(t["name"] for t in ds.get("tags", [])),
                "metadata_modified": ds.get("metadata_modified"),
                "n_resources": len(resources),
                "formats": ", ".join(sorted(set(r["format"] for r in resources if r.get("format")))),
                "resources": json.dumps([{
                    "id": r.get("id"),
                    "name": r.get("name"),
                    "format": r.get("format"),
                    "url": r.get("url"),
                    "datastore_active": r.get("datastore_active", False),
                } for r in resources], ensure_ascii=False),
                "fuente": "istac",
            })
        
        print(f"  {start+len(datasets)}/{total} datasets", end="\r")
        start += limit
        if start >= total or start >= 2000:  # cap at 2000 for speed
            break
    
    df = pd.DataFrame(rows)
    out_path = os.path.join(OUT, "istac_catalogo.parquet")
    df.to_parquet(out_path, index=False)
    print(f"\n  {len(df)} datasets -> {out_path}")
    
except Exception as e:
    print(f"  x Error: {e}")

print("\nDone.")
