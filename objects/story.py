"""
Story Implementation

This module implements a Story object that backs user choices like genre and sub-genre.
"""

import json
from typing import Optional, Dict, Any, List, Union
from .genre import Genre, SubGenre, GenreRegistry
from .archetype import ArchetypeRegistry, ArchetypeEnum
from .style import Style, StyleRegistry
from .story_types import StoryTypeRegistry
from .emotional_function import EmotionalFunction, EmotionalFunctionRegistry
from .plot_line import PlotLine
from .functional_role import FunctionalRole, FunctionalRoleRegistry
from .character import Character

class Story:
    """Represents a story with user-selected genre and sub-genre."""
    
    def __init__(self):
        """Initialize a new story."""
        self.genre: Optional[Genre] = None
        self.sub_genre: Optional[SubGenre] = None
        self._genre_registry = GenreRegistry()
        self._archetype_registry = ArchetypeRegistry()
        self._style_registry = StyleRegistry()
        self._story_type_registry = StoryTypeRegistry()
        self._emotional_function_registry = EmotionalFunctionRegistry()
        self._functional_role_registry = FunctionalRoleRegistry()

        # Story type selections
        self.story_type_name: Optional[str] = None
        self.subtype_name: Optional[str] = None
        self.key_theme: Optional[str] = None
        self.core_arc: Optional[str] = None
        # Writing style selection
        self.writing_style: Optional[Style] = None
        
        # Archetype selections - separate protagonist and secondary characters
        self.protagonist_archetype: Optional[ArchetypeEnum] = None
        self.secondary_archetypes: List[ArchetypeEnum] = []

        # Character selections
        self.characters: List[Character] = []

        # Plot line selection
        self.selected_plot_line: Optional[PlotLine] = None
        
        # Expanded plot line from character generation
        self.expanded_plot_line: Optional[str] = None
    
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
    
    def get_available_emotional_functions(self) -> List[EmotionalFunction]:
        """Get all available emotional functions."""
        return self._emotional_function_registry.get_all_emotional_functions()
    
    def get_available_functional_roles(self) -> List[FunctionalRole]:
        """Get all available functional roles."""
        return self._functional_role_registry.get_all_functional_roles()
    
    def add_character(self, character: Character) -> bool:
        """Add a character to the story. Returns True if successful."""
        if character and isinstance(character, Character):
            self.characters.append(character)
            return True
        return False
    
    def remove_character(self, character_name: str) -> bool:
        """Remove a character from the story by name. Returns True if successful."""
        for i, character in enumerate(self.characters):
            if character.name == character_name:
                self.characters.pop(i)
                return True
        return False
    
    def get_character(self, character_name: str) -> Optional[Character]:
        """Get a character by name."""
        for character in self.characters:
            if character.name == character_name:
                return character
        return None
    
    def get_protagonist(self) -> Optional[Character]:
        """Get the protagonist character (first character with Protagonist functional role)."""
        from .functional_role import FunctionalRoleEnum
        for character in self.characters:
            if character.functional_role == FunctionalRoleEnum.PROTAGONIST:
                return character
        return None
    
    def get_secondary_characters(self) -> List[Character]:
        """Get all non-protagonist characters."""
        from .functional_role import FunctionalRoleEnum
        return [char for char in self.characters if char.functional_role != FunctionalRoleEnum.PROTAGONIST]
    
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
    
    def set_protagonist_archetype(self, archetype: Union[str, ArchetypeEnum]) -> bool:
        """Set the protagonist archetype by name or enum. Returns True if successful."""
        if archetype:
            if isinstance(archetype, str):
                # Convert string to enum
                try:
                    enum_value = ArchetypeEnum(archetype)
                    self.protagonist_archetype = enum_value
                    return True
                except ValueError:
                    return False
            elif isinstance(archetype, ArchetypeEnum):
                self.protagonist_archetype = archetype
                return True
        return False
    
    def set_secondary_archetypes(self, archetypes: Union[List[str], List[ArchetypeEnum]]) -> bool:
        """Set secondary archetypes by names or enums. Returns True if successful."""
        if isinstance(archetypes, list):
            # Convert all items to enum values
            enum_archetypes = []
            for archetype in archetypes:
                if archetype and isinstance(archetype, str):
                    try:
                        enum_value = ArchetypeEnum(archetype)
                        enum_archetypes.append(enum_value)
                    except ValueError:
                        # If any archetype is invalid, return False
                        return False
                elif isinstance(archetype, ArchetypeEnum):
                    enum_archetypes.append(archetype)
                elif archetype:  # Any non-empty invalid type
                    return False
            
            self.secondary_archetypes = enum_archetypes
            return True
        return False
    
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
        
        if self.characters:
            protagonist = self.get_protagonist()
            if protagonist:
                parts.append(f"Protagonist: {protagonist.name} ({protagonist.archetype.value})")
            
            secondary_chars = self.get_secondary_characters()
            if secondary_chars:
                char_names = [f"{char.name} ({char.archetype.value})" for char in secondary_chars]
                parts.append(f"Secondary: {', '.join(char_names)}")
        
        # Also show simple archetype fields (separate from character objects)
        if self.protagonist_archetype:
            parts.append(f"Protagonist Archetype: {self.protagonist_archetype.value}")
        
        if self.secondary_archetypes:
            archetype_names = [archetype.value for archetype in self.secondary_archetypes]
            parts.append(f"Secondary Archetypes: {', '.join(archetype_names)}")

        return " | ".join(parts) if parts else "Story with no selections"
    
    def to_prompt_text(self) -> str:
        """Convert story selections to a formatted text suitable for LLM prompts."""
        lines = []
        lines.append("STORY CONFIGURATION:")
        lines.append("=" * 50)
        
        # Story Type and Subtype with detailed information
        if self.story_type_name and self.subtype_name:
            story_type = self._story_type_registry.get_story_type(self.story_type_name)
            if story_type:
                lines.append(f"Story Type: {self.story_type_name}")
                lines.append(f"Description: {story_type.description}")
                if story_type.examples:
                    lines.append(f"Examples: {', '.join(story_type.examples)}")
                
                # Add subtype details
                subtype = story_type.get_subtype(self.subtype_name)
                if subtype:
                    lines.append(f"Story Subtype: {self.subtype_name}")
                    lines.append(f"Subtype Description: {subtype.description}")
                    if subtype.examples:
                        lines.append(f"Subtype Examples: {', '.join(subtype.examples)}")
                
                # Add story type specific details
                if story_type.narrative_rhythm:
                    lines.append(f"Narrative Rhythm: {story_type.narrative_rhythm}")
                
                if story_type.emotional_arc:
                    lines.append(f"Emotional Arc: {' → '.join(story_type.emotional_arc)}")
                
                if story_type.key_moment:
                    lines.append("Key Moments:")
                    for moment in story_type.key_moment:
                        lines.append(f"  • {moment}")
                
                # Add user-selected theme and core arc
                if self.key_theme:
                    lines.append(f"Selected Key Theme: {self.key_theme}")
                
                if self.core_arc:
                    lines.append(f"Selected Core Arc: {self.core_arc}")
                
                lines.append("")
        
        # Genre Information with detailed information
        if self.genre:
            lines.append(f"Genre: {self.genre.name}")
            
            if self.sub_genre:
                lines.append(f"Sub-Genre: {self.sub_genre.name}")
                
                # Add sub-genre details if available
                if hasattr(self.sub_genre, 'plot') and self.sub_genre.plot:
                    lines.append(f"Plot Type: {self.sub_genre.plot}")
                    
                if hasattr(self.sub_genre, 'examples') and self.sub_genre.examples:
                    lines.append(f"Genre Examples: {', '.join(self.sub_genre.examples)}")
            
            lines.append("")
        
        # Writing Style with detailed information
        if self.writing_style:
            lines.append(f"Writing Style: {self.writing_style.name}")
            lines.append(f"Style Description: {self.writing_style.description}")
            
            if hasattr(self.writing_style, 'characteristics') and self.writing_style.characteristics:
                lines.append("Style Characteristics:")
                for characteristic in self.writing_style.characteristics:
                    lines.append(f"  • {characteristic}")
            
            if hasattr(self.writing_style, 'examples') and self.writing_style.examples:
                lines.append(f"Style Examples: {', '.join(self.writing_style.examples)}")
            
            lines.append("")
        
        # Character Archetypes with detailed descriptions
        # Show full Character objects if they exist
        if self.characters:
            lines.append("CHARACTER ARCHETYPES:")
            
            protagonist = self.get_protagonist()
            if protagonist:
                archetype_obj = self._archetype_registry.get_archetype(protagonist.archetype.value)
                lines.append(f"Protagonist: {protagonist.name}")
                lines.append(f"  Archetype: {protagonist.archetype.value}")
                if archetype_obj:
                    lines.append(f"  Description: {archetype_obj.description}")
                lines.append(f"  Functional Role: {protagonist.functional_role.value}")
                lines.append(f"  Emotional Function: {protagonist.emotional_function.value}")
                emotion_func = self._emotional_function_registry.get_emotional_function(protagonist.emotional_function.value)
                if emotion_func:
                    lines.append(f"    Description: {emotion_func.description}")
                if protagonist.backstory:
                    lines.append(f"  Backstory: {protagonist.backstory}")
                if protagonist.character_arc:
                    lines.append(f"  Character Arc: {protagonist.character_arc}")
            
            secondary_chars = self.get_secondary_characters()
            if secondary_chars:
                lines.append("Secondary Characters:")
                for character in secondary_chars:
                    archetype_obj = self._archetype_registry.get_archetype(character.archetype.value)
                    lines.append(f"  • {character.name}")
                    lines.append(f"    Archetype: {character.archetype.value}")
                    if archetype_obj:
                        lines.append(f"    Description: {archetype_obj.description}")
                    lines.append(f"    Functional Role: {character.functional_role.value}")
                    lines.append(f"    Emotional Function: {character.emotional_function.value}")
                    emotion_func = self._emotional_function_registry.get_emotional_function(character.emotional_function.value)
                    if emotion_func:
                        lines.append(f"      Description: {emotion_func.description}")
                    if character.backstory:
                        lines.append(f"    Backstory: {character.backstory}")
                    if character.character_arc:
                        lines.append(f"    Character Arc: {character.character_arc}")
            elif protagonist and self.sub_genre:
                # If no secondary characters are defined, suggest typical ones for the sub-genre
                typical_secondary = [arch for arch in self.get_typical_archetypes() 
                                   if arch != protagonist.archetype.value]
                if typical_secondary:
                    lines.append("Suggested Secondary Characters (typical for this genre):")
                    for archetype_name in typical_secondary:
                        archetype = self._archetype_registry.get_archetype(archetype_name)
                        lines.append(f"  • {archetype_name}")
                        if archetype:
                            lines.append(f"    Description: {archetype.description}")
            
            lines.append("")
        

        # Plot Line Information
        if self.selected_plot_line:
            lines.append("SELECTED PLOT LINE:")
            lines.append(f"Name: {self.selected_plot_line.name}")
            lines.append(f"Plot Line: {self.selected_plot_line.plotline}")
            lines.append("")

        # Show archetype selections from web UI (protagonist_archetype and secondary_archetypes fields)
        # These are separate from the Character objects and used by the current web UI
        # Only show these if there are NO Character objects
        if not self.characters and (self.protagonist_archetype or self.secondary_archetypes):
            lines.append("CHARACTER ARCHETYPES:")
            
            # Show protagonist archetype
            if self.protagonist_archetype:
                archetype_obj = self._archetype_registry.get_archetype(self.protagonist_archetype.value)
                lines.append(f"Protagonist Archetype: {self.protagonist_archetype.value}")
                if archetype_obj:
                    lines.append(f"  Description: {archetype_obj.description}")
            
            # Show secondary archetypes
            if self.secondary_archetypes:
                lines.append("Secondary Character Archetypes:")
                for archetype_enum in self.secondary_archetypes:
                    archetype_obj = self._archetype_registry.get_archetype(archetype_enum.value)
                    lines.append(f"  • {archetype_enum.value}")
                    if archetype_obj:
                        lines.append(f"    Description: {archetype_obj.description}")
            
            # If no secondary archetypes are selected, suggest typical ones for the sub-genre
            elif not self.secondary_archetypes and self.protagonist_archetype and self.sub_genre:
                typical_secondary = [arch for arch in self.get_typical_archetypes() 
                                   if arch != self.protagonist_archetype.value]
                if typical_secondary:
                    lines.append("Suggested Secondary Character Archetypes (typical for this genre):")
                    for archetype_name in typical_secondary:
                        archetype = self._archetype_registry.get_archetype(archetype_name)
                        lines.append(f"  • {archetype_name}")
                        if archetype:
                            lines.append(f"    Description: {archetype.description}")
            
            lines.append("")
        
        # Add a footer note
        lines.append("=" * 50)
        lines.append("Use this configuration to guide the story creation process.")
        
        return "\n".join(lines)

    def to_prompt_text_for_chapter_outline(self) -> str:
        """
        Convert story selections to a formatted text suitable for chapter outline prompts.
        This version excludes protagonist_archetype, secondary_archetypes, and selected_plot_line fields.
        """
        lines = []
        lines.append("STORY CONFIGURATION:")
        lines.append("=" * 50)
        
        # Story Type and Subtype with detailed information
        if self.story_type_name and self.subtype_name:
            story_type = self._story_type_registry.get_story_type(self.story_type_name)
            if story_type:
                lines.append(f"Story Type: {self.story_type_name}")
                lines.append(f"Description: {story_type.description}")
                if story_type.examples:
                    lines.append(f"Examples: {', '.join(story_type.examples)}")
                
                # Add subtype details
                subtype = story_type.get_subtype(self.subtype_name)
                if subtype:
                    lines.append(f"Story Subtype: {self.subtype_name}")
                    lines.append(f"Subtype Description: {subtype.description}")
                    if subtype.examples:
                        lines.append(f"Subtype Examples: {', '.join(subtype.examples)}")
                
                # Add story type specific details
                if story_type.narrative_rhythm:
                    lines.append(f"Narrative Rhythm: {story_type.narrative_rhythm}")
                
                if story_type.emotional_arc:
                    lines.append(f"Emotional Arc: {' → '.join(story_type.emotional_arc)}")
                
                if story_type.key_moment:
                    lines.append("Key Moments:")
                    for moment in story_type.key_moment:
                        lines.append(f"  • {moment}")
                
                # Add user-selected theme and core arc
                if self.key_theme:
                    lines.append(f"Selected Key Theme: {self.key_theme}")
                
                if self.core_arc:
                    lines.append(f"Selected Core Arc: {self.core_arc}")
                
                lines.append("")
        
        # Genre Information with detailed information
        if self.genre:
            lines.append(f"Genre: {self.genre.name}")
            
            if self.sub_genre:
                lines.append(f"Sub-Genre: {self.sub_genre.name}")
                
                # Add sub-genre details if available
                if hasattr(self.sub_genre, 'plot') and self.sub_genre.plot:
                    lines.append(f"Plot Type: {self.sub_genre.plot}")
                    
                if hasattr(self.sub_genre, 'examples') and self.sub_genre.examples:
                    lines.append(f"Genre Examples: {', '.join(self.sub_genre.examples)}")
            
            lines.append("")
        
        # Writing Style with detailed information
        if self.writing_style:
            lines.append(f"Writing Style: {self.writing_style.name}")
            lines.append(f"Style Description: {self.writing_style.description}")
            
            if hasattr(self.writing_style, 'characteristics') and self.writing_style.characteristics:
                lines.append("Style Characteristics:")
                for characteristic in self.writing_style.characteristics:
                    lines.append(f"  • {characteristic}")
            
            if hasattr(self.writing_style, 'examples') and self.writing_style.examples:
                lines.append(f"Style Examples: {', '.join(self.writing_style.examples)}")
            
            lines.append("")
        
        # Character Archetypes with detailed descriptions - ONLY show full Character objects if they exist
        # Exclude protagonist_archetype, secondary_archetypes, and selected_plot_line fields
        if self.characters:
            lines.append("CHARACTER ARCHETYPES:")
            
            protagonist = self.get_protagonist()
            if protagonist:
                archetype_obj = self._archetype_registry.get_archetype(protagonist.archetype.value)
                lines.append(f"Protagonist: {protagonist.name}")
                lines.append(f"  Archetype: {protagonist.archetype.value}")
                if archetype_obj:
                    lines.append(f"  Description: {archetype_obj.description}")
                lines.append(f"  Functional Role: {protagonist.functional_role.value}")
                lines.append(f"  Emotional Function: {protagonist.emotional_function.value}")
                emotion_func = self._emotional_function_registry.get_emotional_function(protagonist.emotional_function.value)
                if emotion_func:
                    lines.append(f"    Description: {emotion_func.description}")
                if protagonist.backstory:
                    lines.append(f"  Backstory: {protagonist.backstory}")
                if protagonist.character_arc:
                    lines.append(f"  Character Arc: {protagonist.character_arc}")
            
            secondary_chars = self.get_secondary_characters()
            if secondary_chars:
                lines.append("Secondary Characters:")
                for character in secondary_chars:
                    archetype_obj = self._archetype_registry.get_archetype(character.archetype.value)
                    lines.append(f"  • {character.name}")
                    lines.append(f"    Archetype: {character.archetype.value}")
                    if archetype_obj:
                        lines.append(f"    Description: {archetype_obj.description}")
                    lines.append(f"    Functional Role: {character.functional_role.value}")
                    lines.append(f"    Emotional Function: {character.emotional_function.value}")
                    emotion_func = self._emotional_function_registry.get_emotional_function(character.emotional_function.value)
                    if emotion_func:
                        lines.append(f"      Description: {emotion_func.description}")
                    if character.backstory:
                        lines.append(f"    Backstory: {character.backstory}")
                    if character.character_arc:
                        lines.append(f"    Character Arc: {character.character_arc}")
            elif protagonist and self.sub_genre:
                # If no secondary characters are defined, suggest typical ones for the sub-genre
                typical_secondary = [arch for arch in self.get_typical_archetypes() 
                                   if arch != protagonist.archetype.value]
                if typical_secondary:
                    lines.append("Suggested Secondary Characters (typical for this genre):")
                    for archetype_name in typical_secondary:
                        archetype = self._archetype_registry.get_archetype(archetype_name)
                        lines.append(f"  • {archetype_name}")
                        if archetype:
                            lines.append(f"    Description: {archetype.description}")
            
            lines.append("")
        
        # Add expanded plot line if available (excludes selected_plot_line)
        if self.expanded_plot_line:
            lines.append("EXPANDED PLOT LINE:")
            lines.append(self.expanded_plot_line)
            lines.append("")
        
        # Add a footer note
        lines.append("=" * 50)
        lines.append("Use this configuration to guide the story creation process.")
        
        return "\n".join(lines)
    
    def set_selected_plot_line(self, plot_line: PlotLine) -> bool:
        """Set the selected plot line for the story."""
        if plot_line and hasattr(plot_line, 'name') and hasattr(plot_line, 'plotline'):
            self.selected_plot_line = plot_line
            return True
        return False
    
    def get_selected_plot_line(self) -> Optional[PlotLine]:
        """Get the selected plot line."""
        return self.selected_plot_line
    
    def clear_selected_plot_line(self) -> None:
        """Clear the selected plot line."""
        self.selected_plot_line = None
    
    def set_expanded_plot_line(self, expanded_plot_line: str) -> bool:
        """Set the expanded plot line. Returns True if successful."""
        if expanded_plot_line and isinstance(expanded_plot_line, str):
            self.expanded_plot_line = expanded_plot_line.strip()
            return True
        return False
    
    def clear_expanded_plot_line(self) -> None:
        """Clear the expanded plot line."""
        self.expanded_plot_line = None
    
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
            'protagonist_archetype': self.protagonist_archetype.value if self.protagonist_archetype else None,
            'secondary_archetypes': [archetype.value for archetype in self.secondary_archetypes],
            'characters': [char.to_dict() for char in self.characters],
            'selected_plot_line': self.selected_plot_line.to_dict() if self.selected_plot_line else None,
            'expanded_plot_line': self.expanded_plot_line
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
            
            # Load characters
            characters_data = data.get('characters', [])
            self.characters = []
            for char_data in characters_data:
                character = Character.from_dict(char_data)
                if character:
                    self.characters.append(character)
            
            # Load selected plot line
            selected_plot_line_data = data.get('selected_plot_line')
            if selected_plot_line_data and isinstance(selected_plot_line_data, dict):
                if 'name' in selected_plot_line_data and 'plotline' in selected_plot_line_data:
                    plot_line = PlotLine(
                        name=selected_plot_line_data['name'],
                        plotline=selected_plot_line_data['plotline']
                    )
                    self.set_selected_plot_line(plot_line)
            
            # Load expanded plot line
            self.expanded_plot_line = data.get('expanded_plot_line')
            
            # Load archetype fields - convert strings to enums
            protagonist_archetype_str = data.get('protagonist_archetype')
            if protagonist_archetype_str:
                self.set_protagonist_archetype(protagonist_archetype_str)
            
            secondary_archetypes_strs = data.get('secondary_archetypes', [])
            if secondary_archetypes_strs:
                self.set_secondary_archetypes(secondary_archetypes_strs)
                
            return True
        except (json.JSONDecodeError, KeyError, TypeError):
            return False