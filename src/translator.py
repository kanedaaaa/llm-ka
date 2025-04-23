from google.cloud import translate_v2 as translate
from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file(
    "gcloud_auth.json"
)

translate_client = translate.Client(credentials=credentials)

def translate_to_english(text: str) -> str:
    return _translate_text(text, target="en")

def translate_to_georgian(text: str) -> str:
    return _translate_text(text, target="ka")

def _translate_text(text: str, target: str) -> str:
    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=target)
    return result["translatedText"]
