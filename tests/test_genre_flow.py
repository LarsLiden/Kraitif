#!/usr/bin/env python3
"""
Test for Genre and Sub-Genre Selection Flow

This test validates that the new genre and sub-genre selection flow works correctly.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from story import Story


def test_genre_subgenre_flow():
    """Test the complete genre and sub-genre selection flow."""
    print("Testing Genre and Sub-Genre Selection Flow...")
    
    # Create a new story
    story = Story()
    
    # Step 1: Set story type selections
    story.set_story_type_selection("The Quest", "Object Quest", 
                                  "Growth occurs through shared adventure and sacrifice.",
                                  "Trust forged under pressure.")
    
    assert story.story_type_name == "The Quest"
    assert story.subtype_name == "Object Quest"
    assert story.key_theme == "Growth occurs through shared adventure and sacrifice."
    assert story.core_arc == "Trust forged under pressure."
    
    # Step 2: Set genre
    success = story.set_genre("Science Fiction")
    assert success, "Should be able to set Science Fiction genre"
    assert story.genre is not None, "Genre should be set"
    assert story.genre.name == "Science Fiction", f"Expected Science Fiction, got {story.genre.name}"
    
    # Step 3: Get available sub-genres
    sub_genres = story.get_available_sub_genres()
    assert len(sub_genres) == 6, f"Expected 6 Science Fiction sub-genres, got {len(sub_genres)}"
    
    # Verify some expected sub-genres are available
    sub_genre_names = [sg.name for sg in sub_genres]
    assert "Space Opera" in sub_genre_names, "Space Opera should be available"
    assert "Cyberpunk" in sub_genre_names, "Cyberpunk should be available"
    assert "Hard Sci-Fi" in sub_genre_names, "Hard Sci-Fi should be available"
    
    # Step 4: Set sub-genre
    success = story.set_sub_genre("Space Opera")
    assert success, "Should be able to set Space Opera sub-genre"
    assert story.sub_genre is not None, "Sub-genre should be set"
    assert story.sub_genre.name == "Space Opera", f"Expected Space Opera, got {story.sub_genre.name}"
    
    # Verify complete story
    story_str = str(story)
    assert "Genre: Science Fiction" in story_str, "Story string should include genre"
    assert "Sub-genre: Space Opera" in story_str, "Story string should include sub-genre"
    assert "Story Type: The Quest - Object Quest" in story_str, "Story string should include story type"
    
    print("✓ Genre and Sub-Genre Selection Flow tests passed")


def test_genre_invalid_operations():
    """Test invalid genre operations."""
    print("Testing invalid genre operations...")
    
    story = Story()
    
    # Try to set invalid genre
    success = story.set_genre("NonExistent Genre")
    assert not success, "Should not be able to set non-existent genre"
    assert story.genre is None, "Genre should remain None"
    
    # Try to set sub-genre without setting genre first
    success = story.set_sub_genre("Space Opera")
    assert not success, "Should not be able to set sub-genre without genre"
    assert story.sub_genre is None, "Sub-genre should remain None"
    
    # Set valid genre, then try invalid sub-genre
    story.set_genre("Science Fiction")
    success = story.set_sub_genre("High Fantasy")  # This belongs to Fantasy, not Sci-Fi
    assert not success, "Should not be able to set sub-genre from different genre"
    assert story.sub_genre is None, "Sub-genre should remain None"
    
    print("✓ Invalid genre operations tests passed")


def test_story_serialization_with_genre():
    """Test that story serialization includes genre and sub-genre data."""
    print("Testing story serialization with genre data...")
    
    # Create story with all data
    story = Story()
    story.set_story_type_selection("Comedy", "Romantic Comedy", "Love conquers all", "Meet-cute to marriage")
    story.set_genre("Romance")
    story.set_sub_genre("Romantic Comedy")
    
    # Test JSON serialization
    json_data = story.to_json()
    assert '"genre_name": "Romance"' in json_data, "JSON should include genre"
    assert '"sub_genre_name": "Romantic Comedy"' in json_data, "JSON should include sub-genre"
    
    # Test JSON deserialization
    new_story = Story()
    success = new_story.from_json(json_data)
    assert success, "Should be able to load from JSON"
    assert new_story.genre.name == "Romance", "Loaded story should have correct genre"
    assert new_story.sub_genre.name == "Romantic Comedy", "Loaded story should have correct sub-genre"
    assert new_story.story_type_name == "Comedy", "Loaded story should have correct story type"
    assert new_story.key_theme == "Love conquers all", "Loaded story should have correct key theme"
    
    print("✓ Story serialization with genre data tests passed")


def run_genre_tests():
    """Run all genre-related tests."""
    print("=== Running Genre and Sub-Genre Tests ===\n")
    
    try:
        test_genre_subgenre_flow()
        test_genre_invalid_operations()
        test_story_serialization_with_genre()
        
        print("\n✅ All genre and sub-genre tests passed!")
        return True
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return False
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        return False


if __name__ == "__main__":
    success = run_genre_tests()
    sys.exit(0 if success else 1)