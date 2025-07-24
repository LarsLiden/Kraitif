"""
Character Parser Implementation

This module implements functions to parse characters and expanded plot lines 
from AI responses.
"""

import json
import re
from typing import List, Dict, Any, Tuple, Optional
from .character import Character
from .archetype import ArchetypeEnum
from .functional_role import FunctionalRoleEnum
from .emotional_function import EmotionalFunctionEnum


def parse_characters_from_ai_response(ai_response: str) -> Tuple[Optional[str], List[Character]]:
    """
    Parse characters and expanded plot line from AI response containing structured data.
    
    The AI response should contain a JSON block with the format:
    <STRUCTURED_DATA>
    {
      "expanded_plot_line": "Detailed plot description...",
      "characters": [
        {
          "name": "Character name",
          "archetype": "Archetype name",
          "functional_role": "Functional role name",
          "emotional_function": "Emotional function name",
          "backstory": "Character backstory",
          "character_arc": "Character development arc"
        },
        ...
      ]
    }
    </STRUCTURED_DATA>
    
    Args:
        ai_response: The full AI response text
        
    Returns:
        Tuple of (expanded_plot_line, list_of_characters)
        Returns (None, []) if parsing fails
    """
    expanded_plot_line = None
    characters = []
    
    try:
        # Extract the structured data section
        pattern = r'<STRUCTURED_DATA>\s*({.*?})\s*</STRUCTURED_DATA>'
        match = re.search(pattern, ai_response, re.DOTALL)
        
        if not match:
            # Try without the tags in case AI doesn't include them
            # Look for JSON-like structure with characters array
            json_pattern = r'{\s*"expanded_plot_line".*?"characters"\s*:\s*\[.*?\]\s*}'
            match = re.search(json_pattern, ai_response, re.DOTALL)
            if match:
                json_str = match.group(0)
            else:
                return None, []
        else:
            json_str = match.group(1)
        
        # Parse the JSON
        data = json.loads(json_str)
        
        # Extract expanded plot line
        expanded_plot_line = data.get('expanded_plot_line')
        
        # Extract characters
        if 'characters' in data and isinstance(data['characters'], list):
            for item in data['characters']:
                if isinstance(item, dict):
                    character = _create_character_from_dict(item)
                    if character:
                        characters.append(character)
    
    except (json.JSONDecodeError, KeyError, AttributeError, TypeError) as e:
        # If parsing fails, return None and empty list
        # In a production environment, you might want to log this error
        pass
    
    return expanded_plot_line, characters


def _create_character_from_dict(data: Dict[str, Any]) -> Optional[Character]:
    """
    Create a Character object from a dictionary with proper enum conversion.
    
    Args:
        data: Dictionary containing character data
        
    Returns:
        Character object or None if creation fails
    """
    try:
        # Required fields
        name = data.get('name', '').strip()
        archetype_str = data.get('archetype', '').strip()
        functional_role_str = data.get('functional_role', '').strip()
        
        # Handle common typo: emotional_role vs emotional_function
        emotional_function_str = data.get('emotional_function', '').strip()
        if not emotional_function_str:
            emotional_function_str = data.get('emotional_role', '').strip()
        
        # Optional fields
        backstory = data.get('backstory', '').strip()
        character_arc = data.get('character_arc', '').strip()
        
        # Validate required fields
        if not all([name, archetype_str, functional_role_str, emotional_function_str]):
            return None
        
        # Convert strings to enums
        archetype = _find_archetype_enum(archetype_str)
        functional_role = _find_functional_role_enum(functional_role_str)
        emotional_function = _find_emotional_function_enum(emotional_function_str)
        
        # Validate enum conversions
        if not all([archetype, functional_role, emotional_function]):
            return None
        
        return Character(
            name=name,
            archetype=archetype,
            functional_role=functional_role,
            emotional_function=emotional_function,
            backstory=backstory,
            character_arc=character_arc
        )
    
    except (KeyError, TypeError, AttributeError) as e:
        return None


def _find_archetype_enum(archetype_str: str) -> Optional[ArchetypeEnum]:
    """Find ArchetypeEnum by string value with flexible matching."""
    archetype_str_clean = archetype_str.strip()
    
    # First try exact match
    for archetype in ArchetypeEnum:
        if archetype.value == archetype_str_clean:
            return archetype
    
    # Try case-insensitive match
    for archetype in ArchetypeEnum:
        if archetype.value.lower() == archetype_str_clean.lower():
            return archetype
    
    # Try partial match (if the AI value is contained in or contains the enum value)
    for archetype in ArchetypeEnum:
        if (archetype_str_clean.lower() in archetype.value.lower() or 
            archetype.value.lower() in archetype_str_clean.lower()):
            return archetype
    
    return None


def _find_functional_role_enum(role_str: str) -> Optional[FunctionalRoleEnum]:
    """Find FunctionalRoleEnum by string value with flexible matching."""
    role_str_clean = role_str.strip()
    
    # First try exact match
    for role in FunctionalRoleEnum:
        if role.value == role_str_clean:
            return role
    
    # Try case-insensitive match
    for role in FunctionalRoleEnum:
        if role.value.lower() == role_str_clean.lower():
            return role
    
    # Try partial match
    for role in FunctionalRoleEnum:
        if (role_str_clean.lower() in role.value.lower() or 
            role.value.lower() in role_str_clean.lower()):
            return role
    
    # Try word-based matching for common variations
    role_words = set(role_str_clean.lower().split())
    for role in FunctionalRoleEnum:
        enum_words = set(role.value.lower().split())
        # Check if all input words match enum words (allowing for partial word matches)
        if role_words <= enum_words:  # All input words are in enum words
            return role
        # Check for specific common cases like "Support" vs "Supporting"
        if len(role_words) == len(enum_words):
            matches = 0
            for input_word in role_words:
                for enum_word in enum_words:
                    if input_word in enum_word or enum_word in input_word:
                        matches += 1
                        break
            if matches == len(role_words):
                return role
    
    return None


def _find_emotional_function_enum(function_str: str) -> Optional[EmotionalFunctionEnum]:
    """Find EmotionalFunctionEnum by string value with flexible matching."""
    function_str_clean = function_str.strip()
    
    # First try exact match
    for function in EmotionalFunctionEnum:
        if function.value == function_str_clean:
            return function
    
    # Try case-insensitive match
    for function in EmotionalFunctionEnum:
        if function.value.lower() == function_str_clean.lower():
            return function
    
    # Try partial match
    for function in EmotionalFunctionEnum:
        if (function_str_clean.lower() in function.value.lower() or 
            function.value.lower() in function_str_clean.lower()):
            return function
    
    return None