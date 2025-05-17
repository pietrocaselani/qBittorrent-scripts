#!/usr/bin/python3 -u

from qbt_utils import *

try:
    fix_encoding()
    client = get_client()

    # Process torrents
    for torrent in client.torrents.info():
        # Ignore completed and stopped torrents
        if is_torrent_completed(torrent) or torrent.state_enum.is_stopped or torrent.state_enum.is_checking:
            # Remove the "no-trackers" tag if it's present
            if has_all_tags(torrent, NO_TRACKER_TAG):
                print(f'Clearing "{NO_TRACKER_TAG}" tag from "{torrent.name}" (torrent is completed and stopped or checking)')
                remove_tag(torrent, NO_TRACKER_TAG)
            continue

        # Fetch trackers for the current torrent
        trackers = client.torrents.trackers(torrent.hash)
        all_trackers_non_working = True  # Assume all trackers are non-working initially

        for tracker in trackers:
            # Ignore special trackers (DHT, PeX, LSD)
            if tracker.url in IGNORED_TRACKER_URLS:
                continue

            # Check if the tracker is working (status 2)
            if is_tracker_working(tracker) or is_tracker_updating(tracker):
                all_trackers_non_working = False  # At least one tracker is working
                break  # No need to check further

        if all_trackers_non_working:
            # Add the "no-trackers" tag if it's not already present
            if not has_all_tags(torrent, NO_TRACKER_TAG):
                print(f'Tagging "{torrent.name}" with "{NO_TRACKER_TAG}" (all trackers non-working)')
                add_tag(torrent, NO_TRACKER_TAG)
        else:
            # Remove the "no-trackers" tag if it's present
            if has_all_tags(torrent, NO_TRACKER_TAG):
                print(f'Clearing "{NO_TRACKER_TAG}" tag from "{torrent.name}" (working trackers found)')
                remove_tag(torrent, NO_TRACKER_TAG)

except Exception as e:
    print(f"An error occurred: {e}")