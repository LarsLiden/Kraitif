"""
Test suite for the chapter outline prompt functionality.

This module tests the specific functionality for generating chapter outline prompts,
including the exclusion of specified fields from the story configuration.
"""

import unittest
from objects.story import Story
from objects.archetype import ArchetypeEnum
from objects.plot_line import PlotLine


class TestChapterOutlineStoryConfiguration(unittest.TestCase):
    """Test cases for the chapter outline story configuration functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.story = Story()
        
    def test_to_prompt_text_for_chapter_outline_excludes_protagonist_archetype(self):
        """Test that protagonist_archetype is excluded from chapter outline prompt."""
        # Set up a story with protagonist archetype
        self.story.protagonist_archetype = ArchetypeEnum.CHOSEN_ONE
        
        # Generate both regular and chapter outline prompts
        regular_prompt = self.story.to_prompt_text()
        chapter_outline_prompt = self.story.to_prompt_text_for_chapter_outline()
        
        # Regular prompt should contain protagonist archetype
        self.assertIn("Protagonist Archetype: Chosen One", regular_prompt)
        
        # Chapter outline prompt should NOT contain protagonist archetype
        self.assertNotIn("Protagonist Archetype: Chosen One", chapter_outline_prompt)
    
    def test_to_prompt_text_for_chapter_outline_excludes_secondary_archetypes(self):
        """Test that secondary_archetypes are excluded from chapter outline prompt."""
        # Set up a story with secondary archetypes
        self.story.protagonist_archetype = ArchetypeEnum.CHOSEN_ONE
        self.story.secondary_archetypes = [ArchetypeEnum.WISE_MENTOR, ArchetypeEnum.LOYAL_COMPANION]
        
        # Generate both regular and chapter outline prompts
        regular_prompt = self.story.to_prompt_text()
        chapter_outline_prompt = self.story.to_prompt_text_for_chapter_outline()
        
        # Regular prompt should contain secondary archetypes
        self.assertIn("Secondary Character Archetypes:", regular_prompt)
        self.assertIn("Wise Mentor", regular_prompt)
        self.assertIn("Loyal Companion", regular_prompt)
        
        # Chapter outline prompt should NOT contain secondary archetypes
        self.assertNotIn("Secondary Character Archetypes:", chapter_outline_prompt)
        self.assertNotIn("Wise Mentor", chapter_outline_prompt)
        self.assertNotIn("Loyal Companion", chapter_outline_prompt)
    
    def test_to_prompt_text_for_chapter_outline_excludes_selected_plot_line(self):
        """Test that selected_plot_line is excluded from chapter outline prompt."""
        # Set up a story with selected plot line
        plot_line = PlotLine("Test Plot", "This is a test plot line description")
        self.story.set_selected_plot_line(plot_line)
        
        # Generate both regular and chapter outline prompts
        regular_prompt = self.story.to_prompt_text()
        chapter_outline_prompt = self.story.to_prompt_text_for_chapter_outline()
        
        # Regular prompt should contain selected plot line
        self.assertIn("SELECTED PLOT LINE:", regular_prompt)
        self.assertIn("Test Plot", regular_prompt)
        self.assertIn("This is a test plot line description", regular_prompt)
        
        # Chapter outline prompt should NOT contain selected plot line
        self.assertNotIn("SELECTED PLOT LINE:", chapter_outline_prompt)
        self.assertNotIn("Test Plot", chapter_outline_prompt)
        # It's okay if the description text appears elsewhere for other reasons
    
    def test_to_prompt_text_for_chapter_outline_includes_expanded_plot_line(self):
        """Test that expanded_plot_line is included in chapter outline prompt."""
        # Set up a story with expanded plot line
        self.story.set_expanded_plot_line("This is an expanded plot line with character details")
        
        # Generate chapter outline prompt
        chapter_outline_prompt = self.story.to_prompt_text_for_chapter_outline()
        
        # Chapter outline prompt should contain expanded plot line
        self.assertIn("EXPANDED PLOT LINE:", chapter_outline_prompt)
        self.assertIn("This is an expanded plot line with character details", chapter_outline_prompt)
    
    def test_to_prompt_text_for_chapter_outline_includes_characters(self):
        """Test that full Character objects are included in chapter outline prompt."""
        from objects.character import Character
        from objects.functional_role import FunctionalRoleEnum
        from objects.emotional_function import EmotionalFunctionEnum
        
        # Set up a story with character objects
        protagonist = Character(
            name="Hero",
            archetype=ArchetypeEnum.CHOSEN_ONE,
            functional_role=FunctionalRoleEnum.PROTAGONIST,
            emotional_function=EmotionalFunctionEnum.SYMPATHETIC_CHARACTER,
            backstory="A young person destined for greatness",
            character_arc="Learns to accept responsibility"
        )
        self.story.characters.append(protagonist)
        
        # Generate chapter outline prompt
        chapter_outline_prompt = self.story.to_prompt_text_for_chapter_outline()
        
        # Chapter outline prompt should contain character details
        self.assertIn("CHARACTER ARCHETYPES:", chapter_outline_prompt)
        self.assertIn("Protagonist: Hero", chapter_outline_prompt)
        self.assertIn("Archetype: Chosen One", chapter_outline_prompt)
        self.assertIn("A young person destined for greatness", chapter_outline_prompt)
        self.assertIn("Learns to accept responsibility", chapter_outline_prompt)
    
    def test_to_prompt_text_for_chapter_outline_includes_common_story_fields(self):
        """Test that common story fields are still included in chapter outline prompt."""
        # Set up a story with various fields - use valid subtype from data
        self.story.set_story_type_selection(
            "Overcoming the Monster", 
            "Predator", 
            "Courage and perseverance triumph over fear and oppression.", 
            "Ordinary person becomes empowered through challenge."
        )
        
        # Generate chapter outline prompt
        chapter_outline_prompt = self.story.to_prompt_text_for_chapter_outline()
        
        # Should include story type information
        self.assertIn("STORY CONFIGURATION:", chapter_outline_prompt)
        self.assertIn("Story Type: Overcoming the Monster", chapter_outline_prompt)
        self.assertIn("Story Subtype: Predator", chapter_outline_prompt)
        self.assertIn("Selected Key Theme: Courage and perseverance triumph over fear and oppression.", chapter_outline_prompt)
        self.assertIn("Selected Core Arc: Ordinary person becomes empowered through challenge.", chapter_outline_prompt)
    
    def test_to_prompt_text_for_chapter_outline_empty_story(self):
        """Test chapter outline prompt generation with empty story."""
        # Generate chapter outline prompt with empty story
        chapter_outline_prompt = self.story.to_prompt_text_for_chapter_outline()
        
        # Should still contain basic structure
        self.assertIn("STORY CONFIGURATION:", chapter_outline_prompt)
        self.assertIn("Use this configuration to guide the story creation process.", chapter_outline_prompt)
        
        # Should not contain any of the excluded fields
        self.assertNotIn("Protagonist Archetype:", chapter_outline_prompt)
        self.assertNotIn("Secondary Character Archetypes:", chapter_outline_prompt)
        self.assertNotIn("SELECTED PLOT LINE:", chapter_outline_prompt)


if __name__ == '__main__':
    unittest.main()