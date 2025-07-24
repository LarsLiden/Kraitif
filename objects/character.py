"""
Character Implementation

This module implements the Character class that combines archetype, functional role, 
emotional function, and other character attributes.
"""

from typing import Optional
from dataclasses import dataclass
from .archetype import ArchetypeEnum
from .functional_role import FunctionalRoleEnum
from .emotional_function import EmotionalFunctionEnum


@dataclass
class Character:
    """Represents a character in a story with all their attributes."""
    name: str
    archetype: ArchetypeEnum
    functional_role: FunctionalRoleEnum
    emotional_function: EmotionalFunctionEnum
    backstory: str = ""
    character_arc: str = ""
    
    def __str__(self) -> str:
        """String representation of the character."""
        return f"{self.name} ({self.archetype.value})"
    
    def to_dict(self) -> dict:
        """Convert character to dictionary for serialization."""
        return {
            'name': self.name,
            'archetype': self.archetype.value,
            'functional_role': self.functional_role.value,
            'emotional_function': self.emotional_function.value,
            'backstory': self.backstory,
            'character_arc': self.character_arc
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> Optional['Character']:
        """Create character from dictionary data."""
        try:
            # Find enum values by their string values
            archetype = None
            for arch in ArchetypeEnum:
                if arch.value == data['archetype']:
                    archetype = arch
                    break
            
            functional_role = None
            for role in FunctionalRoleEnum:
                if role.value == data['functional_role']:
                    functional_role = role
                    break
            
            emotional_function = None
            for func in EmotionalFunctionEnum:
                if func.value == data['emotional_function']:
                    emotional_function = func
                    break
            
            if not all([archetype, functional_role, emotional_function]):
                return None
            
            return cls(
                name=data['name'],
                archetype=archetype,
                functional_role=functional_role,
                emotional_function=emotional_function,
                backstory=data.get('backstory', ''),
                character_arc=data.get('character_arc', '')
            )
        except (KeyError, TypeError):
            return None