"""
Tests for Chapter functionality
"""

import pytest
import json
from objects.chapter import Chapter
from objects.narrative_function import NarrativeFunctionEnum
from objects.story import Story


class TestChapter:
    """Test cases for Chapter class."""
    
    def test_chapter_creation(self):
        """Test basic chapter creation."""
        chapter = Chapter(
            chapter_number=1,
            title="The Beginning",
            overview="The story starts here."
        )
        
        assert chapter.chapter_number == 1
        assert chapter.title == "The Beginning"
        assert chapter.overview == "The story starts here."
        assert chapter.character_impact == []
        assert chapter.point_of_view is None
        assert chapter.narrative_function is None
        assert chapter.foreshadow_or_echo is None
        assert chapter.scene_highlights is None
    
    def test_chapter_validation(self):
        """Test chapter validation."""
        # Test invalid chapter number
        with pytest.raises(ValueError, match="Chapter number must be >= 1"):
            Chapter(chapter_number=0, title="Test", overview="Test")
        
        # Test empty title
        with pytest.raises(ValueError, match="Chapter title cannot be empty"):
            Chapter(chapter_number=1, title="", overview="Test")
        
        # Test empty overview
        with pytest.raises(ValueError, match="Chapter overview cannot be empty"):
            Chapter(chapter_number=1, title="Test", overview="")
    
    def test_chapter_character_impact(self):
        """Test character impact management."""
        chapter = Chapter(
            chapter_number=1,
            title="Test Chapter",
            overview="Test overview"
        )
        
        # Add character impact
        success = chapter.add_character_impact("Alice", "Discovers her destiny")
        assert success
        assert len(chapter.character_impact) == 1
        assert chapter.character_impact[0]["character"] == "Alice"
        assert chapter.character_impact[0]["effect"] == "Discovers her destiny"
        
        # Add another character impact
        success = chapter.add_character_impact("Bob", "Learns about magic")
        assert success
        assert len(chapter.character_impact) == 2
        
        # Update existing character impact
        success = chapter.add_character_impact("Alice", "Embraces her destiny")
        assert success
        assert len(chapter.character_impact) == 2  # Should not add duplicate
        assert chapter.get_character_impact("Alice") == "Embraces her destiny"
        
        # Test invalid inputs
        assert not chapter.add_character_impact("", "Effect")
        assert not chapter.add_character_impact("Character", "")
        assert not chapter.add_character_impact(None, "Effect")
    
    def test_chapter_get_character_impact(self):
        """Test getting character impact."""
        chapter = Chapter(
            chapter_number=1,
            title="Test Chapter",
            overview="Test overview"
        )
        
        chapter.add_character_impact("Alice", "Major revelation")
        
        # Test getting existing impact
        impact = chapter.get_character_impact("Alice")
        assert impact == "Major revelation"
        
        # Test case insensitive
        impact = chapter.get_character_impact("alice")
        assert impact == "Major revelation"
        
        # Test non-existent character
        impact = chapter.get_character_impact("Bob")
        assert impact is None
        
        # Test invalid input
        impact = chapter.get_character_impact("")
        assert impact is None
    
    def test_chapter_remove_character_impact(self):
        """Test removing character impact."""
        chapter = Chapter(
            chapter_number=1,
            title="Test Chapter",
            overview="Test overview"
        )
        
        chapter.add_character_impact("Alice", "Effect 1")
        chapter.add_character_impact("Bob", "Effect 2")
        
        # Remove existing character
        success = chapter.remove_character_impact("Alice")
        assert success
        assert len(chapter.character_impact) == 1
        assert chapter.get_character_impact("Alice") is None
        assert chapter.get_character_impact("Bob") == "Effect 2"
        
        # Try to remove non-existent character
        success = chapter.remove_character_impact("Charlie")
        assert not success
        
        # Test case insensitive removal
        success = chapter.remove_character_impact("bob")
        assert success
        assert len(chapter.character_impact) == 0
    
    def test_chapter_narrative_function(self):
        """Test narrative function setting."""
        chapter = Chapter(
            chapter_number=1,
            title="Test Chapter",
            overview="Test overview"
        )
        
        # Set valid narrative function
        success = chapter.set_narrative_function("Setting Introduction")
        assert success
        assert chapter.narrative_function == NarrativeFunctionEnum.SETTING_INTRODUCTION
        
        # Set invalid narrative function
        success = chapter.set_narrative_function("Invalid Function")
        assert not success
        
        # Clear narrative function
        success = chapter.set_narrative_function("")
        assert success
        assert chapter.narrative_function is None
        
        success = chapter.set_narrative_function(None)
        assert success
        assert chapter.narrative_function is None
    
    def test_chapter_to_dict(self):
        """Test chapter serialization to dictionary."""
        chapter = Chapter(
            chapter_number=1,
            title="Test Chapter",
            overview="Test overview",
            point_of_view="Alice",
            foreshadow_or_echo="Hints at future conflict",
            scene_highlights="Dramatic revelation"
        )
        chapter.add_character_impact("Alice", "Discovers truth")
        chapter.set_narrative_function("Character Introduction")
        
        data = chapter.to_dict()
        
        assert data["chapter_number"] == 1
        assert data["title"] == "Test Chapter"
        assert data["overview"] == "Test overview"
        assert data["point_of_view"] == "Alice"
        assert data["narrative_function"] == "Character Introduction"
        assert data["foreshadow_or_echo"] == "Hints at future conflict"
        assert data["scene_highlights"] == "Dramatic revelation"
        assert len(data["character_impact"]) == 1
        assert data["character_impact"][0]["character"] == "Alice"
        assert data["character_impact"][0]["effect"] == "Discovers truth"
    
    def test_chapter_from_dict(self):
        """Test chapter deserialization from dictionary."""
        data = {
            "chapter_number": 2,
            "title": "The Journey Begins",
            "overview": "Characters set out on their quest",
            "character_impact": [
                {"character": "Hero", "effect": "Accepts the call"},
                {"character": "Mentor", "effect": "Provides guidance"}
            ],
            "point_of_view": "Hero",
            "narrative_function": "Inciting Incident",
            "foreshadow_or_echo": "Mentions ancient prophecy",
            "scene_highlights": "Emotional farewell scene"
        }
        
        chapter = Chapter.from_dict(data)
        
        assert chapter is not None
        assert chapter.chapter_number == 2
        assert chapter.title == "The Journey Begins"
        assert chapter.overview == "Characters set out on their quest"
        assert chapter.point_of_view == "Hero"
        assert chapter.narrative_function == NarrativeFunctionEnum.INCITING_INCIDENT
        assert chapter.foreshadow_or_echo == "Mentions ancient prophecy"
        assert chapter.scene_highlights == "Emotional farewell scene"
        assert len(chapter.character_impact) == 2
        assert chapter.get_character_impact("Hero") == "Accepts the call"
        assert chapter.get_character_impact("Mentor") == "Provides guidance"
    
    def test_chapter_from_dict_minimal(self):
        """Test chapter creation from minimal dictionary data."""
        data = {
            "chapter_number": 1,
            "title": "Minimal Chapter",
            "overview": "Basic overview"
        }
        
        chapter = Chapter.from_dict(data)
        
        assert chapter is not None
        assert chapter.chapter_number == 1
        assert chapter.title == "Minimal Chapter"
        assert chapter.overview == "Basic overview"
        assert chapter.character_impact == []
        assert chapter.point_of_view is None
        assert chapter.narrative_function is None
    
    def test_chapter_from_dict_invalid(self):
        """Test chapter creation from invalid dictionary data."""
        # Missing required fields
        invalid_data = [
            {},
            {"chapter_number": 1},
            {"title": "Test"},
            {"overview": "Test"},
            {"chapter_number": 1, "title": "Test"},  # Missing overview
            {"chapter_number": "invalid", "title": "Test", "overview": "Test"},  # Invalid type
            None,
            "not a dict"
        ]
        
        for data in invalid_data:
            chapter = Chapter.from_dict(data)
            assert chapter is None
    
    def test_chapter_string_representation(self):
        """Test chapter string representation."""
        chapter = Chapter(
            chapter_number=1,
            title="Test Chapter",
            overview="Test overview",
            point_of_view="Alice"
        )
        chapter.set_narrative_function("Setting Introduction")
        chapter.add_character_impact("Alice", "Effect 1")
        chapter.add_character_impact("Bob", "Effect 2")
        
        string_repr = str(chapter)
        
        assert "Chapter 1: Test Chapter" in string_repr
        assert "Function: Setting Introduction" in string_repr
        assert "POV: Alice" in string_repr
        assert "Characters affected: 2" in string_repr


class TestStoryChapters:
    """Test cases for Story class chapter functionality."""
    
    def test_story_add_chapter(self):
        """Test adding chapters to story."""
        story = Story()
        
        chapter1 = Chapter(1, "First Chapter", "The beginning")
        chapter2 = Chapter(2, "Second Chapter", "The middle")
        
        # Add chapters
        success = story.add_chapter(chapter1)
        assert success
        assert len(story.chapters) == 1
        
        success = story.add_chapter(chapter2)
        assert success
        assert len(story.chapters) == 2
        
        # Try to add duplicate chapter number
        duplicate_chapter = Chapter(1, "Duplicate", "Should not be added")
        success = story.add_chapter(duplicate_chapter)
        assert not success
        assert len(story.chapters) == 2
        
        # Test invalid input
        success = story.add_chapter(None)
        assert not success
        success = story.add_chapter("not a chapter")
        assert not success
    
    def test_story_chapter_ordering(self):
        """Test that chapters are ordered correctly."""
        story = Story()
        
        # Add chapters out of order
        chapter3 = Chapter(3, "Third", "Third chapter")
        chapter1 = Chapter(1, "First", "First chapter")
        chapter2 = Chapter(2, "Second", "Second chapter")
        
        story.add_chapter(chapter3)
        story.add_chapter(chapter1)
        story.add_chapter(chapter2)
        
        ordered_chapters = story.get_chapters_ordered()
        assert len(ordered_chapters) == 3
        assert ordered_chapters[0].chapter_number == 1
        assert ordered_chapters[1].chapter_number == 2
        assert ordered_chapters[2].chapter_number == 3
    
    def test_story_get_chapter(self):
        """Test getting specific chapter from story."""
        story = Story()
        
        chapter1 = Chapter(1, "First Chapter", "The beginning")
        chapter2 = Chapter(2, "Second Chapter", "The middle")
        
        story.add_chapter(chapter1)
        story.add_chapter(chapter2)
        
        # Get existing chapter
        found_chapter = story.get_chapter(1)
        assert found_chapter is not None
        assert found_chapter.title == "First Chapter"
        
        # Get non-existent chapter
        found_chapter = story.get_chapter(99)
        assert found_chapter is None
    
    def test_story_remove_chapter(self):
        """Test removing chapter from story."""
        story = Story()
        
        chapter1 = Chapter(1, "First Chapter", "The beginning")
        chapter2 = Chapter(2, "Second Chapter", "The middle")
        
        story.add_chapter(chapter1)
        story.add_chapter(chapter2)
        
        # Remove existing chapter
        success = story.remove_chapter(1)
        assert success
        assert len(story.chapters) == 1
        assert story.get_chapter(1) is None
        assert story.get_chapter(2) is not None
        
        # Try to remove non-existent chapter
        success = story.remove_chapter(99)
        assert not success
        assert len(story.chapters) == 1
    
    def test_story_update_chapter(self):
        """Test updating chapter in story."""
        story = Story()
        
        original_chapter = Chapter(1, "Original Title", "Original overview")
        story.add_chapter(original_chapter)
        
        # Update with same chapter number
        updated_chapter = Chapter(1, "Updated Title", "Updated overview")
        success = story.update_chapter(1, updated_chapter)
        assert success
        
        found_chapter = story.get_chapter(1)
        assert found_chapter.title == "Updated Title"
        assert found_chapter.overview == "Updated overview"
        
        # Try to update with different chapter number
        wrong_number_chapter = Chapter(2, "Wrong Number", "Wrong overview")
        success = story.update_chapter(1, wrong_number_chapter)
        assert not success
        
        # Try to update non-existent chapter
        success = story.update_chapter(99, updated_chapter)
        assert not success
    
    def test_story_chapters_serialization(self):
        """Test story serialization includes chapters."""
        story = Story()
        
        chapter1 = Chapter(1, "First Chapter", "Beginning of story")
        chapter1.add_character_impact("Hero", "Introduced to world")
        chapter1.set_narrative_function("Setting Introduction")
        
        chapter2 = Chapter(2, "Second Chapter", "Plot thickens")
        chapter2.point_of_view = "Hero"
        chapter2.foreshadow_or_echo = "Hints at villain"
        
        story.add_chapter(chapter1)
        story.add_chapter(chapter2)
        
        # Test JSON serialization
        json_str = story.to_json()
        data = json.loads(json_str)
        
        assert "chapters" in data
        assert len(data["chapters"]) == 2
        assert data["chapters"][0]["chapter_number"] == 1
        assert data["chapters"][0]["title"] == "First Chapter"
        assert data["chapters"][0]["narrative_function"] == "Setting Introduction"
        
        # Test JSON deserialization
        new_story = Story()
        success = new_story.from_json(json_str)
        assert success
        assert len(new_story.chapters) == 2
        
        found_chapter = new_story.get_chapter(1)
        assert found_chapter is not None
        assert found_chapter.title == "First Chapter"
        assert found_chapter.narrative_function == NarrativeFunctionEnum.SETTING_INTRODUCTION
        assert found_chapter.get_character_impact("Hero") == "Introduced to world"
    
    def test_story_string_includes_chapters(self):
        """Test story string representation includes chapter count."""
        story = Story()
        story.set_genre("Fantasy")
        
        # Test without chapters
        story_str = str(story)
        assert "Chapters:" not in story_str
        
        # Test with chapters
        chapter1 = Chapter(1, "First", "Beginning")
        chapter2 = Chapter(2, "Second", "Middle")
        story.add_chapter(chapter1)
        story.add_chapter(chapter2)
        
        story_str = str(story)
        assert "Chapters: 2" in story_str
    
    def test_story_prompt_text_includes_chapters(self):
        """Test story prompt text includes chapter information."""
        story = Story()
        story.set_genre("Fantasy")
        
        chapter1 = Chapter(1, "The Awakening", "Hero discovers powers")
        chapter1.add_character_impact("Hero", "Gains magical abilities")
        chapter1.set_narrative_function("Character Introduction")
        chapter1.point_of_view = "Hero"
        chapter1.foreshadow_or_echo = "Mentions ancient prophecy"
        chapter1.scene_highlights = "Glowing eyes in the darkness"
        
        chapter2 = Chapter(2, "The Journey", "Quest begins")
        chapter2.add_character_impact("Hero", "Accepts responsibility")
        chapter2.add_character_impact("Mentor", "Provides guidance")
        chapter2.set_narrative_function("Inciting Incident")
        
        story.add_chapter(chapter1)
        story.add_chapter(chapter2)
        
        prompt_text = story.to_prompt_text()
        
        assert "CHAPTER STRUCTURE:" in prompt_text
        assert "Chapter 1: The Awakening" in prompt_text
        assert "Chapter 2: The Journey" in prompt_text
        assert "Hero discovers powers" in prompt_text
        assert "Quest begins" in prompt_text
        assert "Character Introduction" in prompt_text
        assert "Inciting Incident" in prompt_text
        assert "Point of View: Hero" in prompt_text
        assert "Foreshadow/Echo: Mentions ancient prophecy" in prompt_text
        assert "Scene Highlights: Glowing eyes in the darkness" in prompt_text
        assert "• Hero: Gains magical abilities" in prompt_text
        assert "• Mentor: Provides guidance" in prompt_text