import re
from typing import List, Dict, Counter
from .flow import Flow

class VariableDetector:
    def detect_variables(self, flow: Flow) -> Dict[str, str]:
        """
        Detects potential variables from repeated string literals or paths.
        Returns a dict of suggested_var_name -> value
        """
        # Very simple heuristic: repeated paths or long tokens
        tokens = []
        for cmd in flow.commands:
            if cmd.type != "command":
                continue
            # Split by whitespace, look for looks-like-path or long args
            parts = cmd.cmd.split()
            for p in parts:
                if len(p) > 5 and (p.startswith("/") or p.startswith("./") or p.count("/") > 1):
                    tokens.append(p)
                elif len(p) > 8 and re.match(r'^[a-zA-Z0-9_\-\.]+$', p):
                    # Long identifier-like string
                    tokens.append(p)

        counts = Counter(tokens)
        suggestions = {}
        var_counter = 1
        
        for token, count in counts.items():
            if count > 1:
                # Suggest it
                name = f"VAR_{var_counter}"
                suggestions[name] = token
                var_counter += 1
                
        return suggestions
