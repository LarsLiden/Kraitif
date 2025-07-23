"""
Test suite for the Prompt class.

This module tests the prompt generation functionality, including
reading template files and combining them with story configuration.
"""

import unittest
import tempfile
import os
from unittest.mock import patch, mock_open
from prompt import Prompt
from story import Story


class TestPrompt(unittest.TestCase):
    """Test cases for the Prompt class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.prompt_generator = Prompt()
        
    def test_init_default_prompts_dir(self):
        """Test that Prompt initializes with default prompts directory."""
        prompt = Prompt()
        self.assertEqual(prompt.prompts_dir, "prompts")
        
    def test_init_custom_prompts_dir(self):
        """Test that Prompt initializes with custom prompts directory."""
        custom_dir = "/custom/prompts"
        prompt = Prompt(custom_dir)
        self.assertEqual(prompt.prompts_dir, custom_dir)
    
    def test_read_template_file_success(self):
        """Test reading a template file successfully."""
        with patch("builtins.open", mock_open(read_data="Test template content")):
            content = self.prompt_generator._read_template_file("test.txt")
            self.assertEqual(content, "Test template content")
    
    def test_read_template_file_not_found(self):
        """Test reading a non-existent template file returns empty string."""
        with patch("builtins.open", side_effect=FileNotFoundError):
            content = self.prompt_generator._read_template_file("nonexistent.txt")
            self.assertEqual(content, "")
    
    def test_read_template_file_io_error(self):
        """Test reading a template file with IO error returns empty string."""
        with patch("builtins.open", side_effect=IOError):
            content = self.prompt_generator._read_template_file("error.txt")
            self.assertEqual(content, "")
    
    @patch("prompt.Prompt._read_template_file")
    @patch("story.Story.to_prompt_text")
    def test_generate_plot_prompt_all_parts(self, mock_story_prompt, mock_read_file):
        """Test generating a plot prompt with all parts present."""
        # Setup mocks
        mock_read_file.side_effect = lambda filename: {
            "plot_lines_pre.txt": "Pre-prompt text",
            "plot_lines_post.txt": "Post-prompt text"
        }.get(filename, "")
        
        mock_story_prompt.return_value = "Story configuration text"
        
        # Create a story and generate prompt
        story = Story()
        result = self.prompt_generator.generate_plot_prompt(story)
        
        # Check that all parts are included and properly separated
        expected = "Pre-prompt text\n\nStory configuration text\n\nPost-prompt text"
        self.assertEqual(result, expected)
        
        # Verify the correct files were read
        mock_read_file.assert_any_call("plot_lines_pre.txt")
        mock_read_file.assert_any_call("plot_lines_post.txt")
        mock_story_prompt.assert_called_once()
    
    @patch("prompt.Prompt._read_template_file")
    @patch("story.Story.to_prompt_text")
    def test_generate_plot_prompt_only_story_config(self, mock_story_prompt, mock_read_file):
        """Test generating a plot prompt with only story configuration."""
        # Setup mocks - empty template files
        mock_read_file.return_value = ""
        mock_story_prompt.return_value = "Story configuration text"
        
        # Create a story and generate prompt
        story = Story()
        result = self.prompt_generator.generate_plot_prompt(story)
        
        # Should only contain the story configuration
        self.assertEqual(result, "Story configuration text")
    
    @patch("prompt.Prompt._read_template_file")
    @patch("story.Story.to_prompt_text")
    def test_generate_plot_prompt_empty_story_config(self, mock_story_prompt, mock_read_file):
        """Test generating a plot prompt with empty story configuration."""
        # Setup mocks
        mock_read_file.side_effect = lambda filename: {
            "plot_lines_pre.txt": "Pre-prompt text",
            "plot_lines_post.txt": "Post-prompt text"
        }.get(filename, "")
        
        mock_story_prompt.return_value = ""
        
        # Create a story and generate prompt
        story = Story()
        result = self.prompt_generator.generate_plot_prompt(story)
        
        # Should contain only the pre and post text
        expected = "Pre-prompt text\n\nPost-prompt text"
        self.assertEqual(result, expected)
    
    @patch("prompt.Prompt._read_template_file")
    @patch("story.Story.to_prompt_text")
    def test_generate_plot_prompt_whitespace_handling(self, mock_story_prompt, mock_read_file):
        """Test that whitespace is properly handled in prompt generation."""
        # Setup mocks with whitespace
        mock_read_file.side_effect = lambda filename: {
            "plot_lines_pre.txt": "  Pre-prompt text  \n\n",
            "plot_lines_post.txt": "\n  Post-prompt text  "
        }.get(filename, "")
        
        mock_story_prompt.return_value = "  Story configuration text  \n"
        
        # Create a story and generate prompt
        story = Story()
        result = self.prompt_generator.generate_plot_prompt(story)
        
        # Should strip whitespace but maintain content
        expected = "Pre-prompt text\n\nStory configuration text\n\nPost-prompt text"
        self.assertEqual(result, expected)
    
    @patch("prompt.Prompt._read_template_file")
    @patch("story.Story.to_prompt_text")
    def test_generate_plot_prompt_all_empty(self, mock_story_prompt, mock_read_file):
        """Test generating a plot prompt when all parts are empty."""
        # Setup mocks - all empty
        mock_read_file.return_value = ""
        mock_story_prompt.return_value = ""
        
        # Create a story and generate prompt
        story = Story()
        result = self.prompt_generator.generate_plot_prompt(story)
        
        # Should return empty string
        self.assertEqual(result, "")
    
    def test_integration_with_real_files(self):
        """Test integration with actual template files if they exist."""
        # This test uses the actual files in the prompts directory
        story = Story()
        
        # Generate prompt - this should work even if template files don't exist
        result = self.prompt_generator.generate_plot_prompt(story)
        
        # Result should be a string (could be empty if no files exist)
        self.assertIsInstance(result, str)
        
        # The result should contain content from the pre and post files if they exist
        # We can't test specific story content since the story is mostly empty
        # But we can verify the prompt generation works without errors


class TestCharacterPrompt(unittest.TestCase):
    """Test cases for the character prompt generation functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.prompt_generator = Prompt()
    
    @patch("prompt.Prompt._read_template_file")
    @patch("story.Story.to_prompt_text")
    def test_generate_character_prompt_all_parts(self, mock_story_prompt, mock_read_file):
        """Test generating a character prompt with all parts present."""
        # Setup mocks
        mock_read_file.side_effect = lambda filename: {
            "characters_pre.txt": "Character pre-prompt text",
            "characters_post.txt": "Character post-prompt text"
        }.get(filename, "")
        
        mock_story_prompt.return_value = "Story configuration text"
        
        # Create a story and generate prompt
        story = Story()
        result = self.prompt_generator.generate_character_prompt(story)
        
        # Check that all parts are included and properly separated
        expected = "Character pre-prompt text\n\nStory configuration text\n\nCharacter post-prompt text"
        self.assertEqual(result, expected)
        
        # Verify the correct files were read
        mock_read_file.assert_any_call("characters_pre.txt")
        mock_read_file.assert_any_call("characters_post.txt")
        mock_story_prompt.assert_called_once()
    
    @patch("prompt.Prompt._read_template_file")
    @patch("story.Story.to_prompt_text")
    def test_generate_character_prompt_only_story_config(self, mock_story_prompt, mock_read_file):
        """Test generating a character prompt with only story configuration."""
        # Setup mocks - empty template files
        mock_read_file.return_value = ""
        mock_story_prompt.return_value = "Story configuration text"
        
        # Create a story and generate prompt
        story = Story()
        result = self.prompt_generator.generate_character_prompt(story)
        
        # Should only contain the story configuration
        self.assertEqual(result, "Story configuration text")
    
    @patch("prompt.Prompt._read_template_file")
    @patch("story.Story.to_prompt_text")
    def test_generate_character_prompt_whitespace_handling(self, mock_story_prompt, mock_read_file):
        """Test that whitespace is properly handled in character prompt generation."""
        # Setup mocks with whitespace
        mock_read_file.side_effect = lambda filename: {
            "characters_pre.txt": "  Character pre-prompt text  \n\n",
            "characters_post.txt": "\n  Character post-prompt text  "
        }.get(filename, "")
        
        mock_story_prompt.return_value = "  Story configuration text  \n"
        
        # Create a story and generate prompt
        story = Story()
        result = self.prompt_generator.generate_character_prompt(story)
        
        # Should strip whitespace but maintain content
        expected = "Character pre-prompt text\n\nStory configuration text\n\nCharacter post-prompt text"
        self.assertEqual(result, expected)
    
    def test_generate_character_prompt_integration(self):
        """Test character prompt generation with actual template files."""
        # This test uses the actual files in the prompts directory
        story = Story()
        
        # Generate prompt - this should work even if template files don't exist
        result = self.prompt_generator.generate_character_prompt(story)
        
        # Result should be a string (could be empty if no files exist)
        self.assertIsInstance(result, str)


if __name__ == '__main__':
    unittest.main()