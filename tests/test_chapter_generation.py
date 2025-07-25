"""
Test suite for chapter generation functionality.

Tests the parse_single_chapter_from_ai_response function and chapter_text handling.
"""

import unittest
import json
from objects.chapter import Chapter
from objects.chapter_parser import parse_single_chapter_from_ai_response
from objects.continuity_state import ContinuityState
from objects.continuity_character import ContinuityCharacter


class TestChapterGeneration(unittest.TestCase):
    """Test cases for chapter generation functionality."""

    def test_parse_single_chapter_from_ai_response_success(self):
        """Test successful parsing of a single chapter with chapter_text."""
        ai_response = '''
        <STRUCTURED_DATA>
        {
          "chapter_text": "The morning sun cast long shadows across the village of Thornfield as Lyra made her way through the bustling marketplace. Today was the harvest festival, and the air thrummed with excitement and anticipation. Little did she know that her world was about to change forever.",
          "chapter_summary": "Lyra discovers her destiny as the Chosen One during the harvest festival when mysterious runes appear on her skin.",
          "continuity_state": {
            "characters": [
              {
                "name": "Lyra",
                "current_location": "Thornfield Village",
                "status": "Overwhelmed but determined",
                "inventory": ["Simple dress", "Market basket"]
              }
            ],
            "objects": [
              {
                "name": "Ancient Scroll",
                "holder": "Aldric",
                "location": "Thornfield Village"
              }
            ],
            "locations_visited": ["Thornfield Village"],
            "open_plot_threads": [
              {
                "id": "chosen_one_revelation",
                "description": "Lyra must learn to control her newfound powers",
                "status": "in progress"
              }
            ]
          }
        }
        </STRUCTURED_DATA>
        '''
        
        chapter = parse_single_chapter_from_ai_response(ai_response, 1)
        
        self.assertIsNotNone(chapter)
        self.assertEqual(chapter.chapter_number, 1)
        self.assertIn("morning sun cast long shadows", chapter.chapter_text)
        self.assertIn("Lyra discovers her destiny", chapter.summary)
        
        # Check continuity state
        self.assertIsNotNone(chapter.continuity_state)
        self.assertEqual(len(chapter.continuity_state.characters), 1)
        self.assertEqual(chapter.continuity_state.characters[0].name, "Lyra")
        self.assertEqual(chapter.continuity_state.characters[0].current_location, "Thornfield Village")
        
        self.assertEqual(len(chapter.continuity_state.objects), 1)
        self.assertEqual(chapter.continuity_state.objects[0].name, "Ancient Scroll")
        
        self.assertIn("Thornfield Village", chapter.continuity_state.locations_visited)
        self.assertEqual(len(chapter.continuity_state.open_plot_threads), 1)

    def test_parse_single_chapter_from_ai_response_missing_text(self):
        """Test parsing fails when chapter_text is missing."""
        ai_response = '''
        <STRUCTURED_DATA>
        {
          "chapter_summary": "Summary without text",
          "continuity_state": {}
        }
        </STRUCTURED_DATA>
        '''
        
        chapter = parse_single_chapter_from_ai_response(ai_response, 1)
        self.assertIsNone(chapter)

    def test_parse_single_chapter_from_ai_response_invalid_json(self):
        """Test parsing handles invalid JSON gracefully."""
        ai_response = '''
        <STRUCTURED_DATA>
        {
          "chapter_text": "Valid text",
          "invalid_json": 
        }
        </STRUCTURED_DATA>
        '''
        
        chapter = parse_single_chapter_from_ai_response(ai_response, 1)
        self.assertIsNone(chapter)

    def test_chapter_text_serialization(self):
        """Test that chapter_text is properly serialized and deserialized."""
        chapter = Chapter(1, "Test Chapter", "Test overview")
        chapter.chapter_text = "This is the full chapter prose text."
        chapter.summary = "Brief chapter summary"
        
        # Test to_dict includes chapter_text
        chapter_dict = chapter.to_dict()
        self.assertIn('chapter_text', chapter_dict)
        self.assertEqual(chapter_dict['chapter_text'], chapter.chapter_text)
        self.assertEqual(chapter_dict['summary'], chapter.summary)
        
        # Test from_dict restores chapter_text
        new_chapter = Chapter.from_dict(chapter_dict)
        self.assertIsNotNone(new_chapter)
        self.assertEqual(new_chapter.chapter_text, chapter.chapter_text)
        self.assertEqual(new_chapter.summary, chapter.summary)
        
        # Test JSON serialization
        json_str = chapter.to_json()
        restored_chapter = Chapter.from_json(json_str)
        self.assertIsNotNone(restored_chapter)
        self.assertEqual(restored_chapter.chapter_text, chapter.chapter_text)

    def test_chapter_text_optional(self):
        """Test that chapter_text is optional and defaults to None."""
        chapter = Chapter(1, "Test Chapter", "Test overview")
        self.assertIsNone(chapter.chapter_text)
        
        # Should still serialize properly
        chapter_dict = chapter.to_dict()
        self.assertIn('chapter_text', chapter_dict)
        self.assertIsNone(chapter_dict['chapter_text'])


if __name__ == '__main__':
    unittest.main()