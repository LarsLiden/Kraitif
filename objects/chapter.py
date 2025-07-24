"""
Chapter Implementation

This module implements a Chapter object that represents a chapter in a story
with metadata about narrative function, character impact, and other elements.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
import json
from .narrative_function import NarrativeFunctionEnum


@dataclass
class Chapter:
    """Represents a chapter in a story with narrative metadata."""
    
    chapter_number: int
    title: str
    overview: str
    character_impact: List[Dict[str, str]] = field(default_factory=list)
    point_of_view: Optional[str] = None
    narrative_function: Optional[NarrativeFunctionEnum] = None
    foreshadow_or_echo: Optional[str] = None
    scene_highlights: Optional[str] = None
    
    def __post_init__(self):
        """Validate the chapter data after initialization."""
        if self.chapter_number < 1:
            raise ValueError("Chapter number must be >= 1")
        
        if not self.title or not self.title.strip():
            raise ValueError("Chapter title cannot be empty")
            
        if not self.overview or not self.overview.strip():
            raise ValueError("Chapter overview cannot be empty")
    
    def add_character_impact(self, character: str, effect: str) -> bool:
        """Add a character impact entry. Returns True if successful."""
        if not character or not character.strip():
            return False
        if not effect or not effect.strip():
            return False
            
        # Check if character already has an impact entry
        for impact in self.character_impact:
            if impact.get('character', '').lower() == character.lower():
                # Update existing entry
                impact['effect'] = effect
                return True
        
        # Add new entry
        self.character_impact.append({
            'character': character.strip(),
            'effect': effect.strip()
        })
        return True
    
    def remove_character_impact(self, character: str) -> bool:
        """Remove a character impact entry. Returns True if successful."""
        if not character:
            return False
            
        for i, impact in enumerate(self.character_impact):
            if impact.get('character', '').lower() == character.lower():
                self.character_impact.pop(i)
                return True
        return False
    
    def get_character_impact(self, character: str) -> Optional[str]:
        """Get the impact description for a specific character."""
        if not character:
            return None
            
        for impact in self.character_impact:
            if impact.get('character', '').lower() == character.lower():
                return impact.get('effect')
        return None
    
    def set_narrative_function(self, narrative_function: str) -> bool:
        """Set the narrative function by name. Returns True if successful."""
        if not narrative_function:
            self.narrative_function = None
            return True
            
        try:
            self.narrative_function = NarrativeFunctionEnum(narrative_function)
            return True
        except ValueError:
            return False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert chapter to dictionary for JSON serialization."""
        return {
            'chapter_number': self.chapter_number,
            'title': self.title,
            'overview': self.overview,
            'character_impact': self.character_impact,
            'point_of_view': self.point_of_view,
            'narrative_function': self.narrative_function.value if self.narrative_function else None,
            'foreshadow_or_echo': self.foreshadow_or_echo,
            'scene_highlights': self.scene_highlights
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Optional['Chapter']:
        """Create a chapter from dictionary data. Returns None if invalid."""
        try:
            if not isinstance(data, dict):
                return None
            
            # Required fields
            chapter_number = data.get('chapter_number')
            title = data.get('title')
            overview = data.get('overview')
            
            if not all([chapter_number is not None, title, overview]):
                return None
            
            # Create chapter with required fields
            chapter = cls(
                chapter_number=int(chapter_number),
                title=str(title),
                overview=str(overview)
            )
            
            # Set optional fields
            character_impact = data.get('character_impact', [])
            if isinstance(character_impact, list):
                chapter.character_impact = character_impact
            
            point_of_view = data.get('point_of_view')
            if point_of_view:
                chapter.point_of_view = str(point_of_view)
            
            narrative_function = data.get('narrative_function')
            if narrative_function:
                chapter.set_narrative_function(narrative_function)
            
            foreshadow_or_echo = data.get('foreshadow_or_echo')
            if foreshadow_or_echo:
                chapter.foreshadow_or_echo = str(foreshadow_or_echo)
            
            scene_highlights = data.get('scene_highlights')
            if scene_highlights:
                chapter.scene_highlights = str(scene_highlights)
            
            return chapter
            
        except (ValueError, TypeError):
            return None
    
    def __str__(self) -> str:
        """String representation of the chapter."""
        parts = [f"Chapter {self.chapter_number}: {self.title}"]
        
        if self.narrative_function:
            parts.append(f"Function: {self.narrative_function.value}")
        
        if self.point_of_view:
            parts.append(f"POV: {self.point_of_view}")
        
        if self.character_impact:
            char_count = len(self.character_impact)
            parts.append(f"Characters affected: {char_count}")
        
        return " | ".join(parts)