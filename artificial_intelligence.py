import character
import environment

class Artificial_Intelligence:
    def __init__(self, character, environment):
        self.chara = character
        self.env = environment
        self.factions = []
        self.objectives = []
        self.factums = []

class Faction:
    def __init__(self, faction_modifiers):
        self.name = faction_modifiers['Name']
        self.hostile = []

    def set_hostile(self, faction):
        self.hostile.append(faction)

class Objective:
    def __init__(self, objective_modifiers):
        self.objective_weight = objective_modiifers['Weight']
        self.objective_type = objective_modifiers['Type']


if __name__ == "__main__":
    print("Testing")
