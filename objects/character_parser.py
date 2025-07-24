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
        emotional_function_str = data.get('emotional_function', '').strip()
        
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
    
    except (KeyError, TypeError, AttributeError):
        return None


def _find_archetype_enum(archetype_str: str) -> Optional[ArchetypeEnum]:
    """Find ArchetypeEnum by string value."""
    for archetype in ArchetypeEnum:
        if archetype.value == archetype_str:
            return archetype
    return None


def _find_functional_role_enum(role_str: str) -> Optional[FunctionalRoleEnum]:
    """Find FunctionalRoleEnum by string value."""
    for role in FunctionalRoleEnum:
        if role.value == role_str:
            return role
    return None


def _find_emotional_function_enum(function_str: str) -> Optional[EmotionalFunctionEnum]:
    """Find EmotionalFunctionEnum by string value."""
    for function in EmotionalFunctionEnum:
        if function.value == function_str:
            return function
    return None