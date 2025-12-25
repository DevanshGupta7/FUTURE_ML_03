import json
from google.cloud import dialogflow_v2
from google.oauth2 import service_account

with open("backend/credentials/dialogflow_key.json", "r", encoding="utf-8") as f:
    credentials_info = json.load(f)

def detect_intent(text, session_id="telegram-user"):
    try:
        credentials = service_account.Credentials.from_service_account_info(
            credentials_info
        )

        session_client = dialogflow_v2.SessionsClient(
            credentials=credentials
        )

        project_id = credentials_info["project_id"]

        session = session_client.session_path(project_id, session_id)

        print(f"text in dialogflow.py: {text}")

        text_input = dialogflow_v2.TextInput(
            text=text,
            language_code="en"
        )

        print(f"text_input: {text_input}")

        query_input = dialogflow_v2.QueryInput(text=text_input)

        print(f"query_input: {query_input}")

        response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )

        print(f"response from dialogflow.py: {response}")

        return response.query_result

    except Exception as e:
        print(f"There is an error in dialogflow.py: {e}")
        return "Error" 