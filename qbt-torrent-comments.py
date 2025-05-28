#!/usr/bin/python3 -u

import sys
from qbt_utils import fix_encoding, get_client

try:
    fix_encoding()
    client = get_client()

    for torrent in client.torrents.info():
        if torrent.comment and torrent.comment.strip():
            print(f"Torrent '{torrent.name}' has a comment: {torrent.comment}")
except Exception as e:
    print(f"An error occurred: {e}")