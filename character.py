import random
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
        self.dodge = 0
        self.parry = 0
        self.toughness = 0
        self.fortitude = 0
        self.will = 0
        self.bruise = 0
        self.stamina = 0
        self.wounds = 0

        self.pl = 0

        self.max_stamina = 0
        self.max_wounds = 0

        self.skills = {}
        self.attacks = {}
        self.conditions = []
        self.powers = {}

    def set_pl(self, pl):
        self.pl = pl

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

#        self.max_stamina = (max(self.get_dodge()+10,self.get_parry()+10) * self.pl)/2
#        self.max_wounds = ((self.get_toughness()+5) * self.pl)

#        self.max_stamina = 100
#        self.max_wounds = 100

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
        if nm not in self.attacks:
            self.attacks[nm] = atk
        if nm not in self.powers:
            self.powers[nm] = atk

    def set_skill(self, name, value):
        self.skills[name] = value

    def roll_toughness(self):
        return Dice.d20() + self.toughness - self.bruise

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

#        print ("Roll is %d" % roll)

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


class Power:
    def __init__(self, name, pow_type):
        self.name = name
        self.power_type = pow_type
        self.points = 0
        self.points_per_rank = 0.0
        self.points_flat = 0

    def get_power_type(self):
        return self.power_type

    def get_name(self):
        return self.name

    def get_points(self):
        return self.points

class Attack(Power):
    def __init__(self, name, skill, rank, defense, resistance, recovery, modifiers={}):
        super().__init__(name, "Attack")
        self.descriptors = {}
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
                modifiers['Ranged'] = rank
                self.points += rank
                self.points_per_rank += 1.0

        if ('Perception-Ranged') in modifiers:
            if modifiers['Perception-Ranged'] == "default":
                modifiers['Perception-Ranged'] = rank
                self.points += rank*2
                self.points_per_rank += 2.0

        if ('Multiattack') in modifiers:
            if modifiers['Multiattack'] == "default":
                modifiers['Multiattack'] = rank
                self.points += rank
                self.points_per_rank += 1.0


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

    vm = Attack("Voltaic Manipulator", "Ranged Combat: Hypersuit Blasters", 10, "Dodge", Character.get_toughness, "Toughness", modifiers={'Ranged':'default'})
    ef = Attack("Electron Flurry", "Melee Combat: Martial Arts", 10, "Parry", "Toughness", "Toughness")
    mf = Attack("Metal Flow", "Melee Combat: Martial Arts", 10, "Parry", "Toughness", "Toughness")
    sk = Attack("Sack", "Melee Combat: Football", 10, "Parry", "Toughness", "Toughness")
    ij = Attack("Injunction", "Melee Combat: Gavels", 10, "Parry", "Toughness", "Toughness")
    rp = Attack("Rocket Punch", "Ranged Combat: Martial Arts", 10, "Dodge", "Toughness", "Toughness", modifiers={'Ranged':'default'})

    men.set_skill("Ranged Combat: Hypersuit Blasters", 10)
    srk.set_skill("Melee Combat: Martial Arts", 10)
    cer.set_skill("Melee Combat: Martial Arts", 10)
    mik.set_skill("Melee Combat: Football", 10)
    ana.set_skill("Melee Combat: Gavels", 10)
    mer.set_skill("Ranged Combat: Martial Arts", 10)

    men.add_attack(vm)
    srk.add_attack(ef)
    cer.add_attack(mf)
    mik.add_attack(sk)
    ana.add_attack(ij)
    mer.add_attack(rp)

    print("Points in the Voltaic Manipulator attack: %d" % rp.get_points())

    combat_sim_wulin(cer, ana, 10000)


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

    ava.set_skill("Ranged Combat: Energy Blasts", ava_pl)
    cau.set_skill("Ranged Combat: Spellcasting", cau_pl)

    ava.add_attack(eb)
    cau.add_attack(ab)

#    combat_sim_classic(cau, ava, 10000)
    combat_sim_new(cau, ava, 10000)


if __name__ == '__main__':
    menlo_cer_sim()
#    avatar_caus_sim()