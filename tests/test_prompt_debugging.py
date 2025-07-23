"""
Test suite for prompt debugging functionality.

This module tests the debugging features added to the AI client,
including prompt type categorization and file saving.
"""

import unittest
import tempfile
import os
import shutil
from unittest.mock import patch, MagicMock
from ai.ai_client import get_ai_response, _save_debug_files
from prompt_types import PromptType


class TestPromptDebugging(unittest.TestCase):
    """Test cases for prompt debugging functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary directory for debug files
        self.test_debug_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        
    def tearDown(self):
        """Clean up test fixtures."""
        # Clean up temporary directory
        if os.path.exists(self.test_debug_dir):
            shutil.rmtree(self.test_debug_dir)
        os.chdir(self.original_cwd)
    
    def test_save_debug_files_creates_directory(self):
        """Test that _save_debug_files creates debug directory if it doesn't exist."""
        # Change to temp directory
        os.chdir(self.test_debug_dir)
        
        # Ensure debug directory doesn't exist
        debug_dir = "debug"
        if os.path.exists(debug_dir):
            shutil.rmtree(debug_dir)
        
        # Call save_debug_files
        _save_debug_files("test prompt", "test response", PromptType.PLOT_LINES)
        
        # Check that debug directory was created
        self.assertTrue(os.path.exists(debug_dir))
        
    def test_save_debug_files_creates_correct_filename(self):
        """Test that _save_debug_files creates file with correct name."""
        # Change to temp directory
        os.chdir(self.test_debug_dir)
        
        # Call save_debug_files
        _save_debug_files("test prompt", "test response", PromptType.PLOT_LINES)
        
        # Check that correct file was created
        expected_file = os.path.join("debug", "plot_lines.txt")
        self.assertTrue(os.path.exists(expected_file))
        
    def test_save_debug_files_content_format(self):
        """Test that _save_debug_files saves content in correct format."""
        # Change to temp directory
        os.chdir(self.test_debug_dir)
        
        test_prompt = "This is a test prompt"
        test_response = "This is a test response"
        
        # Call save_debug_files
        _save_debug_files(test_prompt, test_response, PromptType.PLOT_LINES)
        
        # Read the saved file
        expected_file = os.path.join("debug", "plot_lines.txt")
        with open(expected_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check content format
        self.assertIn("Timestamp:", content)
        self.assertIn("Prompt Type: plot_lines", content)
        self.assertIn("===============PROMPT=================", content)
        self.assertIn(test_prompt, content)
        self.assertIn("===============RESPONSE=================", content)
        self.assertIn(test_response, content)
        
    def test_save_debug_files_overwrites_existing(self):
        """Test that _save_debug_files overwrites existing files."""
        # Change to temp directory
        os.chdir(self.test_debug_dir)
        
        # Create debug directory and file
        debug_dir = "debug"
        os.makedirs(debug_dir, exist_ok=True)
        test_file = os.path.join(debug_dir, "plot_lines.txt")
        with open(test_file, 'w') as f:
            f.write("old content")
        
        # Call save_debug_files with new content
        new_prompt = "new prompt"
        new_response = "new response"
        _save_debug_files(new_prompt, new_response, PromptType.PLOT_LINES)
        
        # Read the file and check it was overwritten
        with open(test_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        self.assertIn(new_prompt, content)
        self.assertIn(new_response, content)
        self.assertNotIn("old content", content)
        
    def test_save_debug_files_handles_exceptions(self):
        """Test that _save_debug_files handles exceptions gracefully."""
        # Test with invalid directory permissions (simulate by using a read-only path)
        with patch('builtins.open', side_effect=PermissionError("Permission denied")):
            # This should not raise an exception
            try:
                _save_debug_files("test prompt", "test response", PromptType.PLOT_LINES)
            except Exception:
                self.fail("_save_debug_files should handle exceptions gracefully")
    
    @patch('ai.ai_client.get_ai_client')
    def test_get_ai_response_calls_save_debug_files(self, mock_get_client):
        """Test that get_ai_response calls _save_debug_files."""
        # Change to temp directory
        os.chdir(self.test_debug_dir)
        
        # Mock the AI client
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "test ai response"
        mock_client.chat.completions.create.return_value = mock_response
        mock_get_client.return_value = mock_client
        
        # Call get_ai_response
        test_prompt = "test prompt for ai"
        result = get_ai_response(test_prompt, PromptType.PLOT_LINES)
        
        # Check that response is correct
        self.assertEqual(result, "test ai response")
        
        # Check that debug file was created
        expected_file = os.path.join("debug", "plot_lines.txt")
        self.assertTrue(os.path.exists(expected_file))
        
        # Check that debug file contains the prompt and response
        with open(expected_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        self.assertIn(test_prompt, content)
        self.assertIn("test ai response", content)
    
    @patch('ai.ai_client.get_ai_client')
    def test_get_ai_response_saves_debug_on_error(self, mock_get_client):
        """Test that get_ai_response saves debug files even when AI call fails."""
        # Change to temp directory
        os.chdir(self.test_debug_dir)
        
        # Mock the AI client to raise an exception
        mock_get_client.side_effect = Exception("AI service error")
        
        # Call get_ai_response
        test_prompt = "test prompt that will fail"
        result = get_ai_response(test_prompt, PromptType.PLOT_LINES)
        
        # Check that error is returned
        self.assertIn("Error:", result)
        
        # Check that debug file was still created
        expected_file = os.path.join("debug", "plot_lines.txt")
        self.assertTrue(os.path.exists(expected_file))
        
        # Check that debug file contains the prompt and error response
        with open(expected_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        self.assertIn(test_prompt, content)
        self.assertIn("Error:", content)


if __name__ == '__main__':
    unittest.main()