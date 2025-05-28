from qbittorrentapi import TorrentDictionary

from qbt_env import QBT_ENV
from qbt_utils import add_tags, has_any_tags

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