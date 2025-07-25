"""
Prompt type enumeration for categorizing different types of AI prompts.

This module defines the PromptType enum used for debugging and categorizing
AI prompt requests throughout the application.
"""

from enum import Enum


class PromptType(Enum):
    """Enumeration of different prompt types used in the application."""
    
    PLOT_LINES = "plot_lines"
    CHARACTERS = "characters"
    CHAPTER_OUTLINE = "chapter_outline"
    CHAPTER = "chapter"
    # Additional prompt types can be added here as the application evolves
    # STORY_GENERATION = "story_generation"
    # CHARACTER_DEVELOPMENT = "character_development"
    # DIALOGUE_GENERATION = "dialogue_generation"