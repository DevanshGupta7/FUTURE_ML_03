from transformers import pipeline

chatbot = pipeline(
    "text-generation",
    model="microsoft/DialoGPT-medium"
)

def hf_reply(user_text: str) -> str:
    response = chatbot(
        user_text,
        max_new_tokens=120,
        do_sample=True,
        temperature=0.7,
        top_p=0.9,
        truncation=True
    )
    return response[0]["generated_text"]