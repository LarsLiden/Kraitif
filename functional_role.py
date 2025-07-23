"""
Functional Roles Implementation

This module implements functional roles loaded from JSON data.
"""

from typing import List, Optional
from dataclasses import dataclass
from enum import Enum
import json
import os


class FunctionalRoleEnum(Enum):
    """Enum for functional role names."""
    PROTAGONIST = "Protagonist"
    ANTAGONIST = "Antagonist"
    DEUTERAGONIST = "Deuteragonist"
    TRITAGONIST = "Tritagonist"
    FOIL = "Foil"
    SUPPORTING_CHARACTER = "Supporting Character"
    CONFIDANT = "Confidant(e)"
    NARRATOR = "Narrator"
    LOVE_INTEREST = "Love Interest"
    COMIC_RELIEF = "Comic Relief"
    MENTOR = "Mentor"
    SIDEKICK = "Sidekick"
    GUARDIAN_GATEKEEPER = "Guardian / Gatekeeper"
    HERALD = "Herald"
    SHAPESHIFTER = "Shapeshifter"
    TEMPTER_TEMPTRESS = "Tempter / Temptress"
    TRICKSTER = "Trickster"
    VILLAIN = "Villain"
    ANTI_HERO = "Anti-Hero"
    EVERYMAN = "Everyman"


@dataclass
class FunctionalRole:
    """Represents a functional role."""
    name: str
    description: str
    
    def __str__(self) -> str:
        return f"{self.name}: {self.description}"


class FunctionalRoleRegistry:
    """Registry for all functional roles."""
    
    def __init__(self):
        """Initialize registry with functional roles from JSON data."""
        # Use default data file in the data directory
        data_file = os.path.join(os.path.dirname(__file__), "data", "functional_roles.json")
        
        self._functional_roles = {}
        self._load_from_json(data_file)
    
    def _load_from_json(self, file_path: str) -> None:
        """Load functional roles from JSON file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            for role_data in data['functional_roles']:
                functional_role = FunctionalRole(
                    name=role_data['name'],
                    description=role_data['description']
                )
                # Store with normalized key
                key = role_data['name'].lower().replace(" ", "_").replace("/", "_").replace("(", "").replace(")", "")
                self._functional_roles[key] = functional_role
    
    def get_functional_role(self, name: str) -> Optional[FunctionalRole]:
        """Get a functional role by name."""
        normalized_name = name.lower().replace(" ", "_").replace("/", "_").replace("(", "").replace(")", "")
        return self._functional_roles.get(normalized_name)
    
    def get_all_functional_roles(self) -> List[FunctionalRole]:
        """Get all functional roles."""
        return list(self._functional_roles.values())
    
    def list_functional_role_names(self) -> List[str]:
        """List all functional role names."""
        return [role.name for role in self._functional_roles.values()]
    
    def search_functional_roles(self, search_term: str) -> List[FunctionalRole]:
        """Search for functional roles by name or description."""
        search_term = search_term.lower()
        results = []
        
        for role in self._functional_roles.values():
            if (search_term in role.name.lower() or 
                search_term in role.description.lower()):
                results.append(role)
        
        return results