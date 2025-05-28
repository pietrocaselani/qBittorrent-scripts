#!/usr/bin/python3 -u

import sys

from qbittorrentapi import TorrentDictionary
from qbt_utils import get_client, get_torrent_state_description
from datetime import datetime

import locale
locale.setlocale(locale.LC_TIME, '')

def human_readable_size(num_bytes):
    """Convert a size in bytes to a human-readable string."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB']:
        if abs(num_bytes) < 1024.0:
            return f"{num_bytes:3.1f} {unit}"
        num_bytes /= 1024.0
    return f"{num_bytes:.1f} PB"

def print_torrent_info(torrent: TorrentDictionary, full_info=False):
    added_on = datetime.fromtimestamp(torrent.added_on).strftime('%c')
    state_description = get_torrent_state_description(torrent.state)
    print("Torrent info:")
    print(f"  Hash: {torrent.hash}")
    print(f"  Name: {torrent.name}")

    if full_info:
        print(f"  Size: {human_readable_size(torrent.size)} ({torrent.size} bytes)")
        print(f"  State: {state_description}")
        print(f"  Progress: {torrent.progress * 100:.2f}%")
        print(f"  Downloaded: {human_readable_size(torrent.downloaded)} ({torrent.downloaded} bytes)")
        print(f"  Uploaded: {human_readable_size(torrent.uploaded)} ({torrent.uploaded} bytes)")
        print(f"  Ratio: {torrent.ratio:.2f}")
        print(f"  ETA: {torrent.eta}")
        print(f"  Category: {torrent.category}")
        print(f"  Tags: {torrent.tags}")
        print(f"  Added on: {added_on}")
        if torrent.completion_on > 0:
            completed_on = datetime.fromtimestamp(torrent.completion_on).strftime('%c')
            print(f"  Completed on: {completed_on}")
        print(f"  Save path: {torrent.save_path}")
        print(f"  Comment: {torrent.comment}")

def show_torrent(torrent_hash):
    try:
        client = get_client()

        # Fetch torrent by hash
        torrent = client.torrents.info(torrent_hashes=torrent_hash)
        if not torrent:
            print(f"No torrent found for hash: {torrent_hash}")
            return

        print_torrent_info(torrent[0], full_info=True)
    except Exception as e:
        print(f"An error occurred: {e}")

def show_all_torrents():
    try:
        client = get_client()
        torrents = client.torrents.info()
        if not torrents:
            print("No torrents found.")
            return
        print("All torrents:")
        for torrent in torrents:
            print_torrent_info(torrent)
            print()
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) == 2:
        torrent_hash = sys.argv[1]
        show_torrent(torrent_hash)
    elif len(sys.argv) == 1:
        show_all_torrents()
    else:
        print("Usage: qbt-show-torrent.py [<torrent_hash>]")
        sys.exit(1)
