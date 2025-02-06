#!/usr/bin/python3 -u

import os
from qbittorrentapi import Client, APIConnectionError
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Fetch environment variables
DEBUG = os.environ['DEBUG'].lower() == 'true'
NO_PRIVATE_TAG = os.environ['QBT_NO_PRIVATE_TAG']
PRIVATE_TAG = os.environ['QBT_PRIVATE_TAG']
HOST = os.environ['QBT_HOST']
USER = os.environ['QBT_USER']
PASS = os.environ['QBT_PASS']

try:
    # Initialize qBittorrent client
    client = Client(host=HOST, username=USER, password=PASS)

    # Test connection
    client.auth_log_in()
    print("Successfully connected to qBittorrent Web UI.")

    # Process torrents
    for torrent in client.torrents.info():
        # Add PRIVATE_TAG if torrent is private and missing the tag
        if torrent.private and PRIVATE_TAG not in torrent.tags.split(', '):
            print(f"Torrent '{torrent.name}' is private, adding tag '{PRIVATE_TAG}'.")
            torrent.addTags(PRIVATE_TAG)
        # Add NO_PRIVATE_TAG if torrent is not private and missing the tag
        elif not torrent.private and NO_PRIVATE_TAG not in torrent.tags.split(', '):
            print(f"Torrent '{torrent.name}' is not private, adding tag '{NO_PRIVATE_TAG}'.")
            torrent.addTags(NO_PRIVATE_TAG)

except APIConnectionError as e:
    print(f"Failed to connect to qBittorrent: {e}")
except Exception as e:
    print(f"An error occurred: {e}")