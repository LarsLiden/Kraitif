#!/usr/bin/env python3
"""
Test cases for post-load page landing functionality.
"""

import unittest
import json
import io
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, get_next_incomplete_step
from objects.story import Story


class TestPostLoadPageLanding(unittest.TestCase):
    """Test post-load page landing functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.app = app
        self.app.config['TESTING'] = True

    def test_get_next_incomplete_step_empty_story(self):
        """Test get_next_incomplete_step with empty story."""
        story = Story()
        next_step = get_next_incomplete_step(story)
        self.assertEqual(next_step, 'index')

    def test_get_next_incomplete_step_story_type_only(self):
        """Test get_next_incomplete_step with only story type set."""
        story = Story()
        story.story_type_name = "Overcoming the Monster"
        next_step = get_next_incomplete_step(story)
        self.assertEqual(next_step, 'story_type')

    def test_get_next_incomplete_step_genre_set_no_subgenre(self):
        """Test the specific example from issue: genre set but sub-genre not set."""
        story = Story()
        story.story_type_name = "Overcoming the Monster"
        story.subtype_name = "Classic Monster Slaying"
        story.key_theme = "Good versus evil"
        story.core_arc = "Hero's courage grows"
        story.set_genre("Fantasy")
        next_step = get_next_incomplete_step(story)
        self.assertEqual(next_step, 'subgenre_selection')

    def test_get_next_incomplete_step_protagonist_set_no_plot_line(self):
        """Test that when protagonist is set but no plot line, redirect to secondary archetype selection."""
        story = Story()
        story.story_type_name = "Overcoming the Monster"
        story.subtype_name = "Classic Monster Slaying"
        story.key_theme = "Good versus evil"
        story.core_arc = "Hero's courage grows"
        story.set_genre("Fantasy")
        story.set_sub_genre("High Fantasy")
        story.set_writing_style("Concise")
        story.set_protagonist_archetype("Chosen One")
        # No plot line set
        next_step = get_next_incomplete_step(story)
        self.assertEqual(next_step, 'secondary_archetype_selection')

    def test_get_next_incomplete_step_plot_line_set_no_characters(self):
        """Test that when plot line is set but no characters, redirect to plot line selected page."""
        from objects.plot_line import PlotLine
        story = Story()
        story.story_type_name = "Overcoming the Monster"
        story.subtype_name = "Classic Monster Slaying"
        story.key_theme = "Good versus evil"
        story.core_arc = "Hero's courage grows"
        story.set_genre("Fantasy")
        story.set_sub_genre("High Fantasy")
        story.set_writing_style("Concise")
        story.set_protagonist_archetype("Chosen One")
        # Set plot line but no characters
        plot_line = PlotLine("Test Plot", "A test plot line")
        story.set_selected_plot_line(plot_line)
        next_step = get_next_incomplete_step(story)
        self.assertEqual(next_step, 'plot_line_selected')

    def test_get_next_incomplete_step_complete_story(self):
        """Test get_next_incomplete_step with complete story including characters."""
        from objects.plot_line import PlotLine
        from objects.character import Character
        from objects.archetype import ArchetypeEnum
        from objects.functional_role import FunctionalRoleEnum
        from objects.emotional_function import EmotionalFunctionEnum
        
        story = Story()
        story.story_type_name = "Overcoming the Monster"
        story.subtype_name = "Classic Monster Slaying"
        story.key_theme = "Good versus evil"
        story.core_arc = "Hero's courage grows"
        story.set_genre("Fantasy")
        story.set_sub_genre("High Fantasy")
        story.set_writing_style("Concise")
        story.set_protagonist_archetype("Chosen One")
        
        # Set plot line
        plot_line = PlotLine("Test Plot", "A test plot line")
        story.set_selected_plot_line(plot_line)
        
        # Add characters
        protagonist = Character(
            name="Hero",
            archetype=ArchetypeEnum.CHOSEN_ONE,
            functional_role=FunctionalRoleEnum.PROTAGONIST,
            emotional_function=EmotionalFunctionEnum.SYMPATHETIC_CHARACTER
        )
        story.add_character(protagonist)
        
        next_step = get_next_incomplete_step(story)
        self.assertEqual(next_step, 'complete_story_selection')

    def test_load_redirects_to_subgenre_selection(self):
        """Test that loading a story with genre set redirects to sub-genre selection."""
        with self.app.test_client() as client:
            # Create a story with genre set but no sub-genre
            story = Story()
            story.story_type_name = "Overcoming the Monster"
            story.subtype_name = "Classic Monster Slaying"
            story.key_theme = "Good versus evil"
            story.core_arc = "Hero's courage grows"
            story.set_genre("Fantasy")
            
            json_data = story.to_json()
            file_data = io.BytesIO(json_data.encode('utf-8'))
            file_data.name = 'test_story.json'
            
            response = client.post('/load', data={'file': (file_data, 'test_story.json')})
            
            self.assertEqual(response.status_code, 302)
            self.assertIn('/subgenre-selection', response.location)

    def test_load_redirects_to_writing_style_selection(self):
        """Test that loading a story with sub-genre set redirects to writing style selection."""
        with self.app.test_client() as client:
            # Create a story with sub-genre set but no writing style
            story = Story()
            story.story_type_name = "Overcoming the Monster"
            story.subtype_name = "Classic Monster Slaying"
            story.key_theme = "Good versus evil"
            story.core_arc = "Hero's courage grows"
            story.set_genre("Fantasy")
            story.set_sub_genre("High Fantasy")
            
            json_data = story.to_json()
            file_data = io.BytesIO(json_data.encode('utf-8'))
            file_data.name = 'test_story.json'
            
            response = client.post('/load', data={'file': (file_data, 'test_story.json')})
            
            self.assertEqual(response.status_code, 302)
            self.assertIn('/writing-style-selection', response.location)

    def test_load_redirects_to_secondary_archetype_selection(self):
        """Test that loading a story with protagonist but no plot line redirects to secondary archetype selection."""
        with self.app.test_client() as client:
            # Create a story with protagonist but no plot line
            story = Story()
            story.story_type_name = "Overcoming the Monster"
            story.subtype_name = "Classic Monster Slaying"
            story.key_theme = "Good versus evil"
            story.core_arc = "Hero's courage grows"
            story.set_genre("Fantasy")
            story.set_sub_genre("High Fantasy")
            story.set_writing_style("Concise")
            story.set_protagonist_archetype("Chosen One")
            # No plot line set
            
            json_data = story.to_json()
            file_data = io.BytesIO(json_data.encode('utf-8'))
            file_data.name = 'test_story.json'
            
            response = client.post('/load', data={'file': (file_data, 'test_story.json')})
            
            self.assertEqual(response.status_code, 302)
            self.assertIn('/secondary-archetype-selection', response.location)

    def test_load_redirects_to_plot_line_selected(self):
        """Test that loading a story with plot line but no characters redirects to plot line selected page."""
        with self.app.test_client() as client:
            # Create a story with plot line but no characters
            from objects.plot_line import PlotLine
            
            story = Story()
            story.story_type_name = "Overcoming the Monster"
            story.subtype_name = "Classic Monster Slaying"
            story.key_theme = "Good versus evil"
            story.core_arc = "Hero's courage grows"
            story.set_genre("Fantasy")
            story.set_sub_genre("High Fantasy")
            story.set_writing_style("Concise")
            story.set_protagonist_archetype("Chosen One")
            
            # Set plot line but no characters
            plot_line = PlotLine("Test Plot", "A test plot line")
            story.set_selected_plot_line(plot_line)
            
            json_data = story.to_json()
            file_data = io.BytesIO(json_data.encode('utf-8'))
            file_data.name = 'test_story.json'
            
            response = client.post('/load', data={'file': (file_data, 'test_story.json')})
            
            self.assertEqual(response.status_code, 302)
            self.assertIn('/plot-line-selected', response.location)

    def test_load_redirects_to_complete_story_selection(self):
        """Test that loading a complete story redirects to completion page."""
        with self.app.test_client() as client:
            # Create a complete story with plot line and characters
            from objects.plot_line import PlotLine
            from objects.character import Character
            from objects.archetype import ArchetypeEnum
            from objects.functional_role import FunctionalRoleEnum
            from objects.emotional_function import EmotionalFunctionEnum
            
            story = Story()
            story.story_type_name = "Overcoming the Monster"
            story.subtype_name = "Classic Monster Slaying"
            story.key_theme = "Good versus evil"
            story.core_arc = "Hero's courage grows"
            story.set_genre("Fantasy")
            story.set_sub_genre("High Fantasy")
            story.set_writing_style("Concise")
            story.set_protagonist_archetype("Chosen One")
            
            # Add plot line
            plot_line = PlotLine("Test Plot", "A test plot line")
            story.set_selected_plot_line(plot_line)
            
            # Add characters
            protagonist = Character(
                name="Hero",
                archetype=ArchetypeEnum.CHOSEN_ONE,
                functional_role=FunctionalRoleEnum.PROTAGONIST,
                emotional_function=EmotionalFunctionEnum.SYMPATHETIC_CHARACTER
            )
            story.add_character(protagonist)
            
            json_data = story.to_json()
            file_data = io.BytesIO(json_data.encode('utf-8'))
            file_data.name = 'test_story.json'
            
            response = client.post('/load', data={'file': (file_data, 'test_story.json')})
            
            self.assertEqual(response.status_code, 302)
            self.assertIn('/complete-story-selection', response.location)

    def test_load_invalid_file_redirects_to_index(self):
        """Test that loading an invalid file redirects to index with error message."""
        with self.app.test_client() as client:
            # Create invalid JSON
            file_data = io.BytesIO(b'invalid json')
            file_data.name = 'invalid.json'
            
            response = client.post('/load', data={'file': (file_data, 'invalid.json')})
            
            self.assertEqual(response.status_code, 302)
            self.assertIn('/', response.location)  # Should redirect to index


if __name__ == '__main__':
    unittest.main()