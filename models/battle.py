from typing import Dict, List

from models.comment import Comment

Url = str


class Battle:
    def __init__(self) -> None:
        self.title = ""
        self.json_url: Url = ""
        self.json_source: Dict = {}
        self.original_image_url: Url = ""
        self.comments: List[Comment] = []

    def url_without_json(self) -> Url:
        return self.json_url.replace(".json", "")
