#!/usr/bin/python3 -u

import sys
from qbt_env import QBT_ENV
from qbt_utils import get_client, get_non_working_trackers, read_trackers

def add_trackers(torrent_hash):
    try:
        client = get_client()
        torrent = client.torrents.info(torrent_hashes=torrent_hash)
        if not torrent:
            print(f"No torrent found for hash: {torrent_hash}")
            return

        torrent_found = torrent[0]

        existing_trackers = {tracker.url for tracker in client.torrents.trackers(torrent_found.hash)}

        trackers = read_trackers(QBT_ENV.TRACKERS_FILE)

        new_trackers = [tracker for tracker in trackers if tracker not in existing_trackers]

        if new_trackers:
            client.torrents.add_trackers(torrent_hash=torrent_found.hash, urls=new_trackers)
            print(f'Added trackers to torrent: {torrent_found.name}')
        else:
            print('No new trackers to add.')

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) == 2:
        torrent_hash = sys.argv[1]
        add_trackers(torrent_hash)
    else:
        print("Usage: qbt-add-trackers-to-torrent.py [<torrent_hash>]")
        sys.exit(1)
