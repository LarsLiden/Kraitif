"""
Emotional Function Implementation

This module implements emotional functions for character development in stories.
"""

from typing import List, Optional
from dataclasses import dataclass
from enum import Enum
import json
import os


class EmotionalFunctionEnum(Enum):
    """Enum for emotional function names."""
    SYMPATHETIC_CHARACTER = "Sympathetic Character"
    UNSYMPATHETIC_CHARACTER = "Unsympathetic Character"
    CATALYST = "Catalyst"
    OBSERVER = "Observer"
    INSTIGATOR = "Instigator"
    VICTIM = "Victim"
    AGGRESSOR = "Aggressor"
    MEDIATOR = "Mediator"


@dataclass
class EmotionalFunction:
    """Represents an emotional function that a character can serve in a story."""
    name: str
    description: str
    
    def __str__(self) -> str:
        return f"{self.name}: {self.description}"


class EmotionalFunctionRegistry:
    """Registry for all emotional functions."""
    
    def __init__(self):
        """Initialize registry with emotional functions from JSON data."""
        # Use default data file in the data directory (up one level from objects/)
        data_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "emotional_functions.json")
        
        self._emotional_functions = {}
        self._load_from_json(data_file)
    
    def _load_from_json(self, file_path: str) -> None:
        """Load emotional functions from JSON file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                if isinstance(data, list):
                    # Handle array format
                    for function_data in data:
                        if isinstance(function_data, dict) and 'name' in function_data and 'description' in function_data:
                            emotional_function = EmotionalFunction(
                                name=function_data['name'],
                                description=function_data['description']
                            )
                            # Store with normalized key
                            key = function_data['name'].lower().replace(" ", "_")
                            self._emotional_functions[key] = emotional_function
                elif isinstance(data, dict) and 'emotional_functions' in data:
                    # Handle object format with emotional_functions key
                    for function_data in data['emotional_functions']:
                        if isinstance(function_data, dict) and 'name' in function_data and 'description' in function_data:
                            emotional_function = EmotionalFunction(
                                name=function_data['name'],
                                description=function_data['description']
                            )
                            # Store with normalized key
                            key = function_data['name'].lower().replace(" ", "_")
                            self._emotional_functions[key] = emotional_function
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            # If file doesn't exist or is malformed, registry will be empty
            pass
    
    def get_emotional_function(self, name: str) -> Optional[EmotionalFunction]:
        """Get an emotional function by name."""
        return self._emotional_functions.get(name.lower().replace(" ", "_"))
    
    def get_all_emotional_functions(self) -> List[EmotionalFunction]:
        """Get all emotional functions."""
        return list(self._emotional_functions.values())
    
    def list_emotional_function_names(self) -> List[str]:
        """List all emotional function names."""
        return [function.name for function in self._emotional_functions.values()]
    
    def search_emotional_functions(self, search_term: str) -> List[EmotionalFunction]:
        """Search for emotional functions by name or description."""
        search_term = search_term.lower()
        results = []
        
        for function in self._emotional_functions.values():
            if (search_term in function.name.lower() or 
                search_term in function.description.lower()):
                results.append(function)
        
        return results