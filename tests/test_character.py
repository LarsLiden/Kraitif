"""
Test the Character class functionality
"""

import unittest
import json
from story import Story
from character import Character
from archetype import ArchetypeEnum
from functional_role import FunctionalRoleEnum
from emotional_function import EmotionalFunctionEnum


class TestCharacterRefactor(unittest.TestCase):
    """Test the new Character refactor."""
    
    def setUp(self):
        """Set up test story."""
        self.story = Story()
    
    def test_character_creation(self):
        """Test creating a character with all required fields."""
        character = Character(
            name="Test Hero",
            archetype=ArchetypeEnum.CHOSEN_ONE,
            functional_role=FunctionalRoleEnum.PROTAGONIST,
            emotional_function=EmotionalFunctionEnum.SYMPATHETIC_CHARACTER,
            backstory="A humble beginning",
            character_arc="From zero to hero"
        )
        
        self.assertEqual(character.name, "Test Hero")
        self.assertEqual(character.archetype, ArchetypeEnum.CHOSEN_ONE)
        self.assertEqual(character.functional_role, FunctionalRoleEnum.PROTAGONIST)
        self.assertEqual(character.emotional_function, EmotionalFunctionEnum.SYMPATHETIC_CHARACTER)
        self.assertEqual(character.backstory, "A humble beginning")
        self.assertEqual(character.character_arc, "From zero to hero")
    
    def test_character_to_dict(self):
        """Test character serialization to dictionary."""
        character = Character(
            name="Test Character",
            archetype=ArchetypeEnum.WISE_MENTOR,
            functional_role=FunctionalRoleEnum.MENTOR,
            emotional_function=EmotionalFunctionEnum.CATALYST
        )
        
        data = character.to_dict()
        expected = {
            'name': 'Test Character',
            'archetype': 'Wise Mentor',
            'functional_role': 'Mentor',
            'emotional_function': 'Catalyst',
            'backstory': '',
            'character_arc': ''
        }
        
        self.assertEqual(data, expected)
    
    def test_character_from_dict(self):
        """Test character deserialization from dictionary."""
        data = {
            'name': 'Test Character',
            'archetype': 'Loyal Companion',
            'functional_role': 'Sidekick',
            'emotional_function': 'Observer',
            'backstory': 'A faithful friend',
            'character_arc': 'Learns independence'
        }
        
        character = Character.from_dict(data)
        
        self.assertIsNotNone(character)
        self.assertEqual(character.name, "Test Character")
        self.assertEqual(character.archetype, ArchetypeEnum.LOYAL_COMPANION)
        self.assertEqual(character.functional_role, FunctionalRoleEnum.SIDEKICK)
        self.assertEqual(character.emotional_function, EmotionalFunctionEnum.OBSERVER)
        self.assertEqual(character.backstory, "A faithful friend")
        self.assertEqual(character.character_arc, "Learns independence")
    
    def test_character_from_dict_invalid(self):
        """Test character deserialization with invalid data."""
        invalid_data = {
            'name': 'Test Character',
            'archetype': 'InvalidArchetype',
            'functional_role': 'Mentor',
            'emotional_function': 'Catalyst'
        }
        
        character = Character.from_dict(invalid_data)
        self.assertIsNone(character)
    
    def test_story_add_character(self):
        """Test adding characters to a story."""
        protagonist = Character(
            name="Hero",
            archetype=ArchetypeEnum.CHOSEN_ONE,
            functional_role=FunctionalRoleEnum.PROTAGONIST,
            emotional_function=EmotionalFunctionEnum.SYMPATHETIC_CHARACTER
        )
        
        secondary = Character(
            name="Mentor",
            archetype=ArchetypeEnum.WISE_MENTOR,
            functional_role=FunctionalRoleEnum.MENTOR,
            emotional_function=EmotionalFunctionEnum.CATALYST
        )
        
        self.assertTrue(self.story.add_character(protagonist))
        self.assertTrue(self.story.add_character(secondary))
        
        self.assertEqual(len(self.story.characters), 2)
        self.assertEqual(self.story.characters[0].name, "Hero")
        self.assertEqual(self.story.characters[1].name, "Mentor")
    
    def test_story_get_protagonist(self):
        """Test getting the protagonist from a story."""
        protagonist = Character(
            name="Hero",
            archetype=ArchetypeEnum.CHOSEN_ONE,
            functional_role=FunctionalRoleEnum.PROTAGONIST,
            emotional_function=EmotionalFunctionEnum.SYMPATHETIC_CHARACTER
        )
        
        secondary = Character(
            name="Mentor",
            archetype=ArchetypeEnum.WISE_MENTOR,
            functional_role=FunctionalRoleEnum.MENTOR,
            emotional_function=EmotionalFunctionEnum.CATALYST
        )
        
        self.story.add_character(protagonist)
        self.story.add_character(secondary)
        
        found_protagonist = self.story.get_protagonist()
        self.assertIsNotNone(found_protagonist)
        self.assertEqual(found_protagonist.name, "Hero")
        self.assertEqual(found_protagonist.functional_role, FunctionalRoleEnum.PROTAGONIST)
    
    def test_story_get_secondary_characters(self):
        """Test getting secondary characters from a story."""
        protagonist = Character(
            name="Hero",
            archetype=ArchetypeEnum.CHOSEN_ONE,
            functional_role=FunctionalRoleEnum.PROTAGONIST,
            emotional_function=EmotionalFunctionEnum.SYMPATHETIC_CHARACTER
        )
        
        secondary1 = Character(
            name="Mentor",
            archetype=ArchetypeEnum.WISE_MENTOR,
            functional_role=FunctionalRoleEnum.MENTOR,
            emotional_function=EmotionalFunctionEnum.CATALYST
        )
        
        secondary2 = Character(
            name="Companion",
            archetype=ArchetypeEnum.LOYAL_COMPANION,
            functional_role=FunctionalRoleEnum.SIDEKICK,
            emotional_function=EmotionalFunctionEnum.OBSERVER
        )
        
        self.story.add_character(protagonist)
        self.story.add_character(secondary1)
        self.story.add_character(secondary2)
        
        secondary_chars = self.story.get_secondary_characters()
        self.assertEqual(len(secondary_chars), 2)
        self.assertEqual(secondary_chars[0].name, "Mentor")
        self.assertEqual(secondary_chars[1].name, "Companion")
    
    def test_story_remove_character(self):
        """Test removing a character from a story."""
        character = Character(
            name="Temporary",
            archetype=ArchetypeEnum.CHOSEN_ONE,
            functional_role=FunctionalRoleEnum.PROTAGONIST,
            emotional_function=EmotionalFunctionEnum.SYMPATHETIC_CHARACTER
        )
        
        self.story.add_character(character)
        self.assertEqual(len(self.story.characters), 1)
        
        success = self.story.remove_character("Temporary")
        self.assertTrue(success)
        self.assertEqual(len(self.story.characters), 0)
        
        # Try to remove non-existent character
        success = self.story.remove_character("NonExistent")
        self.assertFalse(success)
    
    def test_story_json_serialization_with_characters(self):
        """Test story JSON serialization includes characters."""
        protagonist = Character(
            name="Hero",
            archetype=ArchetypeEnum.CHOSEN_ONE,
            functional_role=FunctionalRoleEnum.PROTAGONIST,
            emotional_function=EmotionalFunctionEnum.SYMPATHETIC_CHARACTER,
            backstory="Humble origins",
            character_arc="Saves the world"
        )
        
        self.story.add_character(protagonist)
        self.story.set_genre("Fantasy")
        
        json_str = self.story.to_json()
        data = json.loads(json_str)
        
        self.assertIn('characters', data)
        self.assertEqual(len(data['characters']), 1)
        
        char_data = data['characters'][0]
        self.assertEqual(char_data['name'], 'Hero')
        self.assertEqual(char_data['archetype'], 'Chosen One')
        self.assertEqual(char_data['functional_role'], 'Protagonist')
        self.assertEqual(char_data['emotional_function'], 'Sympathetic Character')
        self.assertEqual(char_data['backstory'], 'Humble origins')
        self.assertEqual(char_data['character_arc'], 'Saves the world')
    
    def test_story_json_deserialization_with_characters(self):
        """Test story JSON deserialization restores characters."""
        data = {
            'genre_name': 'Fantasy',
            'characters': [
                {
                    'name': 'Hero',
                    'archetype': 'Chosen One',
                    'functional_role': 'Protagonist',
                    'emotional_function': 'Sympathetic Character',
                    'backstory': 'Humble origins',
                    'character_arc': 'Saves the world'
                },
                {
                    'name': 'Mentor',
                    'archetype': 'Wise Mentor',
                    'functional_role': 'Mentor',
                    'emotional_function': 'Catalyst',
                    'backstory': 'Former hero',
                    'character_arc': 'Guides the hero'
                }
            ]
        }
        
        json_str = json.dumps(data)
        success = self.story.from_json(json_str)
        
        self.assertTrue(success)
        self.assertEqual(len(self.story.characters), 2)
        
        protagonist = self.story.get_protagonist()
        self.assertIsNotNone(protagonist)
        self.assertEqual(protagonist.name, 'Hero')
        self.assertEqual(protagonist.archetype.value, 'Chosen One')
        
        secondary_chars = self.story.get_secondary_characters()
        self.assertEqual(len(secondary_chars), 1)
        self.assertEqual(secondary_chars[0].name, 'Mentor')
        self.assertEqual(secondary_chars[0].archetype.value, 'Wise Mentor')
    
    def test_story_prompt_text_includes_characters(self):
        """Test that story prompt text includes character information."""
        protagonist = Character(
            name="Hero",
            archetype=ArchetypeEnum.CHOSEN_ONE,
            functional_role=FunctionalRoleEnum.PROTAGONIST,
            emotional_function=EmotionalFunctionEnum.SYMPATHETIC_CHARACTER,
            backstory="Humble farmer's son",
            character_arc="Becomes the chosen savior"
        )
        
        secondary = Character(
            name="Mentor",
            archetype=ArchetypeEnum.WISE_MENTOR,
            functional_role=FunctionalRoleEnum.MENTOR,
            emotional_function=EmotionalFunctionEnum.CATALYST,
            backstory="Former knight",
            character_arc="Guides the hero to victory"
        )
        
        self.story.add_character(protagonist)
        self.story.add_character(secondary)
        
        prompt_text = self.story.to_prompt_text()
        
        # Check protagonist information
        self.assertIn("Protagonist: Hero", prompt_text)
        self.assertIn("Archetype: Chosen One", prompt_text)
        self.assertIn("Functional Role: Protagonist", prompt_text)
        self.assertIn("Emotional Function: Sympathetic Character", prompt_text)
        self.assertIn("Backstory: Humble farmer's son", prompt_text)
        self.assertIn("Character Arc: Becomes the chosen savior", prompt_text)
        
        # Check secondary character information
        self.assertIn("Secondary Characters:", prompt_text)
        self.assertIn("• Mentor", prompt_text)
        self.assertIn("Archetype: Wise Mentor", prompt_text)
        self.assertIn("Functional Role: Mentor", prompt_text)
        self.assertIn("Emotional Function: Catalyst", prompt_text)
        self.assertIn("Backstory: Former knight", prompt_text)
        self.assertIn("Character Arc: Guides the hero to victory", prompt_text)


if __name__ == '__main__':
    unittest.main()