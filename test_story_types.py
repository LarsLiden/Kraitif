#!/usr/bin/env python3
"""
Basic tests for Story Types and SubTypes

This script provides basic validation tests for the story types implementation.
"""

import sys
from story_types import StoryTypeRegistry, StoryType, StorySubType


def test_story_type_registry():
    """Test the StoryTypeRegistry functionality."""
    print("Testing StoryTypeRegistry...")
    
    registry = StoryTypeRegistry()
    
    # Test that all 7 story types are available
    story_types = registry.get_all_story_types()
    assert len(story_types) == 7, f"Expected 7 story types, got {len(story_types)}"
    
    # Test that story type names are correct
    expected_names = [
        "Overcoming the Monster",
        "Rags to Riches", 
        "The Quest",
        "Voyage and Return",
        "Comedy",
        "Tragedy",
        "Rebirth"
    ]
    
    actual_names = registry.list_story_types()
    for name in expected_names:
        assert name in actual_names, f"Missing story type: {name}"
    
    # Test lookup by name
    quest = registry.get_story_type("The Quest")
    assert quest is not None, "Could not find The Quest story type"
    assert quest.name == "The Quest", f"Expected 'The Quest', got '{quest.name}'"
    
    # Test case-insensitive lookup
    quest2 = registry.get_story_type("the quest")
    assert quest2 is not None, "Case-insensitive lookup failed"
    
    # Test lookup with underscores
    quest3 = registry.get_story_type("the_quest")
    assert quest3 is not None, "Underscore lookup failed"
    
    print("✓ StoryTypeRegistry tests passed")


def test_story_subtypes():
    """Test that each story type has the correct subtypes."""
    print("Testing Story SubTypes...")
    
    registry = StoryTypeRegistry()
    
    # Test Overcoming the Monster subtypes
    monster = registry.get_story_type("Overcoming the Monster")
    assert len(monster.subtypes) == 3, f"Expected 3 subtypes for Overcoming the Monster, got {len(monster.subtypes)}"
    assert len(monster.examples) >= 1, "Overcoming the Monster should have examples"
    assert "Beowulf" in monster.examples or "Jaws" in monster.examples, "Should have Beowulf or Jaws as examples"
    
    predator = monster.get_subtype("Predator")
    assert predator is not None, "Could not find Predator subtype"
    assert "Jaws" in predator.examples, "Jaws should be in Predator examples"
    
    # Test Rags to Riches subtypes
    rags = registry.get_story_type("Rags to Riches")
    assert len(rags.subtypes) == 3, f"Expected 3 subtypes for Rags to Riches, got {len(rags.subtypes)}"
    assert len(rags.examples) >= 1, "Rags to Riches should have examples"
    assert rags.key_theme == "Inner transformation is more important than material gain"
    
    # Test The Quest subtypes
    quest = registry.get_story_type("The Quest")
    assert len(quest.subtypes) == 3, f"Expected 3 subtypes for The Quest, got {len(quest.subtypes)}"
    assert len(quest.examples) >= 1, "The Quest should have examples"
    assert "Companions" in quest.common_elements, "Companions should be in Quest common elements"
    
    # Test Voyage and Return
    voyage = registry.get_story_type("Voyage and Return")
    assert len(voyage.examples) >= 1, "Voyage and Return should have examples"
    assert voyage.emotional_arc == "Naïveté → Danger → Escape → Wisdom"
    
    # Test Comedy subtypes
    comedy = registry.get_story_type("Comedy")
    assert len(comedy.subtypes) == 3, f"Expected 3 subtypes for Comedy, got {len(comedy.subtypes)}"
    assert len(comedy.examples) >= 1, "Comedy should have examples"
    
    # Test Tragedy subtypes  
    tragedy = registry.get_story_type("Tragedy")
    assert len(tragedy.examples) >= 1, "Tragedy should have examples"
    assert tragedy.emotional_arc == "Rise → Fall → Catharsis"
    
    # Test Rebirth subtypes
    rebirth = registry.get_story_type("Rebirth")
    assert len(rebirth.examples) >= 1, "Rebirth should have examples"
    assert rebirth.key_theme == "A symbolic 'death' followed by renewal"
    
    print("✓ Story SubTypes tests passed")


def test_story_subtype_class():
    """Test the StorySubType class."""
    print("Testing StorySubType class...")
    
    # Create a subtype
    subtype = StorySubType(
        name="Test Subtype",
        description="A test subtype",
        examples=["Example 1", "Example 2"]
    )
    
    assert subtype.name == "Test Subtype"
    assert subtype.description == "A test subtype"
    assert len(subtype.examples) == 2
    assert "Example 1" in subtype.examples
    
    # Test string representation
    str_repr = str(subtype)
    assert "Test Subtype" in str_repr
    assert "A test subtype" in str_repr
    
    print("✓ StorySubType class tests passed")


def test_story_type_class():
    """Test the StoryType class."""
    print("Testing StoryType class...")
    
    # Create a story type
    story_type = StoryType(
        name="Test Story Type",
        description="A test story type",
        examples=["Example Work 1", "Example Work 2"]
    )
    
    # Test examples
    assert len(story_type.examples) == 2
    assert "Example Work 1" in story_type.examples
    assert "Example Work 2" in story_type.examples
    
    # Add a subtype
    subtype = StorySubType("Test Sub", "Test description")
    story_type.add_subtype(subtype)
    
    assert len(story_type.subtypes) == 1
    assert story_type.get_subtype("Test Sub") is not None
    assert story_type.get_subtype("nonexistent") is None
    
    # Test case-insensitive lookup
    assert story_type.get_subtype("test sub") is not None
    
    print("✓ StoryType class tests passed")


def run_all_tests():
    """Run all tests."""
    print("=== Running Story Types Tests ===\n")
    
    try:
        test_story_type_registry()
        test_story_subtypes()
        test_story_subtype_class()
        test_story_type_class()
        
        print("\n✅ All tests passed!")
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