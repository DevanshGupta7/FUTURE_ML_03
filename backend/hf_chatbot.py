from transformers import pipeline

chatbot = pipeline(
    "conversational",
    model="microsoft/DialoGPT-medium"
)

def hf_reply(text):
    response = chatbot(text)
    return response.generated_responses[-1]