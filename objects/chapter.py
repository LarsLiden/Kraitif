"""
Chapter Implementation

This module implements a Chapter object that represents a chapter in a story
with metadata about narrative function, character impact, and other elements.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
import json
from .narrative_function import NarrativeFunctionEnum
from .continuity_state import ContinuityState


@dataclass
class Chapter:
    """Represents a chapter in a story with narrative metadata, summary, and continuity state."""
    
    chapter_number: int
    title: str
    overview: str
    character_impact: List[Dict[str, str]] = field(default_factory=list)
    point_of_view: Optional[str] = None
    narrative_function: Optional[NarrativeFunctionEnum] = None
    foreshadow_or_echo: Optional[str] = None
    scene_highlights: Optional[str] = None
    summary: Optional[str] = None
    continuity_state: ContinuityState = field(default_factory=ContinuityState)
    chapter_text: Optional[str] = None
    
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
            'scene_highlights': self.scene_highlights,
            'summary': self.summary,
            'continuity_state': self.continuity_state.to_dict(),
            'chapter_text': self.chapter_text
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
            
            # Set summary (optional)
            summary = data.get('summary')
            if summary:
                chapter.summary = str(summary)
            
            # Set chapter_text (optional)
            chapter_text = data.get('chapter_text')
            if chapter_text:
                chapter.chapter_text = str(chapter_text)
            
            # Set continuity state (optional)
            continuity_data = data.get('continuity_state', {})
            if continuity_data:
                continuity_state = ContinuityState.from_dict(continuity_data)
                if continuity_state is not None:
                    chapter.continuity_state = continuity_state
            
            return chapter
            
        except (ValueError, TypeError):
            return None
    
    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=2)
    
    @classmethod
    def from_json(cls, json_str: str) -> Optional['Chapter']:
        """Create chapter from JSON string. Returns None if invalid."""
        try:
            data = json.loads(json_str)
            return cls.from_dict(data)
        except json.JSONDecodeError:
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
        
        if self.summary:
            summary_preview = self.summary[:30] + "..." if len(self.summary) > 30 else self.summary
            parts.append(f"Summary: {summary_preview}")
        
        # Add continuity info
        if self.continuity_state:
            char_count = len(self.continuity_state.characters)
            obj_count = len(self.continuity_state.objects)
            loc_count = len(self.continuity_state.locations_visited)
            thread_count = len(self.continuity_state.open_plot_threads)
            
            if any([char_count, obj_count, loc_count, thread_count]):
                continuity_parts = []
                if char_count > 0:
                    continuity_parts.append(f"Chars: {char_count}")
                if obj_count > 0:
                    continuity_parts.append(f"Objs: {obj_count}")
                if loc_count > 0:
                    continuity_parts.append(f"Locs: {loc_count}")
                if thread_count > 0:
                    continuity_parts.append(f"Threads: {thread_count}")
                
                if continuity_parts:
                    parts.append(f"Continuity: {', '.join(continuity_parts)}")
        
        return " | ".join(parts)