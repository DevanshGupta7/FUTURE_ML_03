from flask import Flask, request, jsonify
from backend.dialogflow import detect_intent
from backend.chatbot import groq_reply
from backend.logic import track_order, refund_order
import os
import requests
from dotenv import load_dotenv
from backend.handler import handle_user_message

load_dotenv()

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TELEGRAM_TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN is not set")

TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

@app.route("/telegram", methods=["POST"])
def telegram_webhook():
    try:
        print("Telegram webhook starts to run")
        data = request.get_json()
        print(f"Telegram chat data: {data}")

        if "message" not in data:
            return "OK", 200

        message = data.get("message")
        if not message:
            return "OK", 200

        chat = message.get("chat")
        if not chat:
            return "OK", 200

        chat_id = chat.get("id")
        if not chat_id:
            return "OK", 200

        user_text = message.get("text")
        if not user_text:
            return "OK", 200

        reply = None

        print(f"user_text: {user_text}")

        df_result = detect_intent(user_text)

        intent_name = df_result.intent.display_name
        is_fallback = df_result.intent.is_fallback
        df_reply = df_result.fulfillment_text

        print(f"Detected intent: {intent_name}")
        print(f"Is fallback: {is_fallback}")

        if not is_fallback:
            print(f"df_result: {df_result}")
            if df_result.fulfillment_text:
                print("Running df_result.fulfillment_text")
                reply = df_result.fulfillment_text
            elif df_result.fulfillment_messages:
                print("Running df_result.fulfillment_messages[0].text.text[0]")
                reply = df_result.fulfillment_messages[0].text.text[0]

            print(f"Reply from is_fallback: {reply}")

        if not reply:
            print("Running groq_reply")
            reply = groq_reply(user_text)

        print(f"Reply from chatbot: {reply}")

        requests.post(
            f"{TELEGRAM_API}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": reply
            }
        )

        return "OK", 200

    except Exception as e:
        print(f"Error in app.py telegram_webhook: {e}")
        return "Error", 400
 
@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        print("Starting webhook")
        data = request.get_json()

        print(f"Data from dialogflow: {data}")

        query_result = data.get("queryResult", {})
        action = query_result.get("action", "")
        params = query_result.get("parameters", {})
        user_text = query_result.get("queryText", "")

        print(f"Action: {action}")

        if action == "track.order.complete":
            print("Running track.order.complete")
            print(params.get("order_id"))
            reply = track_order(params.get("order_id"))

        elif action == "refund.order.start":
            print("Running refund.order.start")
            print(params.get("order_id"))
            reply = refund_order(params.get("order_id"))

        elif action == "fallback.huggingface":
            print("Running fallback.huggingface")
            print(user_text)
            reply = groq_reply(user_text)

        else:
            reply = "How else can I help you?"

        print(f"reply from logic.py: {reply}")

        return jsonify({"fulfillmentText": reply})

    except Exception as e:
        print(f"Error in app.py webhook: {e}")
        return "Error", 400

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    print(f"Data: {data}")
    user_text = data.get("text")

    if not user_text:
        return jsonify({"reply": "Please enter a message."})

    reply = handle_user_message(user_text)
    return jsonify({"reply": reply})

@app.route("/health")
def health():
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)