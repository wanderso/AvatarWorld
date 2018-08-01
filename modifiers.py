import powers
import points
import value_enums

class Modifier_Options:
    def __init__(self, pt_list, val_list):
        self.modifier_plain_text_names = list(pt_list)
        self.modifier_values = list(val_list)

    def get_plaintext_from_value(self, value):
        index = 0
        for entry in self.modifier_values:
            if value == entry:
                return self.modifier_plain_text_names[index]
            index += 1
        return "Plaintext not found for value %s " % repr(value)

    def get_value_from_plaintext(self, plaintext):
        index = 0
        for entry in self.modifier_plain_text_names:
            if plaintext == entry:
                return self.modifier_values[index]
            index += 1
        return "Value not found for plaintext %s " % plaintext

    def get_plain_text_names_list(self):
        return self.modifier_plain_text_names

    def get_values_list(self):
        return self.modifier_values


class Modifier:
    points_per_rank_modifier = None
    modifier_name = None
    modifier_needs_rank = False

    modifier_list_type = False

    modifier_options = None

    def __init__(self, power):
        self.associated_powers = [power]
        self.power_original_value = None
        self.power_new_value = None
        self.modifier_cost = 0
        self.modifier_modifiers = []
        self.applied = False
        self.ppr_modifiers = points.Points_Per_Rank.from_int(type(self).points_per_rank_modifier)
        self.ppr = type(self).points_per_rank_modifier

    def power_single_entry_per_rank_init(self, starting_rank, rank):
        power = self.associated_powers[0]
        self.power_original_value = type(self).get_current_power_value(power)
        self.range_val = points.Rank_Range(rank, starting_rank=starting_rank)
        self.adjust_points = self.adjust_points_per_rank
        self.apply()
        self.power_new_value = type(self).get_current_power_value(power)



    @classmethod
    def get_current_power_value(cls, power):
        pass

    @classmethod
    def get_modifier_options(cls):
        return cls.modifier_options

    @classmethod
    def get_default_value(cls, power):
        return power.get_rank()

    def get_rank_range(self):
        return self.range_val

    def get_starting_rank(self):
        return self.range_val.get_min()

    def get_rank(self):
        return self.range_val.get_max()

    def apply(self):
        if self.applied:
            return
        for power in self.associated_powers:
            self.when_applied(power)
        self.adjust_points()
        self.applied = True

    def remove(self):
        if not self.applied:
            return
        for power in self.associated_powers:
            self.when_removed(power)
        self.adjust_points(pos=False)
        self.applied = False

    def when_applied(self, power):
        pass

    def when_removed(self, power):
        pass

    def when_applied_stored_in_extras(self, power):
        if not power.get_value_in_extras_flaws(self):
            power.add_value_to_extras_flaws(self)

    def when_removed_stored_in_extras(self, power):
        if power.get_value_in_extras_flaws(self):
            power.remove_value_from_extras_flaws(self)

    def adjust_points(self, pos=True):
        pass

    def adjust_points_per_rank(self, pos=True):
        applied_already = (self.applied == True)
        if applied_already:
            remove()
        for power in self.associated_powers:
            pip = power.get_points_in_power()
            rr = self.get_rank_range()
            for entry in rr:
                pip.adjust_ppr_for_range(entry[0],entry[1],self.ppr_modifiers,pos=pos)
        if applied_already:
            apply()

    def apply_modifier_to_modifier(self, modifier):
        pass

    @classmethod
    def get_current_power_value(cls, power):
        pass

    def get_power_original_value(self):
        return self.power_original_value

    def get_power_new_value(self):
        return self.power_new_value

    def represent_modifier_on_sheet_without_rank(self, power):
        retstr = ""
        if type(self).modifier_list_type == True:
            retstr = "%s" % type(self).modifier_options.get_plaintext_from_value(self.power_new_value)
        else:
            retstr = "%s" % type(self).modifier_name
        return retstr

    def represent_modifier_on_sheet_with_rank(self, power):
        retstr = ""
        for mod in self.modifier_modifiers:
            retstr += " %s" % mod.represent_modifier_on_sheet_with_rank(power)
        retstr += "%s" % type(self).modifier_options.get_plaintext_from_value(self.power_new_value)
        if self.get_starting_rank() != 0:
            retstr = "%s %d-%d" % (retstr, self.get_starting_rank(), self.get_rank())
        else:
            retstr = "%s %d" % (retstr, self.get_rank())
        return retstr

    @classmethod
    def get_class_plaintext_name(cls):
        return cls.modifier_name

    @classmethod
    def get_current_power_value(cls, power):
        ret_rank = points.Rank_Range(0, 0)
        for mod in power.get_modifiers():
            if mod.get_class_plaintext_name() == cls.get_class_plaintext_name():
                r = mod.get_rank_range()
                ret_rank += r
        return ret_rank


class Increased_Range(Modifier):
    """Effects have a standard range: personal, close, ranged, or
perception. See Range at the start of this chapter for details.
This modifier increases an effect’s range. Choose one
of the following options. Increasing the range of an effect
from personal to close requires either the Affects Others
or Attack extras (see their descriptions). Making a close effect
into a perception ranged effect requires two applications
of this extra, for +2 cost per rank.
• Ranged: Applied to a close effect, this modifier
makes it a ranged effect.
• Perception: When applied to a ranged effect, this
modifier makes it perception range."""
    points_per_rank_modifier = 1
    modifier_needs_rank = True
    modifier_name = "Increased Range"
    modifier_list_type = True

    modifier_plain_text = value_enums.Power_Range_Names.name_list
    modifier_values = value_enums.Power_Range_Names.val_list

    modifier_options = Modifier_Options(modifier_plain_text,modifier_values)

    def __init__(self, power, rank, starting_rank=0):
        super().__init__(power)
        self.power_single_entry_per_rank_init(starting_rank, rank)

    def when_applied(self, power):
        if power.range < type(self).modifier_values[-1]:
            power.range += 1

    def when_removed(self, power):
        if power.range > type(self).modifier_values[1]:
            power.range -= 1

    @classmethod
    def get_current_power_value(cls, power):
        return power.get_range()






class Increased_Duration(Modifier):
    """Effects have a standard duration: instant, sustained, continuous,
or permanent. See Duration at the start of this
chapter for details. This modifier increases an effect’s duration.
Choose one of the following options:
• Concentration: When applied to an instant duration
effect, this modifier makes it maintainable with concentration,
taking a standard action each turn to do
so. If the effect requires an initial attack check, no additional
attack check is needed to maintain it on a target,
but subsequent rounds of effect also do not benefit
from critical hits. The target is affected on each
of the effect user’s turns, making a normal resistance
check (if any). Once the user stops concentrating for
any reason, the effect ends and the target recovers
normally, including resistance checks to remove ongoing
effects.
• Continuous: When applied to a sustained duration
effect, this modifier makes it continuous"""
    points_per_rank_modifier = 1
    modifier_needs_rank = True
    modifier_name = "Increased Duration"
    modifier_list_type = True

    modifier_plain_text = value_enums.Power_Duration_Names.name_list
    modifier_values = value_enums.Power_Duration_Names.val_list

    modifier_options = Modifier_Options(modifier_plain_text,modifier_values)

    def __init__(self, power, rank, starting_rank=0):
        super().__init__(power)
        self.power_single_entry_per_rank_init(starting_rank, rank)

    def when_applied(self, power):
        if power.duration < type(self).modifier_values[-2]:
            power.duration += 1

    def when_removed(self, power):
        if power.duration < type(self).modifier_values[1]:
            power.duration -= 1

    @classmethod
    def get_current_power_value(cls, power):
        return power.get_duration()


class Secondary_Effect(Modifier):
    """An instant duration effect with this modifier affects the
target once immediately (when the effect is used) and
then once again on the following round, at the end of
the attacker’s turn. The target gets the normal resistance
check against the secondary effect.
Secondary Effects don’t stack, so if you attack a target with
your Secondary Effect on the round after a successful hit,
it doesn’t affect the target twice; it simply delays the second
effect for another round. You can attack the target
with a different effect, however. So, for example, if you hit
a target with a Secondary Damage Effect then, on the following
round, hit with an Affliction, the target suffers both
the Affliction and the Secondary Damage."""
    points_per_rank_modifier = 1
    modifier_needs_rank = True
    modifier_name = "Secondary Effect"
    modifier_list_type = True

    modifier_plain_text = value_enums.Power_Secondary_Effect_Names.name_list
    modifier_values = value_enums.Power_Secondary_Effect_Names.val_list

    modifier_options = Modifier_Options(modifier_plain_text,modifier_values)

    def __init__(self, power, rank, starting_rank=0):
        super().__init__(power)
        self.power_single_entry_per_rank_init(starting_rank, rank)
        modifier_plain_text = value_enums.Power_Range_Names.name_list
        modifier_values = value_enums.Power_Range_Names.val_list

    @classmethod
    def get_current_power_value(cls, power):
        ret_rank = points.Rank_Range(0, 0)
        for mod in power.get_modifiers():
            if mod.get_class_plaintext_name() == cls.get_class_plaintext_name():
                r = mod.get_rank_range()
                ret_rank += r
        return ret_rank

class Increased_Action(Modifier):
    """Using or activating an effect requires a particular amount
of time. See Actions, page 246, for details about the different
types of actions. Modifiers may change the action
needed to use an effect.
• Standard: Using the effect requires a standard action.
• Move: Using the effect requires a move action.
• Free: It requires a free action to use or activate the
effect. Once an effect is activated or deactivated, it
remains so until your next turn. As with all free actions,
the GM may limit the total number of effects a
hero can turn on or off in a turn.
• Reaction: It requires no action to use the effect. It
operates automatically in response to something
else, such as an attack.
• None: It requires no action to use the effect. It is always
active."""
    points_per_rank_modifier = 1
    modifier_needs_rank = True
    modifier_name = "Increased Action"
    modifier_list_type = True

    modifier_plain_text = value_enums.Power_Action_Names.name_list
    modifier_values = value_enums.Power_Action_Names.val_list

    modifier_options = Modifier_Options(modifier_plain_text,modifier_values)

    def __init__(self, power, rank, starting_rank=0):
        super().__init__(power)
        self.power_single_entry_per_rank_init(starting_rank, rank)

    def when_applied(self, power):
        if power.action < type(self).modifier_values[-2]:
            power.action += 1

    def when_removed(self, power):
        if power.action < type(self).modifier_values[1]:
            power.action -= 1

    @classmethod
    def get_current_power_value(cls, power):
        return power.get_action()

class Multiattack(Modifier):
    """A Multiattack effect allows you to hit multiple targets, or a
single target multiple times, in the same standard action.
Multiattack can apply to any effect requiring an attack
check. There are three ways in which a Multiattack effect
can be used:
Single Target
To use a Multiattack against a single target, make your
attack check normally. If successful, increase the attack’s
resistance check DC by +2 for two degrees of success, and
+5 for three or more. This circumstance bonus does not
count against power level limits.
If an Impervious Resistance would ignore the attack before
any increase in the DC, then the attack still has no effect
as usual; a volley of multiple shots is no more likely to
penetrate Impervious Resistance than just one.
Multiple Targets
You can use Multiattack to hit multiple targets at once by
“walking” or “spraying” the Multiattack across an arc. Roll
one attack check per target in the arc. You suffer a penalty
to each check equal to the total number of targets. So
making a Multiattack against five targets is a –5 penalty
to each attack check. If you miss one target, you may still
attempt to hit the others.
Covering Attack
A Multiattack can provide cover for an ally. Take a standard
action and choose an ally in your line of sight, who
receives the benefits of cover against enemies in your
line of sight and in range of your Multiattack. (You have
to be able to shoot at them to get them to keep their
heads down or this maneuver won’t work.) You cannot
lay down a covering attack for an ally in close combat.
An opponent can choose to ignore the cover provided
by your covering attack at the cost of being automatically
attacked by it; make a normal attack check to hit
that opponent."""
    points_per_rank_modifier = 1
    modifier_needs_rank = True
    modifier_name = "Multiattack"

    modifier_list_type = False

    def __init__(self, power, rank, starting_rank=0):
        super().__init__(power)
        self.power_single_entry_per_rank_init(starting_rank, rank)
        self.when_applied = self.when_applied_stored_in_extras
        self.when_removed = self.when_removed_stored_in_extras

class Selective(Modifier):
    """A resistible effect with this extra is discriminating, allowing
you to decide who is and is not affected by it. This is
most useful for area effects (see the Area extra). You must
be able to accurately perceive a target in order to decide
whether or not to affect it. For a degree of selectivity with
non-resistible effects, use the Precise modifier."""
    points_per_rank_modifier = 1
    modifier_needs_rank = True
    modifier_name = "Selective"

    modifier_list_type = False

    def __init__(self, power, rank, starting_rank=0):
        super().__init__(power)
        self.power_single_entry_per_rank_init(starting_rank,rank)
        self.when_applied = self.when_applied_stored_in_extras
        self.when_removed = self.when_removed_stored_in_extras

class Contagious(Modifier):
    """Contagious effects work on both the target and anyone
coming into contact with the target. New targets resist
the effect normally. They also become contagious, and the
effect lingers until all traces of it have been eliminated. A
Contagious effect is also eliminated if its duration expires.
Examples of effects with this extra include “sticky” Afflictions
trapping anyone touching them, disease- or toxinbased
Weaken effects, or even a Nullify effect spreading
from one victim to another."""
    points_per_rank_modifier = 1
    modifier_needs_rank = True
    modifier_name = "Contagious"

    modifier_list_type = False

    def __init__(self, power, rank, starting_rank=0):
        super().__init__(power)
        self.power_single_entry_per_rank_init(starting_rank,rank)
        self.when_applied = self.when_applied_stored_in_extras
        self.when_removed = self.when_removed_stored_in_extras

class Sustained(Modifier):
    """Applied to a permanent duration effect, this modifier makes
it sustained duration, requiring a free action to use (rather
than none, like other permanent effects). The benefit is the
sustained effect can be improved using extra effort, including
using it to perform power stunts. The drawback is the
effect requires a free action each turn to maintain it, and
being unable to do so means the effect shuts off.
Example: The Protection effect is permanent,
meaning it always protects the character, but
concentrating or trying harder does not make the
effect more protective, nor can the character use
it for power stunts. Sustained Protection can be
turned on and off, improved with extra effort, and
used for power stunts. It might represent a power
like a personal force field, or increased density requiring
a modicum of concentration to maintain."""
    points_per_rank_modifier = 0
    modifier_needs_rank = True
    modifier_name = "Sustained"

    modifier_list_type = False

    def __init__(self, power, rank, starting_rank=0):
        super().__init__(power)
        self.power_single_entry_per_rank_init(starting_rank,rank)

    def when_applied(self, power):
        self.when_applied_stored_in_extras(power)
        if power.duration == value_enums.Power_Duration.PERMANENT:
            power.duration = value_enums.Power_Duration.SUSTAINED

    def when_removed(self, power):
        self.when_removed_stored_in_extras(power)
        if power.duration == value_enums.Power_Duration.SUSTAINED:
            power.duration = value_enums.Power_Duration.PERMANENT

class Sleep(Modifier):
    """When this modifier is applied to an effect that causes the
incapacitated condition, the effect leaves them asleep
whenever it would normally render them incapacitated.
See the description of asleep under Conditions."""
    points_per_rank_modifier = 0
    modifier_needs_rank = True
    modifier_name = "Sleep"

    modifier_list_type = False

    def __init__(self, power, rank, starting_rank=0):
        super().__init__(power)
        self.power_single_entry_per_rank_init(starting_rank, rank)

    def when_applied(self, power):
        self.when_applied_stored_in_extras(power)

    def when_removed(self, power):
        self.when_removed_stored_in_extras(power)

extras = """Accurate 1 flat per rank +2 attack check bonus per rank
Affects Corporeal 1 flat per rank Effect works on corporeal beings with rank equal to extra rank.
Affects Insubstantial 1-2 flat points Effect works on insubstantial beings at half (1 rank) or full (2 ranks) effect.
Affects Objects +0-1 per rank Fortitude resisted effect works on objects.
Affects Others +0-1 per rank Personal effect works on others.
Alternate Effect 1-2 flat points Substitute one effect for another in a power.
Alternate Resistance +0-1 per rank Effect uses a different resistance.
Area +1 per rank Effect works on an area.
Attack +0 per rank Personal effect works on others as an attack.
XXX Contagious +1 per rank Effect works on anyone coming into contact with its target. XXX
Dimensional 1-3 flat points Effect works on targets in other dimensions.
Extended Range 1 flat per rank Doubles ranged effect’s distances per rank.
Feature 1 flat per rank Adds a minor capability or benefit to an effect.
Homing 1 flat per rank Attack effect gains additional chances to hit.
Impervious +1 per rank Resistance ignores effects with difficulty modifier of half extra rank or less.
XXX Increased Duration +1 per rank Improves effect’s duration. XXX
Increased Mass 1 flat per rank Effect can carry a greater amount of mass.
XXX Increased Range +1 per rank Improves effect’s range. XXX
Incurable 1 flat point Effect cannot be countered or removed using Healing or Regeneration.
Indirect 1 flat per rank Effect can originate from a point other than the user.
Innate 1 flat point Effect cannot be Nullified.
Insidious 1 flat point Result of the effect is more difficult to detect.
Linked 0 flat points Two or more effects work together as one.
XXX Multiattack +1 per rank Effect can hit multiple targets or a single target multiple times. XXX
Penetrating 1 flat per rank Effect overcomes Impervious Resistance.
Precise 1 flat point Effect can perform delicate and precise tasks.
Reach 1 flat per rank Extend effect’s reach by 5 feet per rank.
XXX Reaction +1 or 3 per rank Changes effect’s required action to reaction. XXX
Reversible 1 flat point Effect can be removed at will as a free action.
Ricochet 1 flat per rank Attacker can bounce effect to change direction.
Secondary Effect +1 per rank Instant effect works on the target twice.
XXX Selective +1 per rank Resistible effect works only on the targets you choose. XXX
XXX Sleep +0 per rank Effect leaves targets asleep rather than incapacitated. XXX
Split 1 flat per rank Effect can split into multiple, smaller, effects.
Subtle 1-2 flat points Effect is less noticeable (1 point) or not noticeable (2 points).
XXX Sustained +0 per rank Makes a permanent effect sustained. XXX
Triggered 1 flat per rank Effect can be set for later activation.
Variable Descriptor 1-2 flat points Effect can change descriptors"""

flaws = """Activation –1-2 flat points Effect requires a move (1 point) or standard (2 points) action to activate.
Check Required –1 flat per rank Must succeed on a check to use effect.
Concentration –1 per rank Sustained effect becomes concentration duration.
Diminished Range –1 flat per rank Reduces short, medium, and long ranges for the effect.
Distracting –1 per rank Vulnerable while using effect.
Fades –1 per rank Effect loses 1 rank each time it is used.
Feedback –1 per rank Suffer damage when your effect’s manifestation is damaged.
Grab-Based –1 per rank Effect requires a successful grab attack to use.
Increased Action –1-3 per rank Increases action required to use effect.
Limited –1 per rank Effect loses about half its effectiveness.
Noticeable –1 flat point Continuous or permanent effect is noticeable.
Permanent –1 per rank Effect cannot be turned off or improved with extra effort.
Quirk –1 flat per rank A minor flaw attached to an effect. The opposite of a Feature.
Reduced Range –1-2 per rank Effect’s range decreases.
Removable –1-2/5 flat points Effect can be taken away from the user.
Resistible –1 per rank Effect gains a resistance check.
Sense-Dependent –1 per rank Target must be able to perceive the effect for it to work.
Side Effect –1-2 per rank Failing to use the effect causes a problematic side effect.
Tiring –1 per rank Effect causes a level of fatigue when used.
Uncontrolled –1 per rank You have no control over the effect.
Unreliable –1 per rank Effect only works about half the time (roll of 11 or more)."""


if __name__ == "__main__":
    for i in range(4,2,-1):
        print(i)