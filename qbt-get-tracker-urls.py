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

    # Collect all private tracker URL prefixes from QBT_ENV.PRIVATE_TRACKERS
    private_tracker_prefixes = set()
    for tracker in QBT_ENV.PRIVATE_TRACKERS:
        for url in tracker.urls:
            # Use the base URL (scheme + netloc)
            parsed = urllib.parse.urlparse(url)
            prefix = f"{parsed.scheme}://{parsed.netloc}"
            private_tracker_prefixes.add(prefix)

    unique_urls = set()
    for norm, urls in normalized_map.items():
        url_to_check = urls[0]
        parsed = urllib.parse.urlparse(url_to_check)
        url_prefix = f"{parsed.scheme}://{parsed.netloc}"
        # Only add if not matching any private tracker prefix
        if url_prefix not in private_tracker_prefixes:
            unique_urls.add(url_to_check)

    with open(QBT_ENV.TRACKERS_FILE, 'w') as file:
        for url in unique_urls:
            file.write(url + '\n')

    print(f"Unique tracker URLs have been written to {QBT_ENV.TRACKERS_FILE}.")

except Exception as e:
    print(f"An error occurred: {e}")
