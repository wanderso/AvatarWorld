import ability

class Defense:
    associated_ability = None
    associated_pl_cap = []
    defense_list = {}
    defense_name = None

class Initiative(Defense):
    associated_ability = ability.Agility
    defense_name = "Initiative"

class Dodge(Defense):
    associated_ability = ability.Agility
    defense_name = "Dodge"

class Parry(Defense):
    associated_ability = ability.Fighting
    defense_name = "Parry"

class Toughness(Defense):
    associated_ability = ability.Stamina
    defense_name = "Toughness"

class Fortitude(Defense):
    associated_ability = ability.Stamina
    defense_name = "Fortitude"

class Will(Defense):
    associated_ability = ability.Awareness
    defense_name = "Will"

Dodge.associated_pl_cap = [Toughness]
Parry.associated_pl_cap = [Toughness]
Toughness.associated_pl_cap = [Dodge, Parry]
Fortitude.associated_pl_cap = [Will]
Will.associated_pl_cap = [Fortitude]


Defense.defense_list = {'Initiative':Initiative,
                        'Dodge':Dodge,
                        'Parry':Parry,
                        'Toughness':Toughness,
                        'Fortitude':Fortitude,
                        'Will':Will}
