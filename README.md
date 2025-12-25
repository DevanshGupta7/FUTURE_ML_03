# FUTURE_ML_03
FUTURE_ML_03 is an AI-powered customer support chatbot designed to automatically handle customer queries related to order tracking, refunds, and returns, similar to real-world e-commerce platforms like Amazon or Flipkart.

The system integrates Dialogflow for intent detection, custom business logic for order handling, and Groq’s hosted LLM for intelligent fallback responses, ensuring accurate and reliable replies even for complex or out-of-scope questions.

The chatbot supports multiple interaction channels, including a Telegram bot and a Streamlit-based web interface, both powered by a single centralized intelligence layer. This architecture guarantees consistent behavior across platforms while keeping the system scalable and maintainable.

To ensure 24/7 automated operation, the project uses webhooks with Dialogflow and the Telegram Bot API, allowing it to respond instantly to user messages without human intervention. For deployment flexibility and cost efficiency, the system avoids loading large models locally and instead relies on Groq’s API, making it suitable for free-tier cloud environments.

Overall, FUTURE_ML_03 demonstrates a production-style chatbot architecture, showcasing skills in AI integration, backend development, cloud deployment, and system design, making it a strong internship-level project with real-world applicability.

***

# 🤖 Customer Support Chatbot (AI-Powered)
An **AI-powered customer support chatbot** that automatically answers customer queries related to **order tracking, refunds, and returns** — similar to platforms like Amazon or Flipkart.

The system is built using **Dialogflow, Telegram Bot API, Groq LLM, Flask, and Streamlit**, and is designed to respond **automatically 24/7 without human intervention**.

## 🚀 Key Features

* 📦 Order Tracking using Order ID
* 💸 Refund & Return Handling with defined business rules
* 🤖 AI-powered fallback responses using Groq LLM
* 💬 Multi-channel support
  * Telegram Bot
  * Web UI (Streamlit)
* 🕒 Responds automatically 24/7
* ⚡ Fast responses without loading large models locally
* 🧠 Single shared intelligence layer across all channels

***

## 🕒 24/7 Automated Response (Requirement Explained)

The chatbot is deployed using Dialogflow and the Telegram Bot API, enabling it to respond to customer queries automatically, 24/7, without any human involvement.

Once deployed:

* Telegram messages are received via webhook
* The backend processes requests instantly
* Responses are sent back automatically
* No manual monitoring or triggering is required

✅ This fully satisfies the “Responds automatically 24/7” requirement.

***

## 🧠 Architecture Overview

The system follows a Channel Adapter Architecture:

* One central intelligence layer
* Multiple channels reuse the same logic
```
User (Telegram / Web UI)
        |
        v
   handle_user_message()
        |
  ---------------------
  |        |         |
Dialogflow  Logic   Groq
(Intent)  (Orders) (Fallback)
```

Why this architecture?

* No duplicated logic
* Consistent responses everywhere
* Easy to extend to new platforms (WhatsApp, Web, Mobile)

***

## 📁 Project Structure

```
FUTURE_ML_03/
│
├── backend/
│   ├── chatbot.py        # Groq LLM integration
│   ├── dialogflow.py     # Dialogflow intent detection
│   ├── handler.py        # Central message handler (core logic)
│   ├── logic.py          # Order tracking & refund rules
│   │
│   ├── data/
│   │   └── Orders_Database.csv
│   │
│   └── credentials/
│       └── dialogflow_key.json
│
├── screenshots/          # Project screenshots (UI & Telegram)
│   ├── Screenshot1.png
│   ├── Screenshot2.png
|   ├── Screenshot3.png
│   └── Screenshot4.png
│
├── app.py                # Flask backend (API + webhooks)
├── streamlit_app.py      # Web UI for chatbot
├── start.py              # Auto-start ngrok, backend & Streamlit
│
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```

***

## 🖼️ Screenshots

Screenshots of the working chatbot are available in the ```screenshots/``` folder.

Included Screenshots

* 📱 Telegram chatbot interaction
* 💬 Streamlit web UI chat interface
* 📦 Order tracking & refund responses

These screenshots demonstrate real-time functionality and end-to-end workflow of the chatbot.

***

## ⚙️ Tech Stack

* Backend: Flask (Python)
* Intent Detection: Dialogflow (Google Cloud)
* LLM Fallback: Groq (LLaMA-3.1)
* Frontend: Streamlit
* Messaging Platform: Telegram Bot API
* Webhook Tunneling: ngrok
* Data Source: CSV (Orders database)

***

## 🧠 Why Groq Instead of Local Models?

Due to memory limitations of free cloud deployments, loading large language models locally is not feasible.

To address this:
* The chatbot integrates Groq’s hosted LLM API
* No heavy models are loaded locally
* Ensures fast, reliable, low-latency responses
* Works smoothly even on free-tier deployments

This approach is realistic and production-oriented.

***

## ▶️ How to Run the Project (Local)

1️⃣ Install dependencies
```
pip install -r requirements.txt
```

2️⃣ Set environment variables (.env)
```
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
NGROK_AUTH_TOKEN=your_ngrok_token
GROQ_API_KEY=your_groq_api_key
```

3️⃣ Start all services
```
python start.py
```

This script:
* Starts ngrok
* Starts Flask backend
* Updates Telegram webhook
* Updates Dialogflow webhook
* Launches Streamlit UI

***

## 🔗 Telegram Webhook Setup (Important)

After every Render or cloud deployment, run:
```
https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook?url=https://your-server-url.com/telegram
```


✅ Successful response
```
{"ok":true,"result":true,"description":"Webhook was set"}
```


❌ Delete webhook (if needed)
```
https://api.telegram.org/bot<YOUR_BOT_TOKEN>/deleteWebhook
```


🧪 Test Telegram bot in browser
```
https://api.telegram.org/bot<BOT_TOKEN>/sendMessage?chat_id=<CHAT_ID>&text=Hello
```

***

## 🖥️ Web UI (Streamlit)

* Chat-style interface
* Real-time responses
* Typing indicator
* Uses ```/chat``` API endpoint
* Same logic as Telegram chatbot

***

## 🧪 Cold Start & Reliability Handling

* No heavy models loaded at startup
* Dialogflow + Groq APIs are invoked only when needed
* Handles cold starts gracefully
* Suitable for free-tier cloud deployments

***

## 📜 License

This project is licensed under the MIT License.

***

## 👨‍💻 Author

Devansh Gupta

AI / ML & Backend Developer

Built as part of an AI & Machine Learning internship project.

***

## ⭐ Final Note

This project demonstrates:
* Real-world chatbot architecture
* Multi-channel AI integration
* Cloud deployment awareness
* Clean backend design

This is not a toy project — it mirrors real customer support systems.












