#!/usr/bin/python3 -u

import sys

from qbt_utils import get_client

import locale

from torrent_util_functions import print_torrent_info
locale.setlocale(locale.LC_TIME, '')

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
