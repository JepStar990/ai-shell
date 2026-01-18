import anthropic
from config import config

class ClaudeAdapter:
    def __init__(self, model="claude-3-haiku-20240307"):
        self.client = anthropic.Anthropic(
            api_key=config.ANTHROPIC_API_KEY
        )
        self.model = model

    def query(self, prompt: str) -> str:
        response = self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
