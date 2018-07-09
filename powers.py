
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


class Protection(Power):
    def __init__(self, name, rank, modifiers={}):
        super().__init__(name, "Protection")
        self.rank = rank
        self.modifiers = modifiers

    def get_rank(self):
        return self.rank