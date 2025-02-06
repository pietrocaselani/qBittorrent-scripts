#!/usr/bin/python3 -u

import os
from qbittorrentapi import Client, APIConnectionError
from dotenv import load_dotenv

load_dotenv()

# Fetch environment variables
DEBUG = os.environ['DEBUG'].lower() == 'true'
NO_TRACKER_TAG = os.environ['QBT_NO_TRACKER_TAG']
HOST = os.environ['QBT_HOST']
USER = os.environ['QBT_USER']
PASS = os.environ['QBT_PASS']

"""
Possible values of torrent state:
Value               Description
error               Some error occurred, applies to paused torrents
missingFiles        Torrent data files are missing
uploading           Torrent is being seeded and data is being transferred
pausedUP/stoppedUP  Torrent is paused and has finished downloading
queuedUP            Queuing is enabled and torrent is queued for upload
stalledUP           Torrent is being seeded, but no connections were made
checkingUP          Torrent has finished downloading and is being checked
forcedUP            Torrent is forced to upload and ignore queue limit
allocating          Torrent is allocating disk space for download
downloading         Torrent is being downloaded and data is being transferred
metaDL              Torrent has just started downloading and is fetching metadata
pausedDL            Torrent is paused and has NOT finished downloading
queuedDL            Queuing is enabled and torrent is queued for download
stalledDL           Torrent is being downloaded, but no connections were made
checkingDL          Same as checkingUP, but torrent has NOT finished downloading
forcedDL            Torrent is forced to download to ignore queue limit
checkingResumeData  Checking resume data on qBt startup
moving              Torrent is moving to another location

Possible values of tracker status:
Value Description
0     Tracker is disabled (used for DHT, PeX, and LSD)
1     Tracker has not been contacted yet
2     Tracker has been contacted and is working
3     Tracker is updating
4     Tracker has been contacted, but it is not working (or doesn't send proper replies)
"""

# Ignored trackers
IGNORED_TRACKER_URLS = {'** [DHT] **', '** [PeX] **', '** [LSD] **'}

try:
    # Initialize qBittorrent client
    client = Client(host=HOST, username=USER, password=PASS)

    # Test connection
    client.auth_log_in()
    print("Successfully connected to qBittorrent Web UI.")

    # Process torrents
    for torrent in client.torrents.info():
        # Ignore completed and stopped torrents
        if torrent.state in ['pausedUP', 'stoppedUP', 'pausedDL', 'stoppedDL']:
            # Remove the "no-trackers" tag if it's present
            if NO_TRACKER_TAG in torrent.tags.split(', '):
                print(f'Clearing "{NO_TRACKER_TAG}" tag from "{torrent.name}" (torrent is completed and stopped)')
                torrent.removeTags(NO_TRACKER_TAG)
            continue

        # Fetch trackers for the current torrent
        trackers = client.torrents.trackers(torrent.hash)
        all_trackers_non_working = True  # Assume all trackers are non-working initially

        for tracker in trackers:
            # Ignore special trackers (DHT, PeX, LSD)
            if tracker.url in IGNORED_TRACKER_URLS:
                continue

            # Check if the tracker is working (status 2)
            if tracker.status == 2:
                all_trackers_non_working = False  # At least one tracker is working
                break  # No need to check further

        torrent_tags = torrent.tags.split(', ')
        if all_trackers_non_working:
            # Add the "no-trackers" tag if it's not already present
            if NO_TRACKER_TAG not in torrent_tags:
                print(f'Tagging "{torrent.name}" with "{NO_TRACKER_TAG}" (all trackers non-working)')
                torrent.addTags(NO_TRACKER_TAG)
        else:
            # Remove the "no-trackers" tag if it's present
            if NO_TRACKER_TAG in torrent_tags:
                print(f'Clearing "{NO_TRACKER_TAG}" tag from "{torrent.name}" (working trackers found)')
                torrent.removeTags(NO_TRACKER_TAG)

except APIConnectionError as e:
    print(f"Failed to connect to qBittorrent: {e}")
except Exception as e:
    print(f"An error occurred: {e}")