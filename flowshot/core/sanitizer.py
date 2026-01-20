import re
import os
from typing import List
from .flow import Flow, Command

class Sanitizer:
    def __init__(self):
        self.replacements = []
        # Basic patterns
        self.add_pattern(r'[a-zA-Z0-9]{32,}', '<TOKEN>') # Long random strings
        self.add_pattern(r'ghp_[a-zA-Z0-9]+', '<GITHUB_TOKEN>')
        
        # User home
        user_home = os.path.expanduser("~")
        if user_home and user_home != "/":
            self.add_pattern(re.escape(user_home), '$HOME')

    def add_pattern(self, pattern: str, replacement: str):
        self.replacements.append((re.compile(pattern), replacement))

    def sanitize_string(self, text: str) -> str:
        for regex, replacement in self.replacements:
            text = regex.sub(replacement, text)
        return text

    def sanitize_flow(self, flow: Flow) -> Flow:
        """
        Returns a new Flow object with sanitized commands.
        Does not modify the original flow in place.
        """
        new_flow = flow.model_copy(deep=True)
        for cmd in new_flow.commands:
            cmd.cmd = self.sanitize_string(cmd.cmd)
        return new_flow
