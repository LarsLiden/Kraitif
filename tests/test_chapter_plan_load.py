#!/usr/bin/env python3
"""
Tests for chapter plan load issue fix

This module tests that loading a story with chapters correctly redirects 
to the chapter-plan page instead of complete-story-selection.
"""

import sys
import os
import json
import tempfile
import unittest
from io import BytesIO
from unittest.mock import patch
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, get_next_incomplete_step
from objects.story import Story
from objects.chapter import Chapter
from objects.character import Character
from objects.plot_line import PlotLine
from objects.archetype import ArchetypeEnum
from objects.functional_role import FunctionalRoleEnum
from objects.emotional_function import EmotionalFunctionEnum


class TestChapterPlanLoad(unittest.TestCase):
    """Test chapter plan load functionality."""
    
    def setUp(self):
        """Set up test client and configure testing."""
        self.app = app.test_client()
        self.app.testing = True
        app.config['TESTING'] = True
    
    def create_complete_story_with_chapters(self):
        """Create a complete story object with chapters for testing."""
        story = Story()
        
        # Set basic story data
        story.story_type_name = "The Quest"
        story.subtype_name = "Spiritual Quest"
        story.key_theme = "Finding inner peace"
        story.core_arc = "Spiritual growth through trials"
        story.set_genre("Fantasy")
        story.set_sub_genre("High Fantasy")
        story.set_writing_style("Lyrical")
        story.set_protagonist_archetype("Chosen One")
        story.set_secondary_archetypes(["Wise Mentor", "Loyal Companion"])
        
        # Add plot line and expanded plot line
        plot_line = PlotLine(
            name="The Chosen One's Quest",
            plotline="A young chosen one must retrieve an ancient magical artifact to save their realm from an encroaching darkness."
        )
        story.selected_plot_line = plot_line
        story.expanded_plot_line = "Expanded version of the plot line with character details..."
        
        # Add characters
        character1 = Character(
            name="Lyra Starbringer",
            archetype=ArchetypeEnum.CHOSEN_ONE,
            functional_role=FunctionalRoleEnum.PROTAGONIST,
            emotional_function=EmotionalFunctionEnum.SYMPATHETIC_CHARACTER,
            backstory="A young woman destined to save the realm.",
            character_arc="Grows from reluctant hero to confident leader."
        )
        character2 = Character(
            name="Master Thorne",
            archetype=ArchetypeEnum.WISE_MENTOR,
            functional_role=FunctionalRoleEnum.MENTOR,
            emotional_function=EmotionalFunctionEnum.MEDIATOR,
            backstory="An ancient wizard who guides heroes.",
            character_arc="Learns to trust in the next generation."
        )
        story.characters = [character1, character2]
        
        # Add chapters
        chapter1 = Chapter(
            chapter_number=1,
            title="The Call to Adventure",
            overview="Lyra discovers her destiny and begins her quest.",
            character_impact=[{"character": "Lyra", "effect": "Reluctantly accepts destiny"}],
            point_of_view="Lyra",
            foreshadow_or_echo="Seeds planted for the final confrontation",
            scene_highlights="Magical awakening scene with glowing artifacts"
        )
        chapter2 = Chapter(
            chapter_number=2,
            title="The Mentor's Guidance",
            overview="Master Thorne teaches Lyra essential skills.",
            character_impact=[{"character": "Lyra", "effect": "Gains confidence"}, {"character": "Master Thorne", "effect": "Bonds with student"}],
            point_of_view="Lyra",
            foreshadow_or_echo="Training prepares for later trials",
            scene_highlights="Intense magical training sequences"
        )
        story.add_chapter(chapter1)
        story.add_chapter(chapter2)
        
        return story
    
    def test_get_next_incomplete_step_with_chapters(self):
        """Test that get_next_incomplete_step returns 'chapter_plan' when chapters exist."""
        story = self.create_complete_story_with_chapters()
        
        result = get_next_incomplete_step(story)
        self.assertEqual(result, 'chapter_plan')
    
    def test_get_next_incomplete_step_without_chapters(self):
        """Test that get_next_incomplete_step returns 'complete_story_selection' without chapters."""
        story = self.create_complete_story_with_chapters()
        # Remove chapters
        story.chapters.clear()
        
        result = get_next_incomplete_step(story)
        self.assertEqual(result, 'complete_story_selection')
    
    def test_get_next_incomplete_step_incomplete_story(self):
        """Test that get_next_incomplete_step returns appropriate step for incomplete story."""
        story = Story()
        story.story_type_name = "The Quest"
        story.subtype_name = "Spiritual Quest"
        # Missing other required fields
        
        result = get_next_incomplete_step(story)
        self.assertEqual(result, 'key_theme_selection')
    
    def test_load_story_with_chapters_redirects_to_chapter_plan(self):
        """Test that loading a story with chapters redirects to chapter-plan page."""
        story = self.create_complete_story_with_chapters()
        
        # Convert story to JSON
        story_json = story.to_json()
        
        # Create a file-like object for upload
        file_data = BytesIO(story_json.encode('utf-8'))
        
        with self.app as client:
            with client.session_transaction() as sess:
                sess.clear()  # Ensure clean state
            
            # Upload the file
            response = client.post('/load', data={
                'file': (file_data, 'test_story.json')
            }, follow_redirects=False)
            
            # Should redirect to chapter-plan
            self.assertEqual(response.status_code, 302)
            self.assertIn('/chapter-plan', response.location)
    
    def test_load_story_without_chapters_redirects_to_complete_story(self):
        """Test that loading a story without chapters redirects to complete-story-selection."""
        story = self.create_complete_story_with_chapters()
        # Remove chapters
        story.chapters.clear()
        
        # Convert story to JSON
        story_json = story.to_json()
        
        # Create a file-like object for upload
        file_data = BytesIO(story_json.encode('utf-8'))
        
        with self.app as client:
            with client.session_transaction() as sess:
                sess.clear()  # Ensure clean state
            
            # Upload the file
            response = client.post('/load', data={
                'file': (file_data, 'test_story.json')
            }, follow_redirects=False)
            
            # Should redirect to complete-story-selection
            self.assertEqual(response.status_code, 302)
            self.assertIn('/complete-story-selection', response.location)
    
    def test_load_incomplete_story_redirects_appropriately(self):
        """Test that loading an incomplete story redirects to the appropriate step."""
        story = Story()
        story.story_type_name = "The Quest"
        story.subtype_name = "Spiritual Quest"
        # Missing other required fields
        
        # Convert story to JSON
        story_json = story.to_json()
        
        # Create a file-like object for upload
        file_data = BytesIO(story_json.encode('utf-8'))
        
        with self.app as client:
            with client.session_transaction() as sess:
                sess.clear()  # Ensure clean state
            
            # Upload the file
            response = client.post('/load', data={
                'file': (file_data, 'test_story.json')
            }, follow_redirects=False)
            
            # Should redirect to key-theme-selection
            self.assertEqual(response.status_code, 302)
            self.assertIn('/key-theme-selection', response.location)


if __name__ == '__main__':
    unittest.main()