from flask import Flask, request, jsonify
from hf_chatbot import hf_reply
from logic import track_order
import os
import requests

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN is not set")

TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

@app.route("/telegram", methods=["POST"])
def telegram_webhook():
    print("Telegram webhook starts to run")
    data = request.get_json()
    print(f"Telegram chat data: {data}")

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        user_text = data["message"].get("text", "")

        reply = hf_reply(user_text)
        print(f"Reply form hf_reply: {reply}")

        requests.post(
            f"{TELEGRAM_API}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": reply
            }
        )

    return "OK", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    print("Starting webhook")
    data = request.get_json()
    print(f"Data from dialogflow: {data}")
    query_result = data.get("queryResult", {})
    action = query_result.get("action", "")
    params = query_result.get("parameters", {})
    user_text = query_result.get("queryText", "")

    print(f"Action: {action}")

    if action == "track.order.complete":
        reply = track_order(params.get("order_id"))

    elif action == "fallback.huggingface":
        reply = hf_reply(user_text)

    else:
        reply = "How else can I help you?"

    return jsonify({"fulfillmentText": reply})

@app.route("/health")
def health():
    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)