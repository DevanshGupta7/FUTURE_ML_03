from backend.dialogflow import detect_intent
from backend.logic import track_order, refund_order
from backend.chatbot import groq_reply

def handle_user_message(user_text):
    df_result = detect_intent(user_text)

    if df_result.fulfillment_text:
        return df_result.fulfillment_text

    action = df_result.action
    params = df_result.parameters or {}

    if action == "track.order.complete":
        return track_order(params.get("order_id"))

    if action == "refund.order.start":
        return refund_order(params.get("order_id"))
    
    if action == "fallback.huggingface":
        return groq_reply(user_text)

    return groq_reply(user_text)