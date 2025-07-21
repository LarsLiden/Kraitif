"""
Story Implementation

This module implements a Story object that backs user choices like genre and sub-genre.
"""

import json
from typing import Optional, Dict, Any, List
from genre import Genre, SubGenre, GenreRegistry
from archetype import ArchetypeRegistry
from style import Style, StyleRegistry


class Story:
    """Represents a story with user-selected genre and sub-genre."""
    
    def __init__(self):
        """Initialize a new story."""
        self.genre: Optional[Genre] = None
        self.sub_genre: Optional[SubGenre] = None
        self._genre_registry = GenreRegistry()
        self._archetype_registry = ArchetypeRegistry()
        self._style_registry = StyleRegistry()
        # Story type selections
        self.story_type_name: Optional[str] = None
        self.subtype_name: Optional[str] = None
        self.key_theme: Optional[str] = None
        self.core_arc: Optional[str] = None
        # Writing style selection
        self.writing_style: Optional[Style] = None
        # Archetype selections - separate protagonist and secondary characters
        self.protagonist_archetype: Optional[str] = None
        self.secondary_archetypes: List[str] = []
        # Keep legacy field for backward compatibility
        self.selected_archetypes: List[str] = []
    
    def set_story_type_selection(self, story_type_name: str, subtype_name: str, 
                                key_theme: Optional[str] = None, core_arc: Optional[str] = None) -> None:
        """Set story type selections."""
        self.story_type_name = story_type_name
        self.subtype_name = subtype_name
        self.key_theme = key_theme
        self.core_arc = core_arc
    
    def get_story_type_selection(self, story_type_name: str, subtype_name: str) -> Dict[str, Any]:
        """Get story type selections for a specific story type and subtype."""
        if self.story_type_name == story_type_name and self.subtype_name == subtype_name:
            return {
                'key_theme': self.key_theme,
                'core_arc': self.core_arc
            }
        return {}
    
    def set_writing_style(self, style_name: str) -> bool:
        """Set the writing style by name. Returns True if successful."""
        style = self._style_registry.get_style(style_name)
        if style:
            self.writing_style = style
            return True
        return False
    
    def get_available_styles(self) -> List[Style]:
        """Get all available writing styles."""
        return self._style_registry.get_all_styles()
    
    def set_genre(self, genre_name: str) -> bool:
        """Set the story genre by name. Returns True if successful."""
        genre = self._genre_registry.get_genre(genre_name)
        if genre:
            self.genre = genre
            # Clear sub-genre if it doesn't belong to this genre
            if self.sub_genre and self.sub_genre not in genre.subgenres:
                self.sub_genre = None
            return True
        return False
    
    def set_sub_genre(self, sub_genre_name: str) -> bool:
        """Set the story sub-genre by name. Returns True if successful."""
        if self.genre:
            sub_genre = self.genre.get_subgenre(sub_genre_name)
            if sub_genre:
                self.sub_genre = sub_genre
                return True
        return False
    
    def get_available_sub_genres(self) -> list:
        """Get available sub-genres for the current genre."""
        if self.genre:
            return self.genre.subgenres
        return []
    
    def add_archetype(self, archetype_name: str) -> bool:
        """Add an archetype to the selection. Returns True if successful."""
        archetype = self._archetype_registry.get_archetype(archetype_name)
        if archetype and archetype_name not in self.selected_archetypes:
            self.selected_archetypes.append(archetype_name)
            return True
        return False
    
    def remove_archetype(self, archetype_name: str) -> bool:
        """Remove an archetype from the selection. Returns True if successful."""
        if archetype_name in self.selected_archetypes:
            self.selected_archetypes.remove(archetype_name)
            return True
        return False
    
    def set_protagonist_archetype(self, archetype_name: str) -> bool:
        """Set the protagonist archetype. Returns True if successful."""
        archetype = self._archetype_registry.get_archetype(archetype_name)
        if archetype:
            self.protagonist_archetype = archetype_name
            # Update legacy field for backward compatibility
            self._update_legacy_selected_archetypes()
            return True
        return False
    
    def set_secondary_archetypes(self, archetype_names: List[str]) -> bool:
        """Set the secondary archetype selection list. Returns True if successful."""
        # Validate all archetypes exist
        valid_archetypes = []
        for name in archetype_names:
            archetype = self._archetype_registry.get_archetype(name)
            if archetype:
                valid_archetypes.append(name)
        
        if len(valid_archetypes) == len(archetype_names):
            self.secondary_archetypes = valid_archetypes
            # Update legacy field for backward compatibility
            self._update_legacy_selected_archetypes()
            return True
        return False
    
    def _update_legacy_selected_archetypes(self):
        """Update the legacy selected_archetypes field for backward compatibility."""
        self.selected_archetypes = []
        if self.protagonist_archetype:
            self.selected_archetypes.append(self.protagonist_archetype)
        self.selected_archetypes.extend(self.secondary_archetypes)

    def set_archetypes(self, archetype_names: List[str]) -> bool:
        """Legacy method - Set the archetype selection list. Returns True if successful."""
        # Validate all archetypes exist
        valid_archetypes = []
        for name in archetype_names:
            archetype = self._archetype_registry.get_archetype(name)
            if archetype:
                valid_archetypes.append(name)
        
        if len(valid_archetypes) == len(archetype_names):
            self.selected_archetypes = valid_archetypes
            # For legacy compatibility, treat first as protagonist, rest as secondary
            if valid_archetypes:
                self.protagonist_archetype = valid_archetypes[0]
                self.secondary_archetypes = valid_archetypes[1:] if len(valid_archetypes) > 1 else []
            else:
                self.protagonist_archetype = None
                self.secondary_archetypes = []
            return True
        return False
    
    def get_typical_archetypes(self) -> List[str]:
        """Get the typical archetypes for the current sub-genre."""
        if self.sub_genre:
            return self.sub_genre.archetypes
        return []
    
    def get_other_archetypes(self) -> List[str]:
        """Get all archetypes that are not typical for the current sub-genre, sorted alphabetically."""
        typical_archetypes = set(self.get_typical_archetypes())
        all_archetypes = self._archetype_registry.list_archetype_names()
        other_archetypes = [name for name in all_archetypes if name not in typical_archetypes]
        return sorted(other_archetypes)
    
    def __str__(self) -> str:
        """String representation of the story."""
        parts = []
        if self.genre:
            parts.append(f"Genre: {self.genre.name}")
        if self.sub_genre:
            parts.append(f"Sub-genre: {self.sub_genre.name}")
        if self.writing_style:
            parts.append(f"Writing Style: {self.writing_style.name}")
        if self.story_type_name and self.subtype_name:
            parts.append(f"Story Type: {self.story_type_name} - {self.subtype_name}")
        if self.protagonist_archetype:
            parts.append(f"Protagonist: {self.protagonist_archetype}")
        if self.secondary_archetypes:
            parts.append(f"Secondary: {', '.join(self.secondary_archetypes)}")
        # Legacy fallback
        elif self.selected_archetypes:
            parts.append(f"Archetypes: {', '.join(self.selected_archetypes)}")
        return " | ".join(parts) if parts else "Story with no selections"
    
    def to_json(self) -> str:
        """Serialize story to JSON string."""
        data = {
            'story_type_name': self.story_type_name,
            'subtype_name': self.subtype_name,
            'key_theme': self.key_theme,
            'core_arc': self.core_arc,
            'genre_name': self.genre.name if self.genre else None,
            'sub_genre_name': self.sub_genre.name if self.sub_genre else None,
            'writing_style_name': self.writing_style.name if self.writing_style else None,
            'protagonist_archetype': self.protagonist_archetype,
            'secondary_archetypes': self.secondary_archetypes,
            'selected_archetypes': self.selected_archetypes  # Keep for backward compatibility
        }
        return json.dumps(data, indent=2)
    
    def from_json(self, json_str: str) -> bool:
        """Load story from JSON string. Returns True if successful."""
        try:
            data = json.loads(json_str)
            
            # Ensure data is a dictionary
            if not isinstance(data, dict):
                return False
            
            # Load story type data
            self.story_type_name = data.get('story_type_name')
            self.subtype_name = data.get('subtype_name')
            self.key_theme = data.get('key_theme')
            self.core_arc = data.get('core_arc')
            
            # Load genre data
            genre_name = data.get('genre_name')
            if genre_name:
                self.set_genre(genre_name)
                
            sub_genre_name = data.get('sub_genre_name')
            if sub_genre_name:
                self.set_sub_genre(sub_genre_name)
            
            # Load writing style data
            writing_style_name = data.get('writing_style_name')
            if writing_style_name:
                self.set_writing_style(writing_style_name)
            
            # Load archetype selections
            protagonist_archetype = data.get('protagonist_archetype')
            if protagonist_archetype:
                self.set_protagonist_archetype(protagonist_archetype)
                
            secondary_archetypes = data.get('secondary_archetypes', [])
            if secondary_archetypes:
                self.set_secondary_archetypes(secondary_archetypes)
            
            # Legacy support for old save format
            selected_archetypes = data.get('selected_archetypes', [])
            if selected_archetypes and not self.protagonist_archetype and not self.secondary_archetypes:
                self.set_archetypes(selected_archetypes)
                
            return True
        except (json.JSONDecodeError, KeyError, TypeError):
            return False