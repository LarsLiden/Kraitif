"""
Test suite for chapter continuity prompt generation functionality.

This module tests the new continuity functionality in chapter prompt generation,
specifically testing that continuity information from the previous chapter is
included in chapter prompts (except for the first chapter).
"""

import unittest
from unittest.mock import patch
from prompt import Prompt
from objects.story import Story
from objects.chapter import Chapter
from objects.continuity_state import ContinuityState
from objects.continuity_character import ContinuityCharacter
from objects.continuity_object import ContinuityObject
from objects.plot_thread import PlotThread


class TestChapterContinuityPrompt(unittest.TestCase):
    """Test cases for chapter continuity prompt generation."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.prompt_generator = Prompt()
        self.story = Story()
        self.story.story_type_name = 'The Quest'
        self.story.subtype_name = 'Spiritual Quest'
    
    def test_chapter_1_no_continuity_section(self):
        """Test that chapter 1 does not include a continuity section."""
        # Create chapter 1
        chapter1 = Chapter(1, 'The Beginning', 'Hero starts the journey')
        self.story.add_chapter(chapter1)
        
        # Generate prompt for chapter 1
        result = self.prompt_generator.generate_chapter_prompt(self.story, 1)
        
        # Should not contain continuity section
        self.assertNotIn("CONTINUITY:", result)
        self.assertNotIn("To maintain continuity", result)
    
    def test_chapter_2_has_continuity_section(self):
        """Test that chapter 2 includes a continuity section from chapter 1."""
        # Create chapter 1 with continuity state
        chapter1 = Chapter(1, 'The Beginning', 'Hero starts the journey')
        char1 = ContinuityCharacter('Hero', 'Village Square', 'Determined', ['Magic Sword'])
        obj1 = ContinuityObject('Ancient Map', 'Hero', 'In Hero backpack')
        thread1 = PlotThread('find_artifact', 'Hero must find the ancient artifact', 'in progress')
        chapter1.continuity_state = ContinuityState([char1], [obj1], ['Village Square'], [thread1])
        
        # Create chapter 2
        chapter2 = Chapter(2, 'First Challenge', 'Hero faces obstacles')
        
        # Add chapters to story
        self.story.add_chapter(chapter1)
        self.story.add_chapter(chapter2)
        
        # Generate prompt for chapter 2
        result = self.prompt_generator.generate_chapter_prompt(self.story, 2)
        
        # Should contain continuity section
        self.assertIn("CONTINUITY:", result)
        self.assertIn("To maintain continuity", result)
        self.assertIn("Hero: Currently at Village Square", result)
        self.assertIn("Ancient Map: Held by Hero", result)
        self.assertIn("find the ancient artifact", result)
    
    def test_chapter_continuity_section_position(self):
        """Test that continuity section appears in the correct position."""
        # Create chapters with continuity
        chapter1 = Chapter(1, 'The Beginning', 'Hero starts the journey')
        char1 = ContinuityCharacter('Hero', 'Village', 'Ready', [])
        chapter1.continuity_state = ContinuityState([char1], [], ['Village'], [])
        
        chapter2 = Chapter(2, 'Next Step', 'Hero continues')
        
        self.story.add_chapter(chapter1)
        self.story.add_chapter(chapter2)
        
        # Generate prompt for chapter 2
        result = self.prompt_generator.generate_chapter_prompt(self.story, 2)
        
        # Find the positions of different sections
        story_config_pos = result.find("STORY CONFIGURATION:")
        continuity_pos = result.find("CONTINUITY:")
        target_chapter_pos = result.find("TARGET CHAPTER TO GENERATE:")
        
        # Verify section order: story config, then continuity, then target chapter
        self.assertTrue(story_config_pos < continuity_pos, 
                       "Continuity section should come after story configuration")
        self.assertTrue(continuity_pos < target_chapter_pos, 
                       "Continuity section should come before target chapter")
    
    def test_empty_continuity_state(self):
        """Test handling of empty continuity state."""
        # Create chapter 1 with empty continuity state
        chapter1 = Chapter(1, 'The Beginning', 'Hero starts the journey')
        chapter1.continuity_state = ContinuityState()  # Empty state
        
        # Create chapter 2
        chapter2 = Chapter(2, 'Next Step', 'Hero continues')
        
        self.story.add_chapter(chapter1)
        self.story.add_chapter(chapter2)
        
        # Generate prompt for chapter 2
        result = self.prompt_generator.generate_chapter_prompt(self.story, 2)
        
        # Should still have continuity section but with "No specific continuity state"
        self.assertIn("CONTINUITY:", result)
        self.assertIn("No specific continuity state to maintain", result)
    
    def test_missing_previous_chapter(self):
        """Test handling when previous chapter doesn't exist."""
        # Create only chapter 2 (no chapter 1)
        chapter2 = Chapter(2, 'Second Chapter', 'Direct to chapter 2')
        self.story.add_chapter(chapter2)
        
        # Generate prompt for chapter 2
        result = self.prompt_generator.generate_chapter_prompt(self.story, 2)
        
        # Should not have continuity section since previous chapter doesn't exist
        self.assertNotIn("CONTINUITY:", result)
    
    def test_previous_chapter_no_continuity_state(self):
        """Test handling when previous chapter has no continuity_state attribute."""
        # Create chapter 1 without setting continuity_state
        chapter1 = Chapter(1, 'The Beginning', 'Hero starts the journey')
        # Don't set continuity_state, it will be default empty ContinuityState
        
        # Create chapter 2
        chapter2 = Chapter(2, 'Next Step', 'Hero continues')
        
        self.story.add_chapter(chapter1)
        self.story.add_chapter(chapter2)
        
        # Generate prompt for chapter 2
        result = self.prompt_generator.generate_chapter_prompt(self.story, 2)
        
        # Should have continuity section with default empty state message
        self.assertIn("CONTINUITY:", result)
        self.assertIn("No specific continuity state to maintain", result)
    
    def test_multiple_chapters_continuity_chain(self):
        """Test continuity across multiple chapters."""
        # Create chapter 1 with continuity
        chapter1 = Chapter(1, 'Beginning', 'Start')
        char1 = ContinuityCharacter('Hero', 'Home', 'Eager', ['Backpack'])
        chapter1.continuity_state = ContinuityState([char1], [], ['Home'], [])
        
        # Create chapter 2 with updated continuity
        chapter2 = Chapter(2, 'Journey Starts', 'Leave home')
        char2 = ContinuityCharacter('Hero', 'Forest', 'Nervous', ['Backpack', 'Map'])
        chapter2.continuity_state = ContinuityState([char2], [], ['Home', 'Forest'], [])
        
        # Create chapter 3
        chapter3 = Chapter(3, 'First Encounter', 'Meet someone')
        
        self.story.add_chapter(chapter1)
        self.story.add_chapter(chapter2)
        self.story.add_chapter(chapter3)
        
        # Generate prompt for chapter 3 (should use chapter 2's continuity)
        result = self.prompt_generator.generate_chapter_prompt(self.story, 3)
        
        # Should contain chapter 2's continuity (not chapter 1's)
        self.assertIn("CONTINUITY:", result)
        self.assertIn("Hero: Currently at Forest", result)  # From chapter 2
        self.assertIn("Nervous", result)  # From chapter 2
        # Verify it's using chapter 2's continuity by checking for Forest location and Map item
        self.assertIn("carrying: Backpack, Map", result)  # From chapter 2
        self.assertNotIn("Eager", result)  # Should not include chapter 1's status
    
    def test_continuity_formatting(self):
        """Test that continuity information is properly formatted."""
        # Create chapter 1 with comprehensive continuity
        chapter1 = Chapter(1, 'Beginning', 'Start')
        char1 = ContinuityCharacter('Hero', 'Village Square', 'Determined', ['Magic Sword', 'Health Potion'])
        char2 = ContinuityCharacter('Mentor', 'Tower', 'Wise', ['Ancient Book'])
        obj1 = ContinuityObject('Mystic Crystal', 'Hero', 'In Hero possession')
        obj2 = ContinuityObject('Hidden Key', None, 'Under the old oak tree')
        thread1 = PlotThread('save_kingdom', 'Hero must save the kingdom', 'in progress')
        thread2 = PlotThread('find_mentor', 'Locate the wise mentor', 'resolved')
        
        chapter1.continuity_state = ContinuityState(
            [char1, char2],
            [obj1, obj2],
            ['Village Square', 'Forest Path', 'Tower'],
            [thread1, thread2]
        )
        
        # Create chapter 2
        chapter2 = Chapter(2, 'Next Step', 'Continue quest')
        self.story.add_chapter(chapter1)
        self.story.add_chapter(chapter2)
        
        # Generate prompt for chapter 2
        result = self.prompt_generator.generate_chapter_prompt(self.story, 2)
        
        # Check that all continuity elements are present and properly formatted
        self.assertIn("Characters:", result)
        self.assertIn("Hero: Currently at Village Square, Determined, carrying: Magic Sword, Health Potion", result)
        self.assertIn("Mentor: Currently at Tower, Wise, carrying: Ancient Book", result)
        
        self.assertIn("Objects:", result)
        self.assertIn("Mystic Crystal: Held by Hero", result)
        self.assertIn("Hidden Key: Located at Under the old oak tree", result)
        
        self.assertIn("Locations Visited: Village Square, Forest Path, Tower", result)
        
        self.assertIn("Open Plot Threads:", result)
        self.assertIn("Hero must save the kingdom (Status: in progress)", result)
        self.assertIn("Locate the wise mentor (Status: resolved)", result)


class TestContinuityStatePromptText(unittest.TestCase):
    """Test cases for the ContinuityState.to_prompt_text method."""
    
    def test_empty_continuity_state(self):
        """Test formatting of empty continuity state."""
        continuity = ContinuityState()
        result = continuity.to_prompt_text()
        self.assertEqual(result, "No specific continuity state to maintain.")
    
    def test_characters_only(self):
        """Test formatting with only characters."""
        char = ContinuityCharacter('Hero', 'Village', 'Brave', ['Sword'])
        continuity = ContinuityState([char], [], [], [])
        result = continuity.to_prompt_text()
        
        self.assertIn("Characters:", result)
        self.assertIn("Hero: Currently at Village, Brave, carrying: Sword", result)
        self.assertNotIn("Objects:", result)
        self.assertNotIn("Locations Visited:", result)
        self.assertNotIn("Open Plot Threads:", result)
    
    def test_objects_only(self):
        """Test formatting with only objects."""
        obj = ContinuityObject('Magic Ring', 'Hero', 'Worn on finger')
        continuity = ContinuityState([], [obj], [], [])
        result = continuity.to_prompt_text()
        
        self.assertIn("Objects:", result)
        self.assertIn("Magic Ring: Held by Hero", result)
        self.assertNotIn("Characters:", result)
    
    def test_locations_only(self):
        """Test formatting with only locations."""
        continuity = ContinuityState([], [], ['Forest', 'Cave'], [])
        result = continuity.to_prompt_text()
        
        self.assertIn("Locations Visited: Forest, Cave", result)
        self.assertNotIn("Characters:", result)
        self.assertNotIn("Objects:", result)
    
    def test_plot_threads_only(self):
        """Test formatting with only plot threads."""
        thread = PlotThread('rescue_princess', 'Hero must rescue the princess', 'urgent')
        continuity = ContinuityState([], [], [], [thread])
        result = continuity.to_prompt_text()
        
        self.assertIn("Open Plot Threads:", result)
        self.assertIn("Hero must rescue the princess (Status: urgent)", result)
        self.assertNotIn("Characters:", result)
    
    def test_character_without_inventory(self):
        """Test formatting character without inventory."""
        char = ContinuityCharacter('Wizard', 'Tower', 'Mysterious', [])
        continuity = ContinuityState([char], [], [], [])
        result = continuity.to_prompt_text()
        
        self.assertIn("Wizard: Currently at Tower, Mysterious", result)
        self.assertNotIn("carrying:", result)
    
    def test_object_without_holder(self):
        """Test formatting object without holder."""
        obj = ContinuityObject('Treasure Chest', None, 'Hidden in cave')
        continuity = ContinuityState([], [obj], [], [])
        result = continuity.to_prompt_text()
        
        self.assertIn("Treasure Chest: Located at Hidden in cave", result)
        self.assertNotIn("Held by", result)
    
    def test_comprehensive_continuity_formatting(self):
        """Test formatting with all types of continuity information."""
        char = ContinuityCharacter('Knight', 'Castle', 'Noble', ['Shield', 'Lance'])
        obj = ContinuityObject('Crown', 'King', 'On throne')
        thread = PlotThread('defend_realm', 'Protect the kingdom', 'active')
        
        continuity = ContinuityState([char], [obj], ['Castle', 'Battlefield'], [thread])
        result = continuity.to_prompt_text()
        
        # Check overall structure
        lines = result.split('\n')
        self.assertTrue(any(line.strip() == "Characters:" for line in lines))
        self.assertTrue(any(line.strip() == "Objects:" for line in lines))
        self.assertTrue(any("Locations Visited:" in line for line in lines))
        self.assertTrue(any(line.strip() == "Open Plot Threads:" for line in lines))
        
        # Check content
        self.assertIn("Knight: Currently at Castle, Noble, carrying: Shield, Lance", result)
        self.assertIn("Crown: Held by King", result)
        self.assertIn("Locations Visited: Castle, Battlefield", result)
        self.assertIn("Protect the kingdom (Status: active)", result)


if __name__ == '__main__':
    unittest.main()