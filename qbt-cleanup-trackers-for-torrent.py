#!/usr/bin/python3 -u

import sys
from qbt_utils import *

def delete_non_working_trackers(torrent_hash):
    try:
        client = get_client()

        # Fetch torrent by hash
        torrent = client.torrents.info(torrent_hashes=torrent_hash)
        if not torrent:
            print(f"No torrent found for hash: {torrent_hash}")
            return

        torrent = torrent[0]
        print(f"Torrent name: {torrent.name}")

        # Fetch non-working trackers for the torrent
        non_working_trackers = get_non_working_trackers(client, torrent.hash)

        if not non_working_trackers:
            print("No non-working trackers found.")
            return

        print(f"The following {len(non_working_trackers)} non-working trackers will be deleted:")
        for tracker_url in non_working_trackers:
            print(f"  - {tracker_url}")

        confirm = input("Do you want to proceed with deleting these trackers? (yes/no): ")
        if confirm.lower() == 'yes':
            client.torrents.removeTrackers(torrent.hash, non_working_trackers)
            print("Non-working trackers deleted.")
        else:
            print("Action canceled.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: qbt-cleanup-trackers-for-torrent.py <torrent_hash>")
        sys.exit(1)

    torrent_hash = sys.argv[1]
    delete_non_working_trackers(torrent_hash)
