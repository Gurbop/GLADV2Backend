class ClashRoyaleCard:
    def __init__(self, name, rarity, elixir_cost, description, hitpoints, damage, attack_speed, targets, range):
        self.name = name
        self.rarity = rarity
        self.elixir_cost = elixir_cost
        self.description = description
        self.hitpoints = hitpoints
        self.damage = damage
        self.attack_speed = attack_speed
        self.targets = targets
        self.range = range

    def show_info(self):
        return f"""
        Card Name: {self.name}
        Rarity: {self.rarity}
        Elixir Cost: {self.elixir_cost}
        Description: {self.description}

        Stats:
        - Hitpoints: {self.hitpoints}
        - Damage: {self.damage} (Area Damage)
        - Attack Speed: {self.attack_speed} seconds
        - Targets: {self.targets}
        - Range: {self.range}

        Special Ability:
        Click on the card to unleash the Electric Burst! This ability deals an additional 200 damage
        to all nearby enemy troops and buildings.

        Strategy:
        The {self.name} is effective for crowd control, stunning and damaging groups of enemy troops.
        Use its special ability strategically to turn the tide of battle in your favor. Be cautious of
        high-damage single-target troops, as the {self.name}'s strength lies in dealing with swarms.
        """

# Example Clash Royale Cards
electric_sparkler = ClashRoyaleCard(
    name="Electric Sparkler",
    rarity="Epic",
    elixir_cost=4,
    description="A dazzling card that electrifies the battlefield. Click on the card to reveal its shocking secrets!",
    hitpoints=800,
    damage=120,
    attack_speed=1.5,
    targets="Ground and Air",
    range=4.5
)

fireball_blaster = ClashRoyaleCard(
    name="Fireball Blaster",
    rarity="Rare",
    elixir_cost=3,
    description="Launches fireballs with explosive force. Handle with care!",
    hitpoints=600,
    damage=180,
    attack_speed=2.0,
    targets="Ground",
    range=5.0
)

# Add more cards as needed

# Function to get card info
def get_card_info(card):
    return card.show_info()

# Example usage
if __name__ == "__main__":
    print(get_card_info(electric_sparkler))
    print(get_card_info(fireball_blaster))
