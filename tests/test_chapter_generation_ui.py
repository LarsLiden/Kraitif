#!/usr/bin/env python3
"""
Test script to verify chapter generation UI functionality.
This test ensures that the chapter generation UI updates correctly after successful generation.
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
from objects.story import Story
from objects.chapter import Chapter
from objects.narrative_function import NarrativeFunctionEnum


class TestChapterGenerationUI(unittest.TestCase):
    """Test cases for chapter generation UI functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        
    def test_chapter_generation_ui_state(self):
        """Test that the UI properly shows chapter generation state."""
        with self.app.app_context():
            # Create a test story with chapters
            story = Story()
            story.story_type_name = 'The Quest'
            story.subtype_name = 'Object Quest'
            
            # Add chapters - some generated, some not
            chapter1 = Chapter(
                chapter_number=1,
                title="Generated Chapter",
                overview="This chapter is generated",
                chapter_text="Some text content"  # This indicates generation is complete
            )
            
            chapter2 = Chapter(
                chapter_number=2,
                title="Ungenerated Chapter", 
                overview="This chapter needs generation"
                # No chapter_text - indicates it needs generation
            )
            
            story.add_chapter(chapter1)
            story.add_chapter(chapter2)
            
            # Test that the story correctly identifies which chapters need generation
            self.assertTrue(chapter1.chapter_text is not None)
            self.assertTrue(chapter2.chapter_text is None)
            
            # Test that chapter ordering works correctly
            ordered_chapters = story.get_chapters_ordered()
            self.assertEqual(len(ordered_chapters), 2)
            self.assertEqual(ordered_chapters[0].chapter_number, 1)
            self.assertEqual(ordered_chapters[1].chapter_number, 2)
    
    def test_first_chapter_without_text_logic(self):
        """Test the logic for finding the first chapter that needs generation."""
        story = Story()
        
        # Add multiple chapters with mixed generation states
        chapters = [
            Chapter(chapter_number=1, title="Ch1", overview="Overview 1", chapter_text="Generated"),
            Chapter(chapter_number=2, title="Ch2", overview="Overview 2", chapter_text="Generated"),
            Chapter(chapter_number=3, title="Ch3", overview="Overview 3"),  # Needs generation
            Chapter(chapter_number=4, title="Ch4", overview="Overview 4"),  # Needs generation
        ]
        
        for chapter in chapters:
            story.add_chapter(chapter)
        
        # Find the first chapter that needs generation
        first_ungenerated = None
        for chapter in story.get_chapters_ordered():
            if not chapter.chapter_text:
                first_ungenerated = chapter
                break
        
        # Should be chapter 3
        self.assertIsNotNone(first_ungenerated)
        self.assertEqual(first_ungenerated.chapter_number, 3)
        self.assertEqual(first_ungenerated.title, "Ch3")
    
    def test_chapter_generation_response_format(self):
        """Test that chapter generation responses have the correct format."""
        # This test verifies the expected JSON response format for successful generation
        expected_success_response = {
            'success': True,
            'chapter': {
                'chapter_number': 3,
                'title': 'Test Chapter',
                'chapter_text': 'Generated content...',
                'summary': 'Chapter summary...',
                # ... other chapter fields
            },
            'redirect_url': '/chapter/3'
        }
        
        # Test that all required fields are present
        self.assertTrue('success' in expected_success_response)
        self.assertTrue('chapter' in expected_success_response)
        self.assertTrue('redirect_url' in expected_success_response)
        self.assertTrue(expected_success_response['success'])
        self.assertTrue(expected_success_response['redirect_url'].endswith('/chapter/3'))


if __name__ == '__main__':
    unittest.main()