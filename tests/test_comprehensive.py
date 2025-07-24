#!/usr/bin/env python3
"""
Comprehensive test runner for all Kraitif tests

This module runs all test suites and provides a comprehensive report
of test coverage and results.
"""

import sys
import os
import unittest
import tempfile
import json
from io import StringIO
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import all test modules
from tests.test_story_types import run_all_tests as run_story_types_tests
from tests.test_genre_flow import run_genre_tests
from tests.test_story_save_load import run_story_save_load_tests
from tests.test_flask_save_load import run_flask_save_load_tests

# Import the main modules for additional edge case testing
from objects.story import Story
from objects.story_types import StoryTypeRegistry
from objects.genre import GenreRegistry
from objects.archetype import ArchetypeRegistry
from objects.style import StyleRegistry


class TestEdgeCases(unittest.TestCase):
    """Additional edge case tests to make the suite more robust."""
    
    def test_story_with_all_none_values(self):
        """Test story behavior with explicitly set None values."""
        story = Story()
        story.story_type_name = None
        story.subtype_name = None
        story.key_theme = None
        story.core_arc = None
        
        # Should handle gracefully
        story_str = str(story)
        self.assertEqual(story_str, "Story with no selections")
        
        # Should serialize without error
        json_str = story.to_json()
        data = json.loads(json_str)
        self.assertIsNone(data['story_type_name'])
    
    def test_registry_case_sensitivity(self):
        """Test that all registries handle case variations properly."""
        story_registry = StoryTypeRegistry()
        genre_registry = GenreRegistry()
        archetype_registry = ArchetypeRegistry()
        style_registry = StyleRegistry()
        
        # Test various case combinations
        test_cases = [
            (story_registry.get_story_type, "THE QUEST", "The Quest"),
            (story_registry.get_story_type, "the quest", "The Quest"),
            (story_registry.get_story_type, "The Quest", "The Quest"),
            (genre_registry.get_genre, "FANTASY", "Fantasy"),
            (genre_registry.get_genre, "fantasy", "Fantasy"),
            (archetype_registry.get_archetype, "CHOSEN ONE", "Chosen One"),
            (archetype_registry.get_archetype, "chosen one", "Chosen One"),
            (style_registry.get_style, "CONCISE", "Concise"),
            (style_registry.get_style, "concise", "Concise"),
        ]
        
        for getter_func, input_name, expected_name in test_cases:
            with self.subTest(input=input_name, expected=expected_name):
                result = getter_func(input_name)
                self.assertIsNotNone(result, f"Failed to find {input_name}")
                self.assertEqual(result.name, expected_name)
    
    def test_story_state_consistency(self):
        """Test that story maintains consistent state across operations."""
        story = Story()
        
        # Set up story
        story.set_story_type_selection("Comedy", "Satirical Comedy", "Theme", "Arc")
        story.set_genre("Comedy")
        story.set_protagonist_archetype("Anti-Hero")
        
        # Verify initial state
        initial_str = str(story)
        self.assertIn("Comedy", initial_str)
        self.assertIn("Anti-Hero", initial_str)
        
        # Serialize and deserialize
        json_str = story.to_json()
        new_story = Story()
        success = new_story.from_json(json_str)
        
        self.assertTrue(success)
        
        # Verify state is preserved
        final_str = str(new_story)
        self.assertIn("Comedy", final_str)
        self.assertIn("Anti-Hero", final_str)
        
        # Verify objects are equal in content
        self.assertEqual(story.story_type_name, new_story.story_type_name)
        self.assertEqual(story.subtype_name, new_story.subtype_name)
        self.assertEqual(story.protagonist_archetype, new_story.protagonist_archetype)
    
    def test_registry_search_functionality(self):
        """Test search functionality across registries."""
        archetype_registry = ArchetypeRegistry()
        style_registry = StyleRegistry()
        
        # Test archetype search
        hero_results = archetype_registry.search_archetypes("hero")
        self.assertGreater(len(hero_results), 0, "Should find hero-related archetypes")
        
        # Verify results contain the search term
        hero_found = any("hero" in arch.name.lower() or "hero" in arch.description.lower() 
                        for arch in hero_results)
        self.assertTrue(hero_found, "Search results should contain hero-related content")
        
        # Test style search
        emotional_results = style_registry.search_styles("emotional")
        # This might return 0 results, which is okay - just verify it doesn't crash
        self.assertIsInstance(emotional_results, list)
    
    def test_invalid_operations_graceful_handling(self):
        """Test that invalid operations are handled gracefully."""
        story = Story()
        
        # Try to set invalid data
        self.assertFalse(story.set_genre(""))
        self.assertFalse(story.set_genre("   "))
        self.assertFalse(story.set_sub_genre("InvalidSubGenre"))
        self.assertFalse(story.set_protagonist_archetype(""))
        self.assertFalse(story.set_secondary_archetypes(["InvalidArchetype"]))
        
        # Story should remain in clean state
        self.assertIsNone(story.genre)
        self.assertIsNone(story.sub_genre)
        self.assertIsNone(story.protagonist_archetype)
        self.assertEqual(story.secondary_archetypes, [])
    
    def test_large_data_handling(self):
        """Test handling of large archetype lists."""
        story = Story()
        archetype_registry = ArchetypeRegistry()
        
        # Get all available archetypes
        all_archetypes = archetype_registry.list_archetype_names()
        
        # Try to set a large secondary archetype list (should work)
        large_list = all_archetypes[:10]  # Take first 10
        result = story.set_secondary_archetypes(large_list)
        self.assertTrue(result)
        self.assertEqual(len(story.secondary_archetypes), 10)
        
        # Test serialization with large data
        json_str = story.to_json()
        self.assertIsInstance(json_str, str)
        self.assertGreater(len(json_str), 100)  # Should be substantial JSON
        
        # Test deserialization
        new_story = Story()
        success = new_story.from_json(json_str)
        self.assertTrue(success)
        self.assertEqual(len(new_story.secondary_archetypes), 10)
    
    def test_json_malformed_data_handling(self):
        """Test handling of various malformed JSON scenarios."""
        story = Story()
        
        malformed_cases = [
            '{"story_type_name": "Valid", "secondary_archetypes": "should_be_list"}',
            '{"story_type_name": 123}',  # Wrong type
            '{"story_type_name": "Test", "extra_unknown_field": "ignored"}',  # Extra fields
        ]
        
        for malformed_json in malformed_cases:
            with self.subTest(json_data=malformed_json):
                # Should either succeed (ignoring bad fields) or fail gracefully
                try:
                    result = story.from_json(malformed_json)
                    # If it succeeds, story should be in valid state
                    if result:
                        str(story)  # Should not crash
                except Exception as e:
                    # If it fails, should be handled gracefully
                    self.fail(f"Should handle malformed JSON gracefully: {e}")


def run_edge_case_tests():
    """Run edge case tests."""
    print("=== Running Edge Case Tests ===\n")
    
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestEdgeCases)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    if result.wasSuccessful():
        print("\n✅ All edge case tests passed!")
        return True
    else:
        print(f"\n❌ {len(result.failures)} test(s) failed, {len(result.errors)} error(s)")
        return False


def run_all_comprehensive_tests():
    """Run all test suites with comprehensive reporting."""
    print("🧪 KRAITIF COMPREHENSIVE TEST SUITE")
    print("=" * 50)
    
    test_results = []
    
    # Run each test suite
    test_suites = [
        ("Story Types & Components", run_story_types_tests),
        ("Genre Flow", run_genre_tests),
        ("Story Save/Load", run_story_save_load_tests),
        ("Flask Save/Load", run_flask_save_load_tests),
        ("Edge Cases", run_edge_case_tests),
    ]
    
    for suite_name, test_func in test_suites:
        print(f"\n🔍 Running {suite_name} Tests...")
        print("-" * 40)
        try:
            result = test_func()
            test_results.append((suite_name, result))
        except Exception as e:
            print(f"❌ {suite_name} tests failed with exception: {e}")
            test_results.append((suite_name, False))
    
    # Summary report
    print("\n" + "=" * 50)
    print("📊 TEST SUITE SUMMARY")
    print("=" * 50)
    
    passed_count = 0
    failed_count = 0
    
    for suite_name, result in test_results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{suite_name:25} {status}")
        if result:
            passed_count += 1
        else:
            failed_count += 1
    
    print("\n" + "=" * 50)
    print(f"Total Test Suites: {len(test_results)}")
    print(f"Passed: {passed_count}")
    print(f"Failed: {failed_count}")
    
    overall_success = failed_count == 0
    
    if overall_success:
        print("\n🎉 ALL TESTS PASSED! The Kraitif test suite is now more robust.")
        print("✨ Load/save functionality is thoroughly tested with comprehensive edge cases.")
    else:
        print(f"\n⚠️  {failed_count} test suite(s) failed. Please review the failures above.")
    
    return overall_success


if __name__ == "__main__":
    success = run_all_comprehensive_tests()
    sys.exit(0 if success else 1)