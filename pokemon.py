import numpy as np
import requests
import math

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
            self.nature = nature
        else:
            raise ValueError("Pokémon not found")
    

    def stat_calc(self):
        attack = 1
        defense = 1
        spattack = 1
        spdefense = 1
        speed = 1
        increase = 1.1
        decrease = 0.9
        if self.nature == 'Adamant':
            attack = increase
            spattack = decrease
        elif self.nature == 'Modest':
            spattack = increase
            attack = decrease
        elif self.nature == 'Jolly':
            speed = increase
            spattack = decrease
        elif self.nature == 'Brave':
            attack = increase
            speed = decrease
        elif self.nature == 'Naughty':
            attack = increase
            spdefense = decrease
        elif self.nature == 'Lonely':
            attack = increase
            defense = decrease
        elif self.nature == 'Bold':
            defense = increase
            attack = decrease
        elif self.nature == 'Relaxed':
            defense = increase
            speed = decrease
        elif self.nature == 'Impish':
            defense = increase
            spattack = decrease
        elif self.nature == 'Lax':
            defense = increase
            spdefense = decrease
        elif self.nature == 'Timid':
            speed = increase
            attack = decrease
        elif self.nature == 'Hasty':
            speed = increase
            defense = decrease
        elif self.nature == 'Naive':
            speed = increase
            spdefense = decrease
        elif self.nature == 'Mild':
            spattack = increase
            defense = decrease
        elif self.nature == 'Quiet':
            spattack = increase
            speed = decrease
        elif self.nature == 'Rash':
            spattack = increase
            spdefense = decrease
        elif self.nature == 'Calm':
            spdefense = increase
            attack = decrease
        elif self.nature == 'Gentle':
            spdefense = increase
            defense = decrease
        elif self.nature == 'Sassy':
            spdefense = increase
            speed = decrease
        elif self.nature == 'Careful':
            spdefense = increase
            spattack = decrease  
        self.nature_mod = [attack,defense,spattack,spdefense,speed]
        placeholder_level = 50
        placeholder_ev = 0
        HP_EV = placeholder_ev
        AT_EV = placeholder_ev
        DF_EV = placeholder_ev
        SA_EV = placeholder_ev
        SD_EV = placeholder_ev
        SP_EV = placeholder_ev
        Level = placeholder_level
        HP_IV = 31
        AT_IV = 31
        DF_IV = 31
        SA_IV = 31
        SD_IV = 31
        SP_IV = 31
        IVs = [AT_IV,DF_IV,SA_IV,SD_IV,SP_IV]
        EVs = [AT_EV,DF_EV,SA_EV,SD_EV,SP_EV]
        HP_final = math.floor(.01*(2*self.base_stats[0] + HP_IV + math.floor(.25*HP_EV))*Level) + Level + 10 
        calced_stats = [HP_final]
        for base_stat in range(1,6):
            stat_change = []
            stat_change = (math.floor(.01*(2*self.base_stats[base_stat] + IVs[base_stat] + math.floor(.25*EVs[base_stat]))*Level) + 5)*self.nature_mod[base_stat]
            calced_stats.append(stat_change)
        return calced_stats

    def show_mon(self):
        print(f"Name: {self.name}")
        print("Types:", ", ".join(self.types))
        print("Stats:")
        values = []
        for stat, value in self.stats.items():
            print(f"  {stat}: {value}")
            values.append(value)
        print(f"  base stat total: {np.sum(values)}")
        print(f"  Nature: {self.nature}")
        self.base_stats = values
        return self.base_stats
    

    #Stat change formula 
    #HP = floor(0.01 x (2 x Base + IV + floor(0.25 x EV)) x Level) + Level + 10
    #Other Stats = (floor(0.01 x (2 x Base + IV + floor(0.25 x EV)) x Level) + 5) x Nature