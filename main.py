import numpy as np
import requests
import math
from pokemon2 import Pokemon
#from move import Pokemove
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

def get_random_mon(pokemon_names):
    return np.random.choice(pokemon_names)
    
def get_random_nature(nature_names):
    return np.random.choice(nature_names)

def move(name, move_type, power, accuracy, stat):
    pokemonmove = {
        "name": name,
        "type": move_type,
        "damage": power,
        "accuracy": accuracy,
        "stat": stat
    }
    return pokemonmove

def damage_calc(move, user, target, level, accuracy):
        # First checks super-effectiveness, stores the multiplier.
        type_chart = {
                    "normal":    {"rock": 0.5, "ghost": 0, "steel": 0.5},
                    "fire":      {"grass": 2, "ice": 2, "bug": 2, "steel": 2,
                                "fire": 0.5, "water": 0.5, "rock": 0.5, "dragon": 0.5},
                    "water":     {"fire": 2, "ground": 2, "rock": 2,
                                "water": 0.5, "grass": 0.5, "dragon": 0.5},
                    "electric":  {"water": 2, "flying": 2,
                                "electric": 0.5, "grass": 0.5, "dragon": 0.5, "ground": 0},
                    "grass":     {"water": 2, "ground": 2, "rock": 2,
                                "fire": 0.5, "grass": 0.5, "poison": 0.5,
                                "flying": 0.5, "bug": 0.5, "dragon": 0.5, "steel": 0.5},
                    "ice":       {"grass": 2, "ground": 2, "flying": 2, "dragon": 2,
                                "fire": 0.5, "water": 0.5, "ice": 0.5, "steel": 0.5},
                    "fighting":  {"normal": 2, "ice": 2, "rock": 2, "dark": 2, "steel": 2,
                                "poison": 0.5, "flying": 0.5, "psychic": 0.5, "bug": 0.5, "fairy": 0.5,
                                "ghost": 0},
                    "poison":    {"grass": 2, "fairy": 2,
                                "poison": 0.5, "ground": 0.5, "rock": 0.5, "ghost": 0.5, "steel": 0},
                    "ground":    {"fire": 2, "electric": 2, "poison": 2, "rock": 2, "steel": 2,
                                "grass": 0.5, "bug": 0.5, "flying": 0},
                    "flying":    {"grass": 2, "fighting": 2, "bug": 2,
                                "electric": 0.5, "rock": 0.5, "steel": 0.5},
                    "psychic":   {"fighting": 2, "poison": 2,
                                "psychic": 0.5, "steel": 0.5, "dark": 0},
                    "bug":       {"grass": 2, "psychic": 2, "dark": 2,
                                "fire": 0.5, "fighting": 0.5, "flying": 0.5, "ghost": 0.5,
                                "poison": 0.5, "steel": 0.5, "fairy": 0.5},
                    "rock":      {"fire": 2, "ice": 2, "flying": 2, "bug": 2,
                                "fighting": 0.5, "ground": 0.5, "steel": 0.5},
                    "ghost":     {"psychic": 2, "ghost": 2,
                                "dark": 0.5, "normal": 0},
                    "dragon":    {"dragon": 2,
                                "steel": 0.5, "fairy": 0},
                    "dark":      {"psychic": 2, "ghost": 2,
                                "fighting": 0.5, "dark": 0.5, "fairy": 0.5},
                    "steel":     {"ice": 2, "rock": 2, "fairy": 2,
                                "fire": 0.5, "water": 0.5, "electric": 0.5, "steel": 0.5},
                    "fairy":     {"fighting": 2, "dragon": 2, "dark": 2,
                                "fire": 0.5, "poison": 0.5, "steel": 0.5},
                }

        # Then, checks the move stats and the target stats.
        def type_effectiveness(move_type, target_types):
            multiplier = 1.0
            for target_type in target_types:
                multiplier *= type_chart.get(move_type, {}).get(target_type, 1)
                print(multiplier)
            return multiplier

        crit_rate = 1/16
        result = np.random.binomial(1, crit_rate)
        critical_hit = 1.5 if result == 1 else 1

        damage_range = np.random.randint(85, 101) / 100

        STAB = 1.5 if move["type"] in user["type"] else 1

        effectiveness = type_effectiveness(move["type"], target["type"])
        if effectiveness > 1:
            print("It's super effective!")
        elif effectiveness == 0:
            print("It had no effect...")
        elif effectiveness < 1:
            print("It's not very effective...")

        if move["stat"] == "attack":
            possible_damage = ((((2*level/5 + 2)*move["damage"]*user["attack"]/target["defense"])/50)+2)
        elif move["stat"] == "special-attack":
            possible_damage = ((((2*level/5 + 2)*move["damage"]*user["special-attack"]/target["special-defense"])/50)+2)
        else:
            possible_damage = 0
        damage = int(possible_damage * critical_hit * damage_range * STAB * effectiveness * (accuracy/100))
        max_hp = target["hp"]
        target["hp"] = max(0, target["hp"] - damage)

        print(f"{user['name']} used {move['name']}!")
        print(critical_hit)
        print(f"It dealt {damage/max_hp*100:.1f} % damage to {target['name']}! {target['name']} has {target['hp']/max_hp*100:.1f} % HP left.\n")

        return target["hp"]


natures = get_nature_list()
PCnature = get_random_nature(natures)
NPCnature = get_random_nature(natures)
Player_Character = Pokemon("snorlax", PCnature)
body_slam = move("body slam", "normal", 85, 100, "attack")
pokemon_list = get_pokemon_list()
NPlayer_Character = Pokemon("empoleon", NPCnature)
Player_Character.show_mon()
NPlayer_Character.show_mon()
PCbase_stats = Player_Character.stat_calc()
NPCbase_stats = NPlayer_Character.stat_calc()
print(PCbase_stats, PCnature)
print(NPCbase_stats, NPCnature)
PC_dict = Player_Character.to_battle_dict()
NPC_dict = NPlayer_Character.to_battle_dict()
body_slam_attack = damage_calc(body_slam, PC_dict, NPC_dict, 50, 100)
