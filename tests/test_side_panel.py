#!/usr/bin/env python3
"""
Tests for Side Panel Update Behavior

This test validates that the side panel properly updates as users make selections.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from app import app
from flask import session


class TestSidePanelUpdates(unittest.TestCase):
    """Test side panel update behavior."""
    
    def setUp(self):
        """Set up test client."""
        self.app = app.test_client()
        self.app.testing = True
    
    def test_initial_state_no_selections(self):
        """Test that initial state shows no selections."""
        with self.app as client:
            with client.session_transaction() as sess:
                sess.clear()  # Ensure clean state
            
            response = client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'No selections made yet', response.data)
            self.assertNotIn(b'Story Type:', response.data)
    
    def test_story_type_selection_updates_panel(self):
        """Test that selecting a story type updates the left panel."""
        with self.app as client:
            with client.session_transaction() as sess:
                sess.clear()  # Ensure clean state
            
            # Select a story type
            response = client.get('/story_type/Comedy')
            self.assertEqual(response.status_code, 200)
            
            # Check that the left panel now shows the story type
            self.assertIn(b'Story Type:', response.data)
            self.assertIn(b'Comedy', response.data)
            self.assertNotIn(b'No selections made yet', response.data)
    
    def test_story_type_change_clears_dependent_selections(self):
        """Test that changing story type clears dependent selections."""
        with self.app as client:
            with client.session_transaction() as sess:
                sess.clear()  # Ensure clean state
            
            # First, make a complete selection
            client.get('/story_type/Comedy')
            client.get('/subtype/Comedy/Romantic%20Comedy')
            client.post('/key-theme-selection', data={'key_theme': 'Chaos gives way to understanding and joyful reunion.'})
            
            # Verify we have selections
            with client.session_transaction() as sess:
                story_data = sess.get('story_data', {})
                self.assertEqual(story_data.get('story_type_name'), 'Comedy')
                self.assertEqual(story_data.get('subtype_name'), 'Romantic Comedy')
                self.assertIsNotNone(story_data.get('key_theme'))
            
            # Now change to a different story type
            response = client.get('/story_type/Tragedy')
            self.assertEqual(response.status_code, 200)
            
            # Verify that dependent selections are cleared
            with client.session_transaction() as sess:
                story_data = sess.get('story_data', {})
                self.assertEqual(story_data.get('story_type_name'), 'Tragedy')
                self.assertIsNone(story_data.get('subtype_name'))
                self.assertIsNone(story_data.get('key_theme'))
                self.assertIsNone(story_data.get('core_arc'))
    
    def test_subtype_selection_updates_panel(self):
        """Test that selecting a subtype updates the left panel."""
        with self.app as client:
            with client.session_transaction() as sess:
                sess.clear()  # Ensure clean state
            
            # Select story type first
            client.get('/story_type/Comedy')
            
            # Select subtype
            response = client.get('/subtype/Comedy/Romantic%20Comedy')
            self.assertEqual(response.status_code, 200)
            
            # Check that the left panel shows both story type and subtype
            self.assertIn(b'Story Type:', response.data)
            self.assertIn(b'Comedy - Romantic Comedy', response.data)
    
    def test_key_theme_selection_updates_panel(self):
        """Test that selecting a key theme updates the left panel."""
        with self.app as client:
            with client.session_transaction() as sess:
                sess.clear()  # Ensure clean state
            
            # Set up story and subtype
            client.get('/story_type/Comedy')
            client.get('/subtype/Comedy/Romantic%20Comedy')
            
            # Select key theme
            response = client.post('/key-theme-selection', 
                                 data={'key_theme': 'Chaos gives way to understanding and joyful reunion.'})
            self.assertEqual(response.status_code, 302)  # Redirect after POST
            
            # Follow redirect to core arc selection
            response = client.get('/core-arc-selection')
            self.assertEqual(response.status_code, 200)
            
            # Check that the left panel shows the key theme
            self.assertIn(b'Key Theme:', response.data)
            self.assertIn(b'Chaos gives way to understanding', response.data)
    
    def test_core_arc_selection_updates_panel(self):
        """Test that selecting a core arc updates the left panel."""
        with self.app as client:
            with client.session_transaction() as sess:
                sess.clear()  # Ensure clean state
            
            # Set up story, subtype, and key theme
            client.get('/story_type/Comedy')
            client.get('/subtype/Comedy/Romantic%20Comedy')
            client.post('/key-theme-selection', 
                       data={'key_theme': 'Chaos gives way to understanding and joyful reunion.'})
            
            # Select core arc
            response = client.post('/core-arc-selection', 
                                 data={'core_arc': 'Truth becomes clear through well-meaning deception.'})
            self.assertEqual(response.status_code, 302)  # Redirect after POST
            
            # Follow redirect to genre selection
            response = client.get('/genre-selection')
            self.assertEqual(response.status_code, 200)
            
            # Check that the left panel shows the core arc
            self.assertIn(b'Core Arc:', response.data)
            self.assertIn(b'Truth becomes clear', response.data)
    
    def test_genre_selection_updates_panel(self):
        """Test that selecting a genre updates the left panel."""
        with self.app as client:
            with client.session_transaction() as sess:
                sess.clear()  # Ensure clean state
            
            # Set up minimal required selections
            client.get('/story_type/Comedy')
            client.get('/subtype/Comedy/Romantic%20Comedy')
            
            # Select genre
            response = client.post('/genre-selection', data={'genre': 'Romance'})
            self.assertEqual(response.status_code, 302)  # Redirect after POST
            
            # Follow redirect to sub-genre selection
            response = client.get('/subgenre-selection')
            self.assertEqual(response.status_code, 200)
            
            # Check that the left panel shows the genre
            self.assertIn(b'Genre:', response.data)
            self.assertIn(b'Romance', response.data)
    
    def test_subgenre_selection_updates_panel(self):
        """Test that selecting a sub-genre updates the left panel."""
        with self.app as client:
            with client.session_transaction() as sess:
                sess.clear()  # Ensure clean state
            
            # Set up minimal required selections
            client.get('/story_type/Comedy')
            client.get('/subtype/Comedy/Romantic%20Comedy')
            client.post('/genre-selection', data={'genre': 'Romance'})
            
            # Select sub-genre
            response = client.post('/subgenre-selection', data={'sub_genre': 'Romantic Comedy'})
            self.assertEqual(response.status_code, 302)  # Redirect after POST
            
            # Follow redirect back to subtype detail page
            response = client.get('/subtype/Comedy/Romantic%20Comedy')
            self.assertEqual(response.status_code, 200)
            
            # Check that the left panel shows the sub-genre
            self.assertIn(b'Sub-Genre:', response.data)
            self.assertIn(b'Romantic Comedy', response.data)
    
    def test_complete_flow_shows_all_selections(self):
        """Test that a complete flow shows all selections in the left panel."""
        with self.app as client:
            with client.session_transaction() as sess:
                sess.clear()  # Ensure clean state
            
            # Complete full flow
            client.get('/story_type/Comedy')
            client.get('/subtype/Comedy/Romantic%20Comedy')
            client.post('/key-theme-selection', 
                       data={'key_theme': 'Chaos gives way to understanding and joyful reunion.'})
            client.post('/core-arc-selection', 
                       data={'core_arc': 'Truth becomes clear through well-meaning deception.'})
            client.post('/genre-selection', data={'genre': 'Romance'})
            client.post('/subgenre-selection', data={'sub_genre': 'Romantic Comedy'})
            
            # Check final state
            response = client.get('/subtype/Comedy/Romantic%20Comedy')
            self.assertEqual(response.status_code, 200)
            
            # Verify all selections are shown in the left panel
            self.assertIn(b'Story Type:', response.data)
            self.assertIn(b'Comedy - Romantic Comedy', response.data)
            self.assertIn(b'Key Theme:', response.data)
            self.assertIn(b'Chaos gives way to understanding', response.data)
            self.assertIn(b'Core Arc:', response.data)
            self.assertIn(b'Truth becomes clear', response.data)
            self.assertIn(b'Genre:', response.data)
            self.assertIn(b'Romance', response.data)
            self.assertIn(b'Sub-Genre:', response.data)
            self.assertIn(b'Romantic Comedy', response.data)


def run_side_panel_tests():
    """Run all side panel tests."""
    print("=== Running Side Panel Update Tests ===\n")
    
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestSidePanelUpdates)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    if result.wasSuccessful():
        print("\n✅ All side panel tests passed!")
        return True
    else:
        print(f"\n❌ {len(result.failures)} test(s) failed, {len(result.errors)} error(s)")
        return False


if __name__ == "__main__":
    success = run_side_panel_tests()
    sys.exit(0 if success else 1)