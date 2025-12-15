# from transformers import pipeline

# chatbot = pipeline(
#     "text2text-generation",
#     model="facebook/blenderbot-400M-distill"
# )

# def hf_reply(text):
#     response = chatbot(text, max_length=120, truncation=True)
#     return response[0]["generated_text"]

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.2"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    device_map="auto",
    dtype=torch.float16
)

def hf_reply(user_text: str) -> str:
    prompt = f"""You are a helpful customer support assistant.
User: {user_text}
Assistant:"""

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    outputs = model.generate(
        **inputs,
        max_new_tokens=150,
        do_sample=True,
        temperature=0.7,
        top_p=0.9
    )

    return tokenizer.decode(outputs[0], skip_special_tokens=True)
