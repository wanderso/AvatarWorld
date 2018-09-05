import enum

class Action_Duration(enum.IntEnum):
    FREE = 1
    MOVE = 2
    STANDARD = 3
    FULL_ROUND = 4

class Turn:
    # By default, a turn consists of any number of free actions, a move action, and a standard action.
    # Actions can be executed in any order.
    # Some free actions can only be done once a turn without resorting to extra effort.
    def __init__(self):
        self.action_order = []
        self.turn_default = {Action_Duration.MOVE:1, Action_Duration.STANDARD:1}

    def insert_action(self, action, index=None):
        if index == None:
            index = len(self.action_order)
        dur = action.get_action_type()
        if dur == Action_Duration.FREE:
            self.action_order.insert(index, action)
        elif dur == Action_Duration.FULL_ROUND:
            if dur in self.turn_default:
                if self.turn_default[dur] > 0:
                    self.turn_default[dur] -= 1
                    self.action_order.insert(index, action)
                else:
                    if (self.turn_default[Action_Duration.MOVE] > 0) and (self.turn_default[Action_Duration.STANDARD] > 0):
                        self.turn_default[Action_Duration.MOVE] -= 1
                        self.turn_default[Action_Duration.STANDARD] -= 1
                        self.action_order.insert(index, action)
                    else:
                        return -1
        else:
            if self.turn_default[dur] > 0:
                self.action_order.insert(index, action)
                self.turn_default[dur] -= 1
            else:
                return -1

    def increase_action(self, action_type, increase=1):
        if action_type not in self.turn_default:
            self.turn_default[action_type] = 0
        self.turn_default[action_type] += increase

    def execute_actions(self):
        for entry in self.action_order:
            entry.execute_action()

class Action:
    def __init__(self, act_val):
        self.action = act_val

    def execute_action(self):
        self.action()

    def get_action_type(self):
        return None

class Free_Action(Action):
    def get_action_type(self):
        return Action_Duration.FREE

class Move_Action(Action):
    def get_action_type(self):
        return Action_Duration.MOVE

class Standard_Action(Action):
    def get_action_type(self):
        return Action_Duration.STANDARD

class Full_Round_Action(Action):
    def get_action_type(self):
        return Action_Duration.FULL_ROUND



if __name__ == "__main__":
    t1 = Turn()
    print(t1.turn_default)

    a_move = Move_Action(None)
    a_std = Standard_Action(None)
    a_rnd = Full_Round_Action(None)
    a_free = Free_Action(None)

    t1.insert_action(a_move)
    t1.insert_action(a_std)
    t1.insert_action(a_free)
    t1.insert_action(a_free)
    print(t1.turn_default)
    print(t1.action_order)