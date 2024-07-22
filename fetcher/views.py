
# scheduler_app/scheduler.py
import schedule
import time
from fetcher.utils import fetch_and_store_data


# Schedule the job to run every minute
schedule.every(15).minute.do(fetch_and_store_data)

# Run the scheduler in a loop
while True:
    schedule.run_pending()
    time.sleep(1)  # Sleep for 1 second between checks