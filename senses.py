import enum

class Sense_Type_Designation(enum.Enum):
    VISUAL = 1
    AUDITORY = 2
    OLFACTORY = 3
    TACTILE = 4
    MENTAL = 5
    RADIO = 6

class Sense_Cluster:
    def __init__(self):
        self.senses_total = []
        self.senses_powers = []

    def add_sense(self, sense):
        self.senses_total.append(sense)

    def remove_sense(self, sense):
        self.senses_total.remove(sense)

    def create_default_sense_cluster(self):
        self.visual = Sense(Sense_Type_Designation.VISUAL, "Visual (Ordinary Frequencies)")
        visual_acute = Acute(modifiers={"Flag Type":"Visual","Rank":1})
        self.visual.add_flag(visual_acute)

class Sense:
    def __init__(self, designation, sense_name):
        self.sense_modifiers = []
        self.sense_type = designation
        self.name = sense_name  
        self.sense_flags = []

    def add_flag(self, sense_flag):
        pass

    def remove_flag(self, sense_flag):
        pass


class Sense_Event:
    def __init__(self, type, location):
        self.sense_type = type
        self.location = location

class Sense_Flag:
    flag_name = None
    entire_type_option = False
    has_descriptor = False
    is_ranked = False
    has_upgraded_power = False

    def __init__(self, modifiers = {}):
        self.sense_type = None
        self.rank = 1
        self.process_modifiers(modifiers)

    def process_modifiers(self, mods):
        if "Flag Type" in mods:
            flag_type = mods["Flag Type"]
            if flag_type in Sense_Flag_Description.sense_type_dict.values():
                key_val = next(key for key, value in Sense_Flag_Description.sense_type_dict.items() if value == flag_type)
                self.set_sense_type(key_val)
        if "Rank" in mods:
            rank_val = mods["Rank"]
            self.set_rank(rank_val)

    def set_sense_type(self, typ):
        self.sense_type = typ

    def get_sense_type(self):
        return self.sense_type

    def edit_rank(self, rank_mod=1):
        self.rank += rank_mod

    def set_rank(self, rnk):
        self.rank = rnk

    def get_point_value(self):
        type_of_flag = type(self)
        ret_val = 0
        if type_of_flag.is_ranked == False:
            if type_of_flag.entire_type_option == False:
                ret_val = type_of_flag.ranks_for_value
            else:
                ret_val = type_of_flag.ranks_for_value[self.rank]
        elif type_of_flag.has_upgraded_power == True:
            ret_val = type_of_flag.ranks_for_value[self.rank]
        else:
            ret_val = type_of_flag.ranks_for_value * self.rank
        return ret_val

    def get_flag_representation_no_sense(self):
        type_of_flag = type(self)
        ret_val = ""
        if type_of_flag.is_ranked == False:
            if type_of_flag.entire_type_option == False:
                ret_val = type_of_flag.flag_name
            else:
                if self.rank == 1:
                    ret_val = type_of_flag.flag_name
                else:
                    ret_val = type_of_flag.flag_name + " " + str(type_of_flag.ranks_for_value[self.rank])

        else:
            if self.rank == 1:
                ret_val = type_of_flag.flag_name
            else:
                ret_val = type_of_flag.flag_name + " " + str(self.rank)
        return ret_val

class Accurate(Sense_Flag):
    """Accurate 2 or 4 ranks
An accurate sense can pinpoint something’s exact location.
You can use an accurate sense to target something
in combat. Visual and tactile senses are normally accurate
for humans. Cost is 2 ranks for one sense, 4 for an entire
sense type."""
    flag_name = "Accurate"
    entire_type_option = True
    ranks_for_value = [None,2,4]
    def __init__(self, modifiers={}):
        super().__init__(modifiers)

class Acute(Sense_Flag):
    """Acute 1-2 ranks
You can sense fine details about anything you can detect
with a particular sense, allowing you to distinguish between
and identify different subjects. Visual and auditory
senses are normally acute for humans. Cost is 1 rank for
one sense, 2 for an entire sense type."""
    flag_name = "Acute"
    entire_type_option = True
    ranks_for_value = [None,1, 2]
    def __init__(self, modifiers={}):
        super().__init__(modifiers)

class Analytical(Sense_Flag):
    """Analytical 1-2 ranks
Beyond even acute, you can perceive specific details
about anything you can detect with an analytical sense,
such as chemical composition, exact dimensions or mass,
frequency of sounds and energy wavelengths, and so
forth. You can only apply this effect to an acute sense. Normal
senses are not analytical. Cost is 1 rank for one sense,
2 for an entire sense type."""
    flag_name = "Analytical"
    entire_type_option = True
    ranks_for_value = [None,1, 2]
    def __init__(self, modifiers={}):
        super().__init__(modifiers)

class Awareness(Sense_Flag):
    """Awareness 1 rank
You can sense the use of effects of a particular descriptor
with a successful Perception check (DC 10, with –1 to
your check per 10 feet range). Examples include Cosmic
Awareness, Divine Awareness, Magical Awareness, Mental
Awareness, and so forth. You can apply other Sense effects
to your Awareness to modify it. Choose the sense type for
your Awareness; it is often a mental sense, but doesn’t
have to be. Awareness counts as an “exotic sense” for noticing
effects with the first rank of the Subtle modifier (see
Subtle under Extras for details)."""
    flag_name = "Awareness"
    has_descriptor = True
    ranks_for_value = 1
    def __init__(self, modifiers={}):
        super().__init__(modifiers)


class Communication_Link(Sense_Flag):
    """Communication Link 1 rank
You have a link with a particular individual, chosen when
you acquire this option, who must also have this ability.
The two of you can communicate over any distance like
a use of the Communication effect. Choose a sense type
as a communication medium when you select this option;
mental is common for psychic or empathic links. If you
apply the Dimensional modifier to your Communication
Link, it extends to other dimensions as well (see Dimensional
under Power Modifiers for details)."""
    flag_name = "Communication Link"
    has_descriptor = True
    ranks_for_value = 1
    def __init__(self, modifiers={}):
        super().__init__(modifiers)

class Counters_Concealment(Sense_Flag):
    """Counters Concealment 2 ranks
A sense type with this trait ignores the Concealment effect
of a particular descriptor; you sense the subject of the effect
normally, as if the Concealment wasn’t even there. So
if you have vision that Counters Invisibility, for example,
then invisible beings are visible to you. For 5 ranks, the
sense type ignores all Concealment effects, regardless of
descriptor. Concealed subjects seem slightly “off” to you,
enough to know they are concealed to others. This trait
does not affect concealment provided by opaque objects,
for that, see Penetrates Concealment."""
    flag_name = "Counters Concealment"
    is_ranked = True
    has_upgraded_power = True
    has_descriptor = True
    ranks_for_value = [None, 2,5]
    def __init__(self, modifiers={}):
        super().__init__(modifiers)

class Counters_Illusion(Sense_Flag):
    """Counters Illusion 2 ranks
A sense type with this trait ignores the Illusion effect; you
automatically succeed on your resistance check against the
illusion if it affects your sense type, realizing that it isn’t real."""
    flag_name = "Counters Illusion"
    ranks_for_value = 2
    def __init__(self, modifiers={}):
        super().__init__(modifiers)

class Danger_Sense(Sense_Flag):
    """Danger Sense 1 rank
When you would normally be surprised in combat, make
a Perception check (DC 10): One degree of success means
you’re not surprised, but can’t act during the surprise
round (so you don’t suffer any conditions of being surprised),
while two or more degrees of success means you
are not surprised and may act during the surprise round
(if any). Failure means you are surprised (although, if you
have Uncanny Dodge, you are not vulnerable). The GM
may raise the DC of the Danger Sense check in some circumstances.
Choose a sense type for your Danger Sense.
Sensory effects targeting that sense also affect your Danger
Sense ability and may “blind” it."""
    flag_name = "Danger Sense"
    ranks_for_value = 1
    def __init__(self, modifiers={}):
        super().__init__(modifiers)

class Darkvision(Sense_Flag):
    """Darkvision 2 ranks
You can see in complete darkness as if it were normal daylight;
darkness provides no concealment to your vision.
This is essentially the same as Counters Concealment
(Darkness)."""
    flag_name = "Darkvision"
    ranks_for_value = 2
    def __init__(self, modifiers={}):
        super().__init__(modifiers)
        self.set_sense_type(Sense_Type_Designation.VISUAL)

class Detect(Sense_Flag):
    """Detect 1-2 ranks
You can sense a particular item or effect by touch with a
Perception check. Detect has no range and only indicates
the presence or absence of something (being neither
acute nor accurate). Choose what sense type your Detect
falls under (often mental). For 2 ranks you can detect
things at range (with the normal –1 per 10 feet modifier to
your Perception check)."""
    flag_name = "Detect"
    ranks_for_value = 1
    def __init__(self, modifiers={}):
        super().__init__(modifiers)

class Direction_Sense(Sense_Flag):
    """Direction Sense 1 rank
You always know what direction north lies in and can retrace
your steps through any place you’ve been."""
    flag_name = "Direction Sense"
    ranks_for_value = 1
    def __init__(self, modifiers={}):
        super().__init__(modifiers)

class Distance_Sense(Sense_Flag):
    """Distance Sense 1 rank
You can accurately and automatically judge distances."""
    flag_name = "Distance Sense"
    ranks_for_value = 1
    def __init__(self, modifiers={}):
        super().__init__(modifiers)

class Extended(Sense_Flag):
    """Extended 1 rank
You have a sense that operates at greater than normal
range. Your range with the sense—the distance used
to determine penalties to your Perception check—is increased
by a factor of 10. Each additional time you apply
this option, your range increases by an additional factor
of 10, so 1 rank means you have a –1 to Perception checks
per 100 feet, 2 ranks makes it –1 per 1,000 feet, and so on.
An extended sense may be limited by conditions like the
horizon and physical barriers between you and the subject,
unless it also Penetrates Concealment."""
    flag_name = "Extended"
    ranks_for_value = 1
    is_ranked = True
    def __init__(self, modifiers={}):
        super().__init__(modifiers)

class Infravision(Sense_Flag):
    """Infravision 1 rank
You can see in the infrared portion of the spectrum, allowing
you to see heat patterns. Darkness does not provide
concealment for objects differing in temperature from
their surroundings. If you have the Track effect, you can
track warm creatures by the faint heat trails they leave behind.
The Gamemaster is the final judge on how long the
trail remains visible."""
    flag_name = "Infravision"
    ranks_for_value = 1
    def __init__(self, modifiers={}):
        super().__init__(modifiers)

class Low_Light_Vision(Sense_Flag):
    """Low-Light Vision 1 rank
You ignore circumstance penalties to visual Perception
checks for poor lighting, so long as it is not completely
dark."""
    flag_name = "Low-Light Vision"
    ranks_for_value = 1
    def __init__(self, modifiers={}):
        super().__init__(modifiers)
        self.set_sense_type(Sense_Type_Designation.VISUAL)

class Microscopic_Vision(Sense_Flag):
    """Microscopic Vision 1-4 ranks
You can view extremely small things. You can make Perception
checks to see tiny things nearby. Cost is 1 rank for
dust-sized objects, 2 ranks for cellular-sized, 3 ranks for
DNA and complex molecules, 4 ranks for atomic-sized. The
GM may require an Expertise skill check to understand
and interpret what you see."""
    flag_name = "Microscopic Vision"
    ranks_for_value = 1
    is_ranked = True
    def __init__(self, modifiers={}):
        super().__init__(modifiers)
        self.set_sense_type(Sense_Type_Designation.VISUAL)

class Penetrates_Concealment(Sense_Flag):
    """Penetrates Concealment 4 ranks
A sense with this trait is unaffected by concealment from
obstacles (rather than Concealment effects). So vision that
Penetrates Concealment sees right through opaque objects,
for example, and hearing that Penetrates Concealment
is unaffected by sound-proofing or intervening materials,
and so forth."""
    flag_name = "Penetrates Concealment"
    ranks_for_value = 4
    def __init__(self, modifiers={}):
        super().__init__(modifiers)


class Postcognition(Sense_Flag):
    """Postcognition 4 ranks
Your senses extend into the past, allowing you to perceive
events that took place previously. You can make Perception
checks to pick up on past information in an area or
from a subject. The Gamemaster sets the DC for these
checks based on how obscure and distant in the past the
information is, from DC 15 (for a vague vision that may or
may not be accurate) to DC 30 (for near complete knowledge
of a particular past event as if you were actually present).
Your normal (present-day) senses don’t work while
you’re using Postcognition; your awareness is focused on
the past. Your postcognitive visions last for as long as you
concentrate. Postcognition does not apply to sensory effects
like Mind Reading or any other ability requiring interaction.
Postcognition may be Limited to past events
connected to your own “past lives” or ancestors, reducing
cost to 2 ranks."""
    flag_name = "Postcognition"
    ranks_for_value = 4
    def __init__(self, modifiers={}):
        super().__init__(modifiers)


class Precognition(Sense_Flag):
    """Precognition 4 ranks
Your senses extend into the future, allowing you to perceive
events that may happen. Your precognitive visions
represent possible futures. If circumstances change, then
the vision may not come to pass. When you use this ability,
the Gamemaster chooses what information to impart.
Your visions may be obscure and cryptic, open to interpretation.
The Gamemaster may require appropriate
Perception skill checks for you to pick up on particularly
detailed information, with a DC ranging from 15 to 30
or more. The GM can also activate your Precognition to
impart specific information to you as an adventure hook
or plot device. Your normal (present-day) senses don’t
work while you’re using Precognition; your awareness is
focused on the future. Your precognitive visions last as
long as you concentrate. Precognition does not apply to
sensory effects like Mind Reading or any other ability requiring
interaction."""
    flag_name = "Precognition"
    ranks_for_value = 4
    def __init__(self, modifiers={}):
        super().__init__(modifiers)

class Radio(Sense_Flag):
    """Radio 1 rank
You can “hear” radio frequencies including AM, FM, television,
cellular, police bands, and so forth. This allows you to
pick up on Radio Communication (see the Communication effect).
This is the base sense of the radio sense type.
It’s ranged, radius, and acute by default."""
    flag_name = "Radio"
    ranks_for_value = 1
    def __init__(self, modifiers={}):
        super().__init__(modifiers)
        self.set_sense_type(Sense_Type_Designation.RADIO)

class Radius(Sense_Flag):
    """Radius 1-2 ranks
You can make Perception checks with a radius sense for
any point around you. Subjects behind you cannot use
Stealth to hide from you without some other concealment.
Auditory, olfactory, and tactile senses are normally
radius for humans. Cost is 1 rank for use with one sense, 2
ranks for one sense type."""
    flag_name = "Radius"
    entire_type_option = True
    ranks_for_value = [None, 1, 2]
    def __init__(self, modifiers={}):
        super().__init__(modifiers)

class Ranged(Sense_Flag):
    """Ranged 1 rank
You can use a sense that normally has no range (taste or
touch in humans) to make Perception checks at range,
with the normal –1 per 10 feet modifier. This can be enhanced
with the Extended Sense effect."""
    flag_name = "Ranged"
    ranks_for_value = 1
    def __init__(self, modifiers={}):
        super().__init__(modifiers)

class Rapid(Sense_Flag):
    """Rapid 1 rank
You can read or take in information from a sense faster than
normal: each rank increases your perception speed by a
factor of 10 (x10, x100, etc.) with a single sense, double cost
for an entire sense type. You can use rapid vision to speedread,
pick up on rapid flickering between frames of a film,
watch video replays in fast-forward speeds, and such, rapid
hearing to listen to time-compressed audio “blips,” and so
forth."""
    flag_name = "Rapid"
    ranks_for_value = 1
    is_ranked = True
    def __init__(self, modifiers={}):
        super().__init__(modifiers)

class Time_Sense(Sense_Flag):
    """Time Sense 1 rank
You always know what time it is and can time events as if
you had an accurate stopwatch."""
    flag_name = "Time Sense"
    ranks_for_value = 1
    def __init__(self, modifiers={}):
        super().__init__(modifiers)
        self.set_sense_type(Sense_Type_Designation.MENTAL)

class Tracking(Sense_Flag):
    """Tracking 1 rank
You can follow trails and track using a particular sense. Basic
DC to follow a trail is 10, modified by circumstances,
as the GM sees fit. You move at your speed rank –1 while
tracking. For 2 ranks, you can move at full normal speed
while tracking."""
    flag_name = "Tracking"
    is_ranked = True
    has_upgraded_power = True
    ranks_for_value = [None, 1, 2]
    def __init__(self, modifiers={}):
        super().__init__(modifiers)

class Ultra_Hearing(Sense_Flag):
    """Ultra-Hearing 1 rank
You can hear very high and low frequency sounds, like
dog whistles or ultrasonic signals, including those used
by some remote controls."""
    flag_name = "Ultra-Hearing"
    ranks_for_value = 1
    def __init__(self, modifiers={}):
        super().__init__(modifiers)
        self.set_sense_type(Sense_Type_Designation.AUDITORY)


class Ultravision(Sense_Flag):
    """Ultravision 1 rank
You can see ultraviolet light, allowing you to see normally
at night by the light of the stars or other UV light sources."""
    flag_name = "Ultravision"
    ranks_for_value = 1
    def __init__(self, modifiers={}):
        super().__init__(modifiers)
        self.set_sense_type(Sense_Type_Designation.VISUAL)

class Sense_Flag_Description:
    mods_dict = {"Accurate": Accurate,
                 "Acute": Acute,
                 "Analytical": Analytical,
                 "Awareness": Awareness,
                 "Communication Link": Communication_Link,
                 "Counters Concealment": Counters_Concealment,
                 "Counters Illusion": Counters_Illusion,
                 "Danger Sense": Danger_Sense,
                 "Darkvision": Darkvision,
                 "Detect": Detect,
                 "Direction Sense": Direction_Sense,
                 "Distance Sense": Distance_Sense,
                 "Extended": Extended,
                 "Infravision": Infravision,
                 "Low-Light Vision": Low_Light_Vision,
                 "Microscopic Vision": Microscopic_Vision,
                 "Penetrates Concealment": Penetrates_Concealment,
                 "Postcognition": Postcognition,
                 "Precognition": Precognition,
                 "Radio": Radio,
                 "Radius": Radius,
                 "Ranged": Ranged,
                 "Rapid": Rapid,
                 "Time Sense": Time_Sense,
                 "Tracking": Tracking,
                 "Ultra-Hearing": Ultra_Hearing,
                 "Ultravision": Ultravision}

    sense_type_dict = {Sense_Type_Designation.VISUAL: "Visual",
                       Sense_Type_Designation.AUDITORY: "Auditory",
                       Sense_Type_Designation.OLFACTORY: "Olfactory",
                       Sense_Type_Designation.TACTILE: "Tactile",
                       Sense_Type_Designation.MENTAL: "Mental",
                       Sense_Type_Designation.RADIO: "Radio"}