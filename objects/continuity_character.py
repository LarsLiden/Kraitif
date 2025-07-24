"""
ContinuityCharacter Implementation

This module implements the ContinuityCharacter class for tracking character state
within the story continuity system.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any


@dataclass
class ContinuityCharacter:
    """Represents a character's state in the continuity system."""
    name: str
    current_location: str
    status: str
    inventory: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """Validate character data after initialization."""
        if not self.name or not self.name.strip():
            raise ValueError("Character name cannot be empty")
        if not self.current_location or not self.current_location.strip():
            raise ValueError("Character current_location cannot be empty")
        if not self.status or not self.status.strip():
            raise ValueError("Character status cannot be empty")
    
    def add_inventory_item(self, item: str) -> bool:
        """Add an item to the character's inventory. Returns True if successful."""
        if not item or not item.strip():
            return False
        item = item.strip()
        if item not in self.inventory:
            self.inventory.append(item)
            return True
        return False
    
    def remove_inventory_item(self, item: str) -> bool:
        """Remove an item from the character's inventory. Returns True if successful."""
        if item in self.inventory:
            self.inventory.remove(item)
            return True
        return False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            'name': self.name,
            'current_location': self.current_location,
            'status': self.status,
            'inventory': self.inventory.copy()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Optional['ContinuityCharacter']:
        """Create character from dictionary data. Returns None if invalid."""
        try:
            if not isinstance(data, dict):
                return None
            
            name = data.get('name')
            current_location = data.get('current_location')
            status = data.get('status')
            
            if not all([name, current_location, status]):
                return None
            
            inventory = data.get('inventory', [])
            if not isinstance(inventory, list):
                inventory = []
            
            return cls(
                name=str(name),
                current_location=str(current_location),
                status=str(status),
                inventory=inventory
            )
        except (ValueError, TypeError):
            return None