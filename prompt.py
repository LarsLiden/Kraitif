"""
Prompt Generation Module

This module implements a Prompt class that generates different types of LLM prompts
by combining template files with story configuration data.
"""

import os
from typing import Optional
from objects.story import Story


class Prompt:
    """Handles generation of LLM prompts by combining template files with story data."""
    
    def __init__(self, prompts_dir: str = "prompts"):
        """
        Initialize the Prompt generator.
        
        Args:
            prompts_dir: Directory containing prompt template files
        """
        self.prompts_dir = prompts_dir
    
    def _read_template_file(self, filename: str) -> str:
        """
        Read a template file from the prompts directory.
        
        Args:
            filename: Name of the template file to read
            
        Returns:
            Content of the template file, or empty string if file not found
        """
        try:
            file_path = os.path.join(self.prompts_dir, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except (FileNotFoundError, IOError):
            return ""
    
    def generate_plot_prompt(self, story: Story) -> str:
        """
        Generate a complete plot prompt by concatenating pre-text, story configuration, and post-text.
        
        Args:
            story: Story object containing the configuration to include in the prompt
            
        Returns:
            Complete prompt text ready for LLM consumption
        """
        # Read the template files
        pre_text = self._read_template_file("plot_lines_pre.txt")
        post_text = self._read_template_file("plot_lines_post.txt")
        
        # Get the story configuration
        story_config = story.to_prompt_text()
        
        # Combine all parts
        parts = []
        
        if pre_text.strip():
            parts.append(pre_text.strip())
        
        if story_config.strip():
            parts.append(story_config.strip())
        
        if post_text.strip():
            parts.append(post_text.strip())
        
        # Join with double newlines for clear separation
        return "\n\n".join(parts)
    
    def generate_character_prompt(self, story: Story) -> str:
        """
        Generate a complete character prompt by concatenating pre-text, story configuration, and post-text.
        
        Args:
            story: Story object containing the configuration to include in the prompt
            
        Returns:
            Complete prompt text ready for LLM consumption
        """
        # Read the template files
        pre_text = self._read_template_file("characters_pre.txt")
        post_text = self._read_template_file("characters_post.txt")
        
        # Get the story configuration
        story_config = story.to_prompt_text()
        
        # Combine all parts
        parts = []
        
        if pre_text.strip():
            parts.append(pre_text.strip())
        
        if story_config.strip():
            parts.append(story_config.strip())
        
        if post_text.strip():
            parts.append(post_text.strip())
        
        # Join with double newlines for clear separation
        return "\n\n".join(parts)

    def generate_chapter_outline_prompt(self, story: Story) -> str:
        """
        Generate a complete chapter outline prompt by concatenating pre-text, story configuration, and post-text.
        This uses a modified version of the story configuration that excludes protagonist_archetype, 
        secondary_archetypes, and selected_plot_line fields.
        
        Args:
            story: Story object containing the configuration to include in the prompt
            
        Returns:
            Complete prompt text ready for LLM consumption
        """
        # Read the template files
        pre_text = self._read_template_file("chapter_outline_pre.txt")
        post_text = self._read_template_file("chapter_outline_post.txt")
        
        # Get the story configuration (excluding specified fields)
        story_config = story.to_prompt_text_for_chapter_outline()
        
        # Combine all parts
        parts = []
        
        if pre_text.strip():
            parts.append(pre_text.strip())
        
        if story_config.strip():
            parts.append(story_config.strip())
        
        if post_text.strip():
            parts.append(post_text.strip())
        
        # Join with double newlines for clear separation
        return "\n\n".join(parts)
    def generate_chapter_prompt(self, story: Story, n: int) -> str:
        """
        Generate a complete chapter prompt by concatenating pre-text, story configuration, and post-text.
        This uses a modified version of the story configuration that excludes protagonist_archetype, 
        secondary_archetypes, and selected_plot_line fields. For chapters, only includes data for 
        chapters 1 to n-1.
        
        Args:
            story: Story object containing the configuration to include in the prompt
            n: The chapter number to generate. Only chapters 1 to n-1 will be included in the prompt.
            
        Returns:
            Complete prompt text ready for LLM consumption
        """
        # Read the template files
        pre_text = self._read_template_file("chapter_pre.txt")
        post_text = self._read_template_file("chapter_post.txt")
        
        # Get the story configuration (excluding specified fields and filtering chapters)
        story_config = story.to_prompt_text_for_chapter(n)
        
        # Get the specific chapter we're generating
        target_chapter = story.get_chapter(n)
        chapter_info = ""
        if target_chapter:
            chapter_info = f"""

TARGET CHAPTER TO GENERATE:
Chapter {n}: {target_chapter.title}
Overview: {target_chapter.overview}
Narrative Function: {target_chapter.narrative_function.value if target_chapter.narrative_function else 'Not specified'}
Point of View: {target_chapter.point_of_view or 'Not specified'}
"""
            if target_chapter.character_impact:
                chapter_info += "\nCharacter Impact:\n"
                for impact in target_chapter.character_impact:
                    chapter_info += f"- {impact['character']}: {impact['effect']}\n"
            
            if target_chapter.foreshadow_or_echo:
                chapter_info += f"\nForeshadow/Echo: {target_chapter.foreshadow_or_echo}\n"
                
            if target_chapter.scene_highlights:
                chapter_info += f"\nScene Highlights: {target_chapter.scene_highlights}\n"
        
        # Combine all parts
        parts = []
        
        if pre_text.strip():
            parts.append(pre_text.strip())
        
        if story_config.strip():
            parts.append(story_config.strip())
            
        if chapter_info.strip():
            parts.append(chapter_info.strip())
        
        if post_text.strip():
            parts.append(post_text.strip())
        
        # Join with double newlines for clear separation
        return "\n\n".join(parts)