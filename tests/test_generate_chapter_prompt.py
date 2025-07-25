"""
Test suite for the generate_chapter_prompt functionality.

This module tests the new chapter prompt generation functionality, including
the Story.to_prompt_text_for_chapter method and Prompt.generate_chapter_prompt method.
"""

import unittest
from unittest.mock import patch, mock_open
from prompt import Prompt
from objects.story import Story
from objects.chapter import Chapter
from objects.archetype import ArchetypeEnum
from objects.plot_line import PlotLine


class TestStoryToPromptTextForChapter(unittest.TestCase):
    """Test cases for the Story.to_prompt_text_for_chapter method."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.story = Story()
        # Set basic story properties
        self.story.story_type_name = 'The Quest'
        self.story.subtype_name = 'Spiritual Quest'
        self.story.key_theme = 'Finding Inner Peace'
        self.story.core_arc = 'Spiritual Awakening'
        
        # Set protagonist and secondary archetypes
        self.story.protagonist_archetype = ArchetypeEnum.CHOSEN_ONE
        self.story.secondary_archetypes = [ArchetypeEnum.WISE_MENTOR]
        
        # Set selected plot line
        self.story.selected_plot_line = PlotLine("Test Plot", "A test plot line description")
        
        # Add some chapters
        chapter1 = Chapter(1, 'The Beginning', 'Hero starts journey')
        chapter2 = Chapter(2, 'First Challenge', 'Hero faces obstacles')
        chapter3 = Chapter(3, 'Transformation', 'Hero changes')
        
        self.story.add_chapter(chapter1)
        self.story.add_chapter(chapter2)
        self.story.add_chapter(chapter3)
    
    def test_to_prompt_text_for_chapter_excludes_protagonist_archetype(self):
        """Test that protagonist_archetype is excluded from chapter prompt."""
        result = self.story.to_prompt_text_for_chapter(2)
        
        # Should not contain protagonist archetype section
        self.assertNotIn("Protagonist Archetype: Chosen One", result)
        self.assertNotIn("CHARACTER ARCHETYPES:", result)
    
    def test_to_prompt_text_for_chapter_excludes_secondary_archetypes(self):
        """Test that secondary_archetypes are excluded from chapter prompt."""
        result = self.story.to_prompt_text_for_chapter(2)
        
        # Should not contain secondary archetype section
        self.assertNotIn("Secondary Character Archetypes:", result)
        self.assertNotIn("Wise Mentor", result)
    
    def test_to_prompt_text_for_chapter_excludes_selected_plot_line(self):
        """Test that selected_plot_line is excluded from chapter prompt."""
        result = self.story.to_prompt_text_for_chapter(2)
        
        # Should not contain selected plot line section
        self.assertNotIn("SELECTED PLOT LINE:", result)
        self.assertNotIn("Test Plot", result)
        self.assertNotIn("A test plot line description", result)
    
    def test_to_prompt_text_for_chapter_includes_common_story_fields(self):
        """Test that common story fields are still included in chapter prompt."""
        result = self.story.to_prompt_text_for_chapter(2)
        
        # Should contain basic story information
        self.assertIn("STORY CONFIGURATION:", result)
        self.assertIn("Story Type: The Quest", result)
        self.assertIn("Story Subtype: Spiritual Quest", result)
        self.assertIn("Finding Inner Peace", result)
        self.assertIn("Spiritual Awakening", result)
    
    def test_to_prompt_text_for_chapter_filters_chapters_correctly(self):
        """Test that only chapters 1 to n-1 are included."""
        # Test for chapter 3 (should include chapters 1 and 2 only)
        result = self.story.to_prompt_text_for_chapter(3)
        
        # Should contain chapters 1 and 2
        self.assertIn("Chapter 1: The Beginning", result)
        self.assertIn("Chapter 2: First Challenge", result)
        # Should not contain chapter 3
        self.assertNotIn("Chapter 3: Transformation", result)
    
    def test_to_prompt_text_for_chapter_no_previous_chapters_for_first(self):
        """Test that no chapters are included when generating for chapter 1."""
        result = self.story.to_prompt_text_for_chapter(1)
        
        # Should not contain any chapter structure section
        self.assertNotIn("CHAPTER STRUCTURE:", result)
        self.assertNotIn("Chapter 1:", result)
        self.assertNotIn("Chapter 2:", result)
        self.assertNotIn("Chapter 3:", result)
    
    def test_to_prompt_text_for_chapter_preserves_original_chapters(self):
        """Test that the original chapters list is preserved after the method call."""
        original_chapter_count = len(self.story.chapters)
        original_chapters = [c.chapter_number for c in self.story.chapters]
        
        # Call the method
        self.story.to_prompt_text_for_chapter(2)
        
        # Verify original chapters are preserved
        self.assertEqual(len(self.story.chapters), original_chapter_count)
        current_chapters = [c.chapter_number for c in self.story.chapters]
        self.assertEqual(current_chapters, original_chapters)
    
    def test_to_prompt_text_for_chapter_includes_expanded_plot_line(self):
        """Test that expanded_plot_line is included when available."""
        self.story.expanded_plot_line = "This is an expanded plot line with more details."
        
        result = self.story.to_prompt_text_for_chapter(2)
        
        # Should contain expanded plot line
        self.assertIn("EXPANDED PLOT LINE:", result)
        self.assertIn("This is an expanded plot line with more details.", result)
    
    def test_to_prompt_text_for_chapter_includes_characters_when_available(self):
        """Test that Character objects are included when they exist."""
        from objects.character import Character
        from objects.functional_role import FunctionalRoleEnum
        from objects.emotional_function import EmotionalFunctionEnum
        
        # Add a character to the story
        character = Character(
            name="Hero",
            archetype=ArchetypeEnum.CHOSEN_ONE,
            functional_role=FunctionalRoleEnum.PROTAGONIST,
            emotional_function=EmotionalFunctionEnum.SYMPATHETIC_CHARACTER,
            backstory="A young hero destined for greatness",
            character_arc="Grows from naive to wise"
        )
        self.story.characters = [character]
        
        result = self.story.to_prompt_text_for_chapter(2)
        
        # Should contain character information
        self.assertIn("CHARACTER ARCHETYPES:", result)
        self.assertIn("Hero", result)
        self.assertIn("Chosen One", result)
    
    def test_to_prompt_text_for_chapter_empty_story(self):
        """Test chapter prompt generation with minimal story data."""
        empty_story = Story()
        result = empty_story.to_prompt_text_for_chapter(1)
        
        # Should still contain the basic structure
        self.assertIn("STORY CONFIGURATION:", result)
        # Should be a valid string
        self.assertIsInstance(result, str)


class TestGenerateChapterPrompt(unittest.TestCase):
    """Test cases for the Prompt.generate_chapter_prompt method."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.prompt_generator = Prompt()
        self.story = Story()
        self.story.story_type_name = 'The Quest'
        self.story.subtype_name = 'Spiritual Quest'
        
        # Add some chapters
        chapter1 = Chapter(1, 'Chapter 1', 'First chapter')
        chapter2 = Chapter(2, 'Chapter 2', 'Second chapter')
        self.story.add_chapter(chapter1)
        self.story.add_chapter(chapter2)
    
    @patch("prompt.Prompt._read_template_file")
    @patch("objects.story.Story.to_prompt_text_for_chapter")
    def test_generate_chapter_prompt_all_parts(self, mock_story_prompt, mock_read_file):
        """Test generating a chapter prompt with all parts present."""
        # Setup mocks
        mock_read_file.side_effect = lambda filename: {
            "chapter_pre.txt": "Chapter pre-prompt text",
            "chapter_post.txt": "Chapter post-prompt text"
        }.get(filename, "")
        
        mock_story_prompt.return_value = "Story configuration text"
        
        # Generate prompt
        result = self.prompt_generator.generate_chapter_prompt(self.story, 3)
        
        # Check that all parts are included and properly separated
        expected = "Chapter pre-prompt text\n\nStory configuration text\n\nChapter post-prompt text"
        self.assertEqual(result, expected)
        
        # Verify the correct files were read
        mock_read_file.assert_any_call("chapter_pre.txt")
        mock_read_file.assert_any_call("chapter_post.txt")
        mock_story_prompt.assert_called_once_with(3)
    
    @patch("prompt.Prompt._read_template_file")
    @patch("objects.story.Story.to_prompt_text_for_chapter")
    def test_generate_chapter_prompt_only_story_config(self, mock_story_prompt, mock_read_file):
        """Test generating a chapter prompt with only story configuration."""
        # Setup mocks - empty template files
        mock_read_file.return_value = ""
        mock_story_prompt.return_value = "Story configuration text"
        
        # Generate prompt
        result = self.prompt_generator.generate_chapter_prompt(self.story, 2)
        
        # Should only contain the story configuration
        self.assertEqual(result, "Story configuration text")
        mock_story_prompt.assert_called_once_with(2)
    
    @patch("prompt.Prompt._read_template_file")
    @patch("objects.story.Story.to_prompt_text_for_chapter")
    def test_generate_chapter_prompt_whitespace_handling(self, mock_story_prompt, mock_read_file):
        """Test that whitespace is properly handled in chapter prompt generation."""
        # Setup mocks with whitespace
        mock_read_file.side_effect = lambda filename: {
            "chapter_pre.txt": "  Chapter pre-prompt text  \n\n",
            "chapter_post.txt": "\n  Chapter post-prompt text  "
        }.get(filename, "")
        
        mock_story_prompt.return_value = "  Story configuration text  \n"
        
        # Generate prompt
        result = self.prompt_generator.generate_chapter_prompt(self.story, 2)
        
        # Should strip whitespace but maintain content
        expected = "Chapter pre-prompt text\n\nStory configuration text\n\nChapter post-prompt text"
        self.assertEqual(result, expected)
    
    @patch("prompt.Prompt._read_template_file")
    @patch("objects.story.Story.to_prompt_text_for_chapter")
    def test_generate_chapter_prompt_different_chapter_numbers(self, mock_story_prompt, mock_read_file):
        """Test generating chapter prompts for different chapter numbers."""
        mock_read_file.return_value = "Template text"
        mock_story_prompt.return_value = "Story config"
        
        # Test different chapter numbers
        for n in [1, 2, 5, 10]:
            result = self.prompt_generator.generate_chapter_prompt(self.story, n)
            self.assertIsInstance(result, str)
            # Verify the correct chapter number was passed to the story method
            mock_story_prompt.assert_called_with(n)
    
    def test_generate_chapter_prompt_integration(self):
        """Test chapter prompt generation with actual template files."""
        # This test uses the actual files in the prompts directory
        result = self.prompt_generator.generate_chapter_prompt(self.story, 2)
        
        # Result should be a string
        self.assertIsInstance(result, str)
        # Should contain some content (even if template files are empty)
        # Since we have actual story data, it should generate something
        self.assertGreater(len(result), 0)
    
    @patch("prompt.Prompt._read_template_file")
    @patch("objects.story.Story.to_prompt_text_for_chapter")
    def test_generate_chapter_prompt_all_empty(self, mock_story_prompt, mock_read_file):
        """Test generating a chapter prompt when all parts are empty."""
        # Setup mocks - all empty
        mock_read_file.return_value = ""
        mock_story_prompt.return_value = ""
        
        # Generate prompt
        result = self.prompt_generator.generate_chapter_prompt(self.story, 1)
        
        # Should return empty string
        self.assertEqual(result, "")
        mock_story_prompt.assert_called_once_with(1)


class TestChapterPromptFunctionality(unittest.TestCase):
    """Integration tests for the complete chapter prompt functionality."""
    
    def test_chapter_prompt_excludes_required_fields(self):
        """Test that the chapter prompt excludes the required fields."""
        # Create a comprehensive story
        story = Story()
        story.story_type_name = 'The Quest'
        story.subtype_name = 'Spiritual Quest'
        story.protagonist_archetype = ArchetypeEnum.CHOSEN_ONE
        story.secondary_archetypes = [ArchetypeEnum.WISE_MENTOR]
        story.selected_plot_line = PlotLine("Test Plot", "Test description")
        
        prompt_gen = Prompt()
        result = prompt_gen.generate_chapter_prompt(story, 1)
        
        # Should not contain the excluded fields
        self.assertNotIn("Protagonist Archetype:", result)
        self.assertNotIn("Secondary Character Archetypes:", result)
        self.assertNotIn("SELECTED PLOT LINE:", result)
    
    def test_chapter_prompt_includes_previous_chapters_only(self):
        """Test that chapter prompt includes only previous chapters."""
        story = Story()
        story.story_type_name = 'The Quest'
        
        # Add chapters
        for i in range(1, 6):
            chapter = Chapter(i, f'Chapter {i}', f'Description for chapter {i}')
            story.add_chapter(chapter)
        
        prompt_gen = Prompt()
        
        # Test for chapter 3 - should include chapters 1 and 2 only
        result = prompt_gen.generate_chapter_prompt(story, 3)
        
        self.assertIn("Chapter 1:", result)
        self.assertIn("Chapter 2:", result)
        self.assertNotIn("Chapter 3:", result)
        self.assertNotIn("Chapter 4:", result)
        self.assertNotIn("Chapter 5:", result)
    
    def test_chapter_prompt_for_first_chapter(self):
        """Test that chapter prompt for first chapter includes no previous chapters."""
        story = Story()
        story.story_type_name = 'The Quest'
        
        # Add chapters
        chapter1 = Chapter(1, 'Chapter 1', 'First chapter')
        chapter2 = Chapter(2, 'Chapter 2', 'Second chapter')
        story.add_chapter(chapter1)
        story.add_chapter(chapter2)
        
        prompt_gen = Prompt()
        result = prompt_gen.generate_chapter_prompt(story, 1)
        
        # Should not contain any chapter structure
        self.assertNotIn("CHAPTER STRUCTURE:", result)
        self.assertNotIn("Chapter 1:", result)
        self.assertNotIn("Chapter 2:", result)


if __name__ == '__main__':
    unittest.main()