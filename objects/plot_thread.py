"""
PlotThread Implementation

This module implements the PlotThread class for tracking open plot threads
within the story continuity system.
"""

from dataclasses import dataclass
from typing import Dict, Optional, Any


@dataclass
class PlotThread:
    """Represents an open plot thread in the story."""
    id: str
    description: str
    status: str
    
    def __post_init__(self):
        """Validate plot thread data after initialization."""
        if not self.id or not self.id.strip():
            raise ValueError("Plot thread id cannot be empty")
        if not self.description or not self.description.strip():
            raise ValueError("Plot thread description cannot be empty")
        if not self.status or not self.status.strip():
            raise ValueError("Plot thread status cannot be empty")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'description': self.description,
            'status': self.status
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Optional['PlotThread']:
        """Create plot thread from dictionary data. Returns None if invalid."""
        try:
            if not isinstance(data, dict):
                return None
            
            id_val = data.get('id')
            description = data.get('description')
            status = data.get('status')
            
            if not all([id_val, description, status]):
                return None
            
            return cls(
                id=str(id_val),
                description=str(description),
                status=str(status)
            )
        except (ValueError, TypeError):
            return None