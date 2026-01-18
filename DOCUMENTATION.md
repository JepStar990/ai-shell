# **AI Shell - Documentation**  

## **📌 Overview**  
**AI Shell** is a command-line tool that converts natural language prompts into executable shell commands using AI (Gemini by default, DeepSeek as fallback). It helps users quickly generate terminal commands without needing to remember complex syntax.  

---

## **🚀 Features**  
✅ **Multi-Adapter Support** – Uses **Gemini** (default) or **DeepSeek** (fallback)  
✅ **Smart Error Handling** – Falls back to alternative APIs if one fails  
✅ **Interactive Confirmation** – Asks before executing commands (optional `--yes` to skip)  
✅ **Context Awareness** – Checks system info (OS, directory, Git status) for better command generation  
✅ **Free & Paid Options** – Works with free-tier APIs  

---

## **⚙️ Setup & Installation**  

### **1. Prerequisites**  
- Python 3.9+  
- `pip` (Python package manager)  

### **2. Clone/Download the Project**  
```bash
git clone https://github.com/your-repo/ai-shell.git
cd ai-shell
```

### **3. Install Dependencies**  
```bash
pip install -r requirements.txt
```

### **4. Set Up API Keys**  
Create a `.env` file:  
```bash
# .env
GOOGLE_API_KEY="your-gemini-api-key"  # Required (get from: https://aistudio.google.com/app/apikey)
DEEPSEEK_API_KEY="your-deepseek-key"  # Optional (fallback)
```

---

## **📂 Project Structure**  
```
ai-shell/
├── adapters/
│   ├── __init__.py       # Adapter imports
│   ├── gemini_adapter.py # Default (Gemini)
│   └── deepseek_adapter.py # Fallback (DeepSeek)
├── config.py            # API & model settings
├── main.py              # CLI interface
├── services.py          # System context & prompts
└── requirements.txt     # Dependencies
```

---

## **🔧 Configuration (`config.py`)**  
```python
@dataclass
class AppConfig:
    DEFAULT_ADAPTER = "gemini"  # or "deepseek"
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")  # Required for Gemini
    DEEPSEEK_API_KEY: str = os.getenv("DEEPSEEK_API_KEY", "")  # Fallback
    MAX_TOKENS: int = 1000  # Limit token usage
    TEMPERATURE: float = 0.3  # Lower = more precise commands
```

---

## **🔌 Adapters**  

### **1. Gemini (Default)**  
- **File:** `adapters/gemini_adapter.py`  
- **Requirements:** `pip install google-generativeai`  
- **Free Tier:** 60 requests/minute  

### **2. DeepSeek (Fallback)**  
- **File:** `adapters/deepseek_adapter.py`  
- **Requirements:** `pip install openai`  
- **Note:** Requires API key & balance  

---

## **💻 Usage**  

### **Basic Command**  
```bash
python main.py ask "List all Python files in this folder"
```

### **Options**  
| Flag | Description | Example |
|------|-------------|---------|
| `--prompt` / `-p` | Direct prompt input | `-p "Delete old log files"` |
| `--max-tokens` | Limit response length | `--max-tokens 500` |
| `--yes` / `-y` | Skip execution confirmation | `-y` |
| `--verbose` | Show detailed AI process | `--verbose` |

### **Examples**  
```bash
# Generate & run a command (with confirmation)
python main.py ask "Find all large files (>100MB)"

# Skip confirmation
python main.py ask "Clean up temp files" --yes

# Force DeepSeek (if Gemini fails)
DEEPSEEK_API_KEY="your-key" python main.py ask "Analyze disk usage"
```

---

## **🛠 Troubleshooting**  

### **1. "API Key Not Found"**  
✅ Fix: Ensure `.env` has `GOOGLE_API_KEY` or `DEEPSEEK_API_KEY`.  

### **2. "Insufficient Balance" (DeepSeek)**  
✅ Fix:  
- Top up at [DeepSeek Billing](https://platform.deepseek.com/billing)  
- Or rely on Gemini (`export DEFAULT_ADAPTER=gemini`)  

### **3. "ModuleNotFoundError"**  
✅ Fix:  
```bash
pip install google-generativeai openai python-dotenv typer rich
```

---

## **📜 License**  
MIT License - Free for personal & commercial use.  

---

## **🔗 Links**  
- **[Gemini API Key](https://aistudio.google.com/app/apikey)**  
- **[DeepSeek Pricing](https://platform.deepseek.com/pricing)**  

---

### **🎯 Summary**  
This tool helps **automate terminal commands** using AI, with **Gemini as the default free option** and DeepSeek as a fallback. Simply:  
1. **Install** (`pip install -r requirements.txt`)  
2. **Configure** (add API keys in `.env`)  
3. **Run** (`python main.py ask "your prompt"`)
