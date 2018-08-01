import enum


class Power_Duration(enum.IntEnum):
    INSTANT = 1
    CONCENTRATION = 2
    SUSTAINED = 3
    CONTINUOUS = 4
    PERMANENT = 5

class Power_Action(enum.IntEnum):
    STANDARD = 1
    MOVE = 2
    FREE = 3
    REACTION = 4
    NONE = 5

class Power_Type(enum.IntEnum):
    ATTACK = 1
    ENHANCED_ABILITY = 4
    ENHANCED_DEFENSE = 3
    ENHANCED_SKILL = 5
    PROTECTION = 2

class Power_Range(enum.IntEnum):
    PERSONAL = 1
    CLOSE = 2
    RANGED = 3
    PERCEPTION = 4

class Power_Secondary_Effect(enum.IntEnum):
    BASE = 1
    SECONDARY_EFFECT = 2
    TERTIARY_EFFECT = 3
    PERMANENT_EFFECT = 4

class Power_Range_Names:
    name_list = ["","Personal", "Close", "Ranged", "Perception-Ranged"]
    val_list = [0,Power_Range.PERSONAL,Power_Range.CLOSE,Power_Range.RANGED,Power_Range.PERCEPTION]

class Power_Duration_Names:
    name_list = ["","Instant","Concentration","Sustained","Continuous","Permanent"]
    val_list = [0,Power_Duration.INSTANT,Power_Duration.CONCENTRATION,Power_Duration.SUSTAINED,Power_Duration.CONTINUOUS,Power_Duration.PERMANENT]

class Power_Action_Names:
    name_list = ["","Standard","Move","Free","Reaction","None"]
    val_list = [0,Power_Action.STANDARD,Power_Action.MOVE,Power_Action.FREE,Power_Action.REACTION,Power_Action.NONE]

class Power_Secondary_Effect_Names:
    name_list = ["","","Secondary Effect","Tertiary Effect","Permanent Effect"]
    val_list = [0,Power_Secondary_Effect.BASE,Power_Secondary_Effect.SECONDARY_EFFECT,Power_Secondary_Effect.TERTIARY_EFFECT,Power_Secondary_Effect.PERMANENT_EFFECT]
