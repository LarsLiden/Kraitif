#!/usr/bin/env python3
"""
Test that the archetype prompt fix works correctly
"""

import unittest
from story import Story


class TestArchetypePromptFix(unittest.TestCase):
    """Test the fix for missing archetypes in STORY_CONFIGURATION"""

    def setUp(self):
        """Set up test story with basic configuration"""
        self.story = Story()
        self.story.story_type_name = 'The Quest'
        self.story.subtype_name = 'Epic Quest'
        self.story.set_genre('Fantasy')
        self.story.set_sub_genre('High Fantasy')
        self.story.set_writing_style('Epic')

    def test_protagonist_and_secondary_archetypes_in_prompt(self):
        """Test that protagonist and secondary archetypes appear in STORY_CONFIGURATION"""
        # Set archetype fields
        self.story.set_protagonist_archetype('Chosen One')
        self.story.set_secondary_archetypes(['Wise Mentor', 'Loyal Companion'])
        
        # Verify no Character objects exist (current web UI state)
        self.assertEqual(len(self.story.characters), 0)
        
        # Get the prompt text
        prompt_text = self.story.to_prompt_text()
        
        # Verify archetype section exists
        self.assertIn("CHARACTER ARCHETYPES:", prompt_text)
        
        # Verify protagonist archetype appears
        self.assertIn("Protagonist Archetype: Chosen One", prompt_text)
        
        # Verify secondary archetypes appear
        self.assertIn("Secondary Character Archetypes:", prompt_text)
        self.assertIn("Wise Mentor", prompt_text)
        self.assertIn("Loyal Companion", prompt_text)
        
        # Verify descriptions are included
        self.assertIn("A protagonist destined for greatness", prompt_text)

    def test_only_protagonist_archetype(self):
        """Test with only protagonist archetype set"""
        self.story.set_protagonist_archetype('Anti-Hero')
        
        prompt_text = self.story.to_prompt_text()
        
        self.assertIn("CHARACTER ARCHETYPES:", prompt_text)
        self.assertIn("Protagonist Archetype: Anti-Hero", prompt_text)
        self.assertIn("Suggested Secondary Character Archetypes", prompt_text)

    def test_no_archetypes_set(self):
        """Test that no CHARACTER ARCHETYPES section appears when no archetypes set"""
        # Don't set any archetypes
        prompt_text = self.story.to_prompt_text()
        
        # Should not have CHARACTER ARCHETYPES section
        self.assertNotIn("CHARACTER ARCHETYPES:", prompt_text)

    def test_character_objects_take_precedence(self):
        """Test that Character objects take precedence over archetype fields"""
        from character import Character
        from archetype import ArchetypeEnum
        from functional_role import FunctionalRoleEnum
        from emotional_function import EmotionalFunctionEnum
        
        # Set archetype fields
        self.story.set_protagonist_archetype('Anti-Hero')
        self.story.set_secondary_archetypes(['Wise Mentor'])
        
        # Add Character object - should take precedence
        protagonist = Character(
            name="Hero",
            archetype=ArchetypeEnum.CHOSEN_ONE,
            functional_role=FunctionalRoleEnum.PROTAGONIST,
            emotional_function=EmotionalFunctionEnum.SYMPATHETIC_CHARACTER,
            backstory="A simple farmer",
            character_arc="Becomes a legendary hero"
        )
        self.story.add_character(protagonist)
        
        prompt_text = self.story.to_prompt_text()
        
        # Should show Character object info, not archetype fields
        self.assertIn("Protagonist: Hero", prompt_text)
        self.assertIn("Chosen One", prompt_text)  # From Character object
        self.assertNotIn("Anti-Hero", prompt_text)  # Should not show archetype field


if __name__ == '__main__':
    unittest.main()