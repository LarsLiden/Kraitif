#!/usr/bin/env python3
"""
Tests for Emotional Function Implementation

This script provides basic validation tests for the emotional function implementation.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from emotional_function import EmotionalFunctionRegistry, EmotionalFunction
from story import Story
import unittest


class TestEmotionalFunction(unittest.TestCase):
    """Test cases for emotional function functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.registry = EmotionalFunctionRegistry()
        self.story = Story()

    def test_emotional_function_registry_initialization(self):
        """Test that the registry loads emotional functions correctly."""
        functions = self.registry.get_all_emotional_functions()
        self.assertEqual(len(functions), 8, f"Expected 8 emotional functions, got {len(functions)}")
        
        # Check that all expected functions are present
        expected_names = [
            "Sympathetic Character",
            "Unsympathetic Character", 
            "Catalyst",
            "Observer",
            "Instigator",
            "Victim",
            "Aggressor",
            "Mediator"
        ]
        
        actual_names = self.registry.list_emotional_function_names()
        for name in expected_names:
            self.assertIn(name, actual_names, f"Missing emotional function: {name}")

    def test_emotional_function_lookup(self):
        """Test looking up emotional functions by name."""
        # Test exact lookup
        catalyst = self.registry.get_emotional_function("Catalyst")
        self.assertIsNotNone(catalyst, "Could not find Catalyst emotional function")
        self.assertEqual(catalyst.name, "Catalyst", f"Expected 'Catalyst', got '{catalyst.name}'")
        
        # Test case-insensitive lookup
        observer = self.registry.get_emotional_function("observer")
        self.assertIsNotNone(observer, "Case-insensitive lookup failed")
        self.assertEqual(observer.name, "Observer", "Case-insensitive lookup returned wrong function")
        
        # Test lookup with spaces converted to underscores
        sympathetic = self.registry.get_emotional_function("sympathetic_character")
        self.assertIsNotNone(sympathetic, "Underscore lookup failed")
        self.assertEqual(sympathetic.name, "Sympathetic Character")

    def test_emotional_function_search(self):
        """Test searching emotional functions by content."""
        # Search by name
        results = self.registry.search_emotional_functions("catalyst")
        self.assertEqual(len(results), 1, "Should find exactly one result for 'catalyst'")
        self.assertEqual(results[0].name, "Catalyst")
        
        # Search by description content
        results = self.registry.search_emotional_functions("empathy")
        self.assertGreater(len(results), 0, "Should find results for 'empathy'")
        
        # Search for a term that appears in multiple descriptions
        results = self.registry.search_emotional_functions("character")
        self.assertGreater(len(results), 1, "Should find multiple results for 'character'")

    def test_story_protagonist_emotional_function(self):
        """Test setting protagonist emotional function in story."""
        # Test valid emotional function
        success = self.story.set_protagonist_emotional_function("Catalyst")
        self.assertTrue(success, "Should successfully set valid emotional function")
        self.assertEqual(self.story.protagonist_emotional_function, "Catalyst")
        
        # Test invalid emotional function
        success = self.story.set_protagonist_emotional_function("Nonexistent Function")
        self.assertFalse(success, "Should fail to set invalid emotional function")

    def test_story_secondary_emotional_functions(self):
        """Test setting secondary emotional functions in story."""
        # Test valid emotional functions
        success = self.story.set_secondary_emotional_functions(["Observer", "Mediator"])
        self.assertTrue(success, "Should successfully set valid emotional functions")
        self.assertEqual(self.story.secondary_emotional_functions, ["Observer", "Mediator"])
        
        # Test with some invalid functions
        success = self.story.set_secondary_emotional_functions(["Observer", "Invalid Function"])
        self.assertFalse(success, "Should fail when any function is invalid")
        
        # Test empty list (should be valid)
        success = self.story.set_secondary_emotional_functions([])
        self.assertTrue(success, "Should successfully set empty list")
        self.assertEqual(self.story.secondary_emotional_functions, [])

    def test_story_emotional_function_availability(self):
        """Test getting available emotional functions from story."""
        functions = self.story.get_available_emotional_functions()
        self.assertEqual(len(functions), 8, "Should return all 8 emotional functions")
        
        # Verify all functions are EmotionalFunction objects
        for func in functions:
            self.assertIsInstance(func, EmotionalFunction)
            self.assertIsInstance(func.name, str)
            self.assertIsInstance(func.description, str)

    def test_story_string_representation_with_emotional_functions(self):
        """Test story string representation includes emotional functions."""
        # Set emotional functions
        self.story.set_protagonist_emotional_function("Catalyst")
        self.story.set_secondary_emotional_functions(["Observer", "Mediator"])
        
        story_str = str(self.story)
        self.assertIn("Catalyst", story_str, "String representation should include protagonist function")
        self.assertIn("Observer", story_str, "String representation should include secondary functions")
        self.assertIn("Mediator", story_str, "String representation should include secondary functions")

    def test_story_json_serialization_with_emotional_functions(self):
        """Test JSON serialization includes emotional functions."""
        # Set emotional functions
        self.story.set_protagonist_emotional_function("Catalyst")
        self.story.set_secondary_emotional_functions(["Observer", "Mediator"])
        
        json_str = self.story.to_json()
        self.assertIn("protagonist_emotional_function", json_str)
        self.assertIn("secondary_emotional_functions", json_str)
        self.assertIn("Catalyst", json_str)
        self.assertIn("Observer", json_str)
        self.assertIn("Mediator", json_str)

    def test_story_json_deserialization_with_emotional_functions(self):
        """Test JSON deserialization preserves emotional functions."""
        # Create a story with emotional functions
        original_story = Story()
        original_story.set_protagonist_emotional_function("Catalyst")
        original_story.set_secondary_emotional_functions(["Observer", "Mediator"])
        
        # Serialize and deserialize
        json_str = original_story.to_json()
        new_story = Story()
        success = new_story.from_json(json_str)
        
        self.assertTrue(success, "Deserialization should succeed")
        self.assertEqual(new_story.protagonist_emotional_function, "Catalyst")
        self.assertEqual(new_story.secondary_emotional_functions, ["Observer", "Mediator"])

    def test_story_prompt_text_includes_emotional_functions(self):
        """Test that prompt text includes emotional function information."""
        # Set up a story with character archetypes and emotional functions
        self.story.set_protagonist_archetype("Chosen One")
        self.story.set_protagonist_emotional_function("Catalyst")
        self.story.set_secondary_archetypes(["Wise Mentor"])
        self.story.set_secondary_emotional_functions(["Observer"])
        
        prompt_text = self.story.to_prompt_text()
        
        # Check that emotional functions are included
        self.assertIn("Emotional Function: Catalyst", prompt_text)
        self.assertIn("Emotional Function: Observer", prompt_text)
        self.assertIn("Pushes others to change", prompt_text)  # Part of Catalyst description


def run_tests():
    """Run all emotional function tests."""
    unittest.main(verbosity=2)


if __name__ == "__main__":
    run_tests()