import numpy as np
import pandas as pd
import requests
import math
from tabulate import tabulate

class Pokemon:

    def __init__(self, name, nature):
        self.url = f"https://pokeapi.co/api/v2/pokemon/{name.lower()}"
        self.response = requests.get(self.url)
        if self.response.status_code == 200:
            self.data = self.response.json()
            self.name = self.data["name"]
            self.types = []
            for t in self.data["types"]:
                self.types.append(t["type"]["name"])
            self.stats = {s["stat"]["name"]: s["base_stat"] for s in self.data["stats"]}
            self.stats_df = pd.DataFrame([self.stats])
            self.nature = nature
        else:
            raise ValueError("Pokémon not found")
    

    def stat_calc(self):
        increase = 1.1
        decrease = 0.9
        nature_modifiers = {
            "adamant": {"attack": increase, "special-attack": decrease},
            "modest": {"special-attack": increase, "attack": decrease},
            "jolly": {"speed": increase, "special-attack": decrease},
            "brave": {"attack": increase, "speed": decrease},
            "naughty": {"attack": increase, "special-defense": decrease},
            "lonely": {"attack": increase, "defense": decrease},
            "bold": {"defense": increase, "attack": decrease},
            "relaxed": {"defense": increase, "speed": decrease},
            "impish": {"defense": increase, "special-attack": decrease},
            "lax": {"defense": increase, "special-defense": decrease},
            "timid": {"speed": increase, "attack": decrease},
            "hasty": {"speed": increase, "defense": decrease},
            "naive": {"speed": increase, "special-defense": decrease},
            "mild": {"special-attack": increase, "defense": decrease},
            "quiet": {"special-attack": increase, "speed": decrease},
            "rash": {"special-attack": increase, "special-defense": decrease},
            "calm": {"special-defense": increase, "attack": decrease},
            "gentle": {"special-defense": increase, "defense": decrease},
            "sassy": {"special-defense": increase, "speed": decrease},
            "careful": {"special-defense": increase, "special-attack": decrease}
        }
        self.nature_mod = {col: 1.0 for col in self.stats_df.columns}
        if self.nature in nature_modifiers:
            self.nature_mod.update(nature_modifiers[self.nature])
        placeholder_level = 50
        level = placeholder_level
        IVs = {
            "hp": 31,
            "attack": 31,
            "defense": 31,
            "special-attack": 31,
            "special-defense": 31,
            "speed": 31
        }
        EVs = {
            "hp": 0,
            "attack": 0,
            "defense": 0,
            "special-attack": 0,
            "special-defense": 0,
            "speed": 0
        }
        calced_stats = {}
        for stat, self.base in self.stats_df.iloc[0].items():
            if stat == "hp":
                value = math.floor(.01*(2*self.base + IVs["hp"] + math.floor(.25*EVs["hp"]))*level) + level + 10 
            else:
                value = math.floor((math.floor(.01*(2*self.base + IVs[stat] + math.floor(.25*EVs[stat]))*level + 5))*self.nature_mod[stat])
            calced_stats[stat] = value
        return calced_stats

    def show_mon(self):
        print(f"Name: {self.name}")
        print("Types:", ", ".join(self.types))
        print("Stats:")
        print(tabulate(self.stats_df, headers="keys", tablefmt="pretty", showindex=False))
    def to_battle_dict(self):
        stats = self.stat_calc()
        return {
            "name": self.name,
            "type": self.types,   
            "hp": stats["hp"],
            "attack": stats["attack"],
            "defense": stats["defense"],
            "special-attack": stats["special-attack"],
            "special-defense": stats["special-defense"],
            "speed": stats["speed"]
        }