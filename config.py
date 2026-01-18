# config.py
import os
from dataclasses import dataclass
from dotenv import load_dotenv
from enum import Enum

load_dotenv()

class AdapterType(str, Enum):
    DEEPSEEK = "deepseek"
    GEMINI = "gemini"
    OPENAI = "openai"
    CLAUDE = "claude"

@dataclass
class AppConfig:
    # Adapter configuration
    DEFAULT_ADAPTER: AdapterType = AdapterType.DEEPSEEK
    FALLBACK_ADAPTER: AdapterType = AdapterType.GEMINI
    
    # API configurations
    DEEPSEEK_API_BASE: str = "https://api.deepseek.com/v1"
    DEEPSEEK_API_KEY: str = os.getenv("DEEPSEEK_API_KEY")
    GEMINI_API_KEY: str = os.getenv("GOOGLE_API_KEY")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY")
    
    # Model defaults
    DEEPSEEK_MODEL: str = "deepseek-chat"
    GEMINI_MODEL: str = "gemini-pro"
    OPENAI_MODEL: str = "gpt-3.5-turbo"
    CLAUDE_MODEL: str = "claude-3-haiku-20240307"
    
    # Generation parameters
    MAX_TOKENS: int = 2000
    TEMPERATURE: float = 0.3

config = AppConfig()
