
# Collecting Okta Event Logs for Log Aggregation Tools

This Python script pulls Okta event logs into a structured format suitable for log aggregation tools such as **Sumo Logic, Splunk, and ELK Stack**. The script can be scheduled using a **cron job** or any task scheduler.  

## Features

- **Efficient log retrieval** → Fetches Okta logs and stores them in a structured format.
- **Continuously fetches logs** → Calls the API repeatedly until all new logs are collected.
- **Resumes from the last processed event** → Saves the last timestamp in `startTime.properties` and resumes fetching from that point.
- **Prevents duplicate runs** → Uses **file locking** to ensure only one instance runs at a time.
- **Logs output in a structured format** → Writes logs to `output-YYYY-MM-DD.log` for easy ingestion by monitoring tools.

## Prerequisites

  Before running the script, ensure you have the following:

- **Python 3.x** installed  
    Check by running:

    ```bash
    python3 --version
    ```

## Required Libraries

The script requires:

- `configparser` (built-in with Python 3)
- `urllib.request` (built-in with Python 3)
- `fcntl` (for Linux/macOS file locking, built-in)
- `json` (built-in)
- `re` (built-in)

  **Optional:** If you are running this on **Windows**, you need to replace `fcntl` with an alternative (e.g., `msvcrt`).

## Setup Instructions

  1. **Clone this repository** (or download the script):

     ```bash
     git clone https://github.com/cxnexo/Collecting-Okta-Event-Logs.git
     cd okta-event-logs
     ```

  2. **Edit `config.properties`**  
     Open the `config.properties` file and add your **Okta organization ID** and **API token**:

     ```ini
     [Config]
     # Okta organization ID (e.g., my-org)
     org=<your-org-id>

     # Okta API token for authentication
     token=<your-api-token>

     # Number of records per API call (max 1000)
     restRecordLimit=1000
     ```

  3. **(Optional) Edit `startTime.properties`**  
     The script automatically generates `startTime.properties` to track the last fetched event.  
     If you want to **manually specify a start time**, add a timestamp in **ISO 8601 format**:

     ```ini
     2025-02-26T14:30:45Z
     ```

## Running the Script

To manually run the script, execute:

  ```bash
  python3 okta_events.py
```

Automating with a Cron Job
To run the script every 5 minutes, add this to your crontab:

  ```bash
*/5 * * * * /usr/bin/python3 /path/to/okta_events.py
```

## Log Output

The script generates log files in the following format:
output-YYYY-MM-DD.log

Each log entry is structured JSON and includes a published timestamp.

Example log output:

```css
output-YYYY-MM-DD.log
```

Each log entry is structured JSON and includes a published timestamp.

Example log output:
Published Time: 2025-02-26T14:30:45Z

  ```css
{
    "eventType": "user.session.start",
    "actor": { "id": "00u123abc", "type": "User", "displayName": "John Doe" },
    "client": { "ipAddress": "192.168.1.1" },
    "published": "2025-02-26T14:30:45Z"
}
```

## Troubleshooting

1. Script does not run or shows a locking error
If you see:

```css
Script is already running. Exiting.
```

This means another instance is already running. If no process is active, remove the lock manually:

```bash
rm lock
```

2. Invalid config.properties values
 If you get an error like:

 ```css
 CONFIG ERROR: 'org' is missing or not set in config.properties
```

Double-check that config.properties is correctly filled in.

3. API Errors
If the script fails to fetch logs due to an invalid API token:

Ensure your Okta API token is correct and has permissions.
Try generating a new token in Okta.

## License

This project is open-source and available under the [MIT](https://choosealicense.com/licenses/mit/) License.## Resources

- [Okta API Documentation](https://developer.okta.com/docs/reference/api/event-hooks/)
- [Python 3 `configparser` Module](https://docs.python.org/3/library/configparser.html)
- [Cron Job Guide](https://crontab.guru/)
- [Systemd Guide](https://www.freedesktop.org/wiki/Software/systemd/)
