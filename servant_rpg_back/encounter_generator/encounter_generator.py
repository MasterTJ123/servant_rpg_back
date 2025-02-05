#Eu so quero meia duzia de funções...não quero fazer um app todo do zero pra isso
#Thiago, boa sorte implementando essas paradas


#primeira passada pelo DeepSeek
from typing import List, Dict, Optional

def generate_encounter(
    party_level: int,
    party_size: int,
    difficulty: str,
    monster_data: List[Dict],
    filters: Optional[Dict] = None
) -> List[Dict]:
    """
    Generates a random encounter for Pathfinder 2E based on party data and difficulty.

    Args:
        party_level (int): The level of the party.
        party_size (int): The number of players in the party.
        difficulty (str): The desired encounter difficulty (e.g., "low", "moderate", "severe", "extreme").
        monster_data (List[Dict]): A list of dictionaries containing monster data (e.g., name, XP, traits).
        filters (Optional[Dict]): Optional filters to narrow down monster selection (e.g., {"type": "undead"}).

    Returns:
        List[Dict]: A list of selected monsters for the encounter, including their details.
    """
    # Step 1: Calculate XP budget based on party level, size, and difficulty
    xp_budget = calculate_xp_budget(party_level, party_size, difficulty)

    # Step 2: Apply filters to monster data (if provided)
    filtered_monsters = apply_filters(monster_data, filters)

    # Step 3: Select monsters that fit the XP budget
    selected_monsters = select_monsters(filtered_monsters, xp_budget)

    return selected_monsters


def calculate_xp_budget(party_level: int, party_size: int, difficulty: str) -> int:
    """
    Calculates the XP budget for the encounter based on Pathfinder 2E rules.

    Args:
        party_level (int): The level of the party.
        party_size (int): The number of players in the party.
        difficulty (str): The desired encounter difficulty.

    Returns:
        int: The total XP budget for the encounter.
    """
    #Não precisa do party_Level aqui, pois não muda a XP por nível, mas sim o monstro que é selecionado
    # Pathfinder 2E XP thresholds per party level (example values, adjust as needed)
    xp_thresholds = {
        "low": 40,
        "moderate": 60,
        "severe": 80,
        "extreme": 120
    }

    # Adjust XP budget based on party size (Pathfinder 2E rules)
    base_xp = xp_thresholds.get(difficulty, 0)
    xp_budget = base_xp * party_size

    return xp_budget


def apply_filters(monster_data: List[Dict], filters: Optional[Dict]) -> List[Dict]:
    """
    Applies filters to the monster data to narrow down the selection.

    Args:
        monster_data (List[Dict]): The list of monster data.
        filters (Optional[Dict]): Filters to apply (e.g., {"type": "undead"}).

    Returns:
        List[Dict]: The filtered list of monsters.
    """
    if not filters:
        return monster_data

    filtered_monsters = []
    for monster in monster_data:
        match = True
        for key, value in filters.items():
            if monster.get(key) != value:
                match = False
                break
        if match:
            filtered_monsters.append(monster)

    return filtered_monsters


def select_monsters(filtered_monsters: List[Dict], xp_budget: int) -> List[Dict]:
    """
    Selects monsters that fit within the XP budget.

    Args:
        filtered_monsters (List[Dict]): The list of filtered monsters.
        xp_budget (int): The total XP budget for the encounter.

    Returns:
        List[Dict]: The selected monsters for the encounter.
    """
    selected_monsters = []
    remaining_budget = xp_budget

    # Sort monsters by XP (ascending) to prioritize smaller monsters first
    #Aqui deve incluir o nivel do monstro, para selecionar do -4 ao +4
    sorted_monsters = sorted(filtered_monsters, key=lambda x: x["xp"])

    for monster in sorted_monsters:
        if monster["xp"] <= remaining_budget:
            selected_monsters.append(monster)
            remaining_budget -= monster["xp"]

    return selected_monsters


# Example Usage
monster_data = [
    {"name": "Goblin", "xp": 20, "type": "humanoid"},
    {"name": "Skeleton", "xp": 30, "type": "undead"},
    {"name": "Orc", "xp": 40, "type": "humanoid"},
    {"name": "Zombie", "xp": 25, "type": "undead"},
]

party_level = 3
party_size = 4
difficulty = "moderate"
filters = {"type": "undead"}

encounter = generate_encounter(party_level, party_size, difficulty, monster_data, filters)
print(encounter)