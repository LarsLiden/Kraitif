"""
Story Types and SubTypes Implementation

This module implements the seven classical story types and their subtypes
as described in narrative theory.
"""

from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field
from enum import Enum
import json
import os


class StoryTypeEnum(Enum):
    """Enum for story type names."""
    OVERCOMING_THE_MONSTER = "Overcoming the Monster"
    RAGS_TO_RICHES = "Rags to Riches"
    THE_QUEST = "The Quest"
    VOYAGE_AND_RETURN = "Voyage and Return"
    COMEDY = "Comedy"
    TRAGEDY = "Tragedy"
    REBIRTH = "Rebirth"


@dataclass
class StorySubType:
    """Represents a specific subtype within a story type."""
    name: str
    description: str
    examples: List[str] = field(default_factory=list)
    
    def __str__(self) -> str:
        return f"{self.name}: {self.description}"


@dataclass
class StoryType:
    """Base class for all story types."""
    name: str
    description: str
    examples: List[str] = field(default_factory=list)
    subtypes: List[StorySubType] = field(default_factory=list)
    narrative_rhythm: str = ""
    key_theme: List[str] = field(default_factory=list)
    emotional_arc: List[str] = field(default_factory=list)
    key_moment: List[str] = field(default_factory=list)
    core_arc: List[str] = field(default_factory=list)
    common_elements: List[str] = field(default_factory=list)
    selectable_fields: List[str] = field(default_factory=list)
    
    def add_subtype(self, subtype: StorySubType) -> None:
        """Add a subtype to this story type."""
        self.subtypes.append(subtype)
    
    def get_subtype(self, name: str) -> Optional[StorySubType]:
        """Get a subtype by name."""
        for subtype in self.subtypes:
            if subtype.name.lower() == name.lower():
                return subtype
        return None
    
    def __str__(self) -> str:
        return f"{self.name}: {self.description}"





class StoryTypeRegistry:
    """Registry for all story types."""
    
    def __init__(self):
        """Initialize registry with story types from JSON data."""
        # Use default data file in the data directory
        data_file = os.path.join(os.path.dirname(__file__), "..", "data", "story_types.json")
        
        self._story_types = {}
        self._load_from_json(data_file)
    
    def _load_from_json(self, file_path: str) -> None:
        """Load story types from JSON file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for story_type_data in data['story_types']:
            # Create subtypes
            subtypes = []
            for subtype_data in story_type_data.get('subtypes', []):
                subtype = StorySubType(
                    name=subtype_data['name'],
                    description=subtype_data['description'],
                    examples=subtype_data.get('examples', [])
                )
                subtypes.append(subtype)
            
            # Create story type
            story_type = StoryType(
                name=story_type_data['name'],
                description=story_type_data['description'],
                examples=story_type_data.get('examples', []),
                subtypes=subtypes,
                narrative_rhythm=story_type_data.get('narrative_rhythm', ''),
                key_theme=story_type_data.get('key_theme', []),
                emotional_arc=story_type_data.get('emotional_arc', []),
                key_moment=story_type_data.get('key_moment', []),
                core_arc=story_type_data.get('core_arc', []),
                common_elements=story_type_data.get('common_elements', []),
                selectable_fields=story_type_data.get('selectable_fields', [])
            )
            
            # Store with normalized key
            key = story_type_data['name'].lower().replace(" ", "_")
            self._story_types[key] = story_type
    
    def get_story_type(self, name: str) -> Optional[StoryType]:
        """Get a story type by name."""
        return self._story_types.get(name.lower().replace(" ", "_"))
    
    def get_all_story_types(self) -> List[StoryType]:
        """Get all story types."""
        return list(self._story_types.values())
    
    def list_story_types(self) -> List[str]:
        """List all story type names."""
        return [story_type.name for story_type in self._story_types.values()]


