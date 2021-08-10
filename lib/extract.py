import re
from typing import List

from lib import html

Url = str


def extract_urls(text: str, remove_tags=True, uniq=True) -> List[Url]:
    urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
    if remove_tags:
        urls = [html.remove_html_tags(url) for url in urls]
    if uniq:
        urls = list(set(urls))
    return urls
