#!/usr/bin/python3 -u

from qbt_utils import fix_encoding, get_client

try:
    fix_encoding()
    client = get_client()

    # Process torrents
    for torrent in client.torrents.info():
        # Retrieve and sort tags alphabetically (case-insensitive)
        original_tags = [tag.strip() for tag in torrent.tags.split(',')]
        sorted_tags = sorted(original_tags, key=lambda tag: tag.lower())

        # Only update if the tags are not already sorted
        if original_tags != sorted_tags:
            sorted_tags_str = ','.join(sorted_tags)
            client.torrents_add_tags(torrent.hash, sorted_tags_str)
            print(f"Sorted tags for torrent '{torrent.name}': {sorted_tags_str}")

except Exception as e:
    print(f"An error occurred: {e}")