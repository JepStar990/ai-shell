import google.generativeai as genai
from config import config

class GeminiAdapter:
    def __init__(self, model="gemini-pro", temperature=0.3):
        genai.configure(api_key=config.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel(model)
        self.temperature = temperature

    def query(self, prompt: str) -> str:
        response = self.model.generate_content(prompt)
        return response.text
