import enum

class Power_Duration(enum.Enum):
    INSTANT = 1
    SUSTAINED = 2
    CONCENTRATION = 3
    CONTINUOUS = 4
    PERMANENT = 5

class Power_Action(enum.Enum):
    STANDARD = 1
    MOVE = 2
    FREE = 3
    REACTION = 4
    NONE = 5

class Power_Type(enum.Enum):
    ATTACK = 1
    ENHANCED_ABILITY = 4
    ENHANCED_DEFENSE = 3
    ENHANCED_SKILL = 5
    PROTECTION = 2


class Power:
    def __init__(self, name, pow_type):
        self.name = name
        self.descriptors = {}
        self.duration = None
        self.action = Power_Action.NONE
        self.power_type = pow_type
        self.points = 0
        self.points_per_rank = 0.0
        self.points_flat = 0
        self.available = True
        self.active = True
        self.natural_power = False

    def get_available(self):
        return self.available

    def get_active(self):
        return self.active

    def get_power_type(self):
        return self.power_type

    def get_name(self):
        return self.name

    def get_points(self):
        return self.points

    def get_character_sheet_repr(self):
        return repr(self)

class Attack(Power):
    def __init__(self, name, skill, rank, defense, resistance, recovery, modifiers={}):
        super().__init__(name, "Attack")
        self.duration = Power_Duration.INSTANT
        self.action = Power_Action.STANDARD
        self.attack_skill = skill
        self.damage_rank = rank
        self.defense = defense
        self.resistance = resistance
        self.recovery = recovery
        self.modifiers = modifiers

        self.points = rank
        self.points_per_rank = 1.0

        if ('Ranged') in modifiers:
            if modifiers['Ranged'] == "default":
                self.modifiers['Ranged'] = rank
                self.points += rank
                self.points_per_rank += 1.0

        if ('Perception-Ranged') in modifiers:
            if modifiers['Perception-Ranged'] == "default":
                self.modifiers['Perception-Ranged'] = rank
                self.points += rank*2
                self.points_per_rank += 2.0

        if ('Multiattack') in modifiers:
            if modifiers['Multiattack'] == "default":
                self.modifiers['Multiattack'] = rank
                self.points += rank
                self.points_per_rank += 1.0

        if ('Selective') in modifiers:
            if modifiers['Selective'] == "default":
                self.modifiers['Selective'] = rank
                self.points += rank
                self.points_per_rank += 1.0

        if ('Reaction') in modifiers:
            if modifiers['Reaction'] == "default":
                self.modifiers['Reaction'] = rank
                self.points += rank*3
                self.points_per_rank += 3.0


    def get_character_sheet_repr(self):
        return_string = "%s: " % self.get_name()
        addl_string = "Damage %d" % self.get_rank()
        """Shadow Hankyū: Subtle 2 Precise Ranged Damage 8, Accurate 8, Affects Corporeal 8, Indirect 4 Limited to (from and to shadows) (37 points)"""

        # The magic happens

        predicate_list = ['Perception-Ranged', 'Ranged', 'Multiattack', 'Reaction', 'Selective']
        for analyze_val in predicate_list:
            if (analyze_val) in self.modifiers:
                if self.modifiers[analyze_val] != self.get_rank():
                    addl_string = ("%s %d" % (analyze_val, self.modifiers[analyze_val])) + addl_string
                else:
                    addl_string = "%s " % analyze_val + addl_string



        return_string = return_string + addl_string + " (%d point" % self.points
        if self.points != 1:
            return_string += "s"
        return_string += ")\n"
        return return_string

    def get_skill(self):
        return self.attack_skill

    def get_rank(self):
        return self.damage_rank

    def get_defense(self):
        return self.defense

    def get_resistance(self):
        return self.resistance

    def get_recovery(self):
        return self.recovery

class Protection(Power):
    def __init__(self, name, rank, modifiers={}):
        super().__init__(name, "Protection")
        self.rank = rank
        self.points = rank
        self.points_per_rank = 1.0
        self.modifiers = modifiers
        self.duration = Power_Duration.PERMANENT
        self.action = Power_Action.NONE

    def get_rank(self):
        return self.rank

    def get_active(self):
        if self.duration == Power_Duration.PERMANENT:
            return True
        elif self.duration == Power_Duration.SUSTAINED:
            return True
            # So long as they've got a free action!


    def get_character_sheet_repr(self):
        return_string = "%s: " % self.get_name()
        addl_string = "Protection %d" % self.get_rank()

        return_string = return_string + addl_string + " (%d point" % self.points
        if self.points != 1:
            return_string += "s"
        return_string += ")\n"
        return return_string
