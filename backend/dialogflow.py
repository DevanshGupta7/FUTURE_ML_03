from google.cloud import dialogflow_v2
import os

PROJECT_ID = os.getenv("DIALOGFLOW_PROJECT_ID")
SESSION_ID = os.getenv("SESSION_ID")
LANGUAGE_CODE = "en"

def detect_intent(text):
    session_client = dialogflow_v2.SessionsClient()
    session = session_client.session_path(PROJECT_ID, SESSION_ID)

    text_input = dialogflow_v2.TextInput(text=text, language_code=LANGUAGE_CODE)
    query_input = dialogflow_v2.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    return response.query_result