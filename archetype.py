"""
Archetypes Implementation

This module implements character archetypes loaded from JSONL data.
"""

from typing import List, Optional
from dataclasses import dataclass
import json
import os


@dataclass
class Archetype:
    """Represents a character archetype."""
    name: str
    description: str
    
    def __str__(self) -> str:
        return f"{self.name}: {self.description}"


class ArchetypeRegistry:
    """Registry for all character archetypes."""
    
    def __init__(self):
        """Initialize registry with archetypes from JSONL data."""
        # Use default data file in the data directory
        data_file = os.path.join(os.path.dirname(__file__), "data", "archetypes.jsonl")
        
        self._archetypes = {}
        self._load_from_jsonl(data_file)
    
    def _load_from_jsonl(self, file_path: str) -> None:
        """Load archetypes from JSONL file."""
        import json
        
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('//'):  # Skip empty lines and comments
                    # Remove trailing comma if present
                    if line.endswith(','):
                        line = line[:-1]
                    
                    try:
                        archetype_data = json.loads(line)
                        archetype = Archetype(
                            name=archetype_data['name'],
                            description=archetype_data['description']
                        )
                        # Store with normalized key
                        key = archetype_data['name'].lower().replace(" ", "_")
                        self._archetypes[key] = archetype
                    except json.JSONDecodeError:
                        # Skip malformed lines
                        continue
    
    def get_archetype(self, name: str) -> Optional[Archetype]:
        """Get an archetype by name."""
        return self._archetypes.get(name.lower().replace(" ", "_"))
    
    def get_all_archetypes(self) -> List[Archetype]:
        """Get all archetypes."""
        return list(self._archetypes.values())
    
    def list_archetype_names(self) -> List[str]:
        """List all archetype names."""
        return [archetype.name for archetype in self._archetypes.values()]
    
    def search_archetypes(self, search_term: str) -> List[Archetype]:
        """Search for archetypes by name or description."""
        search_term = search_term.lower()
        results = []
        
        for archetype in self._archetypes.values():
            if (search_term in archetype.name.lower() or 
                search_term in archetype.description.lower()):
                results.append(archetype)
        
        return results