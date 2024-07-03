import google.generativeai as genai

from Settings import Ai_api


genai.configure(api_key = Ai_api)

generation_config = {
    "temperature" :1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens":8192,
    "response_mime_type": "text/plain",

}


model  = genai.GenerativeModel(
    model_name = "gemini-1.5-flash",
    generation_config = generation_config
)


def generate_data(prompt):
    response = model.start_chat().send_message(prompt)
    return response.text

