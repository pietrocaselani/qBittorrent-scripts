#!/usr/bin/python3 -u

import os
from qbittorrentapi import Client, APIConnectionError
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Fetch environment variables
DEBUG = os.environ['DEBUG'].lower() == 'true'
HOST = os.environ['QBT_HOST']
USER = os.environ['QBT_USER']
PASS = os.environ['QBT_PASS']

# Ignored trackers
IGNORED_TRACKER_URLS = {'** [DHT] **', '** [PeX] **', '** [LSD] **'}

"""
Possible values of tracker status:
Value Description
0     Tracker is disabled (used for DHT, PeX, and LSD)
1     Tracker has not been contacted yet
2     Tracker has been contacted and is working
3     Tracker is updating
4     Tracker has been contacted, but it is not working (or doesn't send proper replies)
"""

try:
    # Initialize qBittorrent client
    client = Client(host=HOST, username=USER, password=PASS)

    # Test connection
    client.auth_log_in()
    print("Successfully connected to qBittorrent Web UI.")

    torrents_to_edit = []

    # Process torrents that are not private and completed or stopped torrents
    torrents = client.torrents.info(status_filter='active', private=False)
    if not torrents:
        print("No torrents to process")
    else:
        print(f"Processing {len(torrents)} torrents...")

        for torrent in torrents:
            # Fetch trackers for the current torrent
            trackers = client.torrents.trackers(torrent.hash)
            non_working_trackers = [tracker.url for tracker in trackers if tracker.status == 4 and tracker.url not in IGNORED_TRACKER_URLS]

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

except APIConnectionError as e:
    print(f"Failed to connect to qBittorrent: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
