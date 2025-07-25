#!/usr/bin/env python3
"""
Add a test route to create a story with 4 chapters where only 2 are generated
"""

def add_4_chapter_test_route():
    """Add a test route to create a story with 4 chapters where chapter 3 and 4 need generation."""
    
    route_code = '''
@app.route('/test-4-chapters')
def test_4_chapters():
    """Test route to create a story with 4 chapters where chapters 3 and 4 need generation."""
    from objects.plot_line import PlotLine
    from objects.character import Character
    from objects.archetype import ArchetypeEnum
    from objects.functional_role import FunctionalRoleEnum
    from objects.emotional_function import EmotionalFunctionEnum
    from objects.chapter import Chapter
    from objects.narrative_function import NarrativeFunctionEnum
    
    # Create test story
    story = Story()
    story.story_type_name = 'The Quest'
    story.subtype_name = 'Object Quest'
    story.key_theme = 'Growth occurs through shared adventure and sacrifice.'
    story.core_arc = 'Hero discovers strength through perseverance.'
    story.set_genre('Fantasy')
    story.set_sub_genre('High Fantasy')
    story.set_writing_style('Lyrical')
    story.protagonist_archetype = ArchetypeEnum.CHOSEN_ONE
    
    # Add plot line
    plot_line = PlotLine(
        name='The Ancient Relic Quest',
        plotline='A young chosen one must retrieve an ancient magical artifact to save their realm from an encroaching darkness.'
    )
    story.selected_plot_line = plot_line
    story.expanded_plot_line = "In the realm of Aethermoor, young Lyra discovers she is the prophesied Chosen One when ancient runes appear on her skin during her village's harvest festival. The mysterious sage Aldric reveals that the Shadowblight is spreading across the land, corrupting everything it touches. Only the legendary Sunstone of Vaelthara can restore the balance."
    
    # Add characters
    characters = [
        Character(
            name="Lyra",
            archetype=ArchetypeEnum.CHOSEN_ONE,
            functional_role=FunctionalRoleEnum.PROTAGONIST,
            emotional_function=EmotionalFunctionEnum.SYMPATHETIC_CHARACTER,
            backstory="A simple village girl who discovers her destiny when ancient runes appear on her skin during the harvest festival.",
            character_arc="Transforms from a frightened, reluctant hero into a confident leader who understands that true power comes from unity and sacrifice."
        ),
        Character(
            name="Aldric",
            archetype=ArchetypeEnum.WISE_MENTOR,
            functional_role=FunctionalRoleEnum.MENTOR,
            emotional_function=EmotionalFunctionEnum.CATALYST,
            backstory="An ancient sage who has waited centuries for the prophesied Chosen One to appear.",
            character_arc="Learns to trust in the new generation and finds peace in passing on his wisdom."
        ),
        Character(
            name="Kael",
            archetype=ArchetypeEnum.LOYAL_COMPANION,
            functional_role=FunctionalRoleEnum.GUARDIAN_GATEKEEPER,
            emotional_function=EmotionalFunctionEnum.VICTIM,
            backstory="A former knight of the fallen kingdom of Drakmoor, haunted by his failure to protect his people.",
            character_arc="Overcomes his guilt and self-doubt to become a true protector."
        )
    ]
    
    for character in characters:
        story.add_character(character)
    
    # Add test chapters - only first 2 have chapter_text (generated), 3 and 4 need generation
    chapters = [
        Chapter(
            chapter_number=1,
            title="The Awakening",
            overview="In the village of Thornfield, Lyra discovers her destiny when ancient runes suddenly appear on her skin during the harvest festival. The mysterious sage Aldric arrives to explain her role as the Chosen One.",
            character_impact=[
                {"character": "Lyra", "effect": "Discovers her identity as the Chosen One and reluctantly accepts her destiny, feeling overwhelmed but determined."},
                {"character": "Aldric", "effect": "Reveals long-held secrets about the prophecy and begins mentoring Lyra, finding purpose in his centuries of waiting."}
            ],
            point_of_view="Lyra",
            narrative_function=NarrativeFunctionEnum.INCITING_INCIDENT,
            foreshadow_or_echo="The glowing runes foreshadow the final ritual where Lyra must sacrifice her ego to save the realm.",
            scene_highlights="The dramatic moment when the runes first glow, the festival crowd's reaction, and Aldric's mystical entrance.",
            chapter_text="The harvest festival was in full swing when it happened. Lyra had been laughing with her friends, the golden wheat swaying in the evening breeze, when the burning sensation began. It started as a tingling in her palms, then spread up her arms like fire racing through her veins.\\n\\nShe gasped, stumbling backward as intricate runes blazed to life across her skin—silver lines that pulsed with an otherworldly light. The music stopped. The laughter died. Every eye in the village square turned to her.\\n\\n'The Chosen One,' whispered an old woman, falling to her knees.\\n\\nThat was when Aldric appeared, as if stepping from the very shadows themselves. His ancient eyes held both sorrow and hope as he looked upon her glowing marks.\\n\\n'It is time,' he said simply.",
            summary="Lyra discovers her destiny as the Chosen One when ancient runes appear on her skin during the harvest festival, and the sage Aldric arrives to guide her."
        ),
        Chapter(
            chapter_number=2,
            title="The Gathering Storm", 
            overview="Lyra and Aldric begin their journey, seeking the first clues to the Sunstone's location. They encounter the spreading Shadowblight and witness its devastating effects on the countryside.",
            character_impact=[
                {"character": "Lyra", "effect": "Sees the true scope of the threat and realizes the urgency of her mission, beginning to overcome her self-doubt."},
                {"character": "Aldric", "effect": "Shares more of his burden and knowledge while training Lyra in basic magic and survival skills."}
            ],
            point_of_view="Lyra",
            narrative_function=NarrativeFunctionEnum.RISING_TENSION,
            foreshadow_or_echo="The corruption patterns echo the ancient texts Aldric carries, hinting at the cyclical nature of this threat.",
            scene_highlights="A haunting scene of a corrupted forest, Lyra's first attempts at magic, and refugees fleeing the blight.",
            chapter_text="Three days had passed since leaving Thornfield, and the world around them grew darker with each mile. Where once green fields had stretched toward the horizon, now twisted black veins spider-webbed across the earth—the unmistakable mark of the Shadowblight.\\n\\nLyra watched in horror as a once-proud oak tree crumbled to ash at their approach, its bark having turned an unnatural shade of violet. 'How long has it been spreading?' she asked, her voice barely above a whisper.\\n\\nAldric's weathered face was grim. 'Faster than ever before. The barrier between realms grows thin.' He knelt beside a corrupted stream, its waters running black as midnight. 'We must find the Sunstone before the blight reaches the capital.'",
            summary="Lyra and Aldric witness the devastating spread of the Shadowblight as they begin their quest for the Sunstone."
        ),
        Chapter(
            chapter_number=3,
            title="Allies and Enemies",
            overview="In the border town of Millhaven, Lyra and Aldric recruit their first companions. They meet Kael, a disgraced knight seeking redemption, and Zara, a thief with hidden magical abilities.",
            character_impact=[
                {"character": "Lyra", "effect": "Learns to trust others and begins developing leadership skills, though still struggling with confidence."},
                {"character": "Kael", "effect": "Finds new purpose in the quest and begins to believe in redemption through service to others."}
            ],
            point_of_view="Kael",
            narrative_function=NarrativeFunctionEnum.CHARACTER_INTRODUCTION,
            foreshadow_or_echo="Kael's story of failure echoes themes of redemption that will be central to the climax.",
            scene_highlights="A tavern brawl that reveals each character's skills, and the group's first bonding moment around a campfire."
            # Note: No chapter_text - this chapter needs generation
        ),
        Chapter(
            chapter_number=4,
            title="The First Trial",
            overview="The party encounters their first major challenge when they must navigate the Whispering Woods. Lyra's powers are tested as illusions and ancient guardians attempt to turn them against each other.",
            character_impact=[
                {"character": "Lyra", "effect": "Gains confidence in her abilities and learns to resist magical manipulation."},
                {"character": "Kael", "effect": "Proves his loyalty and begins to trust his new companions."}
            ],
            point_of_view="Lyra",
            narrative_function=NarrativeFunctionEnum.FIRST_REVERSAL,
            foreshadow_or_echo="The illusions echo the final confrontation where Lyra must distinguish between truth and deception.",
            scene_highlights="Magical illusions that test each character's deepest fears and desires."
            # Note: No chapter_text - this chapter needs generation
        )
    ]
    
    for chapter in chapters:
        story.add_chapter(chapter)
    
    # Save to session
    save_story_to_session(story)
    
    return redirect(url_for('chapter_plan'))
'''
    
    with open('/home/runner/work/Kraitif/Kraitif/app.py', 'r') as f:
        content = f.read()
    
    # Add the route before the existing test route
    insertion_point = content.find("@app.route('/test-simulate-chapter-success")
    if insertion_point != -1:
        new_content = content[:insertion_point] + route_code + "\n\n" + content[insertion_point:]
        
        with open('/home/runner/work/Kraitif/Kraitif/app.py', 'w') as f:
            f.write(new_content)
        
        print("Added test route to app.py")
    else:
        print("Could not find insertion point in app.py")

if __name__ == "__main__":
    add_4_chapter_test_route()