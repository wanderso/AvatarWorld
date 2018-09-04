import character
import environment
import enum

class Objective_Type(enum.IntEnum):
    NULL_OBJECTIVE = 0
    DEFEAT_TARGET = 1

class Target_Type(enum.IntEnum):
    CHARACTER = 1
    FACTION = 2

class Artificial_Intelligence:
    def __init__(self, character, environment):
        self.chara = character
        self.env = environment
        self.factions = []
        self.objectives = []
        self.factums = []
        self.navigation_graph = []
        self.tasks = []
        self.senses = {}

    def process_turn_decision(self):
        if self.tasks == []:
            return ([], [], [])

    def large_process_turn_decision(self):
        for obj in self.objectives:
            if obj.get_type() == Objective_Type.DEFEAT_TARGET:
                obj.get_weight()

class Faction:
    def __init__(self, faction_modifiers):
        self.name = faction_modifiers['Name']
        self.hostile = []

    def set_hostile(self, faction):
        self.hostile.append(faction)

class Objective:
    def __init__(self, objective_modifiers):
        self.objective_type = Objective_Type.NULL_OBJECTIVE
        self.modifiers = objective_modifiers
        self.process_objective()

    def process_objective(self):
        self.objective_weight = self.objective_modifiers['Weight']
        self.objective_type = self.objective_modifiers['Type']
        if self.objective_type == 'Defeat Target':
            self.objective_type = Objective_Type.DEFEAT_TARGET
        if self.objective_type == Objective_Type.DEFEAT_TARGET:
            self.objective_target = self.objective_modifiers['Target']

    def get_type(self):
        return self.objective_type

    def get_weight(self):
        return self.objective_weight


if __name__ == "__main__":
    print("Testing")
