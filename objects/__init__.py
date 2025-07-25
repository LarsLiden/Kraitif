"""
Objects package for Kraitif - contains all story-related data models and business logic.
"""

# Import all main objects and registries for easy access
from .story import Story
from .story_types import StoryTypeRegistry
from .archetype import ArchetypeRegistry, ArchetypeEnum
from .genre import GenreRegistry
from .style import StyleRegistry
from .emotional_function import EmotionalFunctionRegistry, EmotionalFunctionEnum
from .functional_role import FunctionalRoleRegistry, FunctionalRoleEnum
from .narrative_function import NarrativeFunctionRegistry, NarrativeFunctionEnum
from .character import Character
from .character_parser import parse_characters_from_ai_response
from .chapter import Chapter
from .continuity_state import ContinuityState
from .continuity_character import ContinuityCharacter
from .continuity_object import ContinuityObject
from .plot_thread import PlotThread
from .plot_line import PlotLine, parse_plot_lines_from_ai_response

__all__ = [
    'Story',
    'StoryTypeRegistry',
    'ArchetypeRegistry', 'ArchetypeEnum',
    'GenreRegistry',
    'StyleRegistry',
    'EmotionalFunctionRegistry', 'EmotionalFunctionEnum',
    'FunctionalRoleRegistry', 'FunctionalRoleEnum',
    'NarrativeFunctionRegistry', 'NarrativeFunctionEnum',
    'Character',
    'parse_characters_from_ai_response',
    'Chapter',
    'ContinuityState', 'ContinuityCharacter', 'ContinuityObject', 'PlotThread',
    'PlotLine', 'parse_plot_lines_from_ai_response'
]