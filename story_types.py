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
    characteristics: Dict[str, Any] = field(default_factory=dict)
    
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
    
    # Backward compatibility properties
    @property
    def narrative_elements(self) -> Optional[str]:
        """Get narrative elements from characteristics."""
        return self.characteristics.get("narrative_elements")
    
    @property
    def key_theme(self) -> Optional[str]:
        """Get key theme from characteristics."""
        return self.characteristics.get("key_theme")
    
    @property
    def emotional_arc(self) -> Optional[str]:
        """Get emotional arc from characteristics."""
        return self.characteristics.get("emotional_arc")
    
    @property
    def common_elements(self) -> List[str]:
        """Get common elements from characteristics."""
        return self.characteristics.get("common_elements", [])


class StoryTypeRegistry:
    """Registry for all story types."""
    
    def __init__(self, data_file: Optional[str] = None):
        """Initialize registry with optional data file path."""
        if data_file is None:
            # Use default data file in the same directory
            data_file = os.path.join(os.path.dirname(__file__), "story_types_data.json")
        
        self._story_types = {}
        self._load_from_json(data_file)
    
    def _load_from_json(self, file_path: str) -> None:
        """Load story types from JSON file."""
        try:
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
                    characteristics=story_type_data.get('characteristics', {})
                )
                
                # Store with normalized key
                key = story_type_data['name'].lower().replace(" ", "_")
                self._story_types[key] = story_type
                
        except FileNotFoundError:
            # If file doesn't exist, fall back to hardcoded data
            self._load_default_data()
        except Exception as e:
            print(f"Error loading story types data: {e}")
            self._load_default_data()
    
    def _load_default_data(self) -> None:
        """Load default hardcoded data as fallback."""
        # Create story types with hardcoded data
        story_types_data = [
            {
                "name": "Overcoming the Monster",
                "description": "Hero faces a great evil or threat",
                "characteristics": {
                    "narrative_elements": "Anticipation → Dream → Frustration → Nightmare → Thrilling Escape"
                },
                "subtypes": [
                    {
                        "name": "Predator",
                        "description": "The monster actively hunts or terrorizes",
                        "examples": ["Jaws", "Alien"]
                    },
                    {
                        "name": "Holdfast",
                        "description": "The monster guards something precious",
                        "examples": ["The Hobbit's Smaug"]
                    },
                    {
                        "name": "Avenger",
                        "description": "The monster retaliates for past wrongs",
                        "examples": ["Dracula"]
                    }
                ]
            },
            {
                "name": "Rags to Riches",
                "description": "Protagonist rises from humble beginnings to greatness",
                "characteristics": {
                    "key_theme": "Inner transformation is more important than material gain"
                },
                "subtypes": [
                    {
                        "name": "Pure Ascent",
                        "description": "The hero rises steadily",
                        "examples": ["Cinderella"]
                    },
                    {
                        "name": "Fall and Redemption",
                        "description": "Gains are lost before true growth",
                        "examples": ["The Prince and the Pauper"]
                    },
                    {
                        "name": "False Riches",
                        "description": "Superficial success masks inner emptiness",
                        "examples": ["The Great Gatsby"]
                    }
                ]
            },
            {
                "name": "The Quest",
                "description": "A journey with companions, trials, and a goal",
                "characteristics": {
                    "common_elements": ["Companions", "trials", "temptations", "symbolic landscapes"]
                },
                "subtypes": [
                    {
                        "name": "Object Quest",
                        "description": "Seeking a treasure or artifact",
                        "examples": ["Indiana Jones"]
                    },
                    {
                        "name": "Person Quest",
                        "description": "Rescuing or finding someone",
                        "examples": ["Finding Nemo"]
                    },
                    {
                        "name": "Spiritual Quest",
                        "description": "Seeking enlightenment or truth",
                        "examples": ["The Divine Comedy"]
                    }
                ]
            },
            {
                "name": "Voyage and Return",
                "description": "Hero enters a strange world and returns transformed",
                "characteristics": {
                    "emotional_arc": "Naïveté → Danger → Escape → Wisdom"
                },
                "subtypes": [
                    {
                        "name": "Fantasy Realm",
                        "description": "Magical or surreal world",
                        "examples": ["Alice in Wonderland"]
                    },
                    {
                        "name": "Time Travel or Sci-Fi",
                        "description": "Unfamiliar future or past",
                        "examples": ["Back to the Future"]
                    },
                    {
                        "name": "Psychological Journey",
                        "description": "Internal transformation",
                        "examples": ["Brideshead Revisited"]
                    }
                ]
            },
            {
                "name": "Comedy",
                "description": "Confusion and miscommunication resolved in harmony",
                "characteristics": {},
                "subtypes": [
                    {
                        "name": "Romantic Comedy",
                        "description": "Misunderstandings resolved in love",
                        "examples": ["Much Ado About Nothing"]
                    },
                    {
                        "name": "Social Comedy",
                        "description": "Satire of norms and class",
                        "examples": ["The Importance of Being Earnest"]
                    },
                    {
                        "name": "Farce",
                        "description": "Exaggerated chaos and absurdity",
                        "examples": ["The Big Lebowski"]
                    }
                ]
            },
            {
                "name": "Tragedy",
                "description": "A fatal flaw leads to downfall",
                "characteristics": {
                    "emotional_arc": "Rise → Fall → Catharsis"
                },
                "subtypes": [
                    {
                        "name": "Fatal Flaw",
                        "description": "Hubris or obsession leads to downfall",
                        "examples": ["Macbeth"]
                    },
                    {
                        "name": "Innocent Victim",
                        "description": "External forces destroy the hero",
                        "examples": ["Romeo and Juliet"]
                    },
                    {
                        "name": "Corruption Arc",
                        "description": "Moral decay leads to collapse",
                        "examples": ["Citizen Kane"]
                    }
                ]
            },
            {
                "name": "Rebirth",
                "description": "Hero is redeemed or transformed",
                "characteristics": {
                    "key_theme": "A symbolic 'death' followed by renewal"
                },
                "subtypes": [
                    {
                        "name": "Seasonal Rebirth",
                        "description": "Tied to cycles of nature or holidays",
                        "examples": ["A Christmas Carol"]
                    },
                    {
                        "name": "Romantic Rebirth",
                        "description": "Love transforms the character",
                        "examples": ["Beauty and the Beast"]
                    },
                    {
                        "name": "Existential Rebirth",
                        "description": "Awakening from despair or nihilism",
                        "examples": ["Groundhog Day"]
                    }
                ]
            }
        ]
        
        # Create story types from hardcoded data
        for story_type_data in story_types_data:
            subtypes = []
            for subtype_data in story_type_data.get('subtypes', []):
                subtype = StorySubType(
                    name=subtype_data['name'],
                    description=subtype_data['description'],
                    examples=subtype_data.get('examples', [])
                )
                subtypes.append(subtype)
            
            story_type = StoryType(
                name=story_type_data['name'],
                description=story_type_data['description'],
                subtypes=subtypes,
                characteristics=story_type_data.get('characteristics', {})
            )
            
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