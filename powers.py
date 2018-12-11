import modifiers
import points
import value_enums
import senses
import defenses
import action
import character
import enum

"""Power Effects
Name Type Act ion Range Duration Resistance Cost
Affliction Attack Standard Close Instant Fort. or Will 1 per rank
Alternate Form Varies Varies Varies Varies — See description
Blast Attack Standard Ranged Instant Toughness 2 per rank
Burrowing Movement Free Personal Sustained — 1 per rank
Communication Sensory Free Rank Sustained — 4 per rank
Comprehend Sensory None Personal Permanent — 2 per rank
Concealment Sensory Free Personal Sustained — 2 per rank
Create Control Standard Ranged Sustained — 2 per rank
XXX Damage Attack Standard Close Instant Toughness 1 per rank XXX
Dazzle Attack Standard Ranged Instant Fort. or Will 2 per rank
Deflect Defense Standard Ranged Instant — 1 per rank
Duplication Control Standard Close Sustained — 3 per rank
Element Control Control Standard Perception Sustained Strength 2 per rank
Elongation General Free Personal Sustained — 1 per rank
Energy Absorption General Free Personal Sustained — See description
Energy Aura Attack Reaction Close Instant Toughness 4 per rank
Energy Control Attack Standard Ranged Instant Toughness 2 per rank
Enhanced Trait General Free Personal Sustained — As base trait
Environment Control Standard Rank Sustained — 1-2 per rank
Extra Limbs General None Personal Permanent — 1 per rank
Feature General None Personal Permanent — 1 per rank
Flight Movement Free Personal Sustained — 2 per rank
Force Field Defense Free Personal Sustained — 1 per rank
Growth General Free Personal Sustained — 2 per rank
Healing General Standard Close Instant — 2 per rank
Illusion Control Standard Perception Sustained Awareness 1-5 per rank
Immortality Defense None Personal Permanent — 2 per rank
Immunity Defense None Personal Permanent — 1 per rank
Insubstantial General Free Personal Sustained — 5 per rank
Invisibility Sensory Free Personal Sustained — 4 or 8 points
Leaping Movement Free Personal Instant — 1 per rank
Luck Control Control Reaction Perception Instant — 3 per rank
Magic Attack Standard Ranged Instant Toughness 2 per rank
Mental Blast Attack Standard Perception Instant Will 4 per rank
Mimic General Move Personal Sustained — 8 per rank
Mind Control Attack Standard Perception Instant Will 4 per rank
Mind Reading Sensory Standard Perception Sustained Will 2 per rank
Morph General Free Personal Sustained — 5 per rank
Move Object Control Standard Ranged Sustained Strength 2 per rank
Movement Movement Free Personal Sustained — 2 per rank
Nullify Attack Standard Ranged Instant Rank/Will 1 per rank
Power-Lifting General Free Personal Sustained — 1 per rank
Protection Defense None Personal Permanent — 1 per rank
Quickness General Free Personal Sustained — 1 per rank
Regeneration Defense None Personal Permanent — 1 per rank
Remote Sensing Sensory Free Rank Sustained — 1-5 per rank
Senses Sensory None Personal Permanent — 1 per rank
Shapeshift General Move Personal Sustained — 8 per rank
Shrinking General Free Personal Sustained — 2 per rank
Sleep Attack Standard Ranged Instant Fortitude 2 per rank
Snare Attack Standard Ranged Instant Dodge 3 per rank
Speed Movement Free Personal Sustained — 1 per rank
Strike Attack Standard Close Instant Toughness 1 per rank
Suffocation Attack Standard Ranged Instant Fortitude 4 per rank
Summon Control Standard Close Sustained — 2 per rank
Super-Speed See description Free Personal See description — 3 per rank
Swimming Movement Free Personal Sustained — 1 per rank
Teleport Movement Move Rank Instant — 2 per rank
Transform Control Standard Close Sustained — 2-5 per rank
Variable General Standard Personal Sustained — 7 per rank
Weaken Attack Standard Close Instant Fort. or Will 1 per rank"""

class Power_Function_Codes(enum.Enum):
    NO_ACTION = 0
    POWER_FAILED = 1


class Power_Execution_Data:
    def __init__(self, modifiers):
        self.modifiers = modifiers
        self.process_modifiers()

    def process_modifiers(self):
        for key in self.modifiers:
            mod_data = self.modifiers[key]
            if key == "Target":
                self.target = mod_data
            elif key == "Self":
                self.power_user = mod_data

    def __str__(self):
        retstr = ""
        for key in self.modifiers:
            retstr += "'%s': %s, " % (key, str(self.modifiers[key]))
        if len(retstr) != 0:
            retstr = retstr[:-2]
        return "{" + retstr + "}"

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


        self.can_execute_checks = []

        self.before_execution = []

        self.after_execution = []

    def __str__(self):
        return self.get_character_sheet_repr().strip()

    def add_before_execution(self, fun_ptr):
        self.before_execution.append(fun_ptr)

    def remove_before_execution(self, fun_ptr):
        if fun_ptr in self.before_execution:
            self.before_execution.remove(fun_ptr)

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

    def create_action(self):
        act_time = self.get_action()
        ret_action = None
        if act_time == value_enums.Power_Action.STANDARD:
            ret_action = action.Standard_Action()
        elif act_time == value_enums.Power_Action.MOVE:
            ret_action = action.Move_Action()
        elif act_time == value_enums.Power_Action.FREE:
            ret_action = action.Free_Action()
        return ret_action


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
                        possible_modifier_class.process_value_to_modifier_for_power(self, mod_val)
            else:
                entry = possible_modifier_class.get_class_plaintext_name()
                if entry in self.modifiers:
                    possible_modifier_class.process_value_to_modifier_for_power(self,self.modifiers[entry])


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
                last_power_index = []
                for _ in range(0,len(power_values)):
                    index -= 1
                    if power_values[index] > max_power_val:
                        max_power_val = power_values[index]
                        max_power_index = index
                        if power_values[index] == self.get_rank():
                            representation_list.append(" %s" % (text_values_without_rank[index]))
                        else:
                            representation_list.append (" %s" % (text_values_with_rank[index]))
                    elif modifier_modifier_values[index] != last_power_index:
                        if power_values[index] == self.get_rank():
                            representation_list.append(" %s" % (text_values_without_rank[index]))
                        else:
                            representation_list.append(" %s" % (text_values_with_rank[index]))
                    last_power_index = modifier_modifier_values[index]

                if mod_class.reverse_text_order == True:
                    representation_list = reversed(representation_list)
                for entry in representation_list:
                    repr_string += entry
            elif mod_class.modifier_list_type == False:
                mod_list = modifier_lists[mod_type]
                rr_pow = mod_class.get_current_power_value(self)
                if (rr_pow == points.Rank_Range(self.get_rank())) and mod_class.flat_modifier == False:
                    repr_string = (" %s" % (mod_list[0].represent_modifier_on_sheet_without_rank(self)))
                else:
                    repr_string = (" %s %s" % (mod_list[0].represent_modifier_on_sheet_without_rank(self), str(rr_pow)))

            if mod_type not in text_display:
                text_display[mod_type] = [repr_string]
            else:
                text_display[mod_type].append(" " + repr_string)

        return (text_display)

    def get_character_sheet_repr(self):
        return_string = "%s:" % self.get_name()
        addl_string = ""

        modifier_strings = self.repr_process_modifiers()

        total_mods = list(modifiers.Modifier_Description.mods_dict.keys())

        affects_range = ['Increased Range','Reduced Range','Extended Range','Diminished Range']
        affects_duration = ['Increased Duration']
        affects_action = ['Increased Action','Sustained','Decreased Action']

        before_modifiers = ['Multiattack','Selective','Sleep','Contagious','Accurate','Fades','Insidious','Subtle',
                            'Noticeable','Area','Affects Corporeal','Affects Incorporeal','Penetrating','Precise',
                            'Tiring','Impervious','Penetrating','Innate','Activation','Concentration']
        after_modifiers = ['Secondary Effect', 'Affects Others', 'Affects Objects', 'Alternate Resistance',
                           'Check Required','Unreliable','Limited','Split','Triggered','Variable Descriptor',
                           'Reach','Ricochet','Reversible','Side Effect','Uncontrolled','Quirk','Feedback','Grab-Based',
                           'Increased Mass','Homing','Incurable','Indirect','Dimensional','Feature','Distracting',
                           'Resistible','Sense-Dependent']
        display_power = ['Display Power']

        process_order = [after_modifiers,display_power,affects_range,affects_duration,affects_action,before_modifiers]

        for entry in total_mods:
            entry_not_displayed = True
            for lis in process_order:
                if entry in lis:
                    entry_not_displayed = False
            if entry_not_displayed == True:
                print(entry)

        for mod_list in process_order:
            for mod in mod_list:
                if mod == 'Display Power':
                    addl_string = " %s %d" % (type(self).default_plain_text, self.get_rank()) + addl_string
                elif mod in modifier_strings:
                    for value in modifier_strings[mod]:
                        addl_string = value + addl_string

        return_string = return_string + addl_string + " (%d point" % self.get_points()
        if self.points != 1:
            return_string += "s"
        return_string += ")\n"
        return return_string

    def power_available(self, Power_Environment_Data):
        power_available = True

        for fun_ptr in self.can_execute_checks:
            if fun_ptr(Power_Environment_Data) == False:
                power_available = False

        return power_available

    def execute_power(self, Power_Environment_Data):
        if self.power_available(Power_Environment_Data) == False:
            return

        for fun_ptr in self.before_execution:
            ret_code = fun_ptr(Power_Environment_Data)
            if ret_code == Power_Function_Codes.POWER_FAILED:
                return

        self.execute_power_internals(Power_Environment_Data)

        for fun_ptr in self.after_execution:
            fun_ptr(Power_Environment_Data)

    def execute_power_internals(self, Power_Environment_Data):
        pass

    def __call__(self, *args, **kwargs):
        return self.execute_power(*args, **kwargs)


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

    def execute_power_internals(self, Power_Environment_Data):
        print("Executing power %s." % self.name)
        if type(Power_Environment_Data.target) == character.Character:
            power_target = Power_Environment_Data.target
            power_user = Power_Environment_Data.power_user

            self.exec_attack_classic(power_user, power_target, verbose=False)
            
    def exec_attack_classic(self, user, target, verbose=True):
        skill = self.get_skill()
        skill_value = 0

        hit = False

        roll = user.roll_skill(skill)

        if (self.defense == "Dodge") or (self.defense == defenses.Dodge):
            if roll >= target.get_dodge_defense():
                hit = True
        elif (self.defense == "Parry") or (self.defense == defenses.Parry):
            if roll >= target.get_parry_defense():
                hit = True

        if hit:
            tough_roll = target.roll_toughness()
            rank = self.get_rank()
            if (tough_roll >= 15 + rank):
                if verbose:
                    print("No effect")
                pass
            elif (tough_roll >= 10 + rank):
                target.bruise += 1
                if verbose:
                    print("Bruised")
            elif (tough_roll >= 5 + rank):
                target.bruise += 1
                if verbose:
                    print("Dazed")
                # dazed
            elif (tough_roll >= rank):
                target.bruise += 1
                if "Staggered" not in target.conditions:
                    if verbose:
                        print("Staggered")
                    target.conditions.append("Staggered")
                else:
                    target.conditions.append("Incapacitated")
                    if verbose:
                        print("Incapacitated (from Staggered)")
            else:
                target.conditions.append("Incapacitated")
                if verbose:
                    print("Incapacitated")

        else:
            if verbose:
                print("Missed")
                print(roll)


class Protection(Power):
    points_per_rank_default = 1
    default_range = value_enums.Power_Range.PERSONAL
    default_action = value_enums.Power_Action.NONE
    default_duration = value_enums.Power_Duration.PERMANENT

    default_plain_text = "Protection"

    allowed_modifiers = [modifiers.Sustained,modifiers.Impervious]

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

class Senses(Power):
    points_per_rank_default = 1
    default_range = value_enums.Power_Range.PERSONAL
    default_action = value_enums.Power_Action.NONE
    default_duration = value_enums.Power_Duration.PERMANENT

    default_plain_text = "Senses"

    allowed_modifiers = [modifiers.Sustained, modifiers.Impervious, modifiers.Uncontrolled, modifiers.Unreliable]

    def __init__(self, name, rank, modifier_values={}):
        super().__init__(name, "Senses")
        self.rank = rank
        self.points = 0
        self.points_of_senses_max = self.points
        self.points_of_senses_current = 0
        self.points_per_rank = 1.0
        self.sense_flags = []
        self.modifiers = modifier_values
        self.points_in_power = points.Points_In_Power(rank, points.Points_Per_Rank.from_int(
            type(self).points_per_rank_default))
        self.process_modifiers()
        
    def get_points_of_senses_current(self):
        return self.points_of_senses_current

    def add_sense_flag(self, sense_flag):
        self.sense_flags.append(sense_flag)
        self.points_of_senses_current += sense_flag.get_point_value()

    def get_sense_flags(self):
        return self.sense_flags

    def create_sense_flag(self, sense_flag_name, sense_type="Default", rank=1, modifiers = {}):
        if sense_flag_name in senses.Sense_Flag_Description.mods_dict:
            new_flag = senses.Sense_Flag_Description.mods_dict[sense_flag_name]()

    def get_character_sheet_repr(self):
        default_retval = super().get_character_sheet_repr()
        sides = default_retval.split('(')
        left_side = '('.join(sides[:-1])
        right_side = '(' + '('.join(sides[-1:]).rstrip('\n')

        sense_types = {}

        for flag in self.get_sense_flags():
            st = flag.get_sense_type()
            if st == None:
                st = "None"
            if st in sense_types:
                sense_types[st].append(flag)
            else:
                sense_types[st] = [flag]

        flag_text = []
        
        for key in sense_types:
            type_text = key
            if key in senses.Sense_Flag_Description.sense_type_dict:
                type_text = senses.Sense_Flag_Description.sense_type_dict[key]
            key_text = ("%s: " % type_text)
            for entry in sense_types[key]:
                key_text += ("%s, " % entry.get_flag_representation_no_sense())

            key_text = key_text[:-2]
            flag_text.append(key_text)

        final_text = ""

        for entry in flag_text:
            final_text += ("%s, " % entry)

        if final_text != "":
            final_text = final_text[:-2]

        return left_side + "(" + final_text + ") " + right_side

