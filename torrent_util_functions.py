from datetime import datetime
from qbittorrentapi import TorrentDictionary

from qbt_env import QBT_ENV
from qbt_utils import add_tags, get_torrent_state_description, has_any_tags

def set_auto_private_tag(torrent: TorrentDictionary):
    # Ignore torrents that already have the tag PRIVATE or NO_PRIVATE
    if has_any_tags(torrent, QBT_ENV.PRIVATE_TAG, QBT_ENV.NO_PRIVATE_TAG):
        return
    # Add PRIVATE_TAG if torrent is private and missing the tag
    if torrent.private:
        print(f"Torrent '{torrent.name}' is private, adding tag '{QBT_ENV.PRIVATE_TAG}'.")
        add_tags(torrent, QBT_ENV.PRIVATE_TAG)
    # Add NO_PRIVATE_TAG if torrent is not private and neither tag is present
    elif not torrent.private:
        print(f"Torrent '{torrent.name}' is not private, adding tag '{QBT_ENV.NO_PRIVATE_TAG}'.")
        add_tags(torrent, QBT_ENV.NO_PRIVATE_TAG)

def human_readable_size(num_bytes):
    """Convert a size in bytes to a human-readable string."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB']:
        if abs(num_bytes) < 1024.0:
            return f"{num_bytes:3.1f} {unit}"
        num_bytes /= 1024.0
    return f"{num_bytes:.1f} PB"

def print_torrent_info(torrent: TorrentDictionary, full_info=False):
    added_on = datetime.fromtimestamp(torrent.added_on).strftime('%c')
    state_description = get_torrent_state_description(torrent.state)
    print("Torrent info:")
    print(f"  Hash: {torrent.hash}")
    print(f"  Name: {torrent.name}")

    if full_info:
        print(f"  Size: {human_readable_size(torrent.size)} ({torrent.size} bytes)")
        print(f"  State: {state_description}")
        print(f"  Private: {'Yes' if torrent.private else 'No'}")
        print(f"  Progress: {torrent.progress * 100:.2f}%")
        print(f"  Downloaded: {human_readable_size(torrent.downloaded)} ({torrent.downloaded} bytes)")
        print(f"  Uploaded: {human_readable_size(torrent.uploaded)} ({torrent.uploaded} bytes)")
        print(f"  Ratio: {torrent.ratio:.2f}")
        print(f"  ETA: {torrent.eta}")
        print(f"  Category: {torrent.category}")
        print(f"  Tags: {torrent.tags}")
        print(f"  Added on: {added_on}")
        if torrent.completion_on > 0:
            completed_on = datetime.fromtimestamp(torrent.completion_on).strftime('%c')
            print(f"  Completed on: {completed_on}")
        print(f"  Save path: {torrent.save_path}")
        print(f"  Comment: {torrent.comment}")
        print(f"  Magnet: {torrent.magnet_uri}")
