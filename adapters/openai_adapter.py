import openai
from typing import Optional
from config import config
from dataclasses import dataclass
from rich import print

@dataclass
class OpenAIAdapter:
    model: str = config.OPENAI_MODEL
    temperature: float = config.TEMPERATURE
    max_tokens: int = config.MAX_TOKENS

    def __post_init__(self):
        if not config.OPENAI_API_KEY:
            raise ValueError("OpenAI API key not configured")

    def query(self, prompt: str) -> str:
        """Send query to OpenAI with error handling"""
        try:
            response = openai.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                base_url=config.API_BASE
            )
            return response.choices[0].message.content.strip()

        except openai.AuthenticationError:
            print("[red]Error: Invalid OpenAI API key[/red]")
            raise
        except openai.RateLimitError:
            print("[red]Error: Rate limit exceeded[/red]")
            raise
        except Exception as e:
            print(f"[red]OpenAI Error: {str(e)}[/red]")
            raise
