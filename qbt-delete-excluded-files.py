#!/usr/bin/python3 -u

from qbt_utils import fix_encoding, get_client, is_torrent_really_private
import fnmatch
import os

def get_excluded_patterns(client):
    excluded_patterns_str = client.app_preferences().excluded_file_names
    return [pattern.strip() for pattern in excluded_patterns_str.split('\n') if pattern.strip()]

def get_ignored_hashes():
    return []

def collect_files_to_exclude(client, excluded_glob_patterns, ignored_hashes):
    files_to_exclude = {}

    for torrent in client.torrents.info():
        if is_torrent_really_private(torrent) or torrent.hash in ignored_hashes:
            continue

        for file in torrent.files:
            file_path = file.name
            if any(fnmatch.fnmatch(file_path, pattern) for pattern in excluded_glob_patterns) and file.priority != 0:
                if torrent.hash not in files_to_exclude:
                    files_to_exclude[torrent.hash] = {
                        'torrent': torrent,
                        'indices': [],
                        'files': []
                    }
                files_to_exclude[torrent.hash]['indices'].append(str(file.index))
                files_to_exclude[torrent.hash]['files'].append(file)

    return files_to_exclude

def remove_files_and_priority(client, files_to_exclude):
    for torrent_hash, data in files_to_exclude.items():
        torrent = data['torrent']
        indices_str = '|'.join(data['indices'])
        file_names = ', '.join([file.name for file in data['files']])
        print(f"Excluding files: {file_names} from torrent: {torrent.name}")
        client.torrents.file_priority(torrent_hash, indices_str, 0)

        for file in data['files']:
            abs_file_path = os.path.join(torrent.save_path, file.name)
            if os.path.exists(abs_file_path):
                try:
                    os.remove(abs_file_path)
                    print(f"Deleted file from disk: {abs_file_path}")
                except Exception as e:
                    print(f"Failed to delete {abs_file_path}: {e}")
            else:
                print(f"File not found on disk, skipping delete: {abs_file_path}")

def main():
    fix_encoding()
    client = get_client()
    excluded_glob_patterns = get_excluded_patterns(client)

    if not excluded_glob_patterns:
        print("No excluded file patterns found.")
        return

    ignored_hashes = get_ignored_hashes()
    files_to_exclude = collect_files_to_exclude(client, excluded_glob_patterns, ignored_hashes)

    if not files_to_exclude:
        print("No files to exclude based on the current patterns.")
        return

    remove_files_and_priority(client, files_to_exclude)

if __name__ == "__main__":
    main()
