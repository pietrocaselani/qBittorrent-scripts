import json
import os
from datetime import datetime

SCRIPTS_INFO_FILE = os.path.join(os.path.dirname(__file__), 'qbt-scripts-info.json')

def cache_script_info(script_key):
    data = {
        script_key: {
            'last_run': datetime.now().isoformat()
        }
    }
    try:
        with open(SCRIPTS_INFO_FILE, 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Failed to write scripts info file: {e}")

def last_run(script_key):
    try:
        with open(SCRIPTS_INFO_FILE, 'r') as f:
            data = json.load(f)
            last_run_str = data.get(script_key, {}).get('last_run', None)
            if last_run_str is not None:
                try:
                    return datetime.fromisoformat(last_run_str)
                except ValueError:
                    print("Error parsing datetime from scripts info file.")
                    return None
            return None
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        print("Error decoding JSON from scripts info file.")
        return None
    except Exception as e:
        print(f"An error occurred while reading scripts info file: {e}")
        return None