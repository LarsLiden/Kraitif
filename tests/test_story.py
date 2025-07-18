#!/usr/bin/env python3
"""
Tests for Story functionality

This script provides basic validation tests for the Story implementation.
"""

import sys
import os
import tempfile
import json
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from story import Story, StoryBuilder, StoryRegistry
from story_types import StoryTypeRegistry
from genre import GenreRegistry
from archetype import ArchetypeRegistry


def test_story_class():
    """Test the Story class functionality."""
    print("Testing Story class...")
    
    # Create a story
    story = Story(
        title="Test Story",
        description="A test story for validation"
    )
    
    assert story.title == "Test Story"
    assert story.description == "A test story for validation"
    assert story.genre is None
    assert story.sub_genre is None
    assert story.story_type is None
    assert story.story_subtype is None
    assert len(story.archetypes) == 0
    assert len(story.tags) == 0
    assert story.notes == ""
    
    # Test string representation
    str_repr = str(story)
    assert "Test Story" in str_repr
    
    # Test completion status
    assert not story.is_complete
    assert story.completion_percentage < 100.0
    
    # Test tags
    story.add_tag("adventure")
    story.add_tag("fantasy")
    assert len(story.tags) == 2
    assert "adventure" in story.tags
    assert "fantasy" in story.tags
    
    # Test duplicate tag
    story.add_tag("adventure")
    assert len(story.tags) == 2  # Should not add duplicate
    
    # Test remove tag
    story.remove_tag("adventure")
    assert len(story.tags) == 1
    assert "adventure" not in story.tags
    assert "fantasy" in story.tags
    
    print("✓ Story class tests passed")


def test_story_builder():
    """Test the StoryBuilder class functionality."""
    print("Testing StoryBuilder class...")
    
    builder = StoryBuilder()
    
    # Test building a story step by step
    story = (builder
             .set_title("Epic Quest")
             .set_description("A hero's journey")
             .set_genre("Fantasy")
             .set_sub_genre("High Fantasy")
             .set_story_type("The Quest")
             .set_story_subtype("Spiritual Quest")
             .add_archetype("Chosen One")
             .add_archetype("Wise Mentor")
             .add_tag("epic")
             .set_notes("Inspired by LOTR")
             .build())
    
    assert story.title == "Epic Quest"
    assert story.description == "A hero's journey"
    assert story.genre is not None
    assert story.genre.name == "Fantasy"
    assert story.sub_genre is not None
    assert story.sub_genre.name == "High Fantasy"
    assert story.story_type is not None
    assert story.story_type.name == "The Quest"
    assert story.story_subtype is not None
    assert story.story_subtype.name == "Spiritual Quest"
    assert len(story.archetypes) == 2
    assert story.archetypes[0].name == "Chosen One"
    assert story.archetypes[1].name == "Wise Mentor"
    assert "epic" in story.tags
    assert story.notes == "Inspired by LOTR"
    
    # Test completion
    assert story.is_complete
    assert story.completion_percentage == 100.0
    
    # Test available sub-genres
    builder.reset().set_genre("Fantasy")
    sub_genres = builder.get_available_sub_genres()
    assert len(sub_genres) > 0
    assert any(sg.name == "High Fantasy" for sg in sub_genres)
    
    # Test available story subtypes
    builder.set_story_type("The Quest")
    subtypes = builder.get_available_story_subtypes()
    assert len(subtypes) > 0
    assert any(st.name == "Spiritual Quest" for st in subtypes)
    
    # Test suggested archetypes
    builder.set_sub_genre("High Fantasy")
    suggested = builder.get_suggested_archetypes()
    assert len(suggested) > 0
    assert any(a.name == "Chosen One" for a in suggested)
    
    print("✓ StoryBuilder class tests passed")


def test_story_registry():
    """Test the StoryRegistry class functionality."""
    print("Testing StoryRegistry class...")
    
    registry = StoryRegistry()
    
    # Create test stories
    builder = StoryBuilder()
    
    story1 = (builder
              .set_title("Fantasy Adventure")
              .set_genre("Fantasy")
              .set_sub_genre("High Fantasy")
              .set_story_type("The Quest")
              .add_archetype("Chosen One")
              .build())
    
    story2 = (builder.reset()
              .set_title("Sci-Fi Thriller")
              .set_genre("Science Fiction")
              .set_sub_genre("Cyberpunk")
              .set_story_type("Overcoming the Monster")
              .add_archetype("Anti-Hero")
              .build())
    
    story3 = (builder.reset()
              .set_title("Another Quest")
              .set_genre("Adventure")
              .set_sub_genre("Treasure Hunt")
              .set_story_type("The Quest")
              .add_archetype("Chosen One")
              .build())
    
    # Add stories to registry
    registry.add_story(story1)
    registry.add_story(story2)
    registry.add_story(story3)
    
    assert len(registry.stories) == 3
    
    # Test get stories by genre
    fantasy_stories = registry.get_stories_by_genre("Fantasy")
    assert len(fantasy_stories) == 1
    assert fantasy_stories[0].title == "Fantasy Adventure"
    
    # Test get stories by story type
    quest_stories = registry.get_stories_by_story_type("The Quest")
    assert len(quest_stories) == 2
    assert any(s.title == "Fantasy Adventure" for s in quest_stories)
    assert any(s.title == "Another Quest" for s in quest_stories)
    
    # Test get stories by archetype
    chosen_ones = registry.get_stories_by_archetype("Chosen One")
    assert len(chosen_ones) == 2
    assert any(s.title == "Fantasy Adventure" for s in chosen_ones)
    assert any(s.title == "Another Quest" for s in chosen_ones)
    
    # Test search stories
    search_results = registry.search_stories("adventure")
    assert len(search_results) == 1
    assert search_results[0].title == "Fantasy Adventure"
    
    search_results = registry.search_stories("quest")
    assert len(search_results) == 1
    assert search_results[0].title == "Another Quest"
    
    # Test complete/incomplete stories
    complete_stories = registry.get_complete_stories()
    assert len(complete_stories) == 3  # All stories should be complete
    
    incomplete_stories = registry.get_incomplete_stories()
    assert len(incomplete_stories) == 0  # No stories should be incomplete
    
    # Test with an incomplete story
    incomplete_story = builder.reset().set_title("Incomplete Story").build()
    registry.add_story(incomplete_story)
    
    complete_stories = registry.get_complete_stories()
    assert len(complete_stories) == 3  # Still 3 complete stories
    
    incomplete_stories = registry.get_incomplete_stories()
    assert len(incomplete_stories) == 1  # Now 1 incomplete story
    assert incomplete_stories[0].title == "Incomplete Story"
    
    # Test remove story
    registry.remove_story(story2)
    assert len(registry.stories) == 3  # Should have 3 stories left (story1, story3, incomplete_story)
    assert story2 not in registry.stories
    
    print("✓ StoryRegistry class tests passed")


def test_story_serialization():
    """Test story serialization and deserialization."""
    print("Testing Story serialization...")
    
    # Create a story
    builder = StoryBuilder()
    original_story = (builder
                     .set_title("Test Serialization")
                     .set_description("Testing save/load")
                     .set_genre("Fantasy")
                     .set_sub_genre("High Fantasy")
                     .set_story_type("The Quest")
                     .set_story_subtype("Spiritual Quest")
                     .add_archetype("Chosen One")
                     .add_archetype("Wise Mentor")
                     .add_tag("test")
                     .set_notes("Test notes")
                     .build())
    
    # Test to_dict
    story_dict = original_story.to_dict()
    assert story_dict['title'] == "Test Serialization"
    assert story_dict['genre'] == "Fantasy"
    assert story_dict['sub_genre'] == "High Fantasy"
    assert story_dict['story_type'] == "The Quest"
    assert story_dict['story_subtype'] == "Spiritual Quest"
    assert len(story_dict['archetypes']) == 2
    assert "Chosen One" in story_dict['archetypes']
    assert "Wise Mentor" in story_dict['archetypes']
    assert "test" in story_dict['tags']
    assert story_dict['notes'] == "Test notes"
    
    # Test from_dict
    genre_registry = GenreRegistry()
    story_registry = StoryTypeRegistry()
    archetype_registry = ArchetypeRegistry()
    
    restored_story = Story.from_dict(
        story_dict,
        genre_registry,
        story_registry,
        archetype_registry
    )
    
    assert restored_story.title == original_story.title
    assert restored_story.description == original_story.description
    assert restored_story.genre.name == original_story.genre.name
    assert restored_story.sub_genre.name == original_story.sub_genre.name
    assert restored_story.story_type.name == original_story.story_type.name
    assert restored_story.story_subtype.name == original_story.story_subtype.name
    assert len(restored_story.archetypes) == len(original_story.archetypes)
    assert restored_story.tags == original_story.tags
    assert restored_story.notes == original_story.notes
    
    print("✓ Story serialization tests passed")


def test_story_registry_file_operations():
    """Test StoryRegistry file save/load operations."""
    print("Testing StoryRegistry file operations...")
    
    # Create a registry with test stories
    registry = StoryRegistry()
    builder = StoryBuilder()
    
    story1 = (builder
              .set_title("File Test Story 1")
              .set_genre("Fantasy")
              .set_sub_genre("High Fantasy")
              .add_archetype("Chosen One")
              .build())
    
    story2 = (builder.reset()
              .set_title("File Test Story 2")
              .set_genre("Science Fiction")
              .set_sub_genre("Cyberpunk")
              .add_archetype("Anti-Hero")
              .build())
    
    registry.add_story(story1)
    registry.add_story(story2)
    
    # Test save to file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_filename = f.name
    
    try:
        registry.save_to_file(temp_filename)
        
        # Verify file was created and contains expected data
        with open(temp_filename, 'r') as f:
            data = json.load(f)
        
        assert 'stories' in data
        assert 'saved_at' in data
        assert len(data['stories']) == 2
        assert any(s['title'] == 'File Test Story 1' for s in data['stories'])
        assert any(s['title'] == 'File Test Story 2' for s in data['stories'])
        
        # Test load from file
        new_registry = StoryRegistry()
        new_registry.load_from_file(temp_filename)
        
        assert len(new_registry.stories) == 2
        assert any(s.title == 'File Test Story 1' for s in new_registry.stories)
        assert any(s.title == 'File Test Story 2' for s in new_registry.stories)
        
        # Verify story details are preserved
        loaded_story1 = next(s for s in new_registry.stories if s.title == 'File Test Story 1')
        assert loaded_story1.genre.name == 'Fantasy'
        assert loaded_story1.sub_genre.name == 'High Fantasy'
        assert len(loaded_story1.archetypes) == 1
        assert loaded_story1.archetypes[0].name == 'Chosen One'
        
    finally:
        # Clean up temp file
        if os.path.exists(temp_filename):
            os.unlink(temp_filename)
    
    print("✓ StoryRegistry file operations tests passed")


def test_story_builder_edge_cases():
    """Test StoryBuilder edge cases."""
    print("Testing StoryBuilder edge cases...")
    
    builder = StoryBuilder()
    
    # Test setting invalid genre
    story = builder.set_genre("NonExistentGenre").build()
    assert story.genre is None
    
    # Test setting sub-genre without genre
    builder.reset()
    story = builder.set_sub_genre("High Fantasy").build()
    assert story.sub_genre is None
    
    # Test setting invalid sub-genre
    builder.reset()
    story = builder.set_genre("Fantasy").set_sub_genre("Invalid SubGenre").build()
    assert story.genre is not None
    assert story.sub_genre is None
    
    # Test setting story subtype without story type
    builder.reset()
    story = builder.set_story_subtype("Spiritual Quest").build()
    assert story.story_subtype is None
    
    # Test setting invalid archetype
    builder.reset()
    story = builder.add_archetype("Invalid Archetype").build()
    assert len(story.archetypes) == 0
    
    # Test genre change clears incompatible sub-genre
    builder.reset()
    story = (builder
             .set_genre("Fantasy")
             .set_sub_genre("High Fantasy")
             .set_genre("Science Fiction")  # Change genre
             .build())
    
    assert story.genre.name == "Science Fiction"
    assert story.sub_genre is None  # Should be cleared
    
    print("✓ StoryBuilder edge cases tests passed")


def run_all_tests():
    """Run all tests."""
    print("=== Running Story Tests ===\n")
    
    try:
        test_story_class()
        test_story_builder()
        test_story_registry()
        test_story_serialization()
        test_story_registry_file_operations()
        test_story_builder_edge_cases()
        
        print("\n✅ All Story tests passed!")
        return True
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return False
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)