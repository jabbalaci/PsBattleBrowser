from pprint import pprint
from typing import Dict
from xml.sax import saxutils

from models.battle import Battle
from models.comment import Comment
from models.index import Index

from lib import extract, html, imgur
from lib.download import fetch_json

Url = str

REDDIT_BASE_URL = "https://old.reddit.com"
SUBREDDIT_URL = "https://old.reddit.com/r/photoshopbattles/.json"
# SUBREDDIT_URL = "https://old.reddit.com/r/photoshopbattles/.json?count=25&after=t3_ozfg8m"


def get_index_url(after: str) -> Url:
    return f"{SUBREDDIT_URL}?count=25&after={after}" if after else SUBREDDIT_URL


def get_index_entries(after: str) -> Index:
    url = get_index_url(after)
    root = fetch_json(url)
    children = root['data']['children']

    result = Index()
    result.json_url = url
    result.after = root['data']['after']
    result.before = root['data']['before'] if root['data']['before'] else ""
    entries = []
    # print("# after:", result.after)
    # print("# before:", result.before)
    for child in children:
        if child['data']['title'].startswith("PsBattle: "):
            if child['data'].get('score', 0) > 0:
                entries.append(child)
        #
    #
    entries.sort(key=lambda d: d['data'].get('score', 0), reverse=True)  # type: ignore
    result.entries = entries
    return result


def try_to_correct(url: Url) -> Url:
    if url.endswith((".jpg", ".jpeg", ".png")):
        return url
    #
    if "imgur.com" in url:
        if ("/a/" in url) or ("/gallery/" in url):
            return url
        # else
        return f"{url}.jpg"
    #
    return url


def get_shopped_entries(permalink: str) -> Battle:
    result = Battle()
    url = f"{REDDIT_BASE_URL}{permalink}.json"
    root = fetch_json(url)

    result.title = root[0]['data']['children'][0]['data']['title']
    result.json_url = url
    result.json_source = root
    result.original_image_url = root[0]['data']['children'][0]['data']['url']

    children = root[1]['data']['children']
    children.sort(key=lambda d: d['data'].get('score', 0), reverse=True)
    for child in children:
        # print("-----")
        data: Dict = child['data']
        try:
            html_src = saxutils.unescape(data['body_html'])
        except KeyError:
            continue
        #
        plain_text = html.html_to_plain_text(html_src)
        if "I am a bot, and this action was performed automatically." in plain_text:
            continue
        if "[deleted]" in plain_text:
            continue
        # print("# html:", html)
        # print("# plain:", plain_text)
        urls = extract.extract_urls(html_src)
        # print("!!!", urls)
        if len(urls) != 1:
            continue
        image_url = urls[0]
        image_url = try_to_correct(image_url)
        if ("imgur.com" in image_url) and (("/a/" in image_url) or ("/gallery/" in image_url)):
            image_url = imgur.try_to_extract_image_from_album(image_url)
            # print("# from album:", image_url)
        # if "imgur.com" not in image_url:
            # continue
        if not image_url.endswith((".jpg", ".jpeg", ".png")):
            # print('# lost:', image_url)
            continue
        #
        c = Comment()
        c.image_url = image_url
        c.body_html = html_src
        c.body_text = plain_text
        c.score = data['score']
        if c.score <= 0:
            continue

        result.comments.append(c)
    #
    # print("-" * 20)

    return result
