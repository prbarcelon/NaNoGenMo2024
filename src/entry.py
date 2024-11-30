import random

import tracery
from ollama import ChatResponse, chat
from tracery.modifiers import base_english

from entry_grammar import rules as entry_rules
from spell_incantation_generator import SpellIncantationGenerator


generator = SpellIncantationGenerator("./src/data/spell_incantations.tsv")
discovery_count = 0

def generate_journal_entry(intro: str, spell_incantation: str, seed: int) -> str:
    global discovery_count
    discovery_count = discovery_count + 1
    prompt = """As a bestselling author and an expert in fantasy writing for videogames,
books, movies, and television shows with multiple awards, your task today
is to use your decades of experience to help me write flavor text for a
videogame spell incantation. The flavor text will be in first person and
in the style of a research journal entry of a mage that discovered a
spell. The entry documents their findings, discovery, what they thought,
and what they felt. The text should be gender neutral.

Here are some examples:

Entry Title: Reflective Barrier Discovery
Today, I made an incredible breakthrough in my research of mirror magic. As I whispered the incantation, “Spirits of the arcane, guardians of the mystic arts, lend me your unfathomable wisdom! Let the secrets of the universe unfold before me, and bend the forces of magic to my will! Arcanum of the Eldritch Nexus!”, I could feel the energies of the spell coalescing around me.
A series of gleaming mirror panels rose from the ground, curving around me and forming a shimmering barrier. The sight was mesmerizing, the soft, silvery glow emanating from the mirror surfaces enhancing their reflective properties. I realized this spell not only held great beauty, but immense defensive power as well.
As I tested the Reflective Barrier against projectiles and spells, I marveled at the way they seemed to be momentarily caught in the mirror world, only to reverse direction and fly back toward their origin with equal force. I knew I had discovered a formidable defense against enemy attacks.
What intrigued me further was the spell's ability to create confusing reflections. As my allies approached the barrier, their images multiplied and shifted, making it nearly impossible to discern their true positions. This additional layer of deception and protection offered untold strategic advantages on the battlefield.
I have decided to name this spell the “Reflective Barrier,” as it perfectly captures its core essence - a wall of mirrors that simultaneously protects and deceives. I look forward to refining this spell and uncovering even more hidden potential within the realm of mirror magic.

Entry Title: Gale's Symphony of the Boundless Whisper Discovery
Oh, what a whirlwind of a day it has been! My experimentation with elemental magic led me to the discovery of a spectacular new spell. As I uttered the incantation, "Spirits of the relentless tempest, bestow upon me the power to command the unyielding winds! Let the gales carry my voice to the farthest reaches of the world, and let the air be my loyal servant! Gale's Symphony of the Boundless Whisper!", I could sense the air around me dance to a melody unheard before.
A gust of wind swirled around me, building in intensity and forming a breathtaking cyclone. The wind's howling harmonized with the rustling leaves, creating an ethereal symphony that sent shivers down my spine. This spell was more than just a display of sheer power; it was a beautiful union of art and nature.
As I played with my newfound ability, I discovered the spell's incredible versatility. By controlling the strength and direction of the winds, I could send messages across vast distances, or even eavesdrop on conversations from afar, as if carried on the wings of the gentlest breeze. This spell held the potential to be both a powerful tool of communication and a stealthy means of espionage.
Yet, the winds were not just my messengers; they became my allies, shielding me from harm and hindering my enemies. The gusts could deflect arrows and send opponents off balance, while the whispers of the wind could convey information and relay commands to my allies.
With a sense of excitement and pride, I have named this spell "Gale's Symphony of the Boundless Whisper," a moniker that captures the spell's essence and grace. I eagerly anticipate further exploration of this spell's potential and the melding of wind magic with my own expanding repertoire of arcane knowledge.

Entry Title: Tsunami of Abyssal Doom Discovery
Ahoy, what a day to remember! My recent foray into aquatic magic has opened the floodgates to an awe-inspiring new spell. With trepidation and excitement, I chanted the incantation, "Spirits of the ocean depths, surrender your boundless might! Awaken the ancient kraken's wrath, with crushing pressure and merciless tides! Emerge from the abyss, bind your essence with my will, and let the tidal wave of despair wash over my foes! Tsunami of Abyssal Doom!", and the world around me transformed into a tempestuous, watery realm.
As I continued the incantation, I felt the overpowering energy of the ocean's depths surge through me. The air grew heavy with salt and brine, and I sensed the formidable presence of ancient sea creatures lurking just beneath the surface. This spell was not just a display of raw force; it was a connection to the primordial power of the ocean itself.
I could hardly believe my eyes when the ground beneath me morphed into a roiling, darkened sea, churning with the fury of a thousand storms. A colossal wave, its towering crest adorned with menacing tendrils, rose from the depths to my command. It was a sight as fearsome as it was awe-inspiring, and I knew that I had tapped into a force beyond my wildest dreams.
The Tsunami of Abyssal Doom held not only the crushing power of the ocean but also the relentless fury of the creatures that dwell within its depths. As the wave crashed down, the inky tendrils ensnared my foes, dragging them beneath the merciless tide. Their pleas for mercy vanished beneath the cacophony of the tempest, a testament to the spell's overwhelming might.
With a mix of reverence and trepidation, I have dubbed this spell the "Tsunami of Abyssal Doom," a name that encapsulates its boundless power and destructive potential. As I continue my exploration into the mystic arts, I cannot help but wonder what other secrets the depths of the ocean may reveal, and how I might harness that power to shape the future of magic.

The journal entry shall be written in the following format:
<entry>
    <entry_number></entry_number>
    <entry_title></entry_title>
    <entry_content></entry_content>
</entry>

Use the intro provided only. DO NOT modify it!

Here is the entry information you need to write the flavor text:
"""
    content = f"""{prompt}
entry_number: {seed}
spell_incantation: {spell_incantation}
intro: {intro}
"""
    response: ChatResponse = chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": content,
            },
        ],
        options={
            "seed": seed,
        },
    )
    print(response.message.content)
    # Remove everything outside the <entry> tags
    assert "<entry>" in response.message.content, "No <entry> tag found in response."
    # Sometimes this fails, so we'll just ignore if no </entry> tag is found
    # assert "</entry>" in response.message.content, "No </entry> tag found in response."
    result = response.message.content.split("<entry>")[1].split("</entry>")[0]
    assert len(result) > 0, "No entry found in response."
    entry_title = result.split("<entry_title>")[1].split("</entry_title>")[0]
    if entry_title == "":
        entry_title = f"Spell Incantation Discovery No. {discovery_count}"

    entry_content = result.split("<entry_content>")[1].split("</entry_content>")[0]
    journal_entry = f"""# Entry #{seed}: {entry_title}

{entry_content}
"""
    # Clean up the journal entry and reformat it
    while "\n\n" in journal_entry:
        journal_entry = journal_entry.replace("\n\n", "\n")
    items = journal_entry.split("\n")
    items = [item.strip() for item in items]
    journal_entry = "\n\n".join(items)
    journal_entry = journal_entry.strip()
    journal_entry = journal_entry.replace("�", "-")
    return journal_entry


color_elements = ["black", "blue", "green", "orange", "purple", "red", "yellow"]
# Create markdown file to use as output
with open("journal_entries.md", "w", encoding="utf-8") as file:
    # Each entry is 1778 total words/6 entries ~= 296 words.
    # For 50,000 words, we need 169 entries, so just round up to 200.
    # Create an array of 169 integers starting at a random value then
    # incrementing by a random value between 3 and 15.
    deltas = [random.randint(3, 15) for _ in range(201)] # Needed more entries, so going to 201
    # Use the deltas to generate the seeds
    seeds = [random.randint(0, 100)]
    for delta in deltas:
        seeds.append(seeds[-1] + delta)
    # We'll have 201 entries, but that's fine
    counter = 0
    for seed in seeds:
        counter = counter + 1
        try:
            random.seed(seed)
            selected_color_element = random.choice(color_elements)
            entry_rules.update(
                {
                    "origin": f"#[ELEMENT_NAME:{selected_color_element}]introduction#",
                }
            )
            grammar = tracery.Grammar(entry_rules)
            grammar.add_modifiers(base_english)
            intro = grammar.flatten("#origin#")
            # print(intro)
            # print(f"Selected color element: {selected_color_element}")
            incantation = generator.generate_incantation(selected_color_element).replace(';','!')
            # print(f"Incantation: {incantation}")
            entry = generate_journal_entry(intro, incantation, seed)
            file.write(entry)
            file.write("\n\n")
            print(f"Journal entry: {entry}")
            print("=====================================================")
        except Exception as e:
            print(f"Error at entry {seed}, skipping to next entry.")
            print(f"Error: {e}")
            print("=====================================================")
        print(f"Completed entry {counter} of {len(seeds)}.")