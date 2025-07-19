"""
Story Implementation

This module implements a Story object that backs user choices like genre and sub-genre.
"""

import json
from typing import Optional, Dict, Any
from genre import Genre, SubGenre, GenreRegistry


class Story:
    """Represents a story with user-selected genre and sub-genre."""
    
    def __init__(self):
        """Initialize a new story."""
        self.genre: Optional[Genre] = None
        self.sub_genre: Optional[SubGenre] = None
        self._genre_registry = GenreRegistry()
        # Story type selections
        self.story_type_name: Optional[str] = None
        self.subtype_name: Optional[str] = None
        self.key_theme: Optional[str] = None
        self.core_arc: Optional[str] = None
    
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
    
    def __str__(self) -> str:
        """String representation of the story."""
        parts = []
        if self.genre:
            parts.append(f"Genre: {self.genre.name}")
        if self.sub_genre:
            parts.append(f"Sub-genre: {self.sub_genre.name}")
        if self.story_type_name and self.subtype_name:
            parts.append(f"Story Type: {self.story_type_name} - {self.subtype_name}")
        return " | ".join(parts) if parts else "Story with no selections"
    
    def to_json(self) -> str:
        """Serialize story to JSON string."""
        data = {
            'story_type_name': self.story_type_name,
            'subtype_name': self.subtype_name,
            'key_theme': self.key_theme,
            'core_arc': self.core_arc,
            'genre_name': self.genre.name if self.genre else None,
            'sub_genre_name': self.sub_genre.name if self.sub_genre else None
        }
        return json.dumps(data, indent=2)
    
    def from_json(self, json_str: str) -> bool:
        """Load story from JSON string. Returns True if successful."""
        try:
            data = json.loads(json_str)
            
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
                
            return True
        except (json.JSONDecodeError, KeyError, TypeError):
            return False