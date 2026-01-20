from typing import List, Tuple

class Validator:
    DESTRUCTIVE_PATTERNS = ["rm -rf", "mkfs", "dd if="]
    INTERACTIVE_PATTERNS = ["vim", "nano", "less", "more", "man", "top", "htop", "ssh"]
    SUDO_PATTERN = "sudo"

    def validate_command(self, cmd: str) -> List[str]:
        warnings = []
        cmd_lower = cmd.lower()
        
        for pattern in self.DESTRUCTIVE_PATTERNS:
            if pattern in cmd_lower:
                warnings.append(f"Destructive command detected: '{pattern}'")
                
        for pattern in self.INTERACTIVE_PATTERNS:
            if cmd_lower.startswith(pattern + " ") or cmd_lower == pattern:
                warnings.append(f"Interactive command detected: '{pattern}'")
                
        if self.SUDO_PATTERN in cmd_lower.split():
             warnings.append("Sudo usage detected. Scripts should generally run as user.")
             
        return warnings

    def validate_flow(self, flow) -> List[Tuple[int, str, str]]:
        """
        Returns list of (index, command, warning_message)
        """
        results = []
        for idx, cmd in enumerate(flow.commands):
            if cmd.type == "command": # Ignore steps
                warns = self.validate_command(cmd.cmd)
                for w in warns:
                    results.append((idx, cmd.cmd, w))
        return results
