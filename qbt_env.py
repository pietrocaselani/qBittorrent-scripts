import json
import os
from typing import List

class QBTTracker:
    def __init__(self, name, tag, urls):
        self.name = name
        self.tag = tag
        self.urls = urls

    def __repr__(self):
        return f"<QBTPrivateTracker name={self.name!r} tag={self.tag!r} urls={self.urls!r}>"

class QBTCategoryTagMap:
    def __init__(self, mapping):
        # mapping is expected to be a dict: {category: [tags]}
        self.mapping = mapping or {}

    def get_tags(self, category) -> List[str]:
        return self.mapping.get(category, [])

    def __repr__(self):
        return f"<QBTCategoryTagMap {self.mapping!r}>"

class QBTEnv:
    def __init__(self):
        path = os.path.join(os.path.dirname(__file__), 'qbt-env.json')
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.HOST = data.get('QBT_HOST', 'http://localhost')
        self.PORT = data.get('QBT_PORT', 8080)
        self.USER = data.get('QBT_USER', 'admin')
        self.PASS = data.get('QBT_PASS', 'admin')
        self.PRIVATE_TAG = data.get('QBT_PRIVATE_TAG', 'private')
        self.NO_PRIVATE_TAG = data.get('QBT_NO_PRIVATE_TAG', 'no-private')
        self.NO_TRACKER_TAG = data.get('QBT_NO_TRACKER_TAG', 'no-trackers')
        self.TRACKERS_FILE = data.get('QBT_TRACKERS_FILE', 'tracker_urls.txt')
        self.PRIVATE_TRACKERS = []
        for tracker in data.get('QBT_PRIVATE_TRACKERS', []):
            self.PRIVATE_TRACKERS.append(
                QBTTracker(
                    tracker.get('name'),
                    tracker.get('tag'),
                    tracker.get('urls', [])
                )
            )
        self.CATEGORY_TAG_MAP = QBTCategoryTagMap(data.get('QBT_CATEGORY_TAG_MAP', {}))

    def __repr__(self):
        return f"<QBTEnv {self.__dict__}>"

QBT_ENV = QBTEnv()