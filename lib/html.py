import re

from bs4 import BeautifulSoup


def remove_html_tags(text):
    """Remove html tags from a string"""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


def html_to_plain_text(html: str) -> str:
    soup = BeautifulSoup(html, features="html.parser")
    result: str = soup.get_text().strip()
    return result
