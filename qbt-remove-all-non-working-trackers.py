#!/usr/bin/python3 -u

from datetime import datetime
from qbittorrentapi import TorrentState

from cache_scripts_info import cache_script_info, last_run
from qbt_utils import NO_PRIVATE_TAG, get_client, get_non_working_trackers


def should_process_torrent(torrent, last_run_time):
    """Return True if the torrent should be processed based on last_run_time and state."""
    added_on = datetime.fromtimestamp(torrent.added_on)
    if last_run_time and added_on < last_run_time:
        return False
    if torrent.state_enum == TorrentState.STOPPED_UPLOAD:
        return False
    return True


def process_torrents(client, last_run_time):
    """Find and process torrents with non-working trackers."""
    torrents_to_edit = []
    torrents = client.torrents.info(private=False, tag=NO_PRIVATE_TAG)
    for torrent in torrents:
        if not should_process_torrent(torrent, last_run_time):
            continue
        non_working_trackers = get_non_working_trackers(client, torrent.hash)
        if non_working_trackers:
            torrents_to_edit.append((torrent, non_working_trackers))
    return torrents_to_edit


def remove_non_working_trackers(client, torrents_to_edit):
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
    else:
        print("No torrents with non-working trackers found.")


def main():
    try:
        client = get_client()
        last_run_time = last_run("remove_all_non_working_trackers")
        torrents_to_edit = process_torrents(client, last_run_time)
        remove_non_working_trackers(client, torrents_to_edit)
        cache_script_info("remove_all_non_working_trackers")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
