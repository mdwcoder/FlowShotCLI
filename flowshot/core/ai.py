import urllib.request
import json
from typing import Optional
from .flow import Flow

class AI:
    OLLAMA_API = "http://localhost:11434/api"
    MODEL = "llama3" # Default, can be configurable or auto-detected, sticking to a sensible default.
    # Actually, we should probably check what models are available or just pick one.
    # We'll default to 'llama2' or 'mistral' if we can't find one, but user might have anything.
    # "Use Ollama local models"
    
    def is_available(self) -> bool:
        try:
            with urllib.request.urlopen(f"{self.OLLAMA_API}/tags", timeout=2) as response:
                return response.status == 200
        except Exception:
            return False

    def _query(self, prompt: str, system: str = "") -> str:
        if not self.is_available():
            raise RuntimeError("Ollama is not running or unavailable.")

        # Simple generate endpoint
        data = {
            "model": self.MODEL, 
            "prompt": prompt,
            "system": system,
            "stream": False
        }
        
        req = urllib.request.Request(
            f"{self.OLLAMA_API}/generate",
            data=json.dumps(data).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode('utf-8'))
                return result.get("response", "").strip()
        except Exception as e:
            return f"AI Error: {e}"

    def explain(self, flow: Flow) -> str:
        cmds = "\n".join([c.cmd for c in flow.commands if c.type == "command"])
        return self._query(
            prompt=f"Explain what this shell workflow does deeply but concisely:\n\n{cmds}",
            system="You are a senior DevOps engineer."
        )

    def summarize(self, flow: Flow) -> str:
        cmds = "\n".join([c.cmd for c in flow.commands if c.type == "command"])
        return self._query(
            prompt=f"Summarize this workflow in 1 short sentence:\n\n{cmds}",
            system="You provide brief summaries."
        )

    def generate_title(self, flow: Flow) -> str:
        cmds = "\n".join([c.cmd for c in flow.commands if c.type == "command"])
        return self._query(
            prompt=f"Suggest a short, kebab-case filename (no extension) for this workflow:\n\n{cmds}",
            system="You output ONLY the filename."
        )
