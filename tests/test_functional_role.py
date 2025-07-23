"""
Unit tests for functional role functionality.
"""

import pytest
import json
from functional_role import FunctionalRole, FunctionalRoleRegistry, FunctionalRoleEnum
from story import Story


def test_functional_role_class():
    """Test FunctionalRole class."""
    role = FunctionalRole("Protagonist", "Central character whose journey drives the plot.")
    assert role.name == "Protagonist"
    assert role.description == "Central character whose journey drives the plot."
    assert str(role) == "Protagonist: Central character whose journey drives the plot."


def test_functional_role_registry():
    """Test FunctionalRoleRegistry initialization and basic functionality."""
    registry = FunctionalRoleRegistry()
    
    # Test that roles are loaded
    roles = registry.get_all_functional_roles()
    assert len(roles) == 20
    
    # Test getting specific roles
    protagonist = registry.get_functional_role("Protagonist")
    assert protagonist is not None
    assert protagonist.name == "Protagonist"
    assert "Central character" in protagonist.description
    
    antagonist = registry.get_functional_role("Antagonist")
    assert antagonist is not None
    assert antagonist.name == "Antagonist"
    assert "Opposes the protagonist" in antagonist.description
    
    # Test case insensitive lookup
    mentor = registry.get_functional_role("mentor")
    assert mentor is not None
    assert mentor.name == "Mentor"
    
    # Test with complex names
    gatekeeper = registry.get_functional_role("Guardian / Gatekeeper")
    assert gatekeeper is not None
    assert gatekeeper.name == "Guardian / Gatekeeper"
    
    confidant = registry.get_functional_role("Confidant(e)")
    assert confidant is not None
    assert confidant.name == "Confidant(e)"


def test_functional_role_registry_search():
    """Test FunctionalRoleRegistry search functionality."""
    registry = FunctionalRoleRegistry()
    
    # Test search by name
    results = registry.search_functional_roles("protagonist")
    assert len(results) >= 1
    protagonist_found = any(role.name == "Protagonist" for role in results)
    assert protagonist_found
    
    # Test search by description
    results = registry.search_functional_roles("wisdom")
    mentor_found = any(role.name == "Mentor" for role in results)
    assert mentor_found
    
    # Test search that matches multiple roles
    results = registry.search_functional_roles("character")
    assert len(results) >= 3  # Should find multiple roles that mention "character"


def test_functional_role_enum():
    """Test FunctionalRoleEnum values."""
    assert FunctionalRoleEnum.PROTAGONIST.value == "Protagonist"
    assert FunctionalRoleEnum.ANTAGONIST.value == "Antagonist"
    assert FunctionalRoleEnum.MENTOR.value == "Mentor"
    assert FunctionalRoleEnum.ANTI_HERO.value == "Anti-Hero"
    assert FunctionalRoleEnum.CONFIDANT.value == "Confidant(e)"
    assert FunctionalRoleEnum.GUARDIAN_GATEKEEPER.value == "Guardian / Gatekeeper"


def test_functional_role_names_list():
    """Test listing all functional role names."""
    registry = FunctionalRoleRegistry()
    names = registry.list_functional_role_names()
    
    assert len(names) == 20
    assert "Protagonist" in names
    assert "Antagonist" in names
    assert "Mentor" in names
    assert "Anti-Hero" in names
    assert "Everyman" in names


def test_story_functional_role_integration():
    """Test functional role integration with Story class."""
    story = Story()
    
    # Test setting functional role
    success = story.set_functional_role("Protagonist")
    assert success is True
    assert story.functional_role is not None
    assert story.functional_role.name == "Protagonist"
    
    # Test setting invalid functional role
    success = story.set_functional_role("Invalid Role")
    assert success is False
    
    # Test getting available functional roles
    available_roles = story.get_available_functional_roles()
    assert len(available_roles) == 20
    assert any(role.name == "Protagonist" for role in available_roles)
    assert any(role.name == "Antagonist" for role in available_roles)


def test_story_functional_role_serialization():
    """Test functional role serialization in Story class."""
    story = Story()
    
    # Set up story with functional role
    story.set_functional_role("Mentor")
    
    # Test serialization
    json_data = story.to_json()
    data = json.loads(json_data)
    assert data['functional_role_name'] == "Mentor"
    
    # Test deserialization
    new_story = Story()
    success = new_story.from_json(json_data)
    assert success is True
    assert new_story.functional_role is not None
    assert new_story.functional_role.name == "Mentor"


def test_story_functional_role_serialization_without_role():
    """Test functional role serialization when no role is set."""
    story = Story()
    
    # Test serialization without functional role
    json_data = story.to_json()
    data = json.loads(json_data)
    assert data['functional_role_name'] is None
    
    # Test deserialization
    new_story = Story()
    success = new_story.from_json(json_data)
    assert success is True
    assert new_story.functional_role is None


def test_all_required_functional_roles():
    """Test that all required functional roles from the issue are present."""
    registry = FunctionalRoleRegistry()
    names = registry.list_functional_role_names()
    
    required_roles = [
        "Protagonist", "Antagonist", "Deuteragonist", "Tritagonist", "Foil", 
        "Supporting Character", "Confidant(e)", "Narrator", "Love Interest", 
        "Comic Relief", "Mentor", "Sidekick", "Guardian / Gatekeeper", "Herald", 
        "Shapeshifter", "Tempter / Temptress", "Trickster", "Villain", 
        "Anti-Hero", "Everyman"
    ]
    
    for required_role in required_roles:
        assert required_role in names, f"Required role '{required_role}' not found in registry"


if __name__ == "__main__":
    # Run basic tests if executed directly
    test_functional_role_class()
    test_functional_role_registry()
    test_functional_role_enum()
    test_story_functional_role_integration()
    test_story_functional_role_serialization()
    test_all_required_functional_roles()
    print("All functional role tests passed!")