from http import client
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def groq_reply(text):
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a helpful customer support chatbot for Orders like Amazon, Flipkart. If asked anything outside it just tell 'I’m unable to say, as it goes beyond what is permitted.'. Give proper message"},
            {"role": "user", "content": text}
        ]
    )
    return completion.choices[0].message.content