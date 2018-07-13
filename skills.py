import enum

class Skill_Names(enum):
    ACROBATICS = 1
    ATHLETICS = 2
    CLOSE_COMBAT = 3
    DECEPTION = 4
    EXPERTISE = 5
    INSIGHT = 6
    INTIMIDATION = 7
    INVESTIGATION = 8
    PERCEPTION = 9
    PERSUASION = 10
    RANGED_COMBAT = 11
    SLEIGHT_OF_HAND = 12
    STEALTH = 13
    TECHNOLOGY = 14
    TREATMENT = 15
    VEHICLES = 16

class Skill:
    pass

class Acrobatics(Skill):
    pass

class Athletics(Skill):
    pass

class CloseCombat(Skill):
    pass

class Deception(Skill):
    pass

class Expertise(Skill):
    pass

class Insight(Skill):
    pass

class Intimidation(Skill):
    pass

class Investigation(Skill):
    pass

class Perception(Skill):
    pass

class Persuasion(Skill):
    pass

class RangedCombat(Skill):
    pass

class SleightOfHand(Skill):
    pass

class Stealth(Skill):
    pass

class Technology(Skill):
    pass

class Treatment(Skill):
    pass

class Vehicles(Skill):
    pass

"""Acrobatics Agl No move or free
Athletics Str Yes move
Close Combat Fgt Yes standard
Deception Pre Yes standard
Expertise Int No* —
Insight Awe Yes free
Intimidation Pre Yes standard
Investigation Int No —
Perception Awe Yes free
Persuasion Pre Yes —
Ranged Combat Dex Yes standard
Sleight of Hand Dex No standard
Stealth Agl Yes move
Technology Int No standard
Treatment Int No standard
Vehicles Dex No move"""