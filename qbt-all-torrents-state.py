#!/usr/bin/python3 -u

import sys
from qbt_utils import *
from datetime import datetime
import io


# Corrige a saída do console para UTF-8
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
if sys.stderr.encoding != 'utf-8':
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def all_torrents_state():
    try:
        client = get_client()

        # Fetch torrent by hash
        torrents = client.torrents.info()
        if not torrents:
            print(f"No torrents found")
            return

        for torrent in torrents:
            print(f"  Name: {torrent.name} state: {torrent.state}".encode('utf-8', errors='ignore').decode('utf-8'))
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    all_torrents_state()
