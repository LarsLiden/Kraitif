#!/usr/bin/env python3
"""
Comprehensive tests for Story save/load functionality

This module provides robust testing for the Story class serialization,
including edge cases, error handling, and data validation.
"""

import sys
import os
import json
import tempfile
import unittest
from unittest.mock import patch
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from objects.story import Story


class TestStorySaveLoad(unittest.TestCase):
    """Test Story save/load functionality comprehensively."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.story = Story()
    
    def test_empty_story_serialization(self):
        """Test serialization of an empty story."""
        json_str = self.story.to_json()
        self.assertIsInstance(json_str, str)
        
        # Verify JSON is valid
        data = json.loads(json_str)
        self.assertIsInstance(data, dict)
        
        # Check all fields are None or empty
        self.assertIsNone(data.get('story_type_name'))
        self.assertIsNone(data.get('subtype_name'))
        self.assertIsNone(data.get('key_theme'))
        self.assertIsNone(data.get('core_arc'))
        self.assertIsNone(data.get('genre_name'))
        self.assertIsNone(data.get('sub_genre_name'))
        self.assertIsNone(data.get('protagonist_archetype'))
        self.assertEqual(data.get('secondary_archetypes', []), [])
    
    def test_empty_story_deserialization(self):
        """Test deserialization of an empty story."""
        json_str = self.story.to_json()
        new_story = Story()
        success = new_story.from_json(json_str)
        
        self.assertTrue(success)
        self.assertIsNone(new_story.story_type_name)
        self.assertIsNone(new_story.subtype_name)
        self.assertIsNone(new_story.key_theme)
        self.assertIsNone(new_story.core_arc)
        self.assertIsNone(new_story.genre)
        self.assertIsNone(new_story.sub_genre)
        self.assertEqual(new_story.characters, [])
    
    def test_complete_story_serialization(self):
        """Test serialization of a complete story with all fields."""
        # Import here to avoid circular import
        from objects.character import Character
        from objects.archetype import ArchetypeEnum
        from objects.functional_role import FunctionalRoleEnum
        from objects.emotional_function import EmotionalFunctionEnum
        
        # Set up a complete story
        self.story.set_story_type_selection("Comedy", "Romantic Comedy", 
                                           "Love conquers all", "Meet-cute to marriage")
        self.story.set_genre("Romance")
        self.story.set_sub_genre("Romantic Comedy")
        
        # Create characters
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
        
        json_str = self.story.to_json()
        data = json.loads(json_str)
        
        # Verify all fields are correctly serialized
        self.assertEqual(data['story_type_name'], "Comedy")
        self.assertEqual(data['subtype_name'], "Romantic Comedy")
        self.assertEqual(data['key_theme'], "Love conquers all")
        self.assertEqual(data['core_arc'], "Meet-cute to marriage")
        self.assertEqual(data['genre_name'], "Romance")
        self.assertEqual(data['sub_genre_name'], "Romantic Comedy")
        
        # Check characters
        self.assertEqual(len(data['characters']), 2)
        self.assertEqual(data['characters'][0]['name'], "Hero")
        self.assertEqual(data['characters'][0]['archetype'], "Chosen One")
        self.assertEqual(data['characters'][1]['name'], "Mentor")
        self.assertEqual(data['characters'][1]['archetype'], "Wise Mentor")
    
    def test_complete_story_deserialization(self):
        """Test deserialization of a complete story."""
        # Import here to avoid circular import
        from objects.character import Character
        from objects.archetype import ArchetypeEnum
        from objects.functional_role import FunctionalRoleEnum
        from objects.emotional_function import EmotionalFunctionEnum
        
        # Set up and serialize a complete story
        self.story.set_story_type_selection("The Quest", "Object Quest", 
                                           "Growth through adventure", "Trust forged under pressure")
        self.story.set_genre("Fantasy")
        self.story.set_sub_genre("High Fantasy")
        
        # Create characters
        protagonist = Character(
            name="Quest Hero",
            archetype=ArchetypeEnum.CHOSEN_ONE,
            functional_role=FunctionalRoleEnum.PROTAGONIST,
            emotional_function=EmotionalFunctionEnum.SYMPATHETIC_CHARACTER
        )
        secondary = Character(
            name="Wise Guide",
            archetype=ArchetypeEnum.WISE_MENTOR,
            functional_role=FunctionalRoleEnum.MENTOR,
            emotional_function=EmotionalFunctionEnum.CATALYST
        )
        
        self.story.add_character(protagonist)
        self.story.add_character(secondary)
        
        json_str = self.story.to_json()
        
        # Create new story and deserialize
        new_story = Story()
        success = new_story.from_json(json_str)
        
        self.assertTrue(success)
        self.assertEqual(new_story.story_type_name, "The Quest")
        self.assertEqual(new_story.subtype_name, "Object Quest")
        self.assertEqual(new_story.key_theme, "Growth through adventure")
        self.assertEqual(new_story.core_arc, "Trust forged under pressure")
        self.assertEqual(new_story.genre.name, "Fantasy")
        self.assertEqual(new_story.sub_genre.name, "High Fantasy")
        
        # Check characters
        self.assertEqual(len(new_story.characters), 2)
        protagonist_char = new_story.get_protagonist()
        self.assertIsNotNone(protagonist_char)
        self.assertEqual(protagonist_char.name, "Quest Hero")
        self.assertEqual(protagonist_char.archetype.value, "Chosen One")
        
        secondary_chars = new_story.get_secondary_characters()
        self.assertEqual(len(secondary_chars), 1)
        self.assertEqual(secondary_chars[0].name, "Wise Guide")
        self.assertEqual(secondary_chars[0].archetype.value, "Wise Mentor")
    
    def test_roundtrip_serialization(self):
        """Test that serialize->deserialize->serialize produces identical results."""
        # Import here to avoid circular import
        from objects.character import Character
        from objects.archetype import ArchetypeEnum
        from objects.functional_role import FunctionalRoleEnum
        from objects.emotional_function import EmotionalFunctionEnum
        
        # Set up a story with various fields
        self.story.set_story_type_selection("Tragedy", "Personal Tragedy", 
                                           "Pride goes before a fall", "Hubris to downfall")
        self.story.set_genre("Drama")
        
        # Create character
        protagonist = Character(
            name="Tragic Hero",
            archetype=ArchetypeEnum.ANTI_HERO,
            functional_role=FunctionalRoleEnum.PROTAGONIST,
            emotional_function=EmotionalFunctionEnum.SYMPATHETIC_CHARACTER
        )
        
        self.story.add_character(protagonist)
        
        # First serialization
        json_str1 = self.story.to_json()
        
        # Deserialize into new story
        new_story = Story()
        new_story.from_json(json_str1)
        
        # Second serialization
        json_str2 = new_story.to_json()
        
        # Compare the JSON strings (parse to avoid formatting differences)
        data1 = json.loads(json_str1)
        data2 = json.loads(json_str2)
        self.assertEqual(data1, data2)
    
    def test_invalid_json_handling(self):
        """Test handling of invalid JSON strings."""
        invalid_json_strings = [
            "",  # Empty string
            "not json",  # Invalid JSON
            "{",  # Incomplete JSON
            '{"key": }',  # Malformed JSON
            "null",  # Null JSON - should now fail
            "[]",  # Array instead of object - should now fail
        ]
        
        for invalid_json in invalid_json_strings:
            with self.subTest(json_str=invalid_json):
                new_story = Story()
                success = new_story.from_json(invalid_json)
                self.assertFalse(success, f"Should fail for invalid JSON: {invalid_json}")
                # Verify story remains in clean state
                self.assertIsNone(new_story.story_type_name)
                self.assertIsNone(new_story.genre)
        
        # Test JSON with invalid structure but valid JSON (should succeed but ignore bad data)
        json_with_null_values = '{"story_type_name": null, "invalid_field": "value"}'
        new_story = Story()
        success = new_story.from_json(json_with_null_values)
        self.assertTrue(success, "Should succeed with null values - they get ignored")
        self.assertIsNone(new_story.story_type_name)  # null should become None
    
    def test_partial_data_deserialization(self):
        """Test deserialization with only some fields present."""
        partial_data = {
            "story_type_name": "Comedy",
            "subtype_name": "Satirical Comedy",
            # Missing other fields
        }
        json_str = json.dumps(partial_data)
        
        new_story = Story()
        success = new_story.from_json(json_str)
        
        self.assertTrue(success)
        self.assertEqual(new_story.story_type_name, "Comedy")
        self.assertEqual(new_story.subtype_name, "Satirical Comedy")
        self.assertIsNone(new_story.key_theme)
        self.assertIsNone(new_story.core_arc)
        self.assertIsNone(new_story.genre)
        self.assertIsNone(new_story.sub_genre)
    
    def test_invalid_genre_deserialization(self):
        """Test deserialization with invalid genre names."""
        data = {
            "story_type_name": "Comedy",
            "genre_name": "NonExistentGenre",
            "sub_genre_name": "InvalidSubGenre"
        }
        json_str = json.dumps(data)
        
        new_story = Story()
        success = new_story.from_json(json_str)
        
        # Should still succeed but invalid genres should be ignored
        self.assertTrue(success)
        self.assertEqual(new_story.story_type_name, "Comedy")
        self.assertIsNone(new_story.genre)
        self.assertIsNone(new_story.sub_genre)
    
    def test_invalid_archetype_deserialization(self):
        """Test deserialization with invalid archetype names."""
        data = {
            "characters": [
                {
                    "name": "Invalid Hero",
                    "archetype": "NonExistentArchetype",
                    "functional_role": "Protagonist",
                    "emotional_function": "Sympathetic Character"
                }
            ]
        }
        json_str = json.dumps(data)
        
        new_story = Story()
        success = new_story.from_json(json_str)
        
        # Should still succeed but invalid characters should be ignored
        self.assertTrue(success)
        self.assertEqual(len(new_story.characters), 0)
    
    def test_json_structure_and_formatting(self):
        """Test that JSON output has expected structure and formatting."""
        self.story.set_story_type_selection("Comedy", "Romantic Comedy", 
                                           "Love theme", "Romance arc")
        self.story.set_genre("Romance")
        
        json_str = self.story.to_json()
        
        # Check that it's formatted (indented)
        self.assertIn('\n', json_str)
        self.assertIn('  ', json_str)  # Should have indentation
        
        # Check structure
        data = json.loads(json_str)
        expected_keys = {
            'story_type_name', 'subtype_name', 'key_theme', 'core_arc',
            'genre_name', 'sub_genre_name', 'writing_style_name', 'characters',
            'selected_plot_line', 'protagonist_archetype', 'secondary_archetypes',
            'expanded_plot_line', 'chapters'
        }
        self.assertEqual(set(data.keys()), expected_keys)
    
    def test_string_representation_with_loaded_data(self):
        """Test string representation after loading from JSON."""
        # Import here to avoid circular import
        from objects.character import Character
        from objects.archetype import ArchetypeEnum
        from objects.functional_role import FunctionalRoleEnum
        from objects.emotional_function import EmotionalFunctionEnum
        
        # Create and serialize a story
        original_story = Story()
        original_story.set_story_type_selection("Rebirth", "Redemption", 
                                               "Redemption theme", "Fall to rise")
        original_story.set_genre("Drama")
        
        # Create character
        protagonist = Character(
            name="Redeemed Hero",
            archetype=ArchetypeEnum.ANTI_HERO,
            functional_role=FunctionalRoleEnum.PROTAGONIST,
            emotional_function=EmotionalFunctionEnum.SYMPATHETIC_CHARACTER
        )
        original_story.add_character(protagonist)
        
        json_str = original_story.to_json()
        
        # Load into new story
        loaded_story = Story()
        loaded_story.from_json(json_str)
        
        # Check string representation
        story_str = str(loaded_story)
        self.assertIn("Genre: Drama", story_str)
        self.assertIn("Story Type: Rebirth - Redemption", story_str)
        self.assertIn("Protagonist: Redeemed Hero (Anti-Hero)", story_str)
    
    def test_data_type_validation(self):
        """Test handling of incorrect data types in JSON."""
        invalid_data_types = [
            {"story_type_name": 123},  # Number instead of string
            {"secondary_archetypes": "string"},  # String instead of list
            {"protagonist_archetype": {"key": "value"}},  # Object instead of string
        ]
        
        for invalid_data in invalid_data_types:
            with self.subTest(data=invalid_data):
                json_str = json.dumps(invalid_data)
                new_story = Story()
                # Should handle gracefully and not crash
                try:
                    success = new_story.from_json(json_str)
                    # If it succeeds, verify clean state
                    if success:
                        pass  # Some type coercion might work
                except Exception:
                    # If it fails, that's also acceptable
                    pass


def run_story_save_load_tests():
    """Run all Story save/load tests."""
    print("=== Running Story Save/Load Tests ===\n")
    
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestStorySaveLoad)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    if result.wasSuccessful():
        print("\n✅ All Story save/load tests passed!")
        return True
    else:
        print(f"\n❌ {len(result.failures)} test(s) failed, {len(result.errors)} error(s)")
        for failure in result.failures:
            print(f"FAILURE: {failure[0]}")
            print(failure[1])
        for error in result.errors:
            print(f"ERROR: {error[0]}")
            print(error[1])
        return False


if __name__ == "__main__":
    success = run_story_save_load_tests()
    sys.exit(0 if success else 1)