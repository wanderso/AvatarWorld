import enum
import powers

class Ability_List(enum.Enum):
    STRENGTH = 1
    STAMINA = 2
    AGILITY = 3
    DEXTERITY = 4
    FIGHTING = 5
    INTELLIGENCE = 6
    AWARENESS = 7
    PRESENCE = 8

class Ability:
    ability_list = {}
    associated_skills = []
    associated_defenses = []

    def __init__(self, val):
        self.trait_value = val


class Strength(Ability):
    """Strength:
    Default Melee Attack: 1 point/rank
    Power Lifting: 1 point/rank
    Skill: Athletics: 0.5 point/rank
    TOTAL: 2.5 ppr
    """
    associated_skills = ['Athletics']
    associated_defenses = []


class Stamina(Ability):
    """Stamina:
    Increased Toughness: 1 point/rank
    Increased Fortitude: 1 point/rank
    TOTAL: 2 ppr"""
    associated_skills = []
    associated_defenses = ["Toughness", "Fortitude"]


class Agility(Ability):
    """Agility:
    Increased Inititative: 0.25 point/rank
    Increased Dodge: 1 point/rank
    Skill: Acrobatics: 0.5 point/rank
    Skill: Stealth: 0.5 point/rank
    TOTAL: 2.25 ppr"""
    associated_skills = ['Acrobatics', 'Stealth']
    associated_defenses = ["Initiative", "Dodge"]


class Dexterity(Ability):
    """Dexterity:
    Skill: Ranged Combat: *: 0.5 point/rank
    Skill: Sleight of Hand 0.5 ppr
    Skill: Vehicles 0.5 ppr
    TOTAL: 1.5 ppr"""
    associated_skills = ['Ranged Combat:', 'Sleight of Hand', 'Vehicles']
    associated_defenses = []


class Fighting(Ability):
    """
    Increased Parry: 1 point/rank
    Skill: Melee Combat: *: 0.5 point/rank
    TOTAL: 1.5 ppr
    """
    associated_skills = ['Melee Combat:']
    associated_defenses = ['Parry']


class Intelligence(Ability):
    """
    Skill: Expertise: *: 0.5 point/rank
    Skill: Investigation: *: 0.5 point/rank
    Skill: Technology: *: 0.5 point/rank
    Skill: Treatment: *: 0.5 point/rank
    TOTAL: 2 ppr
    """
    associated_skills = ['Expertise:', 'Investigation', 'Technology', 'Treatment']
    associated_defenses = []

class Awareness(Ability):
    """
    Increased Will: 1 point/rank
    Skill: Insight: *: 0.5 point/rank
    Skill: Perception: *: 0.5 point/rank
    TOTAL: 2 ppr
    """
    associated_skills = ['Insight', 'Perception']
    associated_defenses = ['Will']


class Presence(Ability):
    """
    Skill: Deception: *: 0.5 point/rank
    Skill: Intimidation: *: 0.5 point/rank
    Skill: Persuasion: *: 0.5 point/rank
    TOTAL: 1.5 ppr
    """
    associated_skills = ['Deception', 'Intimidation', 'Persuasion']
    associated_defenses = []


Ability.ability_list = {'Strength':Strength,
                    'Stamina':Stamina,
                    'Agility':Agility,
                    'Dexterity':Dexterity,
                    'Fighting':Fighting,
                    'Intelligence':Intelligence,
                    'Awareness':Awareness,
                    'Presence':Presence}



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