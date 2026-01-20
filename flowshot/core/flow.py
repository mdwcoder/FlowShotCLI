import time
from typing import List, Optional
from pydantic import BaseModel, Field
import uuid

class Command(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    cmd: str
    type: str = "command" # command, step
    timestamp: float = Field(default_factory=time.time)
    note: Optional[str] = None

class Flow(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str = "Untitled Flow"
    created_at: float = Field(default_factory=time.time)
    commands: List[Command] = []
    
    def add_command(self, cmd_str: str, note: Optional[str] = None) -> None:
        self.commands.append(Command(cmd=cmd_str, note=note))
        
    def remove_command(self, index: int) -> bool:
        if 0 <= index < len(self.commands):
            self.commands.pop(index)
            return True
        return False
        
    def add_note_to_command(self, index: int, note: str) -> bool:
        if 0 <= index < len(self.commands):
            self.commands[index].note = note
            return True
        return False
