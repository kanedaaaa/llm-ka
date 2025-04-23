from mistral import prompt 
from translator import translate_text

prompt_text = "Who split atom?"

response = prompt(prompt_text)

translated_response = translate_text(response, "ka")

print(translated_response)