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
OUTPUT_FILE = os.environ['QBT_TRACKERS_FILE']

# Ignored trackers
IGNORED_TRACKER_URLS = {'** [DHT] **', '** [PeX] **', '** [LSD] **'}

try:
    # Initialize qBittorrent client
    client = Client(host=HOST, username=USER, password=PASS)

    # Test connection
    client.auth_log_in()
    print("Successfully connected to qBittorrent Web UI.")

    tracker_urls = set()

    # Process torrents
    for torrent in client.torrents.info(private=False):
        # Fetch trackers for the current torrent
        trackers = client.torrents.trackers(torrent.hash)
        for tracker in trackers:
            if tracker.url not in IGNORED_TRACKER_URLS and tracker.status == 2:
                tracker_urls.add(tracker.url)

    # Write tracker URLs to the output file
    with open(OUTPUT_FILE, 'w') as file:
        for url in tracker_urls:
            file.write(url + '\n')

    print(f"Tracker URLs have been written to {OUTPUT_FILE}.")

except APIConnectionError as e:
    print(f"Failed to connect to qBittorrent: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
