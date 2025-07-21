#!/usr/bin/env python3
"""
Test for Writing Style Selection Flow

This test validates that the new writing style selection flow works correctly.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from story import Story


def test_writing_style_flow():
    """Test the complete writing style selection flow."""
    print("Testing Writing Style Selection Flow...")
    
    # Create a new story
    story = Story()
    
    # Step 1: Set story type selections
    story.set_story_type_selection("The Quest", "Object Quest", 
                                  "Growth occurs through shared adventure and sacrifice.",
                                  "Trust forged under pressure.")
    
    # Step 2: Set genre and sub-genre
    story.set_genre("Science Fiction")
    story.set_sub_genre("Space Opera")
    
    # Step 3: Test writing style functionality
    # Get available writing styles
    available_styles = story.get_available_writing_styles()
    assert len(available_styles) >= 15, f"Expected at least 15 writing styles, got {len(available_styles)}"
    
    # Verify some expected styles are available
    style_names = [style.name for style in available_styles]
    assert "Concise" in style_names, "Concise should be available"
    assert "Lyrical" in style_names, "Lyrical should be available"
    assert "Analytical" in style_names, "Analytical should be available"
    assert "Descriptive" in style_names, "Descriptive should be available"
    assert "Suspenseful" in style_names, "Suspenseful should be available"
    
    # Step 4: Set writing style
    success = story.set_writing_style("Concise")
    assert success, "Should be able to set Concise writing style"
    assert story.writing_style is not None, "Writing style should be set"
    assert story.writing_style.name == "Concise", f"Expected Concise, got {story.writing_style.name}"
    assert story.writing_style.description == "Minimalist, efficient, no wasted words", "Description should match"
    
    # Verify complete story
    story_str = str(story)
    assert "Genre: Science Fiction" in story_str, "Story string should include genre"
    assert "Sub-genre: Space Opera" in story_str, "Story string should include sub-genre"
    assert "Writing Style: Concise" in story_str, "Story string should include writing style"
    assert "Story Type: The Quest - Object Quest" in story_str, "Story string should include story type"
    
    print("✓ Writing Style Selection Flow tests passed")


def test_writing_style_invalid_operations():
    """Test invalid writing style operations."""
    print("Testing invalid writing style operations...")
    
    story = Story()
    
    # Try to set invalid writing style
    success = story.set_writing_style("NonExistent Style")
    assert not success, "Should not be able to set non-existent writing style"
    assert story.writing_style is None, "Writing style should remain None"
    
    # Try different valid styles
    success = story.set_writing_style("Lyrical")
    assert success, "Should be able to set Lyrical writing style"
    assert story.writing_style.name == "Lyrical", "Writing style should be set correctly"
    
    success = story.set_writing_style("Satirical")
    assert success, "Should be able to set Satirical writing style"
    assert story.writing_style.name == "Satirical", "Writing style should be updated correctly"
    
    print("✓ Invalid writing style operations tests passed")


def test_story_serialization_with_writing_style():
    """Test that story serialization includes writing style data."""
    print("Testing story serialization with writing style data...")
    
    # Create story with all data including writing style
    story = Story()
    story.set_story_type_selection("Comedy", "Romantic Comedy", "Love conquers all", "Meet-cute to marriage")
    story.set_genre("Romance")
    story.set_sub_genre("Romantic Comedy")
    story.set_writing_style("Romantic")
    
    # Test JSON serialization
    json_data = story.to_json()
    assert '"genre_name": "Romance"' in json_data, "JSON should include genre"
    assert '"sub_genre_name": "Romantic Comedy"' in json_data, "JSON should include sub-genre"
    assert '"writing_style_name": "Romantic"' in json_data, "JSON should include writing style"
    
    # Test JSON deserialization
    new_story = Story()
    success = new_story.from_json(json_data)
    assert success, "Should be able to load from JSON"
    assert new_story.genre.name == "Romance", "Loaded story should have correct genre"
    assert new_story.sub_genre.name == "Romantic Comedy", "Loaded story should have correct sub-genre"
    assert new_story.writing_style.name == "Romantic", "Loaded story should have correct writing style"
    assert new_story.story_type_name == "Comedy", "Loaded story should have correct story type"
    assert new_story.key_theme == "Love conquers all", "Loaded story should have correct key theme"
    
    print("✓ Story serialization with writing style data tests passed")


def test_all_writing_styles():
    """Test that all expected writing styles are available."""
    print("Testing all writing styles...")
    
    story = Story()
    available_styles = story.get_available_writing_styles()
    style_names = [style.name for style in available_styles]
    
    expected_styles = [
        "Concise", "Lyrical", "Analytical", "Whimsical", "Descriptive",
        "Conversational", "Philosophical", "Satirical", "Suspenseful",
        "Romantic", "Detached", "Experimental", "Journalistic",
        "Reflective", "Persuasive"
    ]
    
    for expected_style in expected_styles:
        assert expected_style in style_names, f"Expected style '{expected_style}' should be available"
        
        # Test that we can set each style
        success = story.set_writing_style(expected_style)
        assert success, f"Should be able to set style '{expected_style}'"
        assert story.writing_style.name == expected_style, f"Style should be set to '{expected_style}'"
    
    print("✓ All writing styles tests passed")


def run_writing_style_tests():
    """Run all writing style-related tests."""
    print("=== Running Writing Style Tests ===\n")
    
    try:
        test_writing_style_flow()
        test_writing_style_invalid_operations()
        test_story_serialization_with_writing_style()
        test_all_writing_styles()
        
        print("\n✅ All writing style tests passed!")
        return True
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return False
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        return False


if __name__ == "__main__":
    success = run_writing_style_tests()
    sys.exit(0 if success else 1)