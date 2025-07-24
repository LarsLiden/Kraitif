#!/usr/bin/env python3
"""
Comprehensive tests for Flask app save/load functionality

This module provides robust testing for the Flask application's
file upload/download save/load routes.
"""

import sys
import os
import json
import tempfile
import unittest
from io import BytesIO
from unittest.mock import patch
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
from objects.story import Story


class TestFlaskSaveLoad(unittest.TestCase):
    """Test Flask app save/load functionality comprehensively."""
    
    def setUp(self):
        """Set up test client and configure testing."""
        self.app = app.test_client()
        self.app.testing = True
        app.config['TESTING'] = True
    
    def test_save_empty_story(self):
        """Test saving an empty story produces valid JSON."""
        with self.app as client:
            with client.session_transaction() as sess:
                sess.clear()  # Ensure clean state
            
            response = client.get('/save')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.headers['Content-Type'], 'application/json')
            self.assertIn('attachment', response.headers.get('Content-Disposition', ''))
            self.assertIn('kraitif_story.json', response.headers.get('Content-Disposition', ''))
            
            # Verify content is valid JSON
            json_data = response.get_data(as_text=True)
            data = json.loads(json_data)
            self.assertIsInstance(data, dict)
            
            # Should have all expected fields with None/empty values  
            expected_keys = {
                'story_type_name', 'subtype_name', 'key_theme', 'core_arc',
                'genre_name', 'sub_genre_name', 'writing_style_name', 'protagonist_archetype',
                'secondary_archetypes', 'characters', 'selected_plot_line', 'expanded_plot_line'
            }
            self.assertEqual(set(data.keys()), expected_keys)
    
    def test_save_complete_story(self):
        """Test saving a complete story with all selections."""
        with self.app as client:
            with client.session_transaction() as sess:
                sess.clear()
                # Set up a complete story in session
                sess['story_data'] = {
                    'story_type_name': 'Comedy',
                    'subtype_name': 'Romantic Comedy',
                    'key_theme': 'Love conquers all',
                    'core_arc': 'Meet-cute to marriage',
                    'genre_name': 'Romance',
                    'sub_genre_name': 'Romantic Comedy'
                }
            
            response = client.get('/save')
            self.assertEqual(response.status_code, 200)
            
            # Verify JSON content
            json_data = response.get_data(as_text=True)
            data = json.loads(json_data)
            
            self.assertEqual(data['story_type_name'], 'Comedy')
            self.assertEqual(data['subtype_name'], 'Romantic Comedy')
            self.assertEqual(data['key_theme'], 'Love conquers all')
            self.assertEqual(data['core_arc'], 'Meet-cute to marriage')
            self.assertEqual(data['genre_name'], 'Romance')
            self.assertEqual(data['sub_genre_name'], 'Romantic Comedy')
    
    def test_load_valid_json_file(self):
        """Test loading a valid JSON file."""
        # Create valid story JSON
        story_data = {
            'story_type_name': 'The Quest',
            'subtype_name': 'Object Quest',
            'key_theme': 'Adventure awaits',
            'core_arc': 'Journey arc',
            'genre_name': 'Fantasy',
            'sub_genre_name': 'High Fantasy',
            'protagonist_archetype': 'Chosen One',
            'secondary_archetypes': ['Wise Mentor']
        }
        json_content = json.dumps(story_data, indent=2)
        
        with self.app as client:
            with client.session_transaction() as sess:
                sess.clear()
            
            # Simulate file upload
            data = {
                'file': (BytesIO(json_content.encode('utf-8')), 'test_story.json')
            }
            
            response = client.post('/load', data=data, content_type='multipart/form-data')
            self.assertEqual(response.status_code, 302)  # Redirect after successful load
            
            # Check that story data was loaded into session
            with client.session_transaction() as sess:
                story_data_session = sess.get('story_data', {})
                self.assertEqual(story_data_session.get('story_type_name'), 'The Quest')
                self.assertEqual(story_data_session.get('genre_name'), 'Fantasy')
    
    def test_load_no_file_selected(self):
        """Test loading with no file selected."""
        with self.app as client:
            # No file in request
            response = client.post('/load', data={})
            self.assertEqual(response.status_code, 302)  # Redirect
            
            # Check for error flash message (we can't easily test flash messages in unit tests,
            # but we can verify the redirect happened)
            self.assertIn('Location', response.headers)
    
    def test_load_empty_filename(self):
        """Test loading with empty filename."""
        with self.app as client:
            data = {
                'file': (BytesIO(b'{}'), '')  # Empty filename
            }
            
            response = client.post('/load', data=data, content_type='multipart/form-data')
            self.assertEqual(response.status_code, 302)  # Redirect due to error
    
    def test_load_non_json_file(self):
        """Test loading a non-JSON file."""
        with self.app as client:
            data = {
                'file': (BytesIO(b'not json content'), 'test.txt')
            }
            
            response = client.post('/load', data=data, content_type='multipart/form-data')
            self.assertEqual(response.status_code, 302)  # Redirect due to error
    
    def test_load_invalid_json_content(self):
        """Test loading a file with invalid JSON content."""
        invalid_json = '{"invalid": json content}'
        
        with self.app as client:
            data = {
                'file': (BytesIO(invalid_json.encode('utf-8')), 'invalid.json')
            }
            
            response = client.post('/load', data=data, content_type='multipart/form-data')
            self.assertEqual(response.status_code, 302)  # Redirect due to error
    
    def test_load_valid_json_invalid_story_data(self):
        """Test loading valid JSON that doesn't represent a valid story."""
        # Valid JSON but with invalid story data
        invalid_story_data = {
            'story_type_name': 'NonExistentStoryType',
            'genre_name': 'NonExistentGenre',
            'protagonist_archetype': 'NonExistentArchetype'
        }
        json_content = json.dumps(invalid_story_data)
        
        with self.app as client:
            with client.session_transaction() as sess:
                sess.clear()
            
            data = {
                'file': (BytesIO(json_content.encode('utf-8')), 'invalid_story.json')
            }
            
            response = client.post('/load', data=data, content_type='multipart/form-data')
            self.assertEqual(response.status_code, 302)  # Should still redirect (success)
            
            # Check that story data was loaded (invalid data gets filtered out)
            with client.session_transaction() as sess:
                story_data_session = sess.get('story_data', {})
                self.assertEqual(story_data_session.get('story_type_name'), 'NonExistentStoryType')
                # Invalid genre should result in no genre being set
                self.assertIsNone(story_data_session.get('genre_name'))
    
    def test_save_load_roundtrip(self):
        """Test complete save/load roundtrip preserves data."""
        with self.app as client:
            # Set up initial story data
            with client.session_transaction() as sess:
                sess.clear()
                sess['story_data'] = {
                    'story_type_name': 'Tragedy',
                    'subtype_name': 'Personal Tragedy',
                    'key_theme': 'Pride leads to downfall',
                    'core_arc': 'Hubris to nemesis',
                    'genre_name': 'Drama'
                }
            
            # Save the story
            save_response = client.get('/save')
            self.assertEqual(save_response.status_code, 200)
            saved_json = save_response.get_data(as_text=True)
            
            # Clear session
            with client.session_transaction() as sess:
                sess.clear()
            
            # Load the saved data back
            data = {
                'file': (BytesIO(saved_json.encode('utf-8')), 'roundtrip_test.json')
            }
            load_response = client.post('/load', data=data, content_type='multipart/form-data')
            self.assertEqual(load_response.status_code, 302)
            
            # Verify data was restored
            with client.session_transaction() as sess:
                story_data_session = sess.get('story_data', {})
                self.assertEqual(story_data_session.get('story_type_name'), 'Tragedy')
                self.assertEqual(story_data_session.get('subtype_name'), 'Personal Tragedy')
                self.assertEqual(story_data_session.get('key_theme'), 'Pride leads to downfall')
                self.assertEqual(story_data_session.get('core_arc'), 'Hubris to nemesis')
                self.assertEqual(story_data_session.get('genre_name'), 'Drama')
    
    def test_load_with_archetype_data(self):
        """Test loading a file with archetype selections."""
        story_data = {
            'story_type_name': 'Rebirth',
            'subtype_name': 'Redemption',
            'protagonist_archetype': 'Anti-Hero',
            'secondary_archetypes': ['Wise Mentor', 'Loyal Companion']
        }
        json_content = json.dumps(story_data)
        
        with self.app as client:
            with client.session_transaction() as sess:
                sess.clear()
            
            data = {
                'file': (BytesIO(json_content.encode('utf-8')), 'archetype_story.json')
            }
            
            response = client.post('/load', data=data, content_type='multipart/form-data')
            self.assertEqual(response.status_code, 302)
            
            # Verify archetype data was loaded
            with client.session_transaction() as sess:
                story_data_session = sess.get('story_data', {})
                self.assertEqual(story_data_session.get('protagonist_archetype'), 'Anti-Hero')
                self.assertEqual(story_data_session.get('secondary_archetypes'), ['Wise Mentor', 'Loyal Companion'])
    
    def test_save_with_unicode_content(self):
        """Test saving story with unicode/special characters."""
        with self.app as client:
            with client.session_transaction() as sess:
                sess.clear()
                sess['story_data'] = {
                    'story_type_name': 'Comedy',
                    'key_theme': 'Liebe überwindet alle Hindernisse! 💕',  # German + emoji
                    'core_arc': 'από τη σύγχυση στην αρμονία'  # Greek text
                }
            
            response = client.get('/save')
            self.assertEqual(response.status_code, 200)
            
            # Verify unicode content is preserved
            json_data = response.get_data(as_text=True)
            data = json.loads(json_data)
            self.assertIn('💕', data['key_theme'])
            self.assertIn('σύγχυση', data['core_arc'])
    
    def test_load_with_unicode_content(self):
        """Test loading story with unicode/special characters."""
        story_data = {
            'story_type_name': 'Romance',
            'key_theme': 'L\'amour triomphe de tout 🌹',  # French + emoji
            'core_arc': 'Desde el caos hasta la armonía'  # Spanish
        }
        json_content = json.dumps(story_data, ensure_ascii=False)
        
        with self.app as client:
            with client.session_transaction() as sess:
                sess.clear()
            
            data = {
                'file': (BytesIO(json_content.encode('utf-8')), 'unicode_story.json')
            }
            
            response = client.post('/load', data=data, content_type='multipart/form-data')
            self.assertEqual(response.status_code, 302)
            
            # Verify unicode content was preserved
            with client.session_transaction() as sess:
                story_data_session = sess.get('story_data', {})
                self.assertIn('🌹', story_data_session.get('key_theme', ''))
                self.assertIn('armonía', story_data_session.get('core_arc', ''))


def run_flask_save_load_tests():
    """Run all Flask save/load tests."""
    print("=== Running Flask Save/Load Tests ===\n")
    
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestFlaskSaveLoad)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    if result.wasSuccessful():
        print("\n✅ All Flask save/load tests passed!")
        return True
    else:
        print(f"\n❌ {len(result.failures)} test(s) failed, {len(result.errors)} error(s)")
        for failure in result.failures:
            print(f"FAILURE: {failure[0]}")
            print(failure[1][:500])  # Truncate long output
        for error in result.errors:
            print(f"ERROR: {error[0]}")
            print(error[1][:500])
        return False


if __name__ == "__main__":
    success = run_flask_save_load_tests()
    sys.exit(0 if success else 1)