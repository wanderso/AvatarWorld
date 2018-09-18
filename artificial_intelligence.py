import character
import environment
import enum
import action

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
        weight_current_objective = 0
        current_objective = None
        for obj in self.objectives:
            if obj.get_type() == Objective_Type.DEFEAT_TARGET:
                weight = obj.get_weight()
                if weight > weight_current_objective:
                    current_objective = obj
                    weight_current_objective = obj.get_weight()

        processed_turn = action.Turn()

        if current_objective == None:
            pass
        elif current_objective.type == Objective_Type.DEFEAT_TARGET:
            target_attack = obj.objective_target
            use_attack = self.get_best_attack(target_attack)
            act = use_attack.create_action()

            execute_data = powers.Power_Execution_Data({"Self": self.chara, "Target": target_attack})

            act.set_action(use_attack)
            act.set_data(execute_data)
            
            processed_turn.insert_action(act,0)
        
            
        return processed_turn


    def get_best_attack(self, target):
        power_list = self.chara.get_powers()
        attack_list = []
        for fact in self.factums:
            pass

        for power in power_list:
            if power.get_power_type() == "Attack":
                attack_list.append(power)

        for attack in attack_list:
            print(attack)

        if len(attack_list) == 0:
            return None
        else:
            return attack_list[0]





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
