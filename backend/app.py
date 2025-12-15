from flask import Flask, request, jsonify
from hf_chatbot import hf_reply
from logic import track_order
import os

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    action = data["queryResult"].get("action")
    params = data["queryResult"].get("parameters")
    user_text = data["queryResult"]["queryText"]

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