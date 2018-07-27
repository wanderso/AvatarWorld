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
        return_string = "%s: " % self.get_name()
        addl_string = "%s %d" % (type(self).default_plain_text, self.get_rank())
        """Shadow Hankyū: Subtle 2 Precise Ranged Damage 8, Accurate 8, Affects Corporeal 8, Indirect 4 Limited to (from and to shadows) (37 points)"""

        # The magic happens

        # Set power range

        if self.range != type(self).default_range:
            loop_index = 0
            power_index = None
            default_index = None

            value_list = value_enums.Power_Range_Names.val_list
            name_list = value_enums.Power_Range_Names.name_list

            for entry in value_list:
                if self.range == entry:
                    power_index = entry
                if type(self).default_range == entry:
                    default_index = entry
                loop_index += 1

            check_range = None
            if power_index > default_index:
                check_range = range(default_index+1, power_index)
            elif power_index < default_index:
                check_range = range(power_index, default_index)

            expansion_string = ""

            for index in check_range:
                if self.modifiers[name_list[index]] == self.modifiers[name_list[index+1]]:
                    continue
                else:
                    if self.modifiers[name_list[index]] == self.get_rank():
                        expansion_string = expansion_string + "%s " % (name_list[index])
                    else:
                        expansion_string = expansion_string + "%s %d " % (name_list[index], self.modifiers[name_list[index]])

            addl_string = expansion_string + addl_string
            if self.modifiers[name_list[power_index]] == self.get_rank():
                addl_string = "%s " % (name_list[self.range]) + addl_string
            else:
                addl_string = "%s %d " % (name_list[self.range], self.modifiers[name_list[power_index]]) + addl_string

        return_string = return_string + addl_string + " (%d point" % self.get_points()
        if self.points != 1:
            return_string += "s"
        return_string += ")\n"
        return return_string
    
    def get_points_in_power(self):
        return self.points_in_power

class Attack(Power):
    points_per_rank_default = 1
    default_range = value_enums.Power_Range.CLOSE
    default_action = value_enums.Power_Action.STANDARD
    default_duration = value_enums.Power_Duration.INSTANT

    default_plain_text = "Damage"
    
    allowed_modifiers = [modifiers.Increased_Range]

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
        
        for possible_modifier_class in type(self).allowed_modifiers:
            if possible_modifier_class.modifier_list_type == True:
                modifier_base = possible_modifier_class.get_current_power_value(self)
                modops = possible_modifier_class.get_modifier_options()
                val_list = modops.get_values_list()
                text_list = modops.get_plain_text_names_list()
                check_modifiers_for = []
                check_modifier_index = []
                check_modifier_ranks = []
                modifier_index = 0
                max_modifier_index = modifier_index
                for entry in text_list:
                    if entry in self.modifiers:
                        if self.modifiers[entry] == "default":
                            self.modifiers[entry] = possible_modifier_class.get_default_value(self)
                        check_modifiers_for.append(entry)
                        check_modifier_index.append(modifier_index)
                        check_modifier_ranks.append(self.modifiers[entry])
                        if modifier_index > max_modifier_index:
                            max_modifier_index = modifier_index
                    modifier_index += 1
                modifier_index = 0
                for entry in val_list:
                    if entry == modifier_base:
                        break
                    modifier_index += 1

                for val in range(modifier_index+1,max_modifier_index+1):
#                    print("DEADBEEF")
#                    print(val)
                    val_index = val
                    if text_list[val] not in self.modifiers:
                        self.modifiers[text_list[val]] = 0
                    if text_list[val] in self.modifiers:
                        mod_val = self.modifiers[text_list[val]]
                        for ex_val in range(val_index,max_modifier_index+1):
                            if text_list[ex_val] not in self.modifiers:
                                self.modifiers[text_list[ex_val]] = 0
                            ex_name = text_list[ex_val]
                            if ex_name in text_list:
                                ex_rank = self.modifiers[text_list[ex_val]]
                                if mod_val < ex_rank:
                                    self.modifiers[text_list[val]] = ex_rank
                                    mod_val = ex_rank
                        new_modifier = possible_modifier_class(self, mod_val)
                        self.power_modifiers.append(new_modifier)


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
