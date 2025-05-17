#!/usr/bin/python3 -u

import sys
from qbt_utils import *
from datetime import datetime

def show_torrent(torrent_hash):
    try:
        client = get_client()

        # Fetch torrent by hash
        torrent = client.torrents.info(torrent_hashes=torrent_hash)
        if not torrent:
            print(f"No torrent found for hash: {torrent_hash}")
            return

        torrent = torrent[0]
        added_on = datetime.fromtimestamp(torrent.added_on).strftime('%Y-%m-%d %H:%M:%S')
        state_description = get_torrent_state_description(torrent.state)

        print("Torrent info:")
        print(f"  Hash: {torrent.hash}")
        print(f"  Name: {torrent.name}")
        print(f"  Size: {torrent.size}")
        print(f"  State: {state_description}")
        print(f"  Progress: {torrent.progress * 100:.2f}%")
        print(f"  Downloaded: {torrent.downloaded}")
        print(f"  Uploaded: {torrent.uploaded}")
        print(f"  Ratio: {torrent.ratio:.2f}")
        print(f"  ETA: {torrent.eta}")
        print(f"  Category: {torrent.category}")
        print(f"  Tags: {torrent.tags}")

        print(f"  Added on: {added_on}")
        if torrent.completion_on > 0:
            completed_on = datetime.fromtimestamp(torrent.completion_on).strftime('%Y-%m-%d %H:%M:%S')
            print(f"  Completed on: {completed_on}")
        print(f"  Save path: {torrent.save_path}")
        print(f"  Comment: {torrent.comment}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: qbt-show-torrent.py <torrent_hash>")
        sys.exit(1)

    torrent_hash = sys.argv[1]
    show_torrent(torrent_hash)
