# Collecting Okta Event Logs for Log Aggregation Tools

  This Python script pulls Okta event logs into a structured format suitable for log aggregation tools such as **Sumo Logic, Splunk, and ELK Stack**. The script can be scheduled using a **cron job** or any task scheduler.  

## ✨ Features

- **Efficient log retrieval** → Fetches Okta logs and stores them in a structured format.
- **Continuously fetches logs** → Calls the API repeatedly until all new logs are collected.
- **Resumes from the last processed event** → Saves the last timestamp in `startTime.properties` and resumes fetching from that point.
- **Prevents duplicate runs** → Uses **file locking** to ensure only one instance runs at a time.
- **Logs output in a structured format** → Writes logs to `output-YYYY-MM-DD.log` for easy ingestion by monitoring tools.

  ---

## 🔧 Prerequisites

  Before running the script, ensure you have the following:

- **Python 3.x** installed  
    Check by running:

    ```bash
    python3 --version
    ```

- **Required Python libraries**:
    Install them using:

    ```bash
    pip install -r requirements.txt
    ```

### 🔹 Required Libraries

  The script requires:

- `configparser` (built-in with Python 3)
- `urllib.request` (built-in with Python 3)
- `fcntl` (for Linux/macOS file locking, built-in)
- `json` (built-in)
- `re` (built-in)

  **Optional:** If you are running this on **Windows**, you need to replace `fcntl` with an alternative (e.g., `msvcrt`).

  ---

## ⚙️ Setup Instructions

  1. **Clone this repository** (or download the script):

     ```bash
     git clone https://github.com/your-repo/okta-event-logs.git
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

  ---

## ▶️ Running the Script

  To manually run the script, execute:

  ```bash
  python3 okta_events.py
