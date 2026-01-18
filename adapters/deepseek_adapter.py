import openai
from typing import Optional
from config import config
from dataclasses import dataclass
from rich import print

@dataclass
class DeepSeekAdapter:
    model: str = config.DEEPSEEK_MODEL
    temperature: float = config.TEMPERATURE
    max_tokens: int = config.MAX_TOKENS

    def query(self, prompt: str) -> str:
        """Send query to DeepSeek API"""
        try:
            client = openai.OpenAI(
                base_url=config.DEEPSEEK_API_BASE,
                api_key=config.DEEPSEEK_API_KEY
            )
            response = client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"[red]API Error: {str(e)}[/red]")
            raise
