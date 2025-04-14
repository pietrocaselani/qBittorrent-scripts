#!/usr/bin/python3 -u

import argparse
from qbt_utils import *

def main():
    parser = argparse.ArgumentParser(description="List torrents and their automatic management status.")
    parser.add_argument("--category", type=str, help="Filter torrents by category name")
    parser.add_argument("--auto-tmm-off", action="store_true", help="Show only torrents with automatic management off")  # New argument
    args = parser.parse_args()

    try:
        client = get_client()

        # Fetch torrents, optionally filtered by category
        if args.category:
            torrents = client.torrents.info(category=args.category, sort="name")
        else:
            torrents = client.torrents.info(sort="name")

        # Filter torrents with auto_tmm off if the argument is provided
        if args.auto_tmm_off:
            torrents = [torrent for torrent in torrents if not torrent.auto_tmm]

        # Print the name and automatic management status of each torrent
        for torrent in torrents:
            management_status = "on" if torrent.auto_tmm else "off"
            print(f"Torrent '{torrent.name}' has automatic management {management_status}.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()