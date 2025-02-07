#Eu so quero meia duzia de funções...não quero fazer um app todo do zero pra isso
#Thiago, boa sorte implementando essas paradas


#primeira passada pelo DeepSeek
import random
from typing import List, Dict, Optional
import json

from encounter_templates import *

xp_costs = {
    -4: 10,   # Low-threat lackey
    -3: 15,   # Low- or moderate-threat lackey
    -2: 20,   # Any lackey or standard creature
    -1: 30,   # Any standard creature
     0: 40,   # Any standard creature or low-threat boss
     1: 60,   # Low- or moderate-threat boss
     2: 80,   # Moderate- or severe-threat boss
     3: 120,  # Severe- or extreme-threat boss
     4: 160   # Extreme-threat solo boss
}

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
    xp_budget = calculate_xp_budget(party_size, difficulty)

    # Step 2: Apply filters to monster data (if provided)
    filtered_monsters = apply_filters(monster_data, filters)

    #preciso validar os monstros, se tem algum do nivel adequado

    # Step 3: Select monsters that fit the XP budget
    selected_monsters = select_monsters(filtered_monsters, xp_budget, party_level)

    return selected_monsters


def calculate_xp_budget( party_size: int, difficulty: str) -> int:
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
        "trivial": 40,
        "low": 60,
        "moderate": 80,
        "severe": 120,
        "extreme": 160
    }

    #quanto cada player a mais adiciona
    xp_character_adjustment = {
        "trivial": 10,
        "low": 20,
        "moderate": 20,
        "severe": 30,
        "extreme": 40
    }

    # Adjust XP budget based on party size (Pathfinder 2E rules)
    base_xp = xp_thresholds.get(difficulty, 0)
    character_adjustment = xp_character_adjustment.get(difficulty, 0)

    #4 eh o tamanho padrao da party, a conta e feita em volta disso
    xp_budget = base_xp - ((4 - party_size) * character_adjustment)

    #pra nao ter chance de retornar menos que 10 com parties muito pequenas
    if xp_budget < 10:
        return 10

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


def get_max_level_diff(xp_budget):
    # Determine the maximum level difference based on the XP budget
    for level_diff in sorted(xp_costs.keys(), reverse=True):
        if xp_costs[level_diff] <= xp_budget:
            return level_diff
    return -4  # Default to the lowest level difference if budget is very low

def select_monsters(filtered_monsters: List[Dict], xp_budget: int, party_level: int) -> List[Dict]:
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
    sorted_monsters = sorted(filtered_monsters, key=lambda x: x["level"])

    lower_bound = party_level - 4
    upper_bound = party_level + 4 #A lista fa
    bounded_monsters = [monster for monster in sorted_monsters if lower_bound <= int(monster['level']) <= upper_bound]

    #bounded_monsters possui os monstros dentro do limite  recomendado, selecionados por tipo
    #agora, como que eu escolho isso?
    #primeira coisa, a tabela de custos!
    #bounded_monsters esta ordenada por nivel
    #pego os monstros que a xp permite, e o que o template determina
    #se sobrou XP, 
    
    encounter_types = [
    "Single Boss",
    "Boss and Lieutenant",
    "Elite Enemies",
    "Lieutenant and Lackeys",
    "Mated Pair",
    "Troop",
    "Mook Squad"
]
    selected_encounter_type = random.choice(encounter_types)

    #Ta funcionando, agora preciso refinar para escolher as versões enfraquecidas ou elites também

    print("TEMPLATE DO ENCONTRO: ", selected_encounter_type)
    if selected_encounter_type == "Boss and Lieutenant":
        return select_boss_and_lieutenant(bounded_monsters, party_level, xp_budget)
    elif selected_encounter_type == "Elite Enemies":
        return select_elite_enemies(bounded_monsters, party_level, xp_budget)
    elif selected_encounter_type == "Lieutenant and Lackeys":
        return select_lieutenant_and_lackeys(bounded_monsters, party_level, xp_budget)
    elif selected_encounter_type == "Mated Pair":
        return select_mated_pair(bounded_monsters, party_level, xp_budget)
    elif selected_encounter_type == "Troop":
        return select_troop(bounded_monsters, party_level, xp_budget)
    elif selected_encounter_type == "Mook Squad":
        return select_mook_squad(bounded_monsters, party_level, xp_budget)
    elif selected_encounter_type == "Single Boss":
        return single_boss(bounded_monsters, party_level+3)
    else:
        print(f"Unknown encounter type: {selected_encounter_type}")
        return {"monsters": []}



def get_monsters():
    with open('game_data/monsters-pf2-v2.json', 'r') as file:
        raw_data = json.load(file)

    monsters_data = raw_data['monsters']
    
    return monsters_data

monsters = get_monsters()
party_level = 3
party_size = 4
difficulty = "moderate"
filters = {"type": "Undead"} #tem que ser com letra maiuscula....acho que n tem nenhum tipo com minuscula

encounter = generate_encounter(party_level, party_size, difficulty, monsters, filters)
print(encounter)