#!/usr/bin/python3 -u

from qbt_utils import IGNORED_TRACKER_URLS, TRACKERS_FILE, get_client, is_tracker_working, NO_PRIVATE_TAG
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

    # Process torrents
    for torrent in client.torrents.info(private=False, tag=NO_PRIVATE_TAG):
        # Fetch trackers for the current torrent
        trackers = client.torrents.trackers(torrent.hash)
        for tracker in trackers:
            if tracker.url not in IGNORED_TRACKER_URLS and is_tracker_working(tracker):
                tracker_urls.add(tracker.url)

    # Identify duplicates
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

    # Write only unique (non-duplicate) tracker URLs to the output file
    unique_urls = set()
    for norm, urls in normalized_map.items():
        # Only write the first occurrence of each normalized URL
        unique_urls.add(urls[0])

    with open(TRACKERS_FILE, 'w') as file:
        for url in unique_urls:
            file.write(url + '\n')

    print(f"Unique tracker URLs have been written to {TRACKERS_FILE}.")

except Exception as e:
    print(f"An error occurred: {e}")
