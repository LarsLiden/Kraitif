#!/usr/bin/env python3
"""
Test for edit plot line functionality
"""

import unittest
from app import app
from objects.story import Story
from objects.plot_line import PlotLine
from objects.character import Character
from objects.archetype import ArchetypeEnum
from objects.functional_role import FunctionalRoleEnum
from objects.emotional_function import EmotionalFunctionEnum


class TestEditPlotLine(unittest.TestCase):
    def setUp(self):
        """Set up test client and story."""
        self.app = app.test_client()
        self.app.testing = True
    
    def test_edit_plot_line_route_exists(self):
        """Test that the edit plot line route exists and is accessible."""
        response = self.app.get('/edit-plot-line')
        # Should redirect to secondary archetype selection
        self.assertEqual(response.status_code, 302)
        self.assertIn('secondary-archetype-selection', response.location)
    
    def test_edit_plot_line_clears_data(self):
        """Test that editing plot line clears plot line, expanded plot line, and characters."""
        with self.app as client:
            with client.session_transaction() as sess:
                # Create a story with plot line, expanded plot line, and characters
                story_data = {
                    'story_type_name': 'The Quest',
                    'subtype_name': 'Spiritual Quest',
                    'key_theme': 'Redemption',
                    'core_arc': 'The Hero\'s Journey',
                    'genre_name': 'Fantasy',
                    'sub_genre_name': 'High Fantasy',
                    'writing_style_name': 'Lyrical',
                    'protagonist_archetype': 'Chosen One',
                    'secondary_archetypes': ['Wise Mentor'],
                    'selected_plot_line': {
                        'name': 'Test Plot Line',
                        'plotline': 'A test plot line description'
                    },
                    'expanded_plot_line': 'An expanded version of the plot line',
                    'characters': [
                        {
                            'name': 'Hero',
                            'archetype': 'Chosen One',
                            'functional_role': 'Protagonist',
                            'emotional_function': 'Sympathetic Character',
                            'backstory': 'A young hero',
                            'character_arc': 'Becomes powerful'
                        },
                        {
                            'name': 'Mentor',
                            'archetype': 'Wise Mentor',
                            'functional_role': 'Mentor',
                            'emotional_function': 'Sympathetic Character',
                            'backstory': 'An old wise man',
                            'character_arc': 'Guides the hero'
                        }
                    ]
                }
                sess['story_data'] = story_data
            
            # Access edit plot line route
            response = client.get('/edit-plot-line')
            
            # Check that it redirects properly
            self.assertEqual(response.status_code, 302)
            self.assertIn('secondary-archetype-selection', response.location)
            
            # Check that the session data has been cleared appropriately
            with client.session_transaction() as sess:
                story_data = sess.get('story_data', {})
                
                # Plot line data should be cleared
                self.assertIsNone(story_data.get('selected_plot_line'))
                self.assertIsNone(story_data.get('expanded_plot_line'))
                self.assertEqual(story_data.get('characters', []), [])
                
                # Other story data should remain
                self.assertEqual(story_data.get('story_type_name'), 'The Quest')
                self.assertEqual(story_data.get('protagonist_archetype'), 'Chosen One')
                self.assertEqual(story_data.get('secondary_archetypes'), ['Wise Mentor'])
    
    def test_edit_plot_line_preserves_other_data(self):
        """Test that editing plot line preserves all other story selections."""
        with self.app as client:
            with client.session_transaction() as sess:
                story_data = {
                    'story_type_name': 'Overcoming the Monster',
                    'subtype_name': 'Pure Overcoming',
                    'key_theme': 'Good vs Evil',
                    'core_arc': 'The Hero\'s Journey',
                    'genre_name': 'Fantasy',
                    'sub_genre_name': 'High Fantasy',
                    'writing_style_name': 'Epic',
                    'protagonist_archetype': 'Chosen One',
                    'secondary_archetypes': ['Wise Mentor', 'Loyal Companion'],
                    'selected_plot_line': {
                        'name': 'Monster Quest',
                        'plotline': 'Hero must defeat the great monster'
                    }
                }
                sess['story_data'] = story_data
            
            # Access edit plot line route
            response = client.get('/edit-plot-line')
            
            # Check preserved data - focus on core story elements that don't depend on registry objects
            with client.session_transaction() as sess:
                story_data = sess.get('story_data', {})
                
                # These should all be preserved
                self.assertEqual(story_data.get('story_type_name'), 'Overcoming the Monster')
                self.assertEqual(story_data.get('subtype_name'), 'Pure Overcoming')
                self.assertEqual(story_data.get('key_theme'), 'Good vs Evil')
                self.assertEqual(story_data.get('core_arc'), 'The Hero\'s Journey')
                self.assertEqual(story_data.get('protagonist_archetype'), 'Chosen One')
                self.assertEqual(story_data.get('secondary_archetypes'), ['Wise Mentor', 'Loyal Companion'])
                
                # Plot line should be cleared
                self.assertIsNone(story_data.get('selected_plot_line'))


if __name__ == '__main__':
    unittest.main()