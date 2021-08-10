from typing import Dict, List

Url = str


class Index:
    def __init__(self) -> None:
        self.json_url: Url = ""
        self.before = ""
        self.after = ""
        self.entries: List[Dict] = []

    def url_without_json(self) -> Url:
        return self.json_url.replace(".json", "")
