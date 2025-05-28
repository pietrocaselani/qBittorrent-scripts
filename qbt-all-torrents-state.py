#!/usr/bin/python3 -u

from qbt_utils import get_client, fix_encoding

def all_torrents_state():
    try:
        fix_encoding()
        client = get_client()

        torrents = client.torrents.info()
        if not torrents:
            print("No torrents found")
            return

        for torrent in torrents:
            print(f"  Name: {torrent.name} state: {torrent.state}".encode('utf-8', errors='ignore').decode('utf-8'))
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    all_torrents_state()
