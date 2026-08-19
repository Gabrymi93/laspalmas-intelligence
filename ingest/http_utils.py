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

MAX_RETRIES = 3
BASE_DELAY = 1  # seconds
THROTTLE = 2  # seconds between requests to avoid 429

_last_request_time = 0


def _throttle():
    """Wait between requests to avoid hitting rate limits."""
    global _last_request_time
    elapsed = time.time() - _last_request_time
    if elapsed < THROTTLE:
        time.sleep(THROTTLE - elapsed)
    _last_request_time = time.time()


def fetch_text(url, encoding="utf-8", max_retries=MAX_RETRIES, delay=BASE_DELAY):
    """Fetch URL content with exponential backoff on 429/5xx errors."""
    _throttle()
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
    _throttle()
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


def fetch_bytes(url, max_retries=MAX_RETRIES, delay=BASE_DELAY, timeout=120, params=None):
    """Fetch URL and return raw bytes with retry on 429/5xx."""
    _throttle()
    for attempt in range(max_retries):
        try:
            resp = requests.get(url, headers={"User-Agent": "laspalmas-intelligence/1.0"},
                                timeout=timeout, params=params)
            resp.raise_for_status()
            return resp.content
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


def fetch_json(url, max_retries=MAX_RETRIES, delay=BASE_DELAY, timeout=120, params=None):
    """Fetch URL and parse JSON with retry on 429/5xx."""
    import json
    return json.loads(fetch_bytes(url, max_retries, delay, timeout, params).decode("utf-8"))


def fetch_bytes_post(url, data=None, headers=None, max_retries=MAX_RETRIES, delay=BASE_DELAY, timeout=120):
    """POST URL and return raw bytes with retry on 429/5xx."""
    _throttle()
    for attempt in range(max_retries):
        try:
            resp = requests.post(url, data=data, headers=headers or {"User-Agent": "laspalmas-intelligence/1.0"},
                                 timeout=timeout)
            resp.raise_for_status()
            return resp.content
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
