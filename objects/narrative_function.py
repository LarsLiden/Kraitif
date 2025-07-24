"""
Narrative Functions Implementation

This module implements narrative functions loaded from JSON data.
"""

from typing import List, Optional
from dataclasses import dataclass
from enum import Enum
import json
import os


class NarrativeFunctionEnum(Enum):
    """Narrative function tags representing structural roles of scenes or chapters."""
    
    SETTING_INTRODUCTION = "Setting Introduction"  # Establishes location, mood, tone
    CHARACTER_INTRODUCTION = "Character Introduction"  # Introduces key characters
    INCITING_INCIDENT = "Inciting Incident"  # First major disruption to the status quo
    FIRST_REVERSAL = "First Reversal"  # Unexpected shift in direction or stakes
    RISING_TENSION = "Rising Tension"  # Builds suspense, stakes, and pressure
    SUBPLOT_ACTIVATION = "Subplot Activation"  # Launches secondary threads
    MORAL_CHALLENGE = "Moral Challenge"  # Characters face ethical or emotional conflict
    MIDPOINT_TURN = "Midpoint Turn"  # Major twist or truth changes the trajectory
    RELATIONSHIP_REVERSAL = "Relationship Reversal"  # Shift in character dynamics (betrayal, alliance)
    MOMENT_OF_WEAKNESS = "Moment of Weakness"  # Hero falters emotionally or physically
    SETBACK = "Setback"  # External failure or complication
    TRUTH_REVELATION = "Truth Revelation"  # Important secret or mystery unveiled
    CONFRONTATION = "Confrontation"  # Major clash between protagonist and antagonist
    CLIMAX = "Climax"  # Emotional or physical peak of tension
    TRANSFORMATION = "Transformation"  # Character internal shift or rebirth
    DENOUEMENT = "Denouement"  # Loose ends resolved, consequences shown
    FINAL_IMAGE = "Final Image"  # Last scene or symbolic moment
    FORESHADOWING = "Foreshadowing"  # Seeds planted for future tension
    ECHO = "Echo"  # Payoff for earlier scene or dialogue
    REFLECTION = "Reflection"  # Characters contemplate past actions, change
    THEME_REINFORCEMENT = "Theme Reinforcement"  # Underscores core message or motif
    CATALYST_EVENT = "Catalyst Event"  # Minor event with disproportionate future impact
    UNEXPECTED_REUNION = "Unexpected Reunion"  # Characters reconnect in surprising ways


@dataclass
class NarrativeFunction:
    """Represents a narrative function."""
    name: str
    description: str
    
    def __str__(self) -> str:
        return f"{self.name}: {self.description}"


class NarrativeFunctionRegistry:
    """Registry for all narrative functions."""
    
    def __init__(self):
        """Initialize registry with narrative functions from JSON data."""
        # Use default data file in the data directory
        data_file = os.path.join(os.path.dirname(__file__), "..", "data", "narrative_functions.json")
        
        self._narrative_functions = {}
        self._load_from_json(data_file)
    
    def _load_from_json(self, file_path: str) -> None:
        """Load narrative functions from JSON file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            for function_data in data['narrative_functions']:
                narrative_function = NarrativeFunction(
                    name=function_data['name'],
                    description=function_data['description']
                )
                # Store with normalized key
                key = function_data['name'].lower().replace(" ", "_").replace("/", "_").replace("(", "").replace(")", "")
                self._narrative_functions[key] = narrative_function
    
    def get_narrative_function(self, name: str) -> Optional[NarrativeFunction]:
        """Get a narrative function by name."""
        normalized_name = name.lower().replace(" ", "_").replace("/", "_").replace("(", "").replace(")", "")
        return self._narrative_functions.get(normalized_name)
    
    def get_all_narrative_functions(self) -> List[NarrativeFunction]:
        """Get all narrative functions."""
        return list(self._narrative_functions.values())
    
    def list_narrative_function_names(self) -> List[str]:
        """List all narrative function names."""
        return [function.name for function in self._narrative_functions.values()]
    
    def search_narrative_functions(self, search_term: str) -> List[NarrativeFunction]:
        """Search for narrative functions by name or description."""
        search_term = search_term.lower()
        results = []
        
        for function in self._narrative_functions.values():
            if (search_term in function.name.lower() or 
                search_term in function.description.lower()):
                results.append(function)
        
        return results