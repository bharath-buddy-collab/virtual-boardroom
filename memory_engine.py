import json
import os
import logging
from dataclasses import dataclass, asdict, field
from typing import List, Optional
from datetime import datetime

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MemoryEngine")

# --- DATA SCHEMA (Versioning & History) ---
@dataclass
class BoardroomState:
    """
    State object with history tracking.
    """
    niche: str
    goal: str
    # The current active session data
    cfo_data: Optional[str] = None
    cmo_data: Optional[str] = None
    ceo_data: Optional[str] = None
    # Historical archive (Compacted context)
    history: List[str] = field(default_factory=list)
    last_updated: str = ""

    def to_dict(self):
        return asdict(self)

# --- MEMORY SERVICE ---
class MemoryService:
    def __init__(self, storage_file="boardroom_memory.json"):
        # CLOUD FIX: Use /tmp directory for writable files if it exists
        if os.path.exists("/tmp"):
            self.storage_file = os.path.join("/tmp", storage_file)
        else:
            self.storage_file = storage_file
            
        self._ensure_storage()

    def _ensure_storage(self):
        if not os.path.exists(self.storage_file):
            self.save_state(BoardroomState(niche="", goal=""))

    def save_state(self, state: BoardroomState):
        """
        Saves state to disk.
        """
        state.last_updated = datetime.now().isoformat()
        try:
            with open(self.storage_file, 'w') as f:
                json.dump(state.to_dict(), f, indent=4)
            logger.info(f"💾 State saved to {self.storage_file}.")
        except Exception as e:
            logger.error(f"❌ Save failed: {e}")

    def load_state(self) -> BoardroomState:
        try:
            if not os.path.exists(self.storage_file):
                return BoardroomState(niche="", goal="")
            
            with open(self.storage_file, 'r') as f:
                data = json.load(f)
            
            # Rehydrate
            return BoardroomState(
                niche=data.get("niche", ""),
                goal=data.get("goal", ""),
                cfo_data=data.get("cfo_data"),
                cmo_data=data.get("cmo_data"),
                ceo_data=data.get("ceo_data"),
                history=data.get("history", []),
                last_updated=data.get("last_updated", "")
            )
        except Exception as e:
            logger.error(f"⚠️ Corrupt memory. Resetting. Error: {e}")
            return BoardroomState(niche="", goal="")

    def compact_context(self, state: BoardroomState):
        """
        CONTEXT ENGINEERING: COMPACTION
        Moves the 'Active' CEO directive into 'Long-Term History' to free up
        the context window for the new session.
        """
        if state.ceo_data:
            logger.info("🧹 Compacting previous strategy into history...")
            # Create a summary string
            summary = f"[{state.last_updated}] Strategy for '{state.niche}': {state.ceo_data[:100]}..."
            
            # Push to history (The "Filing Cabinet")
            state.history.append(summary)
            
            # Pruning Strategy: Keep only last 5 historical items (Context Window Management)
            if len(state.history) > 5:
                removed = state.history.pop(0)
                logger.info(f"🗑️ Pruned oldest history: {removed[:20]}...")
            
            # Clear the active slot
            state.ceo_data = None