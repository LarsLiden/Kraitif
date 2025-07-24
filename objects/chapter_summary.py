"""
Chapter Summary Implementation

This module implements a ChapterSummary object that captures the state and recap
of a chapter, including continuity state for characters, objects, and plot threads.
"""

from dataclasses import dataclass, field
from typing import Dict, Optional, Any
import json
from .continuity_state import ContinuityState


@dataclass
class ChapterSummary:
    """Represents a summary of a chapter with continuity state."""
    summary: str
    continuity_state: ContinuityState = field(default_factory=ContinuityState)
    
    def __post_init__(self):
        """Validate chapter summary data after initialization."""
        if not self.summary or not self.summary.strip():
            raise ValueError("Chapter summary cannot be empty")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            'summary': self.summary,
            'continuity_state': self.continuity_state.to_dict()
        }
    
    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=2)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Optional['ChapterSummary']:
        """Create chapter summary from dictionary data. Returns None if invalid."""
        try:
            if not isinstance(data, dict):
                return None
            
            summary = data.get('summary')
            if not summary:
                return None
            
            continuity_data = data.get('continuity_state', {})
            continuity_state = ContinuityState.from_dict(continuity_data)
            if continuity_state is None:
                continuity_state = ContinuityState()
            
            return cls(
                summary=str(summary),
                continuity_state=continuity_state
            )
        except (ValueError, TypeError):
            return None
    
    @classmethod
    def from_json(cls, json_str: str) -> Optional['ChapterSummary']:
        """Create chapter summary from JSON string. Returns None if invalid."""
        try:
            data = json.loads(json_str)
            return cls.from_dict(data)
        except json.JSONDecodeError:
            return None
    
    def __str__(self) -> str:
        """String representation of the chapter summary."""
        char_count = len(self.continuity_state.characters)
        obj_count = len(self.continuity_state.objects)
        loc_count = len(self.continuity_state.locations_visited)
        thread_count = len(self.continuity_state.open_plot_threads)
        
        return (f"Chapter Summary: {self.summary[:50]}... | "
                f"Characters: {char_count}, Objects: {obj_count}, "
                f"Locations: {loc_count}, Plot Threads: {thread_count}")