#!/usr/bin/python3 -u

from qbt_utils import fix_encoding, get_client
from torrent_util_functions import set_auto_private_tag

try:
    fix_encoding()
    client = get_client()

    # Process torrents
    for torrent in client.torrents.info():
        set_auto_private_tag(torrent)

except Exception as e:
    print(f"An error occurred: {e}")