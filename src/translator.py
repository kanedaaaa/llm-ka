from google.cloud import translate_v2 as translate
from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file(
    "gcloud_auth.json"
)

def translate_text(text: str, target: str):
    allowed_languages = ["ka", "en"]
    
    if target not in allowed_languages:
        raise ValueError(f"Invalid target language: '{target}'. Must be one of {allowed_languages}")

    translate_client = translate.Client(credentials=credentials)

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=target)

    print(result["translatedText"])
