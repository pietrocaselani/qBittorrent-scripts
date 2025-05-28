#!/usr/bin/python3 -u

from qbt_utils import IGNORED_TRACKER_URLS, TRACKERS_FILE, get_client, is_tracker_working, NO_PRIVATE_TAG

try:
    client = get_client()

    tracker_urls = set()

    # Process torrents
    for torrent in client.torrents.info(private=False, tag=NO_PRIVATE_TAG):
        # Fetch trackers for the current torrent
        trackers = client.torrents.trackers(torrent.hash)
        for tracker in trackers:
            if tracker.url not in IGNORED_TRACKER_URLS and is_tracker_working(tracker):
                tracker_urls.add(tracker.url)

    # Write tracker URLs to the output file
    with open(TRACKERS_FILE, 'w') as file:
        for url in tracker_urls:
            file.write(url + '\n')

    print(f"Tracker URLs have been written to {TRACKERS_FILE}.")

except Exception as e:
    print(f"An error occurred: {e}")
