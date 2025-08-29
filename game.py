import numpy as np
import requests
import math
from pokemon import Pokemon
#import pokebase as pb

def get_pokemon_list():
    pokemon_url = "https://pokeapi.co/api/v2/pokemon?limit=2000" #searches for a max of 2,000 pokemon to get all forms and variants
    response = requests.get(pokemon_url)
    if response.status_code == 200:
        data = response.json()
        pokemon_names = [p["name"] for p in data["results"]]
    else:
        print("Error:", response.status_code)
    return pokemon_names

def get_nature_list():
    nature_url = "https://pokeapi.co/api/v2/nature?limit=100"
    response = requests.get(nature_url)
    if response.status_code == 200:
        data = response.json()
        nature_names = [n["name"] for n in data["results"]]
    else:
        print("Error:", response.status_code)
    return nature_names

def nature_effects(stats, nature):
    
    for stat in range(len(stats)):
        stats[stat] = stats[stat]*nature_mod[stat]
    return stats

def get_random_mon(pokemon_names):
    return np.random.choice(pokemon_names)
    
def get_random_nature(nature_names):
    return np.random.choice(nature_names)

def damage_calc(move_type, poke_types, move_stats, poke_stats, abilities, items, accuracy):
    # these are all arrays of two or more values, checking both the target and user.
    # First checks super-effectiveness, stores the multiplier.
    effectiveness = []
    # Then, checks the move stats and the target stats.
    # 
    damage 

natures = get_nature_list()
PCnature = get_random_nature(natures)
NPCnature = get_random_nature(natures)
Player_Character = Pokemon(input("Which Pokemon do you choose?  "), PCnature)
pokemon_list = get_pokemon_list()
NPlayer_Character = Pokemon(get_random_mon(pokemon_list), NPCnature)
PCbase_stats = Player_Character.show_mon()
NPCbase_stats = NPlayer_Character.show_mon()
y = Player_Character.stat_calc()
print(y)
