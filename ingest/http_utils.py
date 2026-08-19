"""
Shared HTTP utilities with retry + backoff for ISTAC and other rate-limited APIs.
Usage:
    from http_utils import fetch_text, get_csv_df
    content = fetch_text(url)
    df = get_csv_df(url)
"""
import time
import urllib.request
import urllib.error
import pandas as pd
import requests

MAX_RETRIES = 5
BASE_DELAY = 2  # seconds


def fetch_text(url, encoding="utf-8", max_retries=MAX_RETRIES, delay=BASE_DELAY):
    """Fetch URL content with exponential backoff on 429/5xx errors."""
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "laspalmas-intelligence/1.0"})
            response = urllib.request.urlopen(req, timeout=30)
            return response.read().decode(encoding)
        except urllib.error.HTTPError as e:
            if e.code == 429 or e.code >= 500:
                wait = delay * (2 ** attempt)
                print(f"  [retry {attempt+1}/{max_retries}] HTTP {e.code}, waiting {wait}s...")
                time.sleep(wait)
            else:
                raise
    raise RuntimeError(f"Failed after {max_retries} retries: {url}")


def get_csv_df(url, max_retries=MAX_RETRIES, delay=BASE_DELAY, **kwargs):
    """Download CSV with retry and return pandas DataFrame."""
    for attempt in range(max_retries):
        try:
            resp = requests.get(url, headers={"User-Agent": "laspalmas-intelligence/1.0"}, timeout=120)
            resp.raise_for_status()
            resp.encoding = "utf-8"
            return pd.read_csv(pd.io.common.StringIO(resp.text), **kwargs)
        except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError) as e:
            if hasattr(e, 'response') and e.response is not None:
                code = e.response.status_code
                if code == 429 or code >= 500:
                    wait = delay * (2 ** attempt)
                    print(f"  [retry {attempt+1}/{max_retries}] HTTP {code}, waiting {wait}s...")
                    time.sleep(wait)
                    continue
            raise
    raise RuntimeError(f"Failed after {max_retries} retries: {url}")
