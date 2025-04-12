#!/usr/bin/python3 -u

from qbittorrentapi import TorrentState
from qbt_utils import *

try:
    client = get_client()

    torrents_to_edit = []

    # Process torrents that are not private and completed or stopped torrents
    torrents = client.torrents.info(private=False, tag=NO_PRIVATE_TAG)
    for torrent in torrents:
        if torrent.state_enum == TorrentState.STOPPED_UPLOAD:
            continue

        # Fetch non-working trackers for the current torrent
        non_working_trackers = get_non_working_trackers(client, torrent.hash)

        if non_working_trackers:
            torrents_to_edit.append((torrent, non_working_trackers))

    if torrents_to_edit:
        print("The following torrents have non-working trackers:")
        for torrent, non_working_trackers in torrents_to_edit:
            print(f'Torrent "{torrent.name}" has non-working trackers:')
            for tracker_url in non_working_trackers:
                print(f'  - {tracker_url}')
            try:
                print(f'Removing non-working trackers from torrent "{torrent.name}".')
                client.torrents.removeTrackers(torrent.hash, non_working_trackers)
            except Exception as e:
                print(f'Failed to remove trackers from torrent "{torrent.name}": {e}')

except Exception as e:
    print(f"An error occurred: {e}")
