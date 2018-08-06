import modifiers
import points
import value_enums
import defenses
from time import sleep

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
        self.extras_flaws = []
        self.available = True
        self.active = True
        self.natural_power = False
        self.points_in_power = points.Points_In_Power(self.rank, points.Points_Per_Rank.from_int(type(self).points_per_rank_default))

    def calculate_points(self):
        return self.get_points_in_power().get_points_total()

    def get_available(self):
        return self.available

    def get_active(self):
        return self.active

    def get_action(self):
        return self.action

    def get_duration(self):
        return self.duration

    def get_extras_flaws(self):
        return self.extras_flaws

    def get_modifiers(self):
        return self.power_modifiers

    def get_name(self):
        return self.name

    def get_points_in_power(self):
        return self.points_in_power

    def get_power_type(self):
        return self.power_type

    def get_rank(self):
        return self.rank

    def get_range(self):
        return self.range

    def get_points(self):
        return self.get_points_in_power().get_points_total()

    def affects_defense(self,defense):
        return False

    def get_value_in_extras_flaws(self, value):
        return (value in self.extras_flaws)

    def add_value_to_extras_flaws(self, value):
        self.extras_flaws.append(value)

    def remove_value_from_extras_flaws(self, value):
        self.extras_flaws.remove(value)

    def add_pip_to_power(self, pip, pos=True):
        if pos == True:
            self.points_in_power = self.points_in_power + pip
        elif pos == False:
            self.points_in_power = self.points_in_power - pip

    def append_modifier(self, new_modifier):
        self.power_modifiers.append(new_modifier)

    def remove_modifier(self, old_modifier):
        self.power_modifiers.remove(old_modifier)

    def process_modifiers(self):
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
            else:
                entry = possible_modifier_class.get_class_plaintext_name()
                if entry in self.modifiers:
                    if self.modifiers[entry] == "default":
                        self.modifiers[entry] = possible_modifier_class.get_default_value(self)
                    new_modifier = possible_modifier_class(self, self.modifiers[entry])


    def repr_process_range(self, altered_value, default_value, value_list, name_list):
        addl_string = ""
        if altered_value != default_value:
            loop_index = 0
            power_index = None
            default_index = None

            for entry in value_list:
                if altered_value == entry:
                    power_index = entry
                if default_value == entry:
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
                addl_string = "%s " % (name_list[altered_value]) + addl_string
            else:
                addl_string = "%s %d " % (name_list[altered_value], self.modifiers[name_list[power_index]]) + addl_string
        return addl_string


    def repr_process_modifiers(self):
        modifier_lists = {}
        modifier_values = {}
        text_display = {}

        for modifier in self.power_modifiers:
            mod_class = type(modifier).modifier_name
            if mod_class not in modifier_lists:
                modifier_lists[mod_class] = [modifier]
            else:
                modifier_lists[mod_class].append(modifier)

        for mod_type in modifier_lists:
            mod_class = type(modifier_lists[mod_type][0])
            if mod_class.modifier_list_type == True:
                mod_options = mod_class.get_modifier_options()
                mod_plain_text = mod_options.get_plain_text_names_list()
                mod_values = mod_options.get_values_list()
                power_values = [0] * len(mod_plain_text)
                modifier_modifier_values = [[]] * len(mod_plain_text)
                text_values_with_rank = [""] * len(mod_plain_text)
                text_values_without_rank = [""] * len(mod_plain_text)
                for entry in modifier_lists[mod_type]:
                    index = entry.get_power_new_value()
                    rank_val = entry.get_rank()
                    for i in range(0, index+1):
                        if power_values[i] < rank_val:
                            power_values[i] = rank_val
                            text_values_with_rank[i] = entry.represent_modifier_on_sheet_with_rank(self)
                            text_values_without_rank[i] = entry.represent_modifier_on_sheet_without_rank(self)
                for entry in modifier_lists[mod_type]:
                    index = entry.get_power_new_value()
                    modifier_modifier_values[index] = entry.get_modifier_modifiers()
                modifier_values[mod_type] = power_values
                repr_string = ""
                representation_list = []
                index = len(power_values)
                max_power_val = 0
                max_power_index = len(power_values)-1

                print(power_values)
                print(modifier_modifier_values)
                for _ in range(0,len(power_values)):
                    index -= 1
                    if power_values[index] > max_power_val:
                        max_power_val = power_values[index]
                        max_power_index = index
                        if power_values[index] == self.get_rank():
 #                           print (text_values_without_rank[index])
                            representation_list.append(" %s" % (text_values_without_rank[index]))
                        else:
#                            print(text_values_with_rank[index])
                            representation_list.append (" %s" % (text_values_with_rank[index]))
                    elif modifier_modifier_values[index] != modifier_modifier_values[max_power_index]:
                        if power_values[index] == self.get_rank():
                            representation_list.append(" %s" % (text_values_without_rank[index]))
                        else:
                            representation_list.append(" %s" % (text_values_with_rank[index]))
                if mod_class.reverse_text_order == True:
                    representation_list = reversed(representation_list)
                for entry in representation_list:
                    repr_string += entry
                # The bug's in here
            elif mod_class.modifier_list_type == False:
                mod_list = modifier_lists[mod_type]
                rr_pow = mod_class.get_current_power_value(self)
                if (rr_pow == points.Rank_Range(self.get_rank())) and mod_class.flat_modifier == False:
                    repr_string = (" %s" % (mod_list[0].represent_modifier_on_sheet_without_rank(self)))
                    pass
                else:
                    repr_string = (" %s %s" % (mod_list[0].represent_modifier_on_sheet_without_rank(self), rr_pow))


            text_display[mod_type] = repr_string

        return (text_display)

    def get_character_sheet_repr(self):
        return_string = "%s:" % self.get_name()
        addl_string = ""
        """Shadow Hankyū: Subtle 2 Precise Ranged Damage 8, Accurate 8, Affects Corporeal 8, Indirect 4 Limited to (from and to shadows) (37 points)"""

        # The magic happens

        # Set power range

        modifier_strings = self.repr_process_modifiers()

        affects_range = ['Increased Range']
        affects_duration = ['Increased Duration']
        affects_action = ['Increased Action','Sustained']

        before_modifiers = ['Multiattack','Selective','Sleep','Contagious','Accurate','Fades','Subtle','Noticeable']
        after_modifiers = ['Secondary Effect']
        display_power = ['Display Power']

        process_order = [after_modifiers,display_power,affects_range,affects_duration,affects_action,before_modifiers]

        for mod_list in process_order:
            for mod in mod_list:
                if mod == 'Display Power':
                    addl_string = " %s %d" % (type(self).default_plain_text, self.get_rank()) + addl_string
                elif mod in modifier_strings:
                    addl_string = modifier_strings[mod] + addl_string


#        addl_string = self.repr_process_range(self.range, type(self).default_range, value_enums.Power_Range_Names.val_list, value_enums.Power_Range_Names.name_list) + addl_string

#        addl_string = self.repr_process_range(self.duration, type(self).default_duration, value_enums.Power_Duration_Names.val_list, value_enums.Power_Duration_Names.name_list) + addl_string

#        addl_string = self.repr_process_range(self.action, type(self).default_action,
#                                             value_enums.Power_Action_Names.val_list,
#                                             value_enums.Power_Action_Names.name_list) + addl_string

        return_string = return_string + addl_string + " (%d point" % self.get_points()
        if self.points != 1:
            return_string += "s"
        return_string += ")\n"
        return return_string


class Attack(Power):
    points_per_rank_default = 1
    default_range = value_enums.Power_Range.CLOSE
    default_action = value_enums.Power_Action.STANDARD
    default_duration = value_enums.Power_Duration.INSTANT

    default_plain_text = "Damage"
    
    allowed_modifiers = [modifiers.Increased_Range, modifiers.Increased_Duration, modifiers.Increased_Action, modifiers.Multiattack, modifiers.Selective,
                         modifiers.Sleep, modifiers.Contagious, modifiers.Secondary_Effect, modifiers.Accurate, modifiers.Subtle, modifiers.Fades,
                         modifiers.Noticeable]

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
        self.points_in_power = points.Points_In_Power(rank, points.Points_Per_Rank.from_int(type(self).points_per_rank_default))
        
        self.process_modifiers()

    def dictify(self):
        return {
                "attack_skill": self.attack_skill,
                "rank" : self.rank,
                "defense": self.defense,
                "resistance": self.resistance,
                "recovery": self.recovery,
                "modifiers": self.modifiers,
                "points": self.points,
                "base_power_points": self.base_power_points,
                "points_per_rank": self.points,
                "points_in_power": self.points_in_power
                }

    def get_skill(self):
        return self.attack_skill

    def get_defense(self):
        return self.defense

    def get_resistance(self):
        return self.resistance

    def get_recovery(self):
        return self.recovery

class Protection(Power):
    points_per_rank_default = 1
    default_range = value_enums.Power_Range.PERSONAL
    default_action = value_enums.Power_Action.NONE
    default_duration = value_enums.Power_Duration.PERMANENT

    default_plain_text = "Protection"

    allowed_modifiers = [modifiers.Sustained]

    def __init__(self, name, rank, modifier_values={}):
        super().__init__(name, "Protection")
        self.rank = rank
        self.points = rank
        self.points_per_rank = 1.0
        self.modifiers = modifier_values
        self.points_in_power = points.Points_In_Power(rank, points.Points_Per_Rank.from_int(type(self).points_per_rank_default))
        self.process_modifiers()

    def get_rank(self):
        return self.rank

    def get_active(self):
        if self.duration == value_enums.Power_Duration.PERMANENT:
            return True
        elif self.duration == value_enums.Power_Duration.SUSTAINED:
            return True

    def affects_defense(self,defense):
        if defense != defenses.Toughness:
            return False
        else:
            return self.rank
