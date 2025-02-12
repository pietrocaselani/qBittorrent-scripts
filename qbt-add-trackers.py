#!/usr/bin/python3 -u

from qbt_utils import *

try:
    client = get_client()

    # Read trackers from file
    trackers = read_trackers(TRACKERS_FILE)

    # Process torrents
    for torrent in client.torrents.info(private=False):
        if has_all_tags(torrent, PRIVATE_TAG):
            print(f"Skipping private torrent: {torrent.name}")
            continue

        existing_trackers = {tracker.url for tracker in client.torrents.trackers(torrent.hash)}
        new_trackers = [tracker for tracker in trackers if tracker not in existing_trackers]

        if new_trackers:
            client.torrents.add_trackers(torrent_hash=torrent.hash, urls=new_trackers)
            print(f'Added trackers to torrent: {torrent.name}')

    print('Done.')

except Exception as e:
    print(f"An error occurred: {e}")