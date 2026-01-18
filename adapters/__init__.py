'''
from .deepseek_adapter import DeepSeekAdapter
from .gemini_adapter import GeminiAdapter
from .claude_adapter import ClaudeAdapter
from .openai_adapter import OpenAIAdapter
'''

# Make adapters optional
try:
    from .deepseek_adapter import DeepSeekAdapter
except ImportError as e:
    DeepSeekAdapter = None
    print(f"DeepSeek adapter not available: {str(e)}")

try:
    from .gemini_adapter import GeminiAdapter
except ImportError as e:
    GeminiAdapter = None
    print(f"Gemini adapter not available: {str(e)}")

try:
    from .openai_adapter import OpenAIAdapter
except ImportError as e:
    OpenAIAdapter = None

try:
    from .claude_adapter import ClaudeAdapter
except ImportError as e:
    ClaudeAdapter = None
