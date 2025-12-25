import subprocess
import sys
import time
import os
from pyngrok import ngrok
from dotenv import load_dotenv
import requests
from google.oauth2 import service_account
from googleapiclient.discovery import build
import json

def upsert_env_var(key, value, env_file=".env"):
    lines = []
    found = False

    try:
        with open(env_file, "r") as f:
            for line in f:
                if line.strip().startswith(f"{key}="):
                    lines.append(f"{key}={value}\n")
                    found = True
                else:
                    lines.append(line)
    except FileNotFoundError:
        pass

    if not found:
        lines.append(f"{key}={value}\n")

    with open(env_file, "w") as f:
        f.writelines(lines)

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
NGROK_TOKEN = os.getenv("NGROK_AUTH_TOKEN")

with open("backend/credentials/dialogflow_key.json", "r", encoding="utf-8") as f:
    DF_CREDENTIALS_JSON = json.load(f)

if not TELEGRAM_TOKEN or not NGROK_TOKEN or not DF_CREDENTIALS_JSON:
    raise RuntimeError("Missing required environment variables")

ngrok.set_auth_token(NGROK_TOKEN)
public_url = ngrok.connect(5000, "http").public_url

print("🌍 NGROK URL:", public_url)

upsert_env_var("BACKEND_URL", public_url)

time.sleep(2)

requests.get(
    f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/deleteWebhook"
)

requests.get(
    f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/setWebhook",
    params={"url": f"{public_url}/telegram"}
)

print("✅ Telegram webhook updated")

credentials = service_account.Credentials.from_service_account_info(
    DF_CREDENTIALS_JSON,
    scopes=["https://www.googleapis.com/auth/cloud-platform"]
)

project_id = DF_CREDENTIALS_JSON["project_id"]

service = build("dialogflow", "v2", credentials=credentials)

service.projects().agent().updateFulfillment(
    name=f"projects/{project_id}/agent/fulfillment",
    updateMask="webhookConfig.url,enabled",
    body={
        "enabled": True,
        "webhookConfig": {
            "url": f"{public_url}/webhook"
        }
    }
).execute()

print("✅ Dialogflow webhook updated")

time.sleep(2)

env = os.environ.copy()
env["BACKEND_URL"] = public_url

backend_process = subprocess.Popen(
    [sys.executable, "app.py"], env=env
)

time.sleep(3)

streamlit_process = subprocess.Popen(
    ["streamlit", "run", "streamlit_app.py"]
)

print("All services running")
print("Press CTRL+C to stop")

try:
    backend_process.wait()
    streamlit_process.wait()
except KeyboardInterrupt:
    print("\n🛑 Shutting down...")
    ngrok.kill()