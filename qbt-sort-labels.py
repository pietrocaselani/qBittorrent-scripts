#!/usr/bin/python3 -u

from qbt_utils import *

try:
    client = get_client()

    # Process torrents
    for torrent in client.torrents.info():
        # Retrieve and sort tags alphabetically (case-insensitive)
        sorted_tags = sorted(torrent.tags.split(','), key=lambda tag: tag.lower())

        # Update the torrent's tags with the sorted list
        sorted_tags_str = ','.join(sorted_tags)
        client.torrents_add_tags(torrent.hash, sorted_tags_str)
        print(f"Sorted tags for torrent '{torrent.name}': {sorted_tags_str}")

except Exception as e:
    print(f"An error occurred: {e}")