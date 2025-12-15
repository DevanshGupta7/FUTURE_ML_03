from transformers import pipeline

chatbot = None

def hf_reply(text):
    global chatbot
    if chatbot is None:
        chatbot = pipeline(
            "text2text-generation",
            model="facebook/blenderbot-400M-distill"
        )

    result = chatbot(
        text,
        max_length=120,
        truncatipn=True
    )

    return result[0]["generated_text"]