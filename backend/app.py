from flask import Flask, request, jsonify
from hf_chatbot import hf_reply
from logic import track_order

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

if __name__ == "__main__":
    app.run(port=5000)