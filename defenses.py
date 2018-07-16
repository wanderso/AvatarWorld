import ability

class Defense:
    associated_ability = None
    associated_pl_cap = []
    defense_list = {}

class Initiative(Defense):
    associated_ability = ability.Agility

class Dodge(Defense):
    associated_ability = ability.Agility

class Parry(Defense):
    associated_ability = ability.Fighting

class Toughness(Defense):
    associated_ability = ability.Stamina

class Fortitude(Defense):
    associated_ability = ability.Stamina

class Will(Defense):
    associated_ability = ability.Awareness

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
