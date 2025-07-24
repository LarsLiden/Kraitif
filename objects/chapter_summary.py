"""
Chapter Summary Implementation

This module implements a ChapterSummary object that captures the state and recap
of a chapter, including continuity state for characters, objects, and plot threads.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
import json


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


@dataclass
class ContinuityState:
    """Represents the continuity state of the story at a specific point."""
    characters: List[ContinuityCharacter] = field(default_factory=list)
    objects: List[ContinuityObject] = field(default_factory=list)
    locations_visited: List[str] = field(default_factory=list)
    open_plot_threads: List[PlotThread] = field(default_factory=list)
    
    def add_character(self, character: ContinuityCharacter) -> bool:
        """Add a character to the continuity state. Returns True if successful."""
        if not isinstance(character, ContinuityCharacter):
            return False
        
        # Check if character already exists
        for existing in self.characters:
            if existing.name.lower() == character.name.lower():
                # Update existing character
                existing.current_location = character.current_location
                existing.status = character.status
                existing.inventory = character.inventory.copy()
                return True
        
        self.characters.append(character)
        return True
    
    def remove_character(self, name: str) -> bool:
        """Remove a character from the continuity state. Returns True if successful."""
        for i, character in enumerate(self.characters):
            if character.name.lower() == name.lower():
                self.characters.pop(i)
                return True
        return False
    
    def get_character(self, name: str) -> Optional[ContinuityCharacter]:
        """Get a character by name."""
        for character in self.characters:
            if character.name.lower() == name.lower():
                return character
        return None
    
    def add_object(self, obj: ContinuityObject) -> bool:
        """Add an object to the continuity state. Returns True if successful."""
        if not isinstance(obj, ContinuityObject):
            return False
        
        # Check if object already exists
        for existing in self.objects:
            if existing.name.lower() == obj.name.lower():
                # Update existing object
                existing.holder = obj.holder
                existing.location = obj.location
                return True
        
        self.objects.append(obj)
        return True
    
    def remove_object(self, name: str) -> bool:
        """Remove an object from the continuity state. Returns True if successful."""
        for i, obj in enumerate(self.objects):
            if obj.name.lower() == name.lower():
                self.objects.pop(i)
                return True
        return False
    
    def get_object(self, name: str) -> Optional[ContinuityObject]:
        """Get an object by name."""
        for obj in self.objects:
            if obj.name.lower() == name.lower():
                return obj
        return None
    
    def add_location(self, location: str) -> bool:
        """Add a location to the visited locations. Returns True if successful."""
        if not location or not location.strip():
            return False
        location = location.strip()
        if location not in self.locations_visited:
            self.locations_visited.append(location)
            return True
        return False
    
    def remove_location(self, location: str) -> bool:
        """Remove a location from the visited locations. Returns True if successful."""
        if location in self.locations_visited:
            self.locations_visited.remove(location)
            return True
        return False
    
    def add_plot_thread(self, thread: PlotThread) -> bool:
        """Add a plot thread to the continuity state. Returns True if successful."""
        if not isinstance(thread, PlotThread):
            return False
        
        # Check if plot thread already exists
        for existing in self.open_plot_threads:
            if existing.id.lower() == thread.id.lower():
                # Update existing thread
                existing.description = thread.description
                existing.status = thread.status
                return True
        
        self.open_plot_threads.append(thread)
        return True
    
    def remove_plot_thread(self, thread_id: str) -> bool:
        """Remove a plot thread from the continuity state. Returns True if successful."""
        for i, thread in enumerate(self.open_plot_threads):
            if thread.id.lower() == thread_id.lower():
                self.open_plot_threads.pop(i)
                return True
        return False
    
    def get_plot_thread(self, thread_id: str) -> Optional[PlotThread]:
        """Get a plot thread by id."""
        for thread in self.open_plot_threads:
            if thread.id.lower() == thread_id.lower():
                return thread
        return None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            'characters': [char.to_dict() for char in self.characters],
            'objects': [obj.to_dict() for obj in self.objects],
            'locations_visited': self.locations_visited.copy(),
            'open_plot_threads': [thread.to_dict() for thread in self.open_plot_threads]
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Optional['ContinuityState']:
        """Create continuity state from dictionary data. Returns None if invalid."""
        try:
            if not isinstance(data, dict):
                return None
            
            continuity_state = cls()
            
            # Parse characters
            characters_data = data.get('characters', [])
            if isinstance(characters_data, list):
                for char_data in characters_data:
                    character = ContinuityCharacter.from_dict(char_data)
                    if character:
                        continuity_state.characters.append(character)
            
            # Parse objects
            objects_data = data.get('objects', [])
            if isinstance(objects_data, list):
                for obj_data in objects_data:
                    obj = ContinuityObject.from_dict(obj_data)
                    if obj:
                        continuity_state.objects.append(obj)
            
            # Parse locations
            locations_data = data.get('locations_visited', [])
            if isinstance(locations_data, list):
                continuity_state.locations_visited = [str(loc) for loc in locations_data if loc]
            
            # Parse plot threads
            threads_data = data.get('open_plot_threads', [])
            if isinstance(threads_data, list):
                for thread_data in threads_data:
                    thread = PlotThread.from_dict(thread_data)
                    if thread:
                        continuity_state.open_plot_threads.append(thread)
            
            return continuity_state
        except (ValueError, TypeError):
            return None


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