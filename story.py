"""
Story Implementation

This module implements a Story object that backs user choices like genre, sub-genre,
story type, and archetypes.
"""

from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime
import json

from story_types import StoryType, StorySubType, StoryTypeRegistry
from genre import Genre, SubGenre, GenreRegistry
from archetype import Archetype, ArchetypeRegistry


@dataclass
class Story:
    """Represents a story with user-selected characteristics."""
    
    # Core identification
    title: str = ""
    description: str = ""
    
    # User choices
    genre: Optional[Genre] = None
    sub_genre: Optional[SubGenre] = None
    story_type: Optional[StoryType] = None
    story_subtype: Optional[StorySubType] = None
    archetypes: List[Archetype] = field(default_factory=list)
    
    # Additional metadata
    created_at: datetime = field(default_factory=datetime.now)
    tags: List[str] = field(default_factory=list)
    notes: str = ""
    
    def __str__(self) -> str:
        parts = []
        if self.title:
            parts.append(f"Title: {self.title}")
        if self.genre:
            parts.append(f"Genre: {self.genre.name}")
        if self.sub_genre:
            parts.append(f"Sub-genre: {self.sub_genre.name}")
        if self.story_type:
            parts.append(f"Story Type: {self.story_type.name}")
        if self.story_subtype:
            parts.append(f"Story Subtype: {self.story_subtype.name}")
        if self.archetypes:
            parts.append(f"Archetypes: {', '.join(a.name for a in self.archetypes)}")
        
        return " | ".join(parts) if parts else "Empty Story"
    
    def add_archetype(self, archetype: Archetype) -> None:
        """Add an archetype to the story."""
        if archetype not in self.archetypes:
            self.archetypes.append(archetype)
    
    def remove_archetype(self, archetype: Archetype) -> None:
        """Remove an archetype from the story."""
        if archetype in self.archetypes:
            self.archetypes.remove(archetype)
    
    def add_tag(self, tag: str) -> None:
        """Add a tag to the story."""
        if tag not in self.tags:
            self.tags.append(tag)
    
    def remove_tag(self, tag: str) -> None:
        """Remove a tag from the story."""
        if tag in self.tags:
            self.tags.remove(tag)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert story to dictionary for serialization."""
        return {
            'title': self.title,
            'description': self.description,
            'genre': self.genre.name if self.genre else None,
            'sub_genre': self.sub_genre.name if self.sub_genre else None,
            'story_type': self.story_type.name if self.story_type else None,
            'story_subtype': self.story_subtype.name if self.story_subtype else None,
            'archetypes': [a.name for a in self.archetypes],
            'created_at': self.created_at.isoformat(),
            'tags': self.tags,
            'notes': self.notes
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any], 
                  genre_registry: GenreRegistry,
                  story_registry: StoryTypeRegistry,
                  archetype_registry: ArchetypeRegistry) -> 'Story':
        """Create story from dictionary."""
        story = cls(
            title=data.get('title', ''),
            description=data.get('description', ''),
            created_at=datetime.fromisoformat(data.get('created_at', datetime.now().isoformat())),
            tags=data.get('tags', []),
            notes=data.get('notes', '')
        )
        
        # Set genre and sub-genre
        if data.get('genre'):
            genre = genre_registry.get_genre(data['genre'])
            if genre:
                story.genre = genre
                if data.get('sub_genre'):
                    sub_genre = genre.get_subgenre(data['sub_genre'])
                    if sub_genre:
                        story.sub_genre = sub_genre
        
        # Set story type and subtype
        if data.get('story_type'):
            story_type = story_registry.get_story_type(data['story_type'])
            if story_type:
                story.story_type = story_type
                if data.get('story_subtype'):
                    story_subtype = story_type.get_subtype(data['story_subtype'])
                    if story_subtype:
                        story.story_subtype = story_subtype
        
        # Set archetypes
        for archetype_name in data.get('archetypes', []):
            archetype = archetype_registry.get_archetype(archetype_name)
            if archetype:
                story.add_archetype(archetype)
        
        return story
    
    @property
    def is_complete(self) -> bool:
        """Check if the story has all essential components."""
        return all([
            self.title,
            self.genre,
            self.sub_genre,
            self.story_type,
            len(self.archetypes) > 0
        ])
    
    @property
    def completion_percentage(self) -> float:
        """Calculate completion percentage."""
        components = [
            bool(self.title),
            bool(self.description),
            bool(self.genre),
            bool(self.sub_genre),
            bool(self.story_type),
            bool(self.story_subtype),
            bool(self.archetypes)
        ]
        return (sum(components) / len(components)) * 100


class StoryBuilder:
    """Builder class for creating stories step by step."""
    
    def __init__(self):
        """Initialize with registries."""
        self.genre_registry = GenreRegistry()
        self.story_registry = StoryTypeRegistry()
        self.archetype_registry = ArchetypeRegistry()
        self.story = Story()
    
    def set_title(self, title: str) -> 'StoryBuilder':
        """Set the story title."""
        self.story.title = title
        return self
    
    def set_description(self, description: str) -> 'StoryBuilder':
        """Set the story description."""
        self.story.description = description
        return self
    
    def set_genre(self, genre_name: str) -> 'StoryBuilder':
        """Set the story genre."""
        genre = self.genre_registry.get_genre(genre_name)
        if genre:
            self.story.genre = genre
            # Clear sub-genre if it doesn't belong to this genre
            if self.story.sub_genre and self.story.sub_genre not in genre.subgenres:
                self.story.sub_genre = None
        return self
    
    def set_sub_genre(self, sub_genre_name: str) -> 'StoryBuilder':
        """Set the story sub-genre."""
        if self.story.genre:
            sub_genre = self.story.genre.get_subgenre(sub_genre_name)
            if sub_genre:
                self.story.sub_genre = sub_genre
        return self
    
    def set_story_type(self, story_type_name: str) -> 'StoryBuilder':
        """Set the story type."""
        story_type = self.story_registry.get_story_type(story_type_name)
        if story_type:
            self.story.story_type = story_type
            # Clear story subtype if it doesn't belong to this story type
            if self.story.story_subtype and self.story.story_subtype not in story_type.subtypes:
                self.story.story_subtype = None
        return self
    
    def set_story_subtype(self, story_subtype_name: str) -> 'StoryBuilder':
        """Set the story subtype."""
        if self.story.story_type:
            story_subtype = self.story.story_type.get_subtype(story_subtype_name)
            if story_subtype:
                self.story.story_subtype = story_subtype
        return self
    
    def add_archetype(self, archetype_name: str) -> 'StoryBuilder':
        """Add an archetype to the story."""
        archetype = self.archetype_registry.get_archetype(archetype_name)
        if archetype:
            self.story.add_archetype(archetype)
        return self
    
    def add_tag(self, tag: str) -> 'StoryBuilder':
        """Add a tag to the story."""
        self.story.add_tag(tag)
        return self
    
    def set_notes(self, notes: str) -> 'StoryBuilder':
        """Set the story notes."""
        self.story.notes = notes
        return self
    
    def build(self) -> Story:
        """Build and return the story."""
        return self.story
    
    def reset(self) -> 'StoryBuilder':
        """Reset the builder to start a new story."""
        self.story = Story()
        return self
    
    def get_available_sub_genres(self) -> List[SubGenre]:
        """Get available sub-genres for the current genre."""
        if self.story.genre:
            return self.story.genre.subgenres
        return []
    
    def get_available_story_subtypes(self) -> List[StorySubType]:
        """Get available story subtypes for the current story type."""
        if self.story.story_type:
            return self.story.story_type.subtypes
        return []
    
    def get_suggested_archetypes(self) -> List[Archetype]:
        """Get suggested archetypes based on current sub-genre."""
        if self.story.sub_genre and hasattr(self.story.sub_genre, 'archetypes'):
            suggested = []
            for archetype_name in self.story.sub_genre.archetypes:
                archetype = self.archetype_registry.get_archetype(archetype_name)
                if archetype:
                    suggested.append(archetype)
            return suggested
        return []


class StoryRegistry:
    """Registry for managing multiple stories."""
    
    def __init__(self):
        """Initialize the registry."""
        self.stories: List[Story] = []
        self.genre_registry = GenreRegistry()
        self.story_registry = StoryTypeRegistry()
        self.archetype_registry = ArchetypeRegistry()
    
    def add_story(self, story: Story) -> None:
        """Add a story to the registry."""
        self.stories.append(story)
    
    def remove_story(self, story: Story) -> None:
        """Remove a story from the registry."""
        if story in self.stories:
            self.stories.remove(story)
    
    def get_stories_by_genre(self, genre_name: str) -> List[Story]:
        """Get all stories with a specific genre."""
        return [s for s in self.stories if s.genre and s.genre.name.lower() == genre_name.lower()]
    
    def get_stories_by_story_type(self, story_type_name: str) -> List[Story]:
        """Get all stories with a specific story type."""
        return [s for s in self.stories if s.story_type and s.story_type.name.lower() == story_type_name.lower()]
    
    def get_stories_by_archetype(self, archetype_name: str) -> List[Story]:
        """Get all stories containing a specific archetype."""
        return [s for s in self.stories if any(a.name.lower() == archetype_name.lower() for a in s.archetypes)]
    
    def get_complete_stories(self) -> List[Story]:
        """Get all complete stories."""
        return [s for s in self.stories if s.is_complete]
    
    def get_incomplete_stories(self) -> List[Story]:
        """Get all incomplete stories."""
        return [s for s in self.stories if not s.is_complete]
    
    def search_stories(self, query: str) -> List[Story]:
        """Search stories by title, description, or notes."""
        query = query.lower()
        return [s for s in self.stories if 
                query in s.title.lower() or 
                query in s.description.lower() or 
                query in s.notes.lower()]
    
    def save_to_file(self, filename: str) -> None:
        """Save all stories to a JSON file."""
        data = {
            'stories': [story.to_dict() for story in self.stories],
            'saved_at': datetime.now().isoformat()
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def load_from_file(self, filename: str) -> None:
        """Load stories from a JSON file."""
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.stories = []
        for story_data in data.get('stories', []):
            story = Story.from_dict(
                story_data,
                self.genre_registry,
                self.story_registry,
                self.archetype_registry
            )
            self.stories.append(story)