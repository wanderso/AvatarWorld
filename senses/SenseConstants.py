import enum


class Sense_Type_Designation(enum.Enum):
    VISUAL = 1
    AUDITORY = 2
    OLFACTORY = 3
    TACTILE = 4
    MENTAL = 5
    RADIO = 6


class Sense_Type_Narrow:
    default_narrow_senses = {Sense_Type_Designation.VISUAL: ["Ordinary Frequencies", "Infravision", "Ultravision"],
                             Sense_Type_Designation.AUDITORY: ["Ordinary Frequencies", "Ultrahearing"],
                             Sense_Type_Designation.OLFACTORY: ["Smell and Taste"],
                             Sense_Type_Designation.TACTILE: ["Touch"],
                             Sense_Type_Designation.MENTAL: ["Ordinary Awareness"],
                             Sense_Type_Designation.RADIO: ["Radio Frequencies"]}


