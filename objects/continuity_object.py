"""
ContinuityObject Implementation

This module implements the ContinuityObject class for tracking object state
within the story continuity system.
"""

from dataclasses import dataclass
from typing import Dict, Optional, Any


@dataclass
class ContinuityObject:
    """Represents an object in the continuity system."""
    name: str
    holder: Optional[str]
    location: str
    
    def __post_init__(self):
        """Validate object data after initialization."""
        if not self.name or not self.name.strip():
            raise ValueError("Object name cannot be empty")
        if not self.location or not self.location.strip():
            raise ValueError("Object location cannot be empty")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            'name': self.name,
            'holder': self.holder,
            'location': self.location
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Optional['ContinuityObject']:
        """Create object from dictionary data. Returns None if invalid."""
        try:
            if not isinstance(data, dict):
                return None
            
            name = data.get('name')
            location = data.get('location')
            
            if not all([name, location]):
                return None
            
            holder = data.get('holder')
            
            return cls(
                name=str(name),
                holder=str(holder) if holder else None,
                location=str(location)
            )
        except (ValueError, TypeError):
            return None