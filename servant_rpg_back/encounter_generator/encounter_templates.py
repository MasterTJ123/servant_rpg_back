import random

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

def single_boss(bounded_monsters, target):
    initial_position_to_select = 0
    final_position_to_select = 0

    # Find the interval where monsters match the target level
    for index, monster in enumerate(bounded_monsters):
        if int(monster['level']) == target and initial_position_to_select == 0:
            initial_position_to_select = index
        if int(monster['level']) > target:
            final_position_to_select = index - 1
            break

    # Handle case where the array ends without finding a higher-level monster
    if final_position_to_select == 0:
        final_position_to_select = len(bounded_monsters) - 1

    # Select a random monster from the interval
    if initial_position_to_select <= final_position_to_select:
        selected_monster = bounded_monsters[random.randint(initial_position_to_select, final_position_to_select)]
        print("Selected Boss Monster:", selected_monster)
    else:
        print("No suitable boss monster found within the level range.")


def select_single_boss(bounded_monsters, party_level, max_level_difference):
    """
    Return a list of possible single boss monsters
    
    :param bounded_monsters: List of dictionaries, each containing a 'level' key.
    :param party_level: Integer representing the average level of the party.
    :param max_level_difference: Integer representing the maximum allowed level difference.
    :return: List of selected boss monsters.
    """
    target_level = party_level + max_level_difference
    initial_position_to_select = None
    final_position_to_select = None

    for index, monster in enumerate(bounded_monsters):
        monster_level = int(monster['level'])
        
        if monster_level == target_level and initial_position_to_select is None:
            initial_position_to_select = index
        
        if monster_level > target_level:
            final_position_to_select = index - 1
            break

    if initial_position_to_select is None:
        print("No monsters found at the target level.")
        return []

    if final_position_to_select is None:
        final_position_to_select = len(bounded_monsters) - 1

    return bounded_monsters[initial_position_to_select:final_position_to_select + 1]

def select_boss_and_lackeys(bounded_monsters, party_level, xp_budget):
    """
    Selects a boss monster and four lackeys within the given XP budget.
    
    :param bounded_monsters: List of dictionaries, each containing 'name' and 'level' keys.
    :param party_level: Integer representing the average level of the party.
    :param xp_budget: Integer representing the total XP budget.
    :return: A dictionary containing the selected boss and lackeys.
    """

    boss_level = party_level + 2
    lackey_level = party_level - 4

    # Filter monsters by level
    boss_candidates = [m for m in bounded_monsters if int(m['level']) == boss_level]
    lackey_candidates = [m for m in bounded_monsters if int(m['level']) == lackey_level]

    if not boss_candidates or not lackey_candidates:
        print("Not enough monsters found for this encounter setup.")
        return {"boss": None, "lackeys": []}

    # Randomly pick one boss
    boss = random.choice(boss_candidates)
    boss_xp = xp_costs.get(boss_level - party_level, float('inf'))

    remaining_xp = xp_budget - boss_xp
    lackeys = []

    while remaining_xp > 0 and len(lackeys) < 4:
        lackey = random.choice(lackey_candidates)  # Allow duplicates
        lackey_xp = xp_costs.get(lackey_level - party_level, float('inf'))

        if remaining_xp - lackey_xp >= 0:
            lackeys.append(lackey)
            remaining_xp -= lackey_xp
        else:
            break  # Stop if we can't add more without exceeding budget

    if len(lackeys) < 4:
        print("Could not select enough lackeys within XP budget.")

    return {"boss": boss, "lackeys": lackeys}

# Helper functions for each encounter type:

def select_boss_and_lieutenant(bounded_monsters, party_level, xp_budget):
    boss_level = party_level + 2
    lieutenant_level = party_level

    boss_candidates = [m for m in bounded_monsters if int(m['level']) == boss_level]
    lieutenant_candidates = [m for m in bounded_monsters if int(m['level']) == lieutenant_level]

    if not boss_candidates or not lieutenant_candidates:
        print("Not enough monsters found for Boss and Lieutenant encounter setup.")
        return {"boss": None, "lieutenant": None}

    boss = random.choice(boss_candidates)
    boss_xp = xp_costs.get(boss_level - party_level, float('inf'))

    remaining_xp = xp_budget - boss_xp
    lieutenant_xp = xp_costs.get(lieutenant_level - party_level, float('inf'))

    if remaining_xp - lieutenant_xp >= 0:
        lieutenant = random.choice(lieutenant_candidates)
        return {"boss": boss, "lieutenant": lieutenant}
    else:
        print("Not enough XP to add a lieutenant.")
        return {"boss": boss, "lieutenant": None}

def select_elite_enemies(bounded_monsters, party_level, xp_budget):
    level = party_level
    candidates = [m for m in bounded_monsters if int(m['level']) == level]

    if len(candidates) < 3:
        print("Not enough monsters found for Elite Enemies encounter setup.")
        return {"monsters": []}

    selected_monsters = random.sample(candidates, 3)
    total_xp = sum(xp_costs.get(int(m['level']) - party_level, float('inf')) for m in selected_monsters)

    if total_xp <= xp_budget:
        return {"monsters": selected_monsters}
    else:
        print("Not enough XP to select Elite Enemies.")
        return {"monsters": []}

def select_lieutenant_and_lackeys(bounded_monsters, party_level, xp_budget):
    lieutenant_level = party_level
    lackey_level = party_level - 4

    lieutenant_candidates = [m for m in bounded_monsters if int(m['level']) == lieutenant_level]
    lackey_candidates = [m for m in bounded_monsters if int(m['level']) == lackey_level]

    if not lieutenant_candidates or len(lackey_candidates) < 4:
        print("Not enough monsters found for Lieutenant and Lackeys encounter setup.")
        return {"lieutenant": None, "lackeys": []}

    lieutenant = random.choice(lieutenant_candidates)
    lieutenant_xp = xp_costs.get(lieutenant_level - party_level, float('inf'))

    remaining_xp = xp_budget - lieutenant_xp
    lackeys = []

    while remaining_xp > 0 and len(lackeys) < 4:
        lackey = random.choice(lackey_candidates)
        lackey_xp = xp_costs.get(lackey_level - party_level, float('inf'))

        if remaining_xp - lackey_xp >= 0:
            lackeys.append(lackey)
            remaining_xp -= lackey_xp
        else:
            break

    if len(lackeys) < 4:
        print("Could not select enough lackeys.")
    
    return {"lieutenant": lieutenant, "lackeys": lackeys}

def select_mated_pair(bounded_monsters, party_level, xp_budget):
    level = party_level
    candidates = [m for m in bounded_monsters if int(m['level']) == level]

    if len(candidates) < 2:
        print("Not enough monsters found for Mated Pair encounter setup.")
        return {"monsters": []}

    selected_monsters = random.sample(candidates, 2)
    total_xp = sum(xp_costs.get(int(m['level']) - party_level, float('inf')) for m in selected_monsters)

    if total_xp <= xp_budget:
        return {"monsters": selected_monsters}
    else:
        print("Not enough XP to select Mated Pair.")
        return {"monsters": []}

def select_troop(bounded_monsters, party_level, xp_budget):
    level = party_level
    troop_candidates = [m for m in bounded_monsters if int(m['level']) == level or int(m['level']) == level - 2]

    if len(troop_candidates) < 3:
        print("Not enough monsters found for Troop encounter setup.")
        return {"monsters": []}

    selected_monsters = []
    selected_monsters.append(random.choice([m for m in troop_candidates if int(m['level']) == level]))  # One of party level
    selected_monsters.append(random.choice([m for m in troop_candidates if int(m['level']) == level - 2]))  # One of party level - 2

    total_xp = sum(xp_costs.get(int(m['level']) - party_level, float('inf')) for m in selected_monsters)

    if total_xp <= xp_budget:
        return {"monsters": selected_monsters}
    else:
        print("Not enough XP to select Troop.")
        return {"monsters": []}

def select_mook_squad(bounded_monsters, party_level, xp_budget):
    lackey_level = party_level - 4
    lackey_candidates = [m for m in bounded_monsters if int(m['level']) == lackey_level]

    if len(lackey_candidates) < 6:
        print("Not enough monsters found for Mook Squad encounter setup.")
        return {"monsters": []}

    selected_monsters = random.choices(lackey_candidates, k=6)  # Allow duplicates
    total_xp = sum(xp_costs.get(int(m['level']) - party_level, float('inf')) for m in selected_monsters)

    if total_xp <= xp_budget:
        return {"monsters": selected_monsters}
    else:
        print("Not enough XP to select Mook Squad.")
        return {"monsters": []}
