import sys
import io
from qbittorrentapi import Client, APIConnectionError
from qbt_env import QBT_ENV

# Ignored trackers
IGNORED_TRACKER_URLS = {'** [DHT] **', '** [PeX] **', '** [LSD] **'}

"""
Keep this information as documentation when working with qBittorrent Web UI:
Possible values of torrent state:
Value               Description
error               Some error occurred, applies to paused torrents
missingFiles        Torrent data files are missing
uploading           Torrent is being seeded and data is being transferred
stoppedUP           Torrent is paused and has finished downloading (Previously: pausedUP)
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

def fix_encoding():
    # Corrige a saída do console para UTF-8
    sys.stdout.reconfigure(encoding='utf-8')

    if sys.stdout.encoding != 'utf-8':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    if sys.stderr.encoding != 'utf-8':
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def get_client():
    try:
        client = Client(host=QBT_ENV.HOST, port=QBT_ENV.PORT, username=QBT_ENV.USER, password=QBT_ENV.PASS)
        client.auth_log_in()
        return client
    except APIConnectionError as e:
        print(f"Failed to connect to qBittorrent: {e}")
        raise
    except Exception as e:
        print(f"An error occurred: {e}")
        raise

def read_trackers(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]

# Utility functions acting like extension methods
def has_all_tags(torrent, *tags):
    if len(tags) == 1 and isinstance(tags[0], (list, tuple)):
        tags = tags[0]
    elif isinstance(tags, str):
        tags = [tag.strip() for tag in tags.split(',')]
    torrent_tags = set(torrent.tags.split(', '))
    return all(tag in torrent_tags for tag in tags)

def has_any_tags(torrent, *tags):
    if len(tags) == 1 and isinstance(tags[0], (list, tuple)):
        tags = tags[0]
    elif isinstance(tags, str):
        tags = [tag.strip() for tag in tags.split(',')]
    torrent_tags = set(torrent.tags.split(', '))
    return any(tag in torrent_tags for tag in tags)

def has_no_tags(torrent, *tags):
    if len(tags) == 1 and isinstance(tags[0], (list, tuple)):
        tags = tags[0]
    elif isinstance(tags, str):
        tags = [tag.strip() for tag in tags.split(',')]
    torrent_tags = set(torrent.tags.split(', '))
    return all(tag not in torrent_tags for tag in tags)

def add_tags(torrent, tags):
    if not has_all_tags(torrent, tags):
        torrent.addTags(tags)

def remove_tags(torrent, tags):
    if has_all_tags(torrent, tags):
        torrent.removeTags(tags)

def get_non_working_trackers(client, torrent_hash):
    trackers = client.torrents.trackers(torrent_hash)
    return [tracker.url for tracker in trackers if is_tracker_non_working(tracker) and tracker.url not in IGNORED_TRACKER_URLS]

def is_torrent_completed(torrent):
    return torrent.state_enum.is_complete

def is_torrent_really_private(torrent):
    return (torrent.private and has_any_tags(torrent, QBT_ENV.PRIVATE_TAG)) or (torrent.private == False and has_any_tags(torrent, QBT_ENV.PRIVATE_TAG))

def all_really_non_private_torrents(client):
    return client.torrents.info(tag=QBT_ENV.NO_PRIVATE_TAG)

def all_really_private_torrents(client):
    return client.torrents.info(tag=QBT_ENV.PRIVATE_TAG)

def is_tracker_working(tracker):
    return tracker.status == 2

def is_tracker_updating(tracker):
    return tracker.status == 3

def is_tracker_non_working(tracker):
    return tracker.status in {1, 3, 4}

def get_torrent_state_description(state):
    state_descriptions = {
        'error': 'Some error occurred, applies to paused torrents (error)',
        'missingFiles': 'Torrent data files are missing (missingFiles)',
        'uploading': 'Torrent is being seeded and data is being transferred (uploading)',
        'stoppedUP': 'Torrent is paused and has finished downloading (stoppedUP)',
        'queuedUP': 'Queuing is enabled and torrent is queued for upload (queuedUP)',
        'stalledUP': 'Torrent is being seeded, but no connections were made (stalledUP)',
        'checkingUP': 'Torrent has finished downloading and is being checked (checkingUP)',
        'forcedUP': 'Torrent is forced to upload and ignore queue limit (forcedUP)',
        'allocating': 'Torrent is allocating disk space for download (allocating)',
        'downloading': 'Torrent is being downloaded and data is being transferred (downloading)',
        'metaDL': 'Torrent has just started downloading and is fetching metadata (metaDL)',
        'pausedDL': 'Torrent is paused and has NOT finished downloading (pausedDL)',
        'queuedDL': 'Queuing is enabled and torrent is queued for download (queuedDL)',
        'stalledDL': 'Torrent is being downloaded, but no connections were made (stalledDL)',
        'checkingDL': 'Same as checkingUP, but torrent has NOT finished downloading (checkingDL)',
        'forcedDL': 'Torrent is forced to download to ignore queue limit (forcedDL)',
        'checkingResumeData': 'Checking resume data on qBt startup (checkingResumeData)',
        'moving': 'Torrent is moving to another location (moving)'
    }
    return state_descriptions.get(state, f'Unknown state {state}')