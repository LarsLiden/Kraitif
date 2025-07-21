#!/usr/bin/env python3
"""
Test the writing style selection functionality.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from story import Story
from style import StyleRegistry


def test_writing_style_functionality():
    """Test writing style selection in Story class."""
    print("Testing writing style functionality...")
    
    # Create a story and style registry
    story = Story()
    style_registry = StyleRegistry()
    
    # Test getting available styles
    styles = story.get_available_styles()
    assert len(styles) == 15, f"Expected 15 styles, got {len(styles)}"
    print(f"✓ Found {len(styles)} writing styles")
    
    # Test setting a valid writing style
    success = story.set_writing_style("Concise")
    assert success, "Should be able to set valid writing style"
    assert story.writing_style is not None, "Writing style should be set"
    assert story.writing_style.name == "Concise", "Writing style name should match"
    print("✓ Writing style set successfully")
    
    # Test setting invalid writing style
    success = story.set_writing_style("NonexistentStyle")
    assert not success, "Should not be able to set invalid writing style"
    assert story.writing_style.name == "Concise", "Writing style should remain unchanged"
    print("✓ Invalid writing style rejected correctly")
    
    # Test string representation includes writing style
    story_str = str(story)
    assert "Writing Style: Concise" in story_str, "String representation should include writing style"
    print("✓ String representation includes writing style")
    
    # Test JSON serialization includes writing style
    json_str = story.to_json()
    assert '"writing_style_name": "Concise"' in json_str, "JSON should include writing style"
    print("✓ JSON serialization includes writing style")
    
    # Test JSON deserialization includes writing style
    new_story = Story()
    success = new_story.from_json(json_str)
    assert success, "Should be able to load story from JSON"
    assert new_story.writing_style is not None, "Writing style should be loaded"
    assert new_story.writing_style.name == "Concise", "Writing style should match"
    print("✓ JSON deserialization includes writing style")
    
    print("✅ All writing style functionality tests passed!")


def test_all_required_styles():
    """Test that all required writing styles from the issue are present."""
    print("Testing that all required writing styles are present...")
    
    style_registry = StyleRegistry()
    styles = style_registry.get_all_styles()
    style_names = [style.name for style in styles]
    
    required_styles = [
        "Concise", "Lyrical", "Analytical", "Whimsical", "Descriptive",
        "Conversational", "Philosophical", "Satirical", "Suspenseful",
        "Romantic", "Detached", "Experimental", "Journalistic",
        "Reflective", "Persuasive"
    ]
    
    for required_style in required_styles:
        assert required_style in style_names, f"Required style '{required_style}' not found"
        style = style_registry.get_style(required_style)
        assert style is not None, f"Style '{required_style}' should be retrievable"
        assert style.description, f"Style '{required_style}' should have a description"
        print(f"✓ Found required style: {required_style}")
    
    assert len(style_names) == len(required_styles), f"Expected {len(required_styles)} styles, got {len(style_names)}"
    print("✅ All required writing styles are present!")


if __name__ == "__main__":
    print("=== Running Writing Style Tests ===\n")
    test_writing_style_functionality()
    print()
    test_all_required_styles()
    print("\n✅ All writing style tests passed!")