from typing import Dict

import requests

HEADERS = {
    'User-Agent': "Mozilla/5.0 (X11; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0"
}

Url = str


def fetch_json(url: Url) -> Dict:
    r = requests.get(url, headers=HEADERS)
    d: Dict = r.json()
    return d


def fetch_html(url: Url) -> str:
    r = requests.get(url, headers=HEADERS)
    return r.text
