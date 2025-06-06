#!/usr/bin/python3 -u

from qbt_utils import NO_PRIVATE_TAG, TRACKERS_FILE, fix_encoding, get_client, read_trackers

try:
    fix_encoding()
    client = get_client()

    trackers = read_trackers(TRACKERS_FILE)

    for torrent in client.torrents.info(private=False, tag=NO_PRIVATE_TAG):
        existing_trackers = {tracker.url for tracker in client.torrents.trackers(torrent.hash)}
        new_trackers = [tracker for tracker in trackers if tracker not in existing_trackers]

        if new_trackers:
            client.torrents.add_trackers(torrent_hash=torrent.hash, urls=new_trackers)
            print(f'Added trackers to torrent: {torrent.name}')

    print('Done.')

except Exception as e:
    print(f"An error occurred: {e}")