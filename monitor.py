import time
import requests
from ping3 import ping # type: ignore
from datetime import datetime
from dotenv import load_dotenv # type: ignore
import os

load_dotenv()
slack_webhook_url = os.getenv("https://***REMOVED***/services/T08L30MHSMT/B08NMS0RCUB/dKgUfKPVw2CeidRUroTorkpP")

def send_slack_alert(message):
    payload = {"text": message}
    try:
        response = requests.post(slack_webhook_url, json=payload)
        if response.status_code != 200:
            print(f"Slack error: {response.text}")
    except Exception as e:
        print(f"Failed to send Slack alert: {e}")

def log_status(message):
    with open("status.log", "a") as f:
        f.write(f"{datetime.now()} - {message}\n")

targets = ["8.8.8.8", "1.1.1.1", "192.168.1.19"]  # Google / Cloudflare / Local

while True:
    for target in targets:
        response = ping(target)
        if response:
            msg = f"{target} is UP! Ping: {round(response * 1000, 2)} ms"
        else:
            msg = f"{target} is DOWN!"
            send_slack_alert(f"ALERT: {target} is DOWN!")

        print(msg)
        log_status(msg)

    time.sleep(10)  # Wait before next round
