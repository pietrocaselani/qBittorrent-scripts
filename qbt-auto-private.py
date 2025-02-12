#!/usr/bin/python3 -u

from qbt_utils import *

try:
    client = get_client()

    # Process torrents
    for torrent in client.torrents.info():
        # Ignore torrents that already have the tag PRIVATE or NO_PRIVATE
        if has_any_tags(torrent, PRIVATE_TAG, NO_PRIVATE_TAG):
            continue
        # Add PRIVATE_TAG if torrent is private and missing the tag
        if torrent.private:
            print(f"Torrent '{torrent.name}' is private, adding tag '{PRIVATE_TAG}'.")
            add_tag(torrent, PRIVATE_TAG)
        # Add NO_PRIVATE_TAG if torrent is not private and neither tag is present
        elif not torrent.private:
            print(f"Torrent '{torrent.name}' is not private, adding tag '{NO_PRIVATE_TAG}'.")
            add_tag(torrent, NO_PRIVATE_TAG)

except Exception as e:
    print(f"An error occurred: {e}")