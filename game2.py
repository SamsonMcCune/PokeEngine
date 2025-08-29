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
                    "Normal":    {"Rock": 0.5, "Ghost": 0, "Steel": 0.5},
                    "Fire":      {"Grass": 2, "Ice": 2, "Bug": 2, "Steel": 2,
                                "Fire": 0.5, "Water": 0.5, "Rock": 0.5, "Dragon": 0.5},
                    "Water":     {"Fire": 2, "Ground": 2, "Rock": 2,
                                "Water": 0.5, "Grass": 0.5, "Dragon": 0.5},
                    "Electric":  {"Water": 2, "Flying": 2,
                                "Electric": 0.5, "Grass": 0.5, "Dragon": 0.5, "Ground": 0},
                    "Grass":     {"Water": 2, "Ground": 2, "Rock": 2,
                                "Fire": 0.5, "Grass": 0.5, "Poison": 0.5,
                                "Flying": 0.5, "Bug": 0.5, "Dragon": 0.5, "Steel": 0.5},
                    "Ice":       {"Grass": 2, "Ground": 2, "Flying": 2, "Dragon": 2,
                                "Fire": 0.5, "Water": 0.5, "Ice": 0.5, "Steel": 0.5},
                    "Fighting":  {"Normal": 2, "Ice": 2, "Rock": 2, "Dark": 2, "Steel": 2,
                                "Poison": 0.5, "Flying": 0.5, "Psychic": 0.5, "Bug": 0.5, "Fairy": 0.5,
                                "Ghost": 0},
                    "Poison":    {"Grass": 2, "Fairy": 2,
                                "Poison": 0.5, "Ground": 0.5, "Rock": 0.5, "Ghost": 0.5, "Steel": 0},
                    "Ground":    {"Fire": 2, "Electric": 2, "Poison": 2, "Rock": 2, "Steel": 2,
                                "Grass": 0.5, "Bug": 0.5, "Flying": 0},
                    "Flying":    {"Grass": 2, "Fighting": 2, "Bug": 2,
                                "Electric": 0.5, "Rock": 0.5, "Steel": 0.5},
                    "Psychic":   {"Fighting": 2, "Poison": 2,
                                "Psychic": 0.5, "Steel": 0.5, "Dark": 0},
                    "Bug":       {"Grass": 2, "Psychic": 2, "Dark": 2,
                                "Fire": 0.5, "Fighting": 0.5, "Flying": 0.5, "Ghost": 0.5,
                                "Poison": 0.5, "Steel": 0.5, "Fairy": 0.5},
                    "Rock":      {"Fire": 2, "Ice": 2, "Flying": 2, "Bug": 2,
                                "Fighting": 0.5, "Ground": 0.5, "Steel": 0.5},
                    "Ghost":     {"Psychic": 2, "Ghost": 2,
                                "Dark": 0.5, "Normal": 0},
                    "Dragon":    {"Dragon": 2,
                                "Steel": 0.5, "Fairy": 0},
                    "Dark":      {"Psychic": 2, "Ghost": 2,
                                "Fighting": 0.5, "Dark": 0.5, "Fairy": 0.5},
                    "Steel":     {"Ice": 2, "Rock": 2, "Fairy": 2,
                                "Fire": 0.5, "Water": 0.5, "Electric": 0.5, "Steel": 0.5},
                    "Fairy":     {"Fighting": 2, "Dragon": 2, "Dark": 2,
                                "Fire": 0.5, "Poison": 0.5, "Steel": 0.5},
                }

        # Then, checks the move stats and the target stats.
        def type_effectiveness(move_type, target_types):
            damage_multiplier = 1.0  # start neutral
            for target_type in target_types:  # account for dual-typing
                if target_type in type_chart.get(move_type, {}):
                    damage_multiplier *= type_chart[move_type][target_type]
                else:
                    damage_multiplier *= 1  # neutral if not listed
            return damage_multiplier
        crit_rate = 1/16
        result = np.random.binomial(1, crit_rate)
        critical_hit = 1 if result == 1 else 1.5
        damage_range = np.random.randint(85, 101) / 100
        if move["type"] == user["type"]:
            STAB = 1.5
        else:
            STAB = 1
        if move["stat"] == "attack":
            possible_damage = ((((2*level/5 + 2)*move["damage"]*user["attack"]/target["defense"])/50)+2)*critical_hit*damage_range*STAB*type_effectiveness(move["type"],target["type"])
        elif move["stat"] == "special-attack":
            possible_damage = ((((2*level/5 + 2)*move["damage"]*user["special-attack"]/target["special-defense"])/50)+2)*critical_hit*damage_range*STAB*type_effectiveness(move["type"],target["type"])
        damage = possible_damage*accuracy
        target["hp"] = max(0, target["hp"] - damage)
        return target["hp"]


natures = get_nature_list()
PCnature = get_random_nature(natures)
NPCnature = get_random_nature(natures)
Player_Character = Pokemon(input("Which Pokemon do you choose?  "), PCnature)
body_slam = move("body slam", "normal", 80, 100, "attack")
pokemon_list = get_pokemon_list()
NPlayer_Character = Pokemon(get_random_mon(pokemon_list), NPCnature)
Player_Character.show_mon()
NPlayer_Character.show_mon()
PCbase_stats = Player_Character.stat_calc()
NPCbase_stats = NPlayer_Character.stat_calc()
print(PCbase_stats, PCnature)
print(NPCbase_stats, NPCnature)
PC_dict = Player_Character.to_battle_dict()
NPC_dict = NPlayer_Character.to_battle_dict()
body_slam_attack = damage_calc(body_slam, PC_dict, NPC_dict, 50, 100)