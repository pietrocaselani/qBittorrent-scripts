#!/usr/bin/python3 -u

from qbt_env import QBT_ENV
from qbt_utils import IGNORED_TRACKER_URLS, get_client, is_tracker_working
import urllib.parse

def normalize_url(url):
    parsed = urllib.parse.urlparse(url)
    scheme = parsed.scheme.lower()
    netloc = parsed.netloc.lower()
    path = parsed.path.rstrip('/')
    # For UDP trackers, path may be empty or '/'. Treat both as equivalent
    if path == '':
        path = None
    return (scheme, netloc, path)

try:
    client = get_client()

    tracker_urls = set()
    normalized_map = {}

    for torrent in client.torrents.info(private=False, tag=QBT_ENV.NO_PRIVATE_TAG):
        trackers = client.torrents.trackers(torrent.hash)
        for tracker in trackers:
            if tracker.url not in IGNORED_TRACKER_URLS and is_tracker_working(tracker):
                tracker_urls.add(tracker.url)

    for url in tracker_urls:
        norm = normalize_url(url)
        if norm in normalized_map:
            normalized_map[norm].append(url)
        else:
            normalized_map[norm] = [url]

    duplicates = {k: v for k, v in normalized_map.items() if len(v) > 1}
    if duplicates:
        print("Duplicate tracker URLs detected (normalized):")
        for norm, urls in duplicates.items():
            print(f"  {urls}")

    unique_urls = set()
    for norm, urls in normalized_map.items():
        unique_urls.add(urls[0])

    with open(QBT_ENV.TRACKERS_FILE, 'w') as file:
        for url in unique_urls:
            file.write(url + '\n')

    print(f"Unique tracker URLs have been written to {QBT_ENV.TRACKERS_FILE}.")

except Exception as e:
    print(f"An error occurred: {e}")
