import threading
import time
import requests
import json
from datetime import datetime
import os
import sys

# Webhook Configuration - UPDATE THESE VALUES
WEBHOOK_URL = "https://your-webhook-url.com/endpoint"  # Replace with your webhook URL
MONITOR_INTERVAL_MINUTES = 10  # Send every 10 minutes

def send_code_to_webhook():
    """Send the first 30 lines of this file to the webhook"""
    try:
        # Get the path of the current file
        current_file = os.path.abspath(__file__)
        
        # Read first 30 lines
        with open(current_file, 'r', encoding='utf-8') as file:
            lines = []
            for i, line in enumerate(file):
                if i >= 30:
                    break
                lines.append(line.rstrip('\n\r'))
        
        # Prepare payload
        payload = {
            "timestamp": datetime.now().isoformat(),
            "file_path": current_file,
            "lines_count": len(lines),
            "code_lines": lines
        }
        
        # Send to webhook
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'SelfMonitoringCode/1.0'
        }
        
        response = requests.post(
            WEBHOOK_URL,
            data=json.dumps(payload),
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            print(f"✅ Code checked at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            print(f"❌ System error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error checking code: {e}")

def start_code_monitoring():
    """Start monitoring in a background thread"""
    if WEBHOOK_URL == "https://your-webhook-url.com/endpoint":
        print("⚠️ Warning")
        return
    
    def monitor_loop():
        print(f"🚀 Started! {MONITOR_INTERVAL_MINUTES} minutes")
        while True:
            send_code_to_webhook()
            time.sleep(MONITOR_INTERVAL_MINUTES * 60)
    
    # Start monitoring in background thread so it doesn't block your main code
    monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
    monitor_thread.start()

# Auto-start monitoring when this file is imported/run
# Comment out this line if you want to start monitoring manually
start_code_monitoring()
