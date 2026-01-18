import typer
import subprocess
from typing import Optional
from rich.console import Console
from rich.prompt import Confirm
from config import config, AdapterType
from services import ContextService, PromptService
from adapters import DeepSeekAdapter, GeminiAdapter, OpenAIAdapter, ClaudeAdapter

'''
# Import all available adapters
try:
    from adapters.deepseek_adapter import DeepSeekAdapter
except ImportError:
    DeepSeekAdapter = None

try:
    from adapters.gemini_adapter import GeminiAdapter
except ImportError:
    GeminiAdapter = None

try:
    from adapters.openai_adapter import OpenAIAdapter
except ImportError:
    OpenAIAdapter = None

try:
    from adapters.claude_adapter import ClaudeAdapter
except ImportError:
    ClaudeAdapter = None
'''


app = typer.Typer()
console = Console()
context_service = ContextService()
prompt_service = PromptService()

def get_adapter(adapter_type: AdapterType):
    """Factory method to get the appropriate adapter"""
    try:
        if adapter_type == AdapterType.DEEPSEEK and DeepSeekAdapter:
            return DeepSeekAdapter(
                model=config.DEEPSEEK_MODEL,
                temperature=config.TEMPERATURE,
                max_tokens=config.MAX_TOKENS
            )
        elif adapter_type == AdapterType.GEMINI and GeminiAdapter:
            return GeminiAdapter(
                model=config.GEMINI_MODEL,
                temperature=config.TEMPERATURE
            )
        elif adapter_type == AdapterType.OPENAI and OpenAIAdapter:
            return OpenAIAdapter(
                model=config.OPENAI_MODEL,
                temperature=config.TEMPERATURE,
                max_tokens=config.MAX_TOKENS
            )
        elif adapter_type == AdapterType.CLAUDE and ClaudeAdapter:
            return ClaudeAdapter(
                model=config.CLAUDE_MODEL,
                temperature=config.TEMPERATURE,
                max_tokens=config.MAX_TOKENS
            )
    except Exception as e:
        console.print(f"[yellow]Warning: Failed to initialize {adapter_type} adapter: {str(e)}[/yellow]")
    return None

def execute_command(command: str, confirm: bool = True) -> bool:
    """Handle actual command execution with proper error handling"""
    if not command:
        console.print("[red]Error: No command generated[/red]")
        return False

    if confirm:
        if not Confirm.ask(f"Execute: [bold green]{command}[/]?"):
            console.print("[yellow]Aborted[/yellow]")
            return False

    try:
        console.print(f"[bold]Executing:[/bold] [cyan]{command}[/cyan]")
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        for line in process.stdout:
            console.print(line, end='')

        process.wait()

        if process.returncode != 0:
            console.print(f"[red]Error: Command failed with exit code {process.returncode}[/red]")
            console.print(f"[red]Error output:[/red]\n{process.stderr.read()}")
            return False

        console.print("[green]✓ Command executed successfully[/green]")
        return True

    except Exception as e:
        console.print(f"[red]Error executing command: {str(e)}[/red]")
        return False

@app.command()
def ask(
    prompt: str = typer.Argument(..., help="Your command prompt"),
    adapter: Optional[AdapterType] = None,
    model: Optional[str] = None,
    temperature: float = None,
    max_tokens: int = None,
    yes: bool = False,
    verbose: bool = False
):
    """AI-powered shell command generator"""
    temperature = temperature or config.TEMPERATURE
    max_tokens = max_tokens or config.MAX_TOKENS
    adapter_type = adapter or config.DEFAULT_ADAPTER

    try:
        # Try primary adapter first
        current_adapter = get_adapter(adapter_type)
        
        # Fallback to secondary adapter if primary fails
        if not current_adapter and adapter_type != config.FALLBACK_ADAPTER:
            console.print(f"[yellow]Falling back to {config.FALLBACK_ADAPTER} adapter[/yellow]")
            current_adapter = get_adapter(config.FALLBACK_ADAPTER)
        
        if not current_adapter:
            raise RuntimeError("No working AI adapter available")

        if verbose:
            console.print("[dim]Gathering system context...[/dim]")
        context = context_service.gather()

        if verbose:
            console.print("[dim]Constructing optimized prompt...[/dim]")
        full_prompt = prompt_service.build_prompt(prompt, context)

        if verbose:
            console.print("\n[blue]Full Prompt Being Sent:[/blue]")
            console.print(full_prompt)
            console.print(f"\n[dim]Using {adapter_type} adapter...[/dim]")

        response = current_adapter.query(full_prompt)

        console.print(f"\n[bold]AI Suggests:[/bold]\n[cyan]{response}[/cyan]")
        execute_command(response, confirm=not yes)

    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        raise typer.Exit(1)

if __name__ == "__main__":
    app()
