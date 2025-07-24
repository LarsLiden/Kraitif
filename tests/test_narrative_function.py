"""
Unit tests for narrative function functionality.
"""

import pytest
import json
from objects.narrative_function import NarrativeFunction, NarrativeFunctionRegistry, NarrativeFunctionEnum


def test_narrative_function_class():
    """Test NarrativeFunction class."""
    function = NarrativeFunction("Setting Introduction", "Establishes location, mood, tone to ground the reader in the story world.")
    assert function.name == "Setting Introduction"
    assert function.description == "Establishes location, mood, tone to ground the reader in the story world."
    assert str(function) == "Setting Introduction: Establishes location, mood, tone to ground the reader in the story world."


def test_narrative_function_registry():
    """Test NarrativeFunctionRegistry initialization and basic functionality."""
    registry = NarrativeFunctionRegistry()
    
    # Test that functions are loaded
    functions = registry.get_all_narrative_functions()
    assert len(functions) == 23
    
    # Test getting specific functions
    setting_intro = registry.get_narrative_function("Setting Introduction")
    assert setting_intro is not None
    assert setting_intro.name == "Setting Introduction"
    assert "Establishes location" in setting_intro.description
    
    inciting_incident = registry.get_narrative_function("Inciting Incident")
    assert inciting_incident is not None
    assert inciting_incident.name == "Inciting Incident"
    assert "disruption to the status quo" in inciting_incident.description
    
    # Test case insensitive lookup
    climax = registry.get_narrative_function("climax")
    assert climax is not None
    assert climax.name == "Climax"
    
    # Test non-existent function
    non_existent = registry.get_narrative_function("Non-existent Function")
    assert non_existent is None


def test_narrative_function_registry_search():
    """Test NarrativeFunctionRegistry search functionality."""
    registry = NarrativeFunctionRegistry()
    
    # Test search by name
    results = registry.search_narrative_functions("climax")
    assert len(results) >= 1
    climax_found = any(func.name == "Climax" for func in results)
    assert climax_found
    
    # Test search by description
    results = registry.search_narrative_functions("tension")
    tension_functions = [func for func in results if "tension" in func.description.lower()]
    assert len(tension_functions) >= 1
    
    # Test search that matches multiple functions
    results = registry.search_narrative_functions("character")
    assert len(results) >= 2  # Should find multiple functions that mention "character"


def test_narrative_function_enum():
    """Test NarrativeFunctionEnum values."""
    assert NarrativeFunctionEnum.SETTING_INTRODUCTION.value == "Setting Introduction"
    assert NarrativeFunctionEnum.CHARACTER_INTRODUCTION.value == "Character Introduction"
    assert NarrativeFunctionEnum.INCITING_INCIDENT.value == "Inciting Incident"
    assert NarrativeFunctionEnum.FIRST_REVERSAL.value == "First Reversal"
    assert NarrativeFunctionEnum.RISING_TENSION.value == "Rising Tension"
    assert NarrativeFunctionEnum.SUBPLOT_ACTIVATION.value == "Subplot Activation"
    assert NarrativeFunctionEnum.MORAL_CHALLENGE.value == "Moral Challenge"
    assert NarrativeFunctionEnum.MIDPOINT_TURN.value == "Midpoint Turn"
    assert NarrativeFunctionEnum.RELATIONSHIP_REVERSAL.value == "Relationship Reversal"
    assert NarrativeFunctionEnum.MOMENT_OF_WEAKNESS.value == "Moment of Weakness"
    assert NarrativeFunctionEnum.SETBACK.value == "Setback"
    assert NarrativeFunctionEnum.TRUTH_REVELATION.value == "Truth Revelation"
    assert NarrativeFunctionEnum.CONFRONTATION.value == "Confrontation"
    assert NarrativeFunctionEnum.CLIMAX.value == "Climax"
    assert NarrativeFunctionEnum.TRANSFORMATION.value == "Transformation"
    assert NarrativeFunctionEnum.DENOUEMENT.value == "Denouement"
    assert NarrativeFunctionEnum.FINAL_IMAGE.value == "Final Image"
    assert NarrativeFunctionEnum.FORESHADOWING.value == "Foreshadowing"
    assert NarrativeFunctionEnum.ECHO.value == "Echo"
    assert NarrativeFunctionEnum.REFLECTION.value == "Reflection"
    assert NarrativeFunctionEnum.THEME_REINFORCEMENT.value == "Theme Reinforcement"
    assert NarrativeFunctionEnum.CATALYST_EVENT.value == "Catalyst Event"
    assert NarrativeFunctionEnum.UNEXPECTED_REUNION.value == "Unexpected Reunion"


def test_narrative_function_names_list():
    """Test listing all narrative function names."""
    registry = NarrativeFunctionRegistry()
    names = registry.list_narrative_function_names()
    
    assert len(names) == 23
    assert "Setting Introduction" in names
    assert "Character Introduction" in names
    assert "Inciting Incident" in names
    assert "Climax" in names
    assert "Denouement" in names
    assert "Foreshadowing" in names
    assert "Echo" in names
    assert "Transformation" in names


def test_all_required_narrative_functions():
    """Test that all required narrative functions from the issue are present."""
    registry = NarrativeFunctionRegistry()
    names = registry.list_narrative_function_names()
    
    required_functions = [
        "Setting Introduction", "Character Introduction", "Inciting Incident", 
        "First Reversal", "Rising Tension", "Subplot Activation", "Moral Challenge", 
        "Midpoint Turn", "Relationship Reversal", "Moment of Weakness", "Setback", 
        "Truth Revelation", "Confrontation", "Climax", "Transformation", 
        "Denouement", "Final Image", "Foreshadowing", "Echo", "Reflection", 
        "Theme Reinforcement", "Catalyst Event", "Unexpected Reunion"
    ]
    
    for required_function in required_functions:
        assert required_function in names, f"Required narrative function '{required_function}' not found in registry"


def test_enum_values_match_registry():
    """Test that all enum values have corresponding entries in the registry."""
    registry = NarrativeFunctionRegistry()
    registry_names = set(registry.list_narrative_function_names())
    
    # Get all enum values
    enum_values = set(item.value for item in NarrativeFunctionEnum)
    
    # Check that all enum values are in the registry
    assert enum_values == registry_names, f"Enum values and registry names don't match. Enum: {enum_values}, Registry: {registry_names}"


def test_narrative_function_descriptions():
    """Test that all narrative functions have meaningful descriptions."""
    registry = NarrativeFunctionRegistry()
    functions = registry.get_all_narrative_functions()
    
    for function in functions:
        assert function.description is not None
        assert len(function.description) > 10, f"Description for {function.name} is too short"
        assert function.description.strip() == function.description, f"Description for {function.name} has leading/trailing whitespace"


def test_registry_case_insensitive_lookup():
    """Test that registry lookup is case insensitive."""
    registry = NarrativeFunctionRegistry()
    
    # Test various case combinations
    test_cases = [
        ("Setting Introduction", "Setting Introduction"),
        ("CHARACTER INTRODUCTION", "Character Introduction"),
        ("inciting incident", "Inciting Incident"),
        ("CLIMAX", "Climax")
    ]
    
    for test_input, expected_name in test_cases:
        function = registry.get_narrative_function(test_input)
        assert function is not None, f"Failed to find function for input: {test_input}"
        assert function.name == expected_name


def test_search_functionality():
    """Test search functionality with various terms."""
    registry = NarrativeFunctionRegistry()
    
    # Test specific search terms
    search_tests = [
        ("introduction", ["Setting Introduction", "Character Introduction"]),
        ("character", ["Character Introduction"]),  # Should at least find this one
        ("tension", ["Rising Tension"]),  # Should at least find this one
        ("reversal", ["First Reversal", "Relationship Reversal"]),
        ("revelation", ["Truth Revelation"])
    ]
    
    for search_term, expected_names in search_tests:
        results = registry.search_narrative_functions(search_term)
        result_names = [func.name for func in results]
        
        for expected_name in expected_names:
            assert expected_name in result_names, f"Expected to find '{expected_name}' when searching for '{search_term}'"


if __name__ == "__main__":
    # Run basic tests if executed directly
    test_narrative_function_class()
    test_narrative_function_registry()
    test_narrative_function_enum()
    test_narrative_function_names_list()
    test_all_required_narrative_functions()
    test_enum_values_match_registry()
    print("All narrative function tests passed!")