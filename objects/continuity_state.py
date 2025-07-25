"""
ContinuityState Implementation

This module implements the ContinuityState class for tracking the overall
continuity state of the story including characters, objects, and plot threads.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from .continuity_character import ContinuityCharacter
from .continuity_object import ContinuityObject
from .plot_thread import PlotThread


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
    
    def to_prompt_text(self) -> str:
        """Convert continuity state to formatted text for use in prompts."""
        if not any([self.characters, self.objects, self.locations_visited, self.open_plot_threads]):
            return "No specific continuity state to maintain."
        
        parts = []
        
        # Characters section
        if self.characters:
            parts.append("Characters:")
            for char in self.characters:
                char_info = f"- {char.name}: Currently at {char.current_location}, {char.status}"
                if char.inventory:
                    char_info += f", carrying: {', '.join(char.inventory)}"
                parts.append(char_info)
        
        # Objects section
        if self.objects:
            parts.append("\nObjects:")
            for obj in self.objects:
                if obj.holder:
                    parts.append(f"- {obj.name}: Held by {obj.holder}")
                else:
                    parts.append(f"- {obj.name}: Located at {obj.location}")
        
        # Locations section
        if self.locations_visited:
            parts.append(f"\nLocations Visited: {', '.join(self.locations_visited)}")
        
        # Plot threads section
        if self.open_plot_threads:
            parts.append("\nOpen Plot Threads:")
            for thread in self.open_plot_threads:
                parts.append(f"- {thread.description} (Status: {thread.status})")
        
        return "\n".join(parts)