import random
import powers
import skills
import ability
import defenses
#https://pastebin.com/azrdkPdB blorp

class Dice:
    @staticmethod
    def d20():
        return random.randint(1, 20)

    @staticmethod
    def d10():
        return random.randint(1, 10)

    @staticmethod
    def d4():
        return random.randint(1, 4)

    @staticmethod
    def ndn(n, m):
        ret_val = 0
        for _ in range(n):
            ret_val += random.randint(1,m)
        return ret_val


class Condition:
    def __init__(self, condition_name, recovery):
        self.name = condition_name
        self.recovery = recovery


class Character:
    def __init__(self, name):
        self.name = name
        self.minion = False

        self.dodge_ranks = 0
        self.parry_ranks = 0
        self.fortitude_ranks = 0
        self.will_ranks = 0

        self.initiative = 0
        self.dodge = 0
        self.parry = 0
        self.toughness = 0
        self.fortitude = 0
        self.will = 0

        self.bruise = 0
        self.stamina = 0
        self.wounds = 0

        self.pl = 0
        self.exp = 0
        self.spent_points = 0

        self.max_stamina = 0
        self.max_wounds = 0

        self.abilities = {}

        self.skills = {}
        self.skill_ranks = {}

        self.advantages_natural = {}

        self.advantages = {}

        self.powers = {}
        self.attacks = {}

        self.conditions = []

    def set_pl(self, pl):
        self.pl = pl

    def set_dodge_ranks(self, value):
        self.dodge_ranks = value

    def set_parry_ranks(self, value):
        self.parry_ranks = value

    def set_fortitude_ranks(self, value):
        self.fortitude_ranks = value

    def set_will_ranks(self, value):
        self.will_ranks = value


    def generate_defenses(self, update=[defenses.Initiative, defenses.Dodge, defenses.Parry, defenses.Toughness, defenses.Fortitude, defenses.Will]):
        for entry in update:
            update_value = 0
            if entry == defenses.Dodge:
                update_value = self.dodge_ranks
            elif entry == defenses.Parry:
                update_value = self.parry_ranks
            elif entry == defenses.Fortitude:
                update_value = self.fortitude_ranks
            elif entry == defenses.Will:
                update_value = self.will_ranks
            value_ability_name = entry.associated_ability.ability_name
            if value_ability_name in self.abilities:
                update_value += self.abilities[value_ability_name]
            for power in powers:
                if power.power_type == "Enhanced Defenses":
                    if entry.defense_name in power.abilities:
                        update_value += power.abilities[entry.defense_name]
                        # TODO: Check if power is active!
                elif power.power_type == "Protection":
                    if entry.defense_name == "Toughness":
                        update_value += power.rank
            if entry == defenses.Dodge:
                self.dodge = update_value
            elif entry == defenses.Parry:
                self.parry = update_value
            elif entry == defenses.Fortitude:
                self.fortitude = update_value
            elif entry == defenses.Will:
                self.will = update_value
            elif entry == defenses.Toughness:
                self.toughness = update_value
            elif entry == defenses.Initiative:
                self.initiative = update_value

    def generate_health_classic(self):
        self.bruise = 0
        self.conditions = []



    def generate_health_light(self):
        self.max_stamina = max(self.get_dodge(),self.get_parry()) + self.pl
        self.max_wounds = self.get_toughness() + self.pl

        self.bruise = 0
        self.conditions = []

        self.stamina = self.max_stamina
        self.wounds = self.max_wounds

    def generate_health_wulin(self):
        self.max_stamina = max(self.get_dodge(),self.get_parry()) * self.pl
        self.max_wounds = 0

        self.stamina = self.max_stamina
        self.wounds = 0

        self.conditions = []

    def generate_health_new(self):
        self.max_stamina = max(self.get_dodge(),self.get_parry()) * self.pl
        self.max_wounds = (self.get_toughness()) * self.pl

        self.wounds = self.max_wounds
        self.stamina = self.max_stamina

        self.conditions = []

    def generate_health_evade(self):
        self.max_stamina = max(self.get_dodge(), self.get_parry()) + self.pl
        self.max_wounds = (self.get_toughness()) * self.pl

        self.wounds = self.max_wounds
        self.stamina = self.max_stamina

        self.conditions = []

    def heal_stamina(self, healval):
        self.stamina += healval
        if self.stamina > self.max_stamina:
            self.stamina = self.max_stamina

    def get_fortitude(self):
        return self.fortitude

    def get_will(self):
        return self.will

    def get_dodge(self):
        return self.dodge

    def get_parry(self):
        return self.parry

    def get_dodge_defense(self):
        return self.dodge + 10

    def get_parry_defense(self):
        return self.parry + 10

    def get_toughness(self):
        return self.toughness

    def add_attack(self, atk):
        nm = atk.get_name()
        sk = atk.get_skill()

        if nm not in self.attacks:
            self.attacks[nm] = atk
        if nm not in self.powers:
            self.powers[nm] = atk
        if sk not in self.skill_ranks:
            self.skill_ranks[sk] = 0
            self.calculate_skill(sk)

    def set_skill_ranks(self, name, value):
        self.skill_ranks[name] = value
        self.calculate_skill(name)

    def set_base_ability(self, ability_name, value):
        self.abilities[ability_name] = value
        for power in self.powers:
            if power.power_type == "Enhanced Ability":
                if ability_name in power.abilities:
                    self.abilities[ability_name] += power.abilities[ability_name]
                # TODO: Check if power is active!

        # set skills!
        if ability_name in ability.Ability.ability_list:
            for entry in ability.Ability.ability_list[ability_name].associated_skills:
                if ":" in entry:
                    for skill_name in self.skills:
                        if skill_name.split(':')[0]+':' == entry:
                            self.calculate_skill(skill_name)
                else:
                    self.calculate_skill(entry)

        # set powers!


    def calculate_skill(self, name):
        skill_val = 0
        if name in self.skill_ranks:
            skill_val += self.skill_ranks[name]
        if name.split(':')[0] in skills.Skill.skill_abilities:
            skill_ability = skills.Skill.skill_abilities[name.split(':')[0]]
            if skill_ability in self.abilities:
                skill_val += self.abilities[skill_ability]
        for power in self.powers:
            if power.power_type == "Enhanced Skill":
                skill_val += power.rank
                ## TODO: Needs to check if power is active!
        self.skills[name] = skill_val

    def roll_toughness(self):
        return Dice.d20() + self.toughness - self.bruise

    def exec_attack_evasion(self, atk_name, atk_target):
        if atk_name not in self.attacks:
            print("Error - invalid attack name. %s does not have attack %s" % (self.name, atk_name))
            return
        atk = self.attacks[atk_name]
        skill = atk.get_skill()
        skill_value = 0
        if skill in self.skills:
            skill_value = self.skills[skill]

        roll = Dice.d20() + skill_value

        hit = False
        dodged = False

        tdv = None # target defense value

        if (callable(atk.defense)):
            tdv = atk.defense(target)
        elif (atk.defense == "Dodge"):
            tdv = atk_target.get_dodge_defense()
        elif (atk.defense == "Parry"):
            tdv = atk_target.get_parry_defense()

        default_target = 10
        if roll >= default_target:
            hit = True

        if hit:
            pass

    def exec_attack_classic(self, atk_name, atk_target):
        if atk_name not in self.attacks:
            print("Error - invalid attack name. %s does not have attack %s" % (self.name, atk_name))
            return
        atk = self.attacks[atk_name]
        skill = atk.get_skill()
        skill_value = 0
        if skill in self.skills:
            skill_value = self.skills[skill]

        roll = Dice.d20() + skill_value

        hit = False

        if (atk.defense == "Dodge"):
            if roll >= atk_target.get_dodge_defense():
                hit = True

        elif (atk.defense == "Parry"):
            if roll >= atk_target.get_parry_defense():
                hit = True

        if hit:
            tough_roll = atk_target.roll_toughness()
            rank = atk.get_rank()
            if (tough_roll >= 15 + rank):
                pass
            elif (tough_roll >= 10 + rank):
                atk_target.bruise += 1
            elif (tough_roll >= 5 + rank):
                atk_target.bruise += 1
                # dazed
            elif (tough_roll >= rank):
                atk_target.bruise += 1
                if "Staggered" not in atk_target.conditions:
                    atk_target.conditions.append("Staggered")
                else:
                    atk_target.conditions.append("Incapacitated")
            else:
                atk_target.conditions.append("Incapacitated")

    def exec_attack_light(self, atk_name, atk_target):
        if atk_name not in self.attacks:
            print("Error - invalid attack name. %s does not have attack %s" % (self.name, atk_name))
            return
        atk = self.attacks[atk_name]
        skill = atk.get_skill()
        skill_value = 0
        if skill in self.skills:
            skill_value = self.skills[skill]

        roll = Dice.d20() + skill_value
        hit = False

        if (atk.defense == "Dodge"):
            if roll >= atk_target.get_dodge_defense():
                hit = True

        elif (atk.defense == "Parry"):
            if roll >= atk_target.get_parry_defense():
                hit = True

        if hit:
            tough_roll = atk_target.roll_toughness()
            rank = atk.get_rank()
            if (tough_roll >= 15 + rank):
                pass
            elif (tough_roll >= 10 + rank):
                atk_target.bruise += 1
            elif (tough_roll >= 5 + rank):
                atk_target.bruise += 1
            elif (tough_roll >= rank):
                atk_target.bruise += 1
                if "Staggered" not in atk_target.conditions:
                    atk_target.conditions.append("Staggered")
                else:
                    atk_target.conditions.append("Incapacitated")
            else:
                atk_target.conditions.append("Incapacitated")

        else:
            self.stamina -= accuracy

    def exec_attack_new(self, atk_name, atk_target):
        if atk_name not in self.attacks:
            print("Error - invalid attack name. %s does not have attack %s" % (self.name, atk_name))
            return
        atk = self.attacks[atk_name]
        skill = atk.get_skill()
        skill_value = 0
        if skill in self.skills:
            skill_value = self.skills[skill]


        roll = Dice.d20() + skill_value

        base_hit = 10
        def_num = base_hit

        defense = atk.get_defense()
        hit = False

        if (defense == "Dodge"):
            if roll >= base_hit:
                hit = True
            def_num = atk_target.get_dodge()

        elif (defense == "Parry"):
            if roll >= base_hit:
                hit = True
            def_num = atk_target.get_parry()



        if hit:
            rank = atk.get_rank()
            resistance = atk.get_resistance()
            atk_dodge = False

            if atk_target.stamina > 0:
                atk_dodge = True

            if atk_dodge:
                atk_target.stamina -= max(0, skill_value)
                atk_target.stamina -= max(0, roll - (def_num))

            else:
                atk_target.wounds -= max(0, int(rank))
                dam = Dice.d20() + rank
                dam -= atk_target.get_toughness()
                atk_target.wounds -= max(0, dam)

                if atk_target.wounds < 0:
                    atk_target.conditions.append("Incapacitated")


    def exec_attack_wulin(self, atk_name, atk_target):

        if atk_name not in self.attacks:
            print("Error - invalid attack name. %s does not have attack %s" % (self.name, atk_name))
            return

        atk = self.attacks[atk_name]
        skill = atk.get_skill()
        skill_value = 0
        if skill in self.skills:
            skill_value = self.skills[skill]


        roll = Dice.d20() + skill_value

        base_hit = 10
        def_num = base_hit

        defense = atk.get_defense()
        hit = False

        if (defense == "Dodge"):
            if roll >= base_hit:
                hit = True
            def_num = atk_target.get_dodge()

        elif (defense == "Parry"):
            if roll >= base_hit:
                hit = True
            def_num = atk_target.get_parry()



        if hit:
            rank = atk.get_rank()
            resistance = atk.get_resistance()
            atk_dodge = False

            if atk_target.stamina > 0:
                atk_dodge = True

            if atk_dodge:
                atk_target.stamina -= max(0, skill_value)
                atk_target.stamina -= max(0, roll - (def_num))

            else:
                atk_target.wounds += rank

                if(callable(resistance)):
                    resistance = resistance(atk_target)
                elif(resistance == "Toughness"):
                    resistance = atk_target.get_toughness()
                elif(resistance == "Fortitude"):
                    resistance = atk_target.get_fortitude()
                elif(resistance == "Will"):
                    resistance = atk_target.get_will()


                toughness_roll = Dice.ndn(12,resistance) - Dice.ndn(1,atk_target.wounds)

                if toughness_roll > rank:
                    pass
                else:
                    atk_target.conditions.append("Incapacitated")

    def print_character_sheet(self):
        return_string = ""
        return_string += ("%s - (PL %d, %d EXP)" % (self.name, self.pl, self.pl*15))
        return_string += "\n\n"
        if self.exp > self.spent_points:
            return_string += "(%d points extra)\n\n" % (self.exp-self.spent_points)
        elif self.exp < self.spent_points:
            return_string += "(%d points over)\n\n" % (self.spent_points-self.exp)
        return_string += "Traits\n\n"
        trait_list = [("STR","Strength"),("STA","Stamina"),("AGL","Agility"),("DEX","Dexterity"),
                      ("FGT","Fighting"),("INT","Intelligence"),("AWE","Awareness"),("PRE","Presence")]

        abil_pts = 0

        for entry in trait_list:
            abil_val = 0
            if entry[1] in self.abilities:
                abil_val = self.abilities[entry[1]]
                abil_pts += abil_val*2
            return_string += ("%s %d (%d points)\n" %(entry[0],abil_val,abil_val*2))

        return_string += "\n(%d points)" % abil_pts

        return_string += "\n\nSkills:\n"

        skill_list = []

        for key in self.skill_ranks:
            skill_list.append(key)

        total_ranks = 0

        for entry in sorted(skill_list):
            return_string += "%s: %d " % (entry, self.skills[entry])
            skill_name = entry.split(":")[0]
            addl_str = ""
            if skill_name in skills.Skill.skill_abilities:
                addl_str += "("
                ability_name = skills.Skill.skill_abilities[skill_name]
                ability_val = 0
                if ability_name in self.abilities:
                    ability_val = self.abilities[ability_name]
                if ability_val > 0:
                    addl_str += "+"
                for tup in trait_list:
                    if tup[1] == ability_name:
                        addl_str += "%d %s)" %(ability_val,tup[0])
            addl_str += " + (%d ranks)" % self.skill_ranks[entry]
            total_ranks += self.skill_ranks[entry]
            addl_str += "\n"

            return_string += addl_str

        if total_ranks%2 == 0:
            return_string += "\n(%d points)" % (total_ranks/2)
        else:
            return_string += "\n(%d.5 points)" % (total_ranks / 2)

        return_string += "\n\nAdvantages:\n"

        adv_pts = 0

        for entry in self.advantages_natural:
            pass

        return return_string

        """
Advantages:
Attractive, Benefit 6 (Wealth 4, OmniForce Clearance 2), Defensive Roll 2, Equipment 30
(39 points)
 
Equipment: 
PixNet Camera and Communications System (Linked Commlink, Video Recorder, Night-Vision Goggles, Mini-Tracer) (5 points of Equipment)

Armor: 
OmniCorp Special Operations Infiltration 'Wraith' Suit: (3 points of Equipment)
	Textured Light Combat Mycofibers (Blade/Bullet Resistant): Subtle Protection 2 (3 points) 

Weapons: 
OmniCorp Polycarbonate Weighted Quarterstaff: 
	Strength-Based Damage 4, Reach 1 (5 points of Equipment)	

Utility Belt: (45 points of Equipment)

Vehicles: (82 points total)
CR-15 'Chariot' VTOL Gunship - (81 points)

Gargantuan, Strength 9, Toughness 12, Dodge/Parry 6 (-4 size penalty) Flight 8 (16 points)

Vehicle Armor and Features: (31 points total)
RCS Cross Section Reduction: Concealment (Radio) (2 points)
Comms Network: Communications 3 (Radio), Onboard Computer System (13 points)
Autopilot and Gunnery Computer: Autopilot 1, Enhanced Vehicles 4, Enhanced Ranged Combat: Vehicle-Mounted Weapons 4, Enhanced Advantages: Move-By Attack (6 points)
Radar Dish: Senses 5 (Accurate Radio, Extended Range), Enhanced Perception 6, Skill Mastery: Perception (9 points)

Vehicle-Mounted Weapons: (34 point array)
Missile Pod: Unreliable (Limited Use) Ranged Burst Area 2 Damage 8 (32 points)
Tankbuster: Unreliable (Limited Use) Nullify Protection 8 Alternate Resistance (Impervious Toughness) Accurate 1 Homing 2 Linked to Ranged Damage 8 Accurate 1 Homing 2 (32 points - 1 point for alternate effect)
Light HEAT Cannon: Ranged Multiattack Penetrating Damage 8 (32 points)

Damage-Proof Luxury Cognoscenti - (81 points - 1 point for Alternate Vehicle)
Large, Strength 7, Toughness 16, Dodge/Parry 10 (0 size penalty), Speed 6 (21 points)

Vehicle Armor and Features: (30 points)
Damage-Proof: Impervious Toughness 16 (16 points)
Luxe: Luxury 3 (Extreme), Alarm 3, Bulletproof Tires 2 (Toughness 13), Navigation System (9 points)
Kelvi Integrated Tracking Technology: Autopilot 1, Communications, Onboard Computer System, Remote Control, Enhanced Vehicle-Mounted Weapons 2 (5 points)

Vehicle-Mounted Tools: (30 points)
Light HEAT Turret: Ranged Penetrating Damage 8 (24 points)
Riot Control Cannon: Ranged Multiattack Damage 8 (24 points - 1 point for Alternate Effect)
Electrobarrier: Reaction (to touching Vehicle) Close Damage 6 (24 points - 1 point for Alternate Effect)
Pursuit Mode: (24 points of Linked Powers - 1 point for Alternate Effect)
	Afterburner and Power Slide: Enhanced Strength 2 (total 9), Enhanced Speed 2 (total 8), Enhanced Vehicles 4 (6 points)
	Pursuit Weaponry: (18 point Array)
		Immobilizer: Ranged Damage 8 Homing 1 (17 points)
		Grappling Line: Move Object 8 Accurate 1 (17 points - 1 point for alternate effect)
Stealth Mode: (24 points of Linked Powers - 1 point for Alternate Effect)
	Run Silent: Blending Concealment 6 (Audio: All Frequencies, Vision: Infrared, Radio: Radar, Olfactory: Exhaust) (6 points)
	Polymorphic Smart Tires: Movement 2 (Sure-Footed, Trackless) (4 points)
	Optical Camouflage Texture: Environment 1 (Visibility -5), Partial Concealment 4 (Vision: All Frequencies) (6 points)
	Diamond in the Rough: Enhanced Deception 12 (Limited to Disguise), Enhanced Stealth 6, Skill Mastery: Deception, Stealth (8 points) 
EMP: Unreliable (Limited Use) Close Burst Area 2 (120 ft) Affects Objects Affliction 8 (Impaired/Disabled/Incapacitated) Alternate Resistance (Technology Check) Limited to (Use on Machines) (24 points - 1 point for Alternate Effect)
Tankbuster Missile: Unreliable (Limited Use) Nullify Protection 8 Alternate Resistance (Impervious Toughness) Linked to Ranged Damage 8 (24 points - 1 point for alternate effect)

HQ: Wraith's Tower: (Medium Headquarters) (10 points)
Defense System, Fire Suppression System, Computer, Living Space, Library, Garage, Gym, Security System 3

(105/150 points total)


Powers: 
#1 Worshipper: Enhanced Skill: Stealth 2, Luck 1, Senses 1 (Low-Light Vision) (3 points)
(3 points)


 
Defenses:
Initiative: +6 = (+6 AGL)
Dodge: +10 = (+6 AGL) + (4 ranks) 
Parry: +10 = (+4 FGT) + (6 ranks)
Toughness: +6/4/2 = (+2 STA) + (2 Defensive Roll) + (2 from Wraith Suit)
Fortitude: +10 = (+2 STA) + (8 Ranks)
Will: +6 = (+2 AWE) + (4 Ranks)
(22 points)"""




class CharacterGenerators:
    @staticmethod
    def default_char(name, pl, def_focus):
        chara = Character(name)
        chara.set_pl(pl)
        if def_focus == "Defense":
            chara.dodge = int(6*pl/4)
            chara.parry = int(6*pl/4)
            chara.toughness = 2*pl - (chara.dodge)
        elif def_focus == "Toughness":
            chara.toughness = int(6*pl/4)
            chara.dodge = 2*pl - (chara.toughness)
            chara.parry = 2*pl - (chara.toughness)
        elif def_focus == "Balanced":
            chara.toughness = pl
            chara.dodge = pl
            chara.parry = pl

        chara.generate_health_new()
        return chara



def combat_sim(men, cer, iterations, atk_fun, health_fun):

    men_wins = 0
    cer_wins = 0
    init_wins = 0

    total_rounds = 0
    round_dict = {}

    health_fun(men)
    health_fun(cer)

    print("%s Stamina: %d %s Wounds: %d" % (men.name, men.stamina, men.name, men.wounds))
    print("%s Stamina: %d %s Wounds: %d" % (cer.name, cer.stamina, cer.name, cer.wounds))

    men_atk_name = ""
    cer_atk_name = ""

    for key in men.attacks:
        men_atk_name = key

    for key in cer.attacks:
        cer_atk_name = key


    for _ in range(iterations):
        combat_rounds = 0
        while ("Incapacitated" not in men.conditions and "Incapacitated" not in cer.conditions):
            atk_fun(men, men_atk_name, cer)
            atk_fun(cer, cer_atk_name, men)

            combat_rounds += 1

        if ("Incapacitated") in cer.conditions and ("Incapacitated") in men.conditions:
            init_wins += 1
        elif ("Incapacitated") in cer.conditions:
            men_wins += 1
        elif ("Incapacitated") in men.conditions:
            cer_wins += 1

        total_rounds += combat_rounds

        str_rounds = str(combat_rounds)

        if str_rounds in round_dict:
            round_dict[str_rounds] += 1
        else:
            round_dict[str_rounds] = 1

        health_fun(men)
        health_fun(cer)

    print("%s wins: %d, %s wins: %d, Draws (init winner): %d" % (men.name, men_wins, cer.name, cer_wins, init_wins))
    print("Average fight length: %f" % (total_rounds/iterations))

def combat_sim_new(atk1, atk2, iterations):

    combat_sim(atk1, atk2, iterations, Character.exec_attack_new, Character.generate_health_new)

def combat_sim_classic(atk1, atk2, iterations):

    combat_sim(atk1, atk2, iterations, Character.exec_attack_classic, Character.generate_health_classic)

def combat_sim_wulin(atk1, atk2, iterations):

    combat_sim(atk1, atk2, iterations, Character.exec_attack_wulin, Character.generate_health_wulin)


def menlo_cer_sim():

    men = CharacterGenerators.default_char("Doctor Menlo", 10, "Defense")
    srk = CharacterGenerators.default_char("Lightning Strike", 10, "Defense")
    cer = CharacterGenerators.default_char("Cerulean", 10, "Toughness")
    mik = CharacterGenerators.default_char("Pendulum", 10, "Toughness")
    ana = CharacterGenerators.default_char("Miss Trial", 10, "Balanced")
    mer = CharacterGenerators.default_char("Metal Knuckle", 10, "Balanced")

    vm = powers.Attack("Voltaic Manipulator", "Ranged Combat: Hypersuit Blasters", 10, "Dodge", Character.get_toughness, Character.get_toughness, modifiers={'Ranged':'default'})
    ef = powers.Attack("Electron Flurry", "Melee Combat: Martial Arts", 10, "Parry", Character.get_toughness, Character.get_toughness)
    mf = powers.Attack("Metal Flow", "Melee Combat: Martial Arts", 10, "Parry", Character.get_toughness, Character.get_toughness)
    sk = powers.Attack("Sack", "Melee Combat: Football", 10, "Parry", Character.get_toughness, Character.get_toughness)
    ij = powers.Attack("Injunction", "Melee Combat: Gavels", 10, "Parry", Character.get_toughness, Character.get_toughness)
    rp = powers.Attack("Rocket Punch", "Ranged Combat: Martial Arts", 10, "Dodge", Character.get_toughness, Character.get_toughness, modifiers={'Ranged':'default'})

    men.set_skill_ranks("Ranged Combat: Hypersuit Blasters", 8)
    srk.set_skill_ranks("Melee Combat: Martial Arts", 10)
    cer.set_skill_ranks("Melee Combat: Martial Arts", 5)
    mik.set_skill_ranks("Melee Combat: Football", 10)
    ana.set_skill_ranks("Melee Combat: Gavels", 10)
    mer.set_skill_ranks("Ranged Combat: Martial Arts", 10)

    men.set_skill_ranks("Acrobatics", 2)
    men.set_skill_ranks("Technology", 10)
    men.set_skill_ranks("Treatment", 10)
    men.set_skill_ranks("Expertise: Science", 10)
    men.set_skill_ranks("Perception", 8)

    men.set_base_ability("Intelligence", 10)
    men.set_base_ability("Awareness", 6)
    men.set_base_ability("Dexterity", 2)
    men.set_base_ability("Agility", -2)
    cer.set_base_ability("Fighting", 5)
    

    men.add_attack(vm)
    srk.add_attack(ef)
    cer.add_attack(mf)
    mik.add_attack(sk)
    ana.add_attack(ij)
    mer.add_attack(rp)

    print("Points in the Voltaic Manipulator attack: %d" % rp.get_points())

    combat_sim_new(cer, men, 10000)
    print(men.print_character_sheet())


def avatar_caus_sim():

    ava_wins = 0
    cau_wins = 0
    init_wins = 0

    ava_pl = 16
    cau_pl = 15

    ava = CharacterGenerators.default_char("Adeltom", ava_pl, "Balanced")
    cau = CharacterGenerators.default_char("Causality", cau_pl, "Defense")

    eb = Attack("Energy Blasts", "Ranged Combat: Energy Blasts", ava_pl, "Dodge", "Toughness", "Toughness")
    ab = Attack("Acausal Burst", "Ranged Combat: Spellcasting", cau_pl, "Dodge", "Toughness", "Toughness")

    ava.set_skill_ranks("Ranged Combat: Energy Blasts", ava_pl)
    cau.set_skill_ranks("Ranged Combat: Spellcasting", cau_pl)

    ava.add_attack(eb)
    cau.add_attack(ab)

    combat_sim_new(cau, ava, 10000)


if __name__ == '__main__':
    menlo_cer_sim()
#    avatar_caus_sim()