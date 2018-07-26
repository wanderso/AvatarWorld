import modifiers
import points
import value_enums


class Power:
    points_per_rank_default = None
    default_range = None
    default_action = None
    default_duration = None

    def __init__(self, name, pow_type):
        self.name = name
        self.descriptors = {}
        self.duration = type(self).default_duration
        self.action = type(self).default_action
        self.range = type(self).default_range
        self.power_type = pow_type
        self.rank = 1
        self.points = 0
        self.points_flat = 0
        self.power_modifiers = []
        self.available = True
        self.active = True
        self.natural_power = False
        self.points_in_power = None

    def calculate_points(self):
        return self.get_points_in_power().get_points_total()

    def get_available(self):
        return self.available

    def get_active(self):
        return self.active

    def get_power_type(self):
        return self.power_type

    def get_name(self):
        return self.name

    def get_rank(self):
        return self.rank

    def get_range(self):
        return self.range

    def get_points(self):
        return self.get_points_in_power().get_points_total()

    def get_character_sheet_repr(self):
        return repr(self)
    
    def get_points_in_power(self):
        return self.points_in_power

class Attack(Power):
    points_per_rank_default = 1
    default_range = value_enums.Power_Range.CLOSE
    default_action = value_enums.Power_Action.STANDARD
    default_duration = value_enums.Power_Duration.INSTANT

    default_plain_text = "Damage"

    def __init__(self, name, skill, rank, defense, resistance, recovery, modifier_values={}):
        super().__init__(name, "Attack")
        self.attack_skill = skill
        self.rank = rank
        self.defense = defense
        self.resistance = resistance
        self.recovery = recovery
        self.modifiers = modifier_values

        self.points = rank

        self.base_power_points = rank
        
        self.points_per_rank = 1.0

        self.points_per_rank_numerator = 1
        self.points_per_rank_denominator = 1

        self.points_in_power = points.Points_In_Power(rank, points.Points_Per_Rank.from_int(1))

        if ('Ranged') in self.modifiers:
            if self.modifiers['Ranged'] == "default":
                self.modifiers['Ranged'] = rank
            ranged = modifiers.Increased_Range(self, self.modifiers['Ranged'])
            self.power_modifiers.append(ranged)

        if ('Perception-Ranged') in self.modifiers:
            if self.modifiers['Perception-Ranged'] == "default":
                self.modifiers['Perception-Ranged'] = rank
            if 'Ranged' not in self.modifiers:
                self.modifiers['Ranged'] = 0
            if self.modifiers['Ranged'] < self.modifiers['Perception-Ranged']:
                ranged_addl = modifiers.Increased_Range(self, self.modifiers['Perception-Ranged'], starting_rank=self.modifiers['Ranged'])
                self.modifiers['Ranged'] = self.modifiers['Perception-Ranged']
                self.power_modifiers.append(ranged_addl)
            perception_ranged = modifiers.Increased_Range(self, self.modifiers['Perception-Ranged'])
            self.power_modifiers.append(perception_ranged)

        if ('Multiattack') in self.modifiers:
            if self.modifiers['Multiattack'] == "default":
                self.modifiers['Multiattack'] = rank
#                self.adjust_points_per_rank(1)

        if ('Selective') in self.modifiers:
            if self.modifiers['Selective'] == "default":
                self.modifiers['Selective'] = rank
#                self.adjust_points_per_rank(1)

        if ('Reaction') in self.modifiers:
            if self.modifiers['Reaction'] == "default":
                self.modifiers['Reaction'] = rank
#                self.adjust_points_per_rank(3)



    def get_character_sheet_repr(self):
        return_string = "%s: " % self.get_name()
        addl_string = "%s %d" % (type(self).default_plain_text, self.get_rank())
        """Shadow Hankyū: Subtle 2 Precise Ranged Damage 8, Accurate 8, Affects Corporeal 8, Indirect 4 Limited to (from and to shadows) (37 points)"""

        # The magic happens

        # Set power range

        if self.range != type(self).default_range:
            range_expansion = False
            check_range = None
            if self.range < type(self).default_range:
                check_range = range(self.range, self.default_range)
                for entry in check_range:
                    if self.modifiers[value_enums.Power_Range_Names.name_list[entry]] != self.get_rank():
                        range_expansion = True
                    print("DEADBEEF")
                    print(value_enums.Power_Range_Names.name_list[entry])
            else:
                check_range = range(self.range, self.default_range, -1)
                for entry in check_range:
                    if self.modifiers[value_enums.Power_Range_Names.name_list[entry]] != self.get_rank():
                        range_expansion = True
            if range_expansion == True:
                expansion_string = ""
                for entry in check_range:
                    entry_name = value_enums.Power_Range_Names.name_list[entry]
                    expansion_string = expansion_string + "%s %d " % (entry_name, self.modifiers[entry_name])
                addl_string = expansion_string + addl_string
            else:
                addl_string = "%s " % (value_enums.Power_Range_Names.name_list[self.range]) + addl_string

#        predicate_list = ['Ranged', 'Perception-Ranged', 'Multiattack', 'Reaction', 'Selective']
        predicate_list = ['Multiattack', 'Reaction', 'Selective']

        for analyze_val in predicate_list:
            if (analyze_val) in self.modifiers:
                if self.modifiers[analyze_val] != self.get_rank():
                    addl_string = ("%s %d " % (analyze_val, self.modifiers[analyze_val])) + addl_string
                else:
                    addl_string = "%s " % analyze_val + addl_string



        return_string = return_string + addl_string + " (%d point" % self.get_points()
        if self.points != 1:
            return_string += "s"
        return_string += ")\n"
        return return_string

    def get_skill(self):
        return self.attack_skill

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
        self.duration = value_enums.Power_Duration.PERMANENT
        self.action = value_enums.Power_Action.NONE
        self.points_in_power = points.Points_In_Power(rank, points.Points_Per_Rank.from_int(1))

    def get_rank(self):
        return self.rank

    def get_active(self):
        if self.duration == value_enums.Power_Duration.PERMANENT:
            return True
        elif self.duration == value_enums.Power_Duration.SUSTAINED:
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
