import os
import subprocess
from typing import Dict, Optional

class ContextService:
    def gather(self) -> Dict[str, str]:
        """Gathers all relevant system context with better error handling"""
        return {
            "cwd": self._get_cwd(),
            "files": self._get_files(),
            "git": self._get_git_status(),
            "system": self._get_system_info()
        }
    
    def _get_cwd(self) -> str:
        try:
            return os.getcwd()
        except:
            return "Unknown directory"
    
    def _get_files(self) -> str:
        try:
            return subprocess.run(
                ["ls", "-la"],
                capture_output=True,
                text=True
            ).stdout
        except:
            return ""
    
    def _get_git_status(self) -> str:
        try:
            return subprocess.run(
                ["git", "status", "--short"],
                capture_output=True,
                text=True
            ).stdout
        except:
            return ""
    
    def _get_system_info(self) -> str:
        try:
            if os.name == 'nt':
                return subprocess.run(
                    ["systeminfo"],
                    capture_output=True,
                    text=True
                ).stdout[:500]  # Limit output
            else:
                return subprocess.run(
                    ["uname", "-a"],
                    capture_output=True,
                    text=True
                ).stdout
        except:
            return "Unknown system"


class PromptService:
    def build_prompt(self, user_prompt: str, context: Dict[str, str]) -> str:
        """Constructs an optimized prompt with context"""
        return f"""
        You are an expert shell command generator. Given the following context:

        Current directory: {context['cwd']}
        Files in directory:
        {context['files'] or 'No files found'}
        Git status:
        {context['git'] or 'No git repository found'}
        System: {context['system'] or 'Unknown system'}

        The user requests: {user_prompt}

        Provide exactly one shell command that would accomplish this task.
        The command should:
        - Be valid for the current system context
        - Be efficient and safe
        - Work on the current operating system
        - Include any necessary flags

        Output ONLY the command itself, without:
        - Any explanation
        - Additional text
        - Code blocks
        - Markdown formatting

        Command:
        """
