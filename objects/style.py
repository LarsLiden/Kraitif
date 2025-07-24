"""
Writing Styles Implementation

This module implements writing styles loaded from JSON data.
"""

from typing import List, Optional
from dataclasses import dataclass, field
from enum import Enum
import json
import os


class StyleEnum(Enum):
    """Enum for writing style names."""
    CONCISE = "Concise"
    LYRICAL = "Lyrical"
    ANALYTICAL = "Analytical"
    WHIMSICAL = "Whimsical"
    DESCRIPTIVE = "Descriptive"
    CONVERSATIONAL = "Conversational"
    PHILOSOPHICAL = "Philosophical"
    SATIRICAL = "Satirical"
    SUSPENSEFUL = "Suspenseful"
    ROMANTIC = "Romantic"
    DETACHED = "Detached"
    EXPERIMENTAL = "Experimental"
    JOURNALISTIC = "Journalistic"
    REFLECTIVE = "Reflective"
    PERSUASIVE = "Persuasive"


@dataclass
class Style:
    """Represents a writing style."""
    name: str
    description: str
    characteristics: List[str] = field(default_factory=list)
    examples: List[str] = field(default_factory=list)
    
    def __str__(self) -> str:
        return f"{self.name}: {self.description}"


class StyleRegistry:
    """Registry for all writing styles."""
    
    def __init__(self):
        """Initialize registry with styles from JSON data."""
        # Use default data file in the data directory (up one level from objects/)
        data_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "styles.json")
        
        self._styles = {}
        self._load_from_json(data_file)
    
    def _load_from_json(self, file_path: str) -> None:
        """Load styles from JSON file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for style_data in data['styles']:
            # Create style
            style = Style(
                name=style_data['name'],
                description=style_data['description'],
                characteristics=style_data.get('characteristics', []),
                examples=style_data.get('examples', [])
            )
            
            # Store with normalized key
            key = style_data['name'].lower().replace(" ", "_")
            self._styles[key] = style
    
    def get_style(self, name: str) -> Optional[Style]:
        """Get a style by name."""
        return self._styles.get(name.lower().replace(" ", "_"))
    
    def get_all_styles(self) -> List[Style]:
        """Get all styles."""
        return list(self._styles.values())
    
    def list_styles(self) -> List[str]:
        """List all style names."""
        return [style.name for style in self._styles.values()]
    
    def search_styles(self, search_term: str) -> List[Style]:
        """Search for styles by name, description, or characteristics."""
        search_term = search_term.lower()
        results = []
        
        for style in self._styles.values():
            if (search_term in style.name.lower() or 
                search_term in style.description.lower() or
                any(search_term in char.lower() for char in style.characteristics)):
                results.append(style)
        
        return results