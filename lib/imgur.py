import re

from lib.download import fetch_html

Url = str


def try_to_extract_image_from_album(url: Url) -> Url:
    html = fetch_html(url)
    m = re.search(r'<meta name="twitter:image" data-react-helmet="true" content="(.*?)">', html)
    return m.group(1) if m else url
