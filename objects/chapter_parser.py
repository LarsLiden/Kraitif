"""
Chapter Parser Implementation

This module implements parsing of AI responses to extract chapter data
from structured JSON responses.
"""

import json
import re
from typing import List, Optional, Dict, Any
from .chapter import Chapter
from .narrative_function import NarrativeFunctionEnum


def parse_chapters_from_ai_response(ai_response: str) -> List[Chapter]:
    """
    Parse chapters from AI response JSON.
    
    Args:
        ai_response: Raw AI response containing structured JSON
        
    Returns:
        List of Chapter objects parsed from the response
    """
    chapters = []
    
    try:
        # Extract JSON from the response
        json_data = _extract_json_from_response(ai_response)
        if not json_data:
            return chapters
        
        # Get chapters array from JSON
        chapters_data = json_data.get('chapters', [])
        if not isinstance(chapters_data, list):
            return chapters
        
        # Parse each chapter
        for chapter_data in chapters_data:
            chapter = _create_chapter_from_dict(chapter_data)
            if chapter:
                chapters.append(chapter)
        
        return chapters
    
    except (json.JSONDecodeError, ValueError, TypeError) as e:
        print(f"Error parsing chapters from AI response: {e}")
        return chapters


def parse_single_chapter_from_ai_response(ai_response: str, chapter_number: int) -> Optional[Chapter]:
    """
    Parse a single chapter with chapter_text from AI response JSON.
    
    Args:
        ai_response: Raw AI response containing structured JSON with chapter_text
        chapter_number: The chapter number being generated
        
    Returns:
        Chapter object with chapter_text, summary, and continuity_state, or None if parsing fails
    """
    try:
        # Extract JSON from the response
        json_data = _extract_json_from_response(ai_response)
        if not json_data:
            return None
        
        # Create a chapter object from the response
        chapter = _create_single_chapter_from_dict(json_data, chapter_number)
        return chapter
    
    except (json.JSONDecodeError, ValueError, TypeError) as e:
        print(f"Error parsing single chapter from AI response: {e}")
        return None


def _extract_json_from_response(ai_response: str) -> Optional[Dict[str, Any]]:
    """Extract JSON data from AI response."""
    if not ai_response:
        return None
    
    try:
        # First try to parse the entire response as JSON
        return json.loads(ai_response.strip())
    except json.JSONDecodeError:
        pass
    
    # Look for JSON block between markers
    patterns = [
        r'<STRUCTURED_DATA>\s*(\{.*?\})\s*</STRUCTURED_DATA>',
        r'```json\s*(\{.*?\})\s*```',
        r'```\s*(\{.*?\})\s*```',
        r'(\{.*?\})',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, ai_response, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                continue
    
    return None


def _create_chapter_from_dict(chapter_data: Dict[str, Any]) -> Optional[Chapter]:
    """Create a Chapter object from dictionary data."""
    try:
        if not isinstance(chapter_data, dict):
            return None
        
        # Required fields
        chapter_number = chapter_data.get('chapter_number')
        title = chapter_data.get('title', '').strip()
        overview = chapter_data.get('overview', '').strip()
        
        if not all([chapter_number is not None, title, overview]):
            return None
        
        # Create chapter with required fields
        chapter = Chapter(
            chapter_number=int(chapter_number),
            title=title,
            overview=overview
        )
        
        # Set optional fields
        character_impact = chapter_data.get('character_impact', [])
        if isinstance(character_impact, list):
            chapter.character_impact = character_impact
        
        point_of_view = chapter_data.get('point_of_view')
        if point_of_view and isinstance(point_of_view, str):
            chapter.point_of_view = point_of_view.strip()
        
        narrative_function = chapter_data.get('narrative_function')
        if narrative_function and isinstance(narrative_function, str):
            chapter.set_narrative_function(narrative_function.strip())
        
        foreshadow_or_echo = chapter_data.get('foreshadow_or_echo')
        if foreshadow_or_echo and isinstance(foreshadow_or_echo, str):
            chapter.foreshadow_or_echo = foreshadow_or_echo.strip()
        
        scene_highlights = chapter_data.get('scene_highlights')
        if scene_highlights and isinstance(scene_highlights, str):
            chapter.scene_highlights = scene_highlights.strip()
        
        return chapter
        
    except (ValueError, TypeError) as e:
        print(f"Error creating chapter from dict: {e}")
        return None


def _create_single_chapter_from_dict(data: Dict[str, Any], chapter_number: int) -> Optional[Chapter]:
    """Create a Chapter object with chapter_text from dictionary data."""
    try:
        if not isinstance(data, dict):
            return None
        
        # Get required fields from the response
        chapter_text = data.get('chapter_text', '').strip()
        chapter_summary = data.get('chapter_summary', '').strip()
        
        if not chapter_text:
            return None
        
        # Create chapter with minimal required fields - we'll get title and overview from existing chapter
        # For now, use placeholder values that will be updated when merging with existing chapter
        chapter = Chapter(
            chapter_number=chapter_number,
            title=f"Chapter {chapter_number}",  # Placeholder, will be updated
            overview="Generated chapter content"  # Placeholder, will be updated
        )
        
        # Set the generated fields
        chapter.chapter_text = chapter_text
        chapter.summary = chapter_summary
        
        # Parse continuity state if present
        continuity_data = data.get('continuity_state', {})
        if continuity_data and isinstance(continuity_data, dict):
            from .continuity_state import ContinuityState
            continuity_state = ContinuityState.from_dict(continuity_data)
            if continuity_state:
                chapter.continuity_state = continuity_state
        
        return chapter
        
    except (ValueError, TypeError) as e:
        print(f"Error creating single chapter from dict: {e}")
        return None


def validate_chapter_character_names(chapters: List[Chapter], story_character_names: List[str]) -> List[str]:
    """
    Validate that all character names in chapters exist in the story.
    
    Args:
        chapters: List of Chapter objects to validate
        story_character_names: List of character names that exist in the story
        
    Returns:
        List of character names that are referenced in chapters but not in story
    """
    missing_characters = set()
    story_names_lower = [name.lower() for name in story_character_names]
    
    for chapter in chapters:
        # Check point_of_view character
        if chapter.point_of_view:
            if chapter.point_of_view.lower() not in story_names_lower:
                missing_characters.add(chapter.point_of_view)
        
        # Check character_impact characters
        for impact in chapter.character_impact:
            character_name = impact.get('character', '').strip()
            if character_name and character_name.lower() not in story_names_lower:
                missing_characters.add(character_name)
    
    return list(missing_characters)