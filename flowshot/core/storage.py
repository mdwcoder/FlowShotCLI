import json
import os
from pathlib import Path
from typing import Optional, List, Dict
from pydantic import BaseModel
from .flow import Flow

class RecorderState(BaseModel):
    is_recording: bool = False
    start_offset: int = 0
    history_file_path: Optional[str] = None
    current_flow_id: Optional[str] = None

class StorageModel(BaseModel):
    recorder_state: RecorderState = RecorderState()
    flows: Dict[str, Flow] = {}
    
    # helper for currently active flow
    @property
    def current_flow(self) -> Optional[Flow]:
        if self.recorder_state.current_flow_id and self.recorder_state.current_flow_id in self.flows:
            return self.flows[self.recorder_state.current_flow_id]
        return None

class Storage:
    def __init__(self, storage_dir: Optional[Path] = None):
        if storage_dir is None:
            # Default to ~/.flowshot
            self.storage_dir = Path.home() / ".flowshot"
        else:
            self.storage_dir = storage_dir
            
        self.data_file = self.storage_dir / "flows.json"
        self._ensure_storage()
        self.data = self._load()

    @property
    def current_flow(self) -> Optional[Flow]:
        return self.data.current_flow

    def _ensure_storage(self):
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        if not self.data_file.exists():
            self._save(StorageModel())

    def _load(self) -> StorageModel:
        try:
            with open(self.data_file, "r") as f:
                content = f.read()
                if not content.strip():
                    return StorageModel()
                return StorageModel.model_validate_json(content)
        except (json.JSONDecodeError, FileNotFoundError):
             return StorageModel()

    def _save(self, data: StorageModel):
        with open(self.data_file, "w") as f:
            f.write(data.model_dump_json(indent=2))

    def save(self):
        self._save(self.data)
        
    def get_flow(self, flow_id: str) -> Optional[Flow]:
        return self.data.flows.get(flow_id)
        
    def save_flow(self, flow: Flow):
        self.data.flows[flow.id] = flow
        self.save()
        
    def delete_flow(self, flow_id: str):
        if flow_id in self.data.flows:
            del self.data.flows[flow_id]
            self.save()

    def update_recorder_state(self, 
                            is_recording: Optional[bool] = None, 
                            start_offset: Optional[int] = None, 
                            history_path: Optional[str] = None, 
                            current_flow_id: Optional[str] = None):
                            
        if is_recording is not None:
            self.data.recorder_state.is_recording = is_recording
        if start_offset is not None:
            self.data.recorder_state.start_offset = start_offset
        if history_path is not None:
            self.data.recorder_state.history_file_path = history_path
        if current_flow_id is not None:
            self.data.recorder_state.current_flow_id = current_flow_id
            
        self.save()
