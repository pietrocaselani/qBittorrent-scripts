from qbittorrentapi import TorrentDictionary

from qbt_utils import NO_PRIVATE_TAG, PRIVATE_TAG, add_tag, has_any_tags

def set_tag_private(torrent: TorrentDictionary):
    # Ignore torrents that already have the tag PRIVATE or NO_PRIVATE
    if has_any_tags(torrent, PRIVATE_TAG, NO_PRIVATE_TAG):
        return
    # Add PRIVATE_TAG if torrent is private and missing the tag
    if torrent.private:
        print(f"Torrent '{torrent.name}' is private, adding tag '{PRIVATE_TAG}'.")
        add_tag(torrent, PRIVATE_TAG)
    # Add NO_PRIVATE_TAG if torrent is not private and neither tag is present
    elif not torrent.private:
        print(f"Torrent '{torrent.name}' is not private, adding tag '{NO_PRIVATE_TAG}'.")
        add_tag(torrent, NO_PRIVATE_TAG)