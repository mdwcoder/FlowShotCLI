import os
import time
from pathlib import Path
from typing import List, Optional
from .storage import Storage, RecorderState
from .flow import Flow, Command
from .dedup import deduplicate_commands

HISTORY_FILES = [
    Path.home() / ".zsh_history",
    Path.home() / ".bash_history",
    Path.home() / ".history", # generic fallback
]

class Recorder:
    def __init__(self, storage: Storage):
        self.storage = storage

    def _detect_history_file(self) -> Optional[Path]:
        # Respect user environment variable if set
        if "HISTFILE" in os.environ:
             histfile = Path(os.environ["HISTFILE"])
             if histfile.exists():
                 return histfile

        # Check common locations
        for p in HISTORY_FILES:
            if p.exists():
                return p
        return None

    def start(self) -> str:
        """
        Start recording. Returns the path of the history file being watched.
        """
        history_file = self._detect_history_file()
        if not history_file:
            raise FileNotFoundError("Could not find a valid shell history file (.zsh_history or .bash_history)")

        # Initialize a new flow
        new_flow = Flow()
        self.storage.save_flow(new_flow)

        # Get current file size as offset
        # We use strict bytes offset to be safe
        try:
            current_offset = history_file.stat().st_size
        except FileNotFoundError:
            current_offset = 0

        self.storage.update_recorder_state(
            is_recording=True,
            start_offset=current_offset,
            history_path=str(history_file),
            current_flow_id=new_flow.id
        )
        return str(history_file)

    def stop(self) -> Flow:
        """
        Stop recording and return the captured Flow.
        """
        state = self.storage.data.recorder_state
        if not state.is_recording:
             # If not recording, just return empty or catch error. 
             # Ideally check valid flow exists.
             if state.current_flow_id and state.current_flow_id in self.storage.data.flows:
                 return self.storage.data.flows[state.current_flow_id]
             raise RuntimeError("Not currently recording")

        history_path = Path(state.history_file_path)
        if not history_path.exists():
            # If history file disappeared, we can't do much.
            # Stop recording and return what we have (empty)
            self.storage.update_recorder_state(is_recording=False)
            raise FileNotFoundError(f"History file {history_path} not found")

        # Read new content
        new_lines = []
        try:
            with open(history_path, "rb") as f:
                f.seek(state.start_offset)
                content = f.read().decode("utf-8", errors="replace") # Decode safely
                new_lines = content.splitlines()
        except Exception as e:
            self.storage.update_recorder_state(is_recording=False)
            raise RuntimeError(f"Failed to read history file: {e}")

        # Process lines to clean bash/zsh timestamps if present
        # This is basic; complex zsh history with multiline needs robust parsing.
        # For MVP we assume standard one-line or simple zsh extended history.
        cleaned_commands = self._parse_history_lines(new_lines)
        
        # Get active Flow
        flow = self.storage.get_flow(state.current_flow_id)
        if not flow:
            # Fallback (shouldn't happen)
            flow = Flow()

        for cmd_str in cleaned_commands:
            if cmd_str.strip(): # ignore empty lines
                flow.add_command(cmd_str)

        # Deduplicate
        flow.commands = deduplicate_commands(flow.commands)

        self.storage.save_flow(flow)
        self.storage.update_recorder_state(is_recording=False)

        return flow
    
    def _parse_history_lines(self, lines: List[str]) -> List[str]:
        cleaned = []
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Zsh extended history format: : 1678900000:0;command
            if line.startswith(": ") and ";" in line:
                parts = line.split(";", 1)
                if len(parts) == 2:
                    cleaned.append(parts[1])
            else:
                cleaned.append(line)
        return cleaned

    def is_recording(self) -> bool:
        return self.storage.data.recorder_state.is_recording
