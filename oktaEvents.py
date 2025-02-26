import json
import datetime
import urllib.request
import re
import configparser
import fcntl
import os

LOCK_FILE = 'lock'

def main():
    """ Main function that locks the script and starts the Okta event retrieval process. """
    lock_fd = open(LOCK_FILE, 'w')

    try:
        # Lock file to prevent multiple executions
        fcntl.lockf(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        print("OKTA Events Script LOCKED", datetime.datetime.now())

        config = configparser.ConfigParser()
        config.read('config.properties')

        org = config.get("Config", "org", fallback="")
        token = config.get("Config", "token", fallback="")
        rest_record_limit = config.get("Config", "restRecordLimit", fallback="1000")

        validate_config(org, token, rest_record_limit)

        runit(org, token, rest_record_limit)

    except ValueError as e:
        print(f"CONFIG ERROR: {e}")
    except IOError:
        print("Script is already running. Exiting.")

    finally:
        lock_fd.close()
        os.remove(LOCK_FILE)  # Remove lock file on exit
        print("OKTA Events Script UNLOCKED", datetime.datetime.now())

def validate_config(org, token, rest_record_limit):
    """ Validates the required config parameters before running the script. """
    if not org or org == "<enter the org id here>":
        raise ValueError("'org' is missing or not set in config.properties")
    if not token or token == "<enter your token here>":
        raise ValueError("'token' is missing or not set in config.properties")
    if not rest_record_limit.isdigit() or int(rest_record_limit) > 1000:
        raise ValueError("'restRecordLimit' must be a number (max 1000)")

def runit(org, token, rest_record_limit):
    """ Calls Okta API and writes event data to a file. """
    json_data = get_data_from_endpoint(org, token, get_start_time(), rest_record_limit)
    write_to_file(json_data, org, token, rest_record_limit)

def get_data_from_endpoint(org, token, start_time, limit):
    """ Retrieves event data from Okta API. """
    if int(limit) > 1000:
        limit = "1000"

    url = f"https://{org}.oktapreview.com/api/v1/events?startDate={start_time}&limit={limit}"
    headers = {"Authorization": f"SSWS {token}"}

    request = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(request) as response:
            return json.load(response)
    except urllib.error.URLError as e:
        print(f"API ERROR: {e}")
        return []

def get_start_time():
    """ Reads last recorded timestamp from startTime.properties or generates a new one. """
    try:
        with open('startTime.properties', 'r', encoding="utf-8") as f:
            timestamp = f.readline().strip()
        if timestamp:
            return timestamp  # Directly return the stored ISO format
    except FileNotFoundError:
        pass

    # If file doesn't exist, generate a new timestamp
    offset_time = get_offset_start_time()
    return offset_time.strftime('%Y-%m-%dT%H:%M:%SZ')

def write_offset_time_to_file(year, month, day, hour, minute, second):
    """ Writes timestamp to startTime.properties in ISO 8601 format. """
    timestamp = f"{year}-{month}-{day}T{hour}:{minute}:{second}Z"
    with open("startTime.properties", 'w', encoding="utf-8") as f:
        f.write(timestamp + "\n")

def get_offset_start_time():
    """ Returns the current time plus a small offset (5 seconds). """
    now = datetime.datetime.now()
    return now + datetime.timedelta(seconds=5)

def write_to_file(json_data, org, token, rest_record_limit):
    """ Writes retrieved event data to a log file. """
    last_written_published_time = ""
    file_name = f"output-{datetime.datetime.now().date()}.log"

    with open(file_name, 'a', encoding="utf-8") as event_log_file:
        for event in json_data:
            last_written_published_time = event['published']
            event_log_file.write(f"Published Time: {last_written_published_time}\n")
            json.dump(event, event_log_file, indent=4)
            event_log_file.write("\n")

    if last_written_published_time:
        match = re.match(r"(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})", last_written_published_time)
        if match:
            write_offset_time_to_file(*match.groups())

# Start script
if __name__ == "__main__":
    main()
