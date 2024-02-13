cards_bracket = {
    "Tower": ["Cannon", "Tesla"],
    "Spell": ["Zap", "Fireball"],
    "Ground": ["Hog Rider", "Goblin", "Barbarian", "Ice Golem", "Knight", "Ice Spirit"],
    "Air": ["Minions", "Baby Dragon", "Mega Minion"]
}

def analyze_deck(deck):
    air_count = 0
    ground_count = 0
    spell_count = 0
    tower_count = 0
    elixir_total = 0

    for card_name in deck:
        if card_name in cards:
            card = cards[card_name]
            elixir_total += card.elixir_cost
            if card.card_type == "Air":
                air_count += 1
            elif card.card_type == "Ground":
                ground_count += 1
            elif card.card_type == "Spell":
                spell_count += 1
            elif card.card_type == "Tower":
                tower_count += 1

    if air_count == 0:
        print("The deck lacks anti-air cards.")
    if ground_count == 0:
        print("The deck lacks ground troops for defense.")
    if spell_count == 0:
        print("The deck lacks a spell card.")
    if tower_count == 0:
        print("The deck lacks a defensive tower.")
    print(f"Total Elixir Cost: {elixir_total}")

# Example usage:
analyze_deck(["Hog Rider", "Ice Spirit", "Goblin Barrel", "Goblin", "Barbarian", "Zapies", "Ice Golem", "Knight", "Cannon"])
