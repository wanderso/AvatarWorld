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
    reverse_text_order = False
    flat_modifier = False
    modifier_list_type = False
    modifier_pyramid_type = False
    modifier_is_flaw = False
    modifier_needs_description = False

    modifier_options = None

    def __init__(self):
        self.linked_to = []
        self.power_original_value = None
        self.power_new_value = None
        self.modifier_modifiers = []

    def set_modifier_rank(self, starting_rank=0, rank=1):
        self.base_modifier = type(self).points_per_rank_modifier
        self.range_val = points.Rank_Range(rank, starting_rank=starting_rank)

        self.points_in_modifier = points.Points_Modifier_Adjuster(rank)
        self.points_in_modifier.adjust_x_for_ranks(self.base_modifier, rank, starting_rank=starting_rank, pos=True)

    def link_modifier_per_rank(self, starting_rank, rank, target):
        is_power = (issubclass(type(target), powers.Power))

        if is_power:
            self.power_original_value = type(self).get_current_power_value(target)

        self.set_modifier_rank(starting_rank=starting_rank,rank=rank)

        self.adjust_points = self.adjust_points_per_rank
        self.apply(target)

        if is_power:
            self.power_new_value = type(self).get_current_power_value(target)

    def link_modifier_flat_with_rank(self, starting_rank, rank, power):
        self.base_modifier = type(self).points_per_rank_modifier
        self.range_val = points.Rank_Range(rank, starting_rank=starting_rank)

        self.power_original_value = type(self).get_current_power_value(power)

        total_p = (self.get_rank()-self.get_starting_rank())

        if type(self).modifier_pyramid_type == True:
            for i in range(self.get_starting_rank(),self.get_rank()):
                total_p += i

        if type(self).modifier_is_flaw:
            total_p = -1 * total_p

        self.flat_points = points.Flat_Points(total_p)

        self.adjust_points = self.adjust_points_for_flat
        self.apply(power)

        self.power_new_value = type(self).get_current_power_value(power)

    def alter_x_modifiers(self, adjustval, rank, starting_rank=0):
        for power in self.linked_to:
            self.remove(power)
            self.points_in_modifier.adjust_x_for_ranks(adjustval, rank, starting_rank=starting_rank, pos=True)
            self.apply(power)

    @classmethod
    def get_current_power_value(cls, power):
        pass

    @classmethod
    def get_modifier_options(cls):
        return cls.modifier_options

    @classmethod
    def get_power_default(cls, power):
        return 0

    @classmethod
    def get_default_value(cls, power):
        if cls.flat_modifier == False:
            return power.get_rank()
        else:
            return 1

    def get_modifier_modifiers(self):
        return self.modifier_modifiers

    def calculate_points(self):
        return self.points_in_modifier.get_points_total()

    def get_linked_to_list(self):
        return self.linked_to

    def get_rank_range(self):
        return self.range_val

    def get_starting_rank(self):
        return self.range_val.get_min()

    def get_rank(self):
        return self.range_val.get_max()

    def apply(self, target):
        if target in self.linked_to:
            return
        if(issubclass(type(target), powers.Power)):
            self.when_applied(target)
            self.adjust_points(target)
        elif (issubclass(type(target), Modifier)):
            lln = list(target.get_linked_to_list())
            self.when_applied_to_modifier(target)
            self.adjust_points_with_modifier(target, pos=True)
        target.append_modifier(self)
        self.linked_to.append(target)

    def remove(self, target):
        if not (target in self.linked_to):
            return
        if (issubclass(type(target), powers.Power)):
            self.when_removed(target)
            self.adjust_points(target, pos=False)
        elif (issubclass(type(target), Modifier)):
            self.when_removed_from_modifier(target)
            self.adjust_points_with_modifier(target, pos=False)
        target.remove_modifier(self)
        self.linked_to.remove(target)

    def when_applied(self, target):
        pass

    def when_removed(self, target):
        pass

    def when_applied_to_modifier(self, target):
        pass

    def when_removed_from_modifier(self, target):
        pass

    def append_modifier(self,target):
        self.modifier_modifiers.append(target)

    def remove_modifier(self,target):
        self.modifier_modifiers.remove(target)

    def when_applied_stored_in_extras(self, power):
        if not power.get_value_in_extras_flaws(self):
            power.add_value_to_extras_flaws(self)

    def when_removed_stored_in_extras(self, power):
        if power.get_value_in_extras_flaws(self):
            power.remove_value_from_extras_flaws(self)

    def adjust_points(self, power, pos=True):
        pass

    def adjust_points_for_flat(self, power, pos=True):
        applied_already = (power in self.linked_to)
        pip = power.get_points_in_power()
        if pos == True:
            pip.add_flat_points(self.flat_points)
        else:
            pip.remove_flat_points(self.flat_points)

    def adjust_points_per_rank(self, power, pos=True):
        power.add_pip_to_power(self.points_in_modifier, pos=pos)

    def adjust_points_with_modifier(self, mod, pos=True):
        # Errors probably in here.
        for target in mod.linked_to:
            if (issubclass(type(target), powers.Power)):
                pip_t = target.get_points_in_power()
                pip_t.points_modifier_adjust_by_y(mod.points_in_modifier,pos=(not pos))
            elif (issubclass(type(target), Modifier)):
                pip_t = target.points_in_modifier
                mod.adjust_points_with_modifier(target, pos=(not pos))
        if (mod.get_rank_range().get_max() < self.get_rank_range().get_max()):
            print("Could be trouble")
        mod.points_in_modifier += self.points_in_modifier
        for target in mod.linked_to:
            if (issubclass(type(target), powers.Power)):
                pip_t = target.get_points_in_power()
                pip_t.points_modifier_adjust_by_y(mod.points_in_modifier,pos=pos)
            elif (issubclass(type(target), Modifier)):
                pip_t = target.points_in_modifier
                mod.adjust_points_with_modifier(target, pos=pos)

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
        modstr = ""
        for mod in self.modifier_modifiers:
            modstr += "%s" % (mod.represent_modifier_on_sheet_without_rank(power))
            rr = mod.get_rank_range()
            if (rr.get_min() != 0) or (rr.get_max() != power.get_rank()) or (len(rr.rank_range) != 1):
                modstr += " %s" % (str(rr))
            modstr += ", "
        if type(self).modifier_list_type == True:
            retstr += "%s" % type(self).modifier_options.get_plaintext_from_value(self.power_new_value)
        else:
            retstr += "%s" % type(self).modifier_name
        if modstr == "":
            pass
        else:
            retstr = "[%s (%s)]" % (retstr, modstr[:-2])
        return retstr

    def represent_modifier_on_sheet_with_rank(self, power):
        retstr = self.represent_modifier_on_sheet_without_rank(power)
        newarray = retstr.split("(")
        retstr = "%s %s" % (newarray[0], self.get_rank_range())
        if len(newarray) != 1:
            for str in newarray[1:]:
                retstr += ("(" + str)
        return retstr

    @classmethod
    def get_class_plaintext_name(cls):
        return cls.modifier_name

    @classmethod
    def get_current_power_value(cls, power):
        if cls.modifier_list_type == True:
            rrs = []
            power_val = cls.get_power_default(power)
            rrpr = points.Rank_Range_With_Points(power.get_rank())
            for mod in power.get_extras_flaws():
                if mod.get_class_plaintext_name() == cls.get_class_plaintext_name():
                    rrs.append(mod.get_rank_range())
            for r in rrs:
                rrpr.add_rank_range(r)
            return power_val + rrpr.return_max_int()
        else:
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
    points_per_rank_modifier = points.Points_Per_Rank_X_Modifier(1)
    modifier_needs_rank = True
    modifier_name = "Increased Range"
    modifier_list_type = True

    modifier_plain_text = value_enums.Power_Range_Names.name_list
    modifier_values = value_enums.Power_Range_Names.val_list

    modifier_options = Modifier_Options(modifier_plain_text,modifier_values)

    def __init__(self, power, rank, starting_rank=0):
        super().__init__()
        self.link_modifier_per_rank(starting_rank, rank, power)

    def when_applied(self, power):
        if power.range < type(self).modifier_values[-1] and power.range > type(self).modifier_values[1]:
            power.range += 1

    def when_removed(self, power):
        if power.range > type(self).modifier_values[1] and power.range > type(self).modifier_values[1]:
            power.range -= 1

    @classmethod
    def get_power_default(cls, power):
        return type(power).default_range

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
    points_per_rank_modifier = points.Points_Per_Rank_X_Modifier(1)
    modifier_needs_rank = True
    modifier_name = "Increased Duration"
    modifier_list_type = True

    modifier_plain_text = value_enums.Power_Duration_Names.name_list
    modifier_values = value_enums.Power_Duration_Names.val_list

    modifier_options = Modifier_Options(modifier_plain_text,modifier_values)

    def __init__(self, power, rank, starting_rank=0):
        super().__init__()
        self.link_modifier_per_rank(starting_rank, rank, power)

    def when_applied(self, power):
        if power.duration < type(self).modifier_values[-2]:
            power.duration += 1

    def when_removed(self, power):
        if power.duration < type(self).modifier_values[1]:
            power.duration -= 1

    @classmethod
    def get_power_default(cls, power):
        return type(power).default_duration

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
    points_per_rank_modifier = points.Points_Per_Rank_X_Modifier(1)
    modifier_needs_rank = True
    modifier_name = "Secondary Effect"
    modifier_list_type = True
    reverse_text_order = True

    modifier_plain_text = value_enums.Power_Secondary_Effect_Names.name_list
    modifier_values = value_enums.Power_Secondary_Effect_Names.val_list

    modifier_options = Modifier_Options(modifier_plain_text,modifier_values)

    def __init__(self, power, rank, starting_rank=0):
        super().__init__()
        self.link_modifier_per_rank(starting_rank, rank, power)

    def when_applied(self, power):
        self.when_applied_stored_in_extras(power)

    def when_removed(self, power):
        self.when_removed_stored_in_extras(power)

    @classmethod
    def get_power_default(cls,power):
        return cls.modifier_options.get_values_list()[1]

    @classmethod
    def get_current_power_value(cls, power):
        rrs = []
        power_val = cls.get_power_default(power)
        rrpr = points.Rank_Range_With_Points(power.get_rank())
        for mod in power.get_extras_flaws():
            if mod.get_class_plaintext_name() == cls.get_class_plaintext_name():
                rrs.append(mod.get_rank_range())
        for r in rrs:
            rrpr.add_rank_range(r)
        return power_val + rrpr.return_max_int()

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
    points_per_rank_modifier = points.Points_Per_Rank_X_Modifier(1)
    modifier_needs_rank = True
    modifier_name = "Increased Action"
    modifier_list_type = True

    modifier_plain_text = value_enums.Power_Action_Names.name_list
    modifier_values = value_enums.Power_Action_Names.val_list

    modifier_options = Modifier_Options(modifier_plain_text,modifier_values)

    def __init__(self, power, rank, starting_rank=0):
        super().__init__()
        self.link_modifier_per_rank(starting_rank, rank, power)

    def when_applied(self, power):
        if power.action < type(self).modifier_values[-2]:
            power.action += 1

    def when_removed(self, power):
        if power.action < type(self).modifier_values[1]:
            power.action -= 1

    @classmethod
    def get_power_default(cls, power):
        return type(power).default_action

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
    points_per_rank_modifier = points.Points_Per_Rank_X_Modifier(1)
    modifier_needs_rank = True
    modifier_name = "Multiattack"

    modifier_list_type = False

    def __init__(self, power, rank, starting_rank=0):
        super().__init__()
        self.link_modifier_per_rank(starting_rank, rank, power)
        self.when_applied = self.when_applied_stored_in_extras
        self.when_removed = self.when_removed_stored_in_extras

class Selective(Modifier):
    """A resistible effect with this extra is discriminating, allowing
you to decide who is and is not affected by it. This is
most useful for area effects (see the Area extra). You must
be able to accurately perceive a target in order to decide
whether or not to affect it. For a degree of selectivity with
non-resistible effects, use the Precise modifier."""
    points_per_rank_modifier = points.Points_Per_Rank_X_Modifier(1)
    modifier_needs_rank = True
    modifier_name = "Selective"

    modifier_list_type = False

    def __init__(self, power, rank, starting_rank=0):
        super().__init__()
        self.link_modifier_per_rank(starting_rank, rank, power)
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
    points_per_rank_modifier = points.Points_Per_Rank_X_Modifier(1)
    modifier_needs_rank = True
    modifier_name = "Contagious"

    modifier_list_type = False

    def __init__(self, power, rank, starting_rank=0):
        super().__init__()
        self.link_modifier_per_rank(starting_rank, rank, power)
        self.when_applied = self.when_applied_stored_in_extras
        self.when_removed = self.when_removed_stored_in_extras

class Fades(Modifier):
    """Each time you use an effect with this flaw, it loses 1 rank
of effectiveness. For effects with a duration longer than
instant, each round is considered “one use.” Once the effect
reaches 0 ranks, it stops working. A faded effect can
be “recovered” in some fashion, such as recharging, rest,
repair, reloading, and so forth. The GM decides when and
how a faded effect recovers, but it should generally occur
outside of combat and take at least an hour’s time. The GM
may allow a hero to recover a faded effect immediately
and completely by spending a hero point."""
    points_per_rank_modifier = points.Points_Per_Rank_X_Modifier(-1)
    modifier_needs_rank = True
    modifier_name = "Fades"

    modifier_list_type = False

    def __init__(self, power, rank, starting_rank=0):
        super().__init__()
        self.link_modifier_per_rank(starting_rank, rank, power)
        self.when_applied = self.when_applied_stored_in_extras
        self.when_removed = self.when_removed_stored_in_extras

class Limited(Modifier):
    """An effect with this flaw is not effective all the time. Limited
powers generally break down into two types: those
usable only in certain situations and those usable only on
certain things. For example Only While Singing Loudly,
Only While Flying, Only on Men (or Women), Only Against
Fire, Not Usable on Yellow Things, and so forth. As a general
rule, the effect must lose about half its usefulness to
qualify for this modifier. Anything less limiting is better
handled as an occasional complication.
Partially Limited
If your effect is only somewhat effective in particular circumstances,
apply the flaw to only some of its ranks. For
example, an attack effect that does less damage against
targets with Protection (to represent a diminished ability
to penetrate armor, for example) applies the Limited flaw
to only those ranks that are ineffective."""
    points_per_rank_modifier = points.Points_Per_Rank_X_Modifier(-1)
    modifier_needs_rank = True
    modifier_name = "Limited"
    modifier_list_type = False
    modifier_needs_description = True

    def __init__(self, power, rank, condition, starting_rank=0):
        super().__init__()
        self.link_modifier_per_rank(starting_rank, rank, power)
        self.process_condition(condition)
        self.when_applied = self.when_applied_stored_in_extras
        self.when_removed = self.when_removed_stored_in_extras

    def process_condition(self, condition):
        self.condition_plain_text = condition.plaintext
        self.condition_check = condition.funct


    class Limited_Condition:
        def __init__(self, init_list):
            self.plaintext = init_list[0]
            self.funct = init_list[1]



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
    points_per_rank_modifier = points.Points_Per_Rank_X_Modifier(0)
    modifier_needs_rank = True
    modifier_name = "Sustained"

    modifier_list_type = False

    def __init__(self, power, rank, starting_rank=0):
        super().__init__()
        self.link_modifier_per_rank(starting_rank, rank, power)

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
    points_per_rank_modifier = points.Points_Per_Rank_X_Modifier(0)
    modifier_needs_rank = True
    modifier_name = "Sleep"

    modifier_list_type = False

    def __init__(self, power, rank, starting_rank=0):
        super().__init__()
        self.link_modifier_per_rank(starting_rank, rank, power)

    def when_applied(self, power):
        self.when_applied_stored_in_extras(power)

    def when_removed(self, power):
        self.when_removed_stored_in_extras(power)

class Affects_Corporeal(Modifier):
    """An incorporeal being can use an effect with this extra on
the corporeal world (see the Insubstantial effect description).
When an effect is used against a corporeal target,
the effect’s rank is equal to the rank of this extra, up to a
maximum of the effect’s full rank. Characters with lower
ranks 1–3 of Insubstantial do not require this extra for
their effects to work on the physical world, although they
can apply it to their Strength rank to allow them to exert
some Strength while Insubstantial."""
    points_per_rank_modifier = points.Points_Flat_Modifier(1)
    modifier_needs_rank = True
    modifier_name = "Affects Corporeal"
    modifier_list_type = False
    flat_modifier = True

    def __init__(self, power, rank, starting_rank=0):
        super().__init__()
        self.link_modifier_flat_with_rank(starting_rank, rank, power)

        def when_applied(self, power):
            self.when_applied_stored_in_extras(power)

        def when_removed(self, power):
            self.when_removed_stored_in_extras(power)

class Affects_Incorporeal(Modifier):
    """An effect with this extra works on insubstantial targets,
in addition to having its normal effect on corporeal targets.
Rank 1 allows the effect to work at half its normal
rank against insubstantial targets (rounded down); rank 2
allows the effect to function at its full rank against them"""
    points_per_rank_modifier = points.Points_Flat_Modifier(1)
    modifier_needs_rank = True
    modifier_name = "Affects Incorporeal"
    modifier_list_type = False
    flat_modifier = True

    def __init__(self, power, rank, starting_rank=0):
        super().__init__()
        self.link_modifier_flat_with_rank(starting_rank, rank, power)

    def when_applied(self, power):
        self.when_applied_stored_in_extras(power)

    def when_removed(self, power):
        self.when_removed_stored_in_extras(power)

class Affects_Objects(Modifier):
    """This modifier allows effects normally resisted by Fortitude
to work on non-living objects (those with no Stamina).
Generally, this extra applies to effects like Heal or Weaken,
allowing them to work on objects in the same way as they
do living creatures. If the effect Affects Only Objects,
working on objects but not on living creatures, it has a net
modifier of +0.
Objects do not get resistance checks; the effect works on
the targeted object at its maximum degree of success. At
the GM’s discretion, someone holding, carrying, or wearing
an object can make a Dodge resistance check against
the effect, representing pulling the object out of the way
at the last moment."""
    points_per_rank_modifier = points.Points_Per_Rank_X_Modifier(1)
    modifier_needs_rank = True
    modifier_name = "Affects Objects"
    modifier_list_type = False
    flat_modifier = False

    def __init__(self, power, rank, starting_rank=0):
        super().__init__()
        self.link_modifier_per_rank(starting_rank, rank, power)
        self.affects_only = points.Rank_Range(0,0)

    def when_applied(self, power):
        self.when_applied_stored_in_extras(power)

    def when_removed(self, power):
        self.when_removed_stored_in_extras(power)

    def affects_only_objects(self, rank, starting_rank=0):
        self.alter_x_modifiers(points.Points_Per_Rank_X_Modifier(-1), rank, starting_rank=starting_rank)
        self.affects_only.add_range(starting_rank, rank)

    def represent_modifier_on_sheet_without_rank(self, power):
        retstr = ""
        modstr = ""
        only_val = False
        for mod in self.modifier_modifiers:
            modstr += "%s" % (mod.represent_modifier_on_sheet_without_rank(power))
            rr = mod.get_rank_range()
            if (rr.get_min() != 0) or (rr.get_max() != power.get_rank()) or (len(rr.rank_range) != 1):
                modstr += " %s" % (str(rr))
            modstr += ", "
        if self.affects_only.is_empty() == True:
            retstr = "Affects Objects"
        elif self.affects_only == self.get_rank_range():
            retstr = "Affects Only Objects"
        else:
            retstr = "Affects Objects %s (Affects Only Objects %s)" % (self.get_rank_range()-self.affects_only,self.affects_only)
        if modstr != "":
            retstr = "%s (%s)" % (retstr, modstr[:-2])
        return retstr

    def represent_modifier_on_sheet_with_rank(self, power):
        retstr = self.represent_modifier_on_sheet_without_rank(power)
        newarray = retstr.split("(")
        if (self.affects_only.is_empty() == True) or (self.affects_only == self.get_rank_range()):
            retstr = "%s %s" % (newarray[0], str(self.get_rank_range()))
        else:
            retstr = "%s" % (newarray[0])
        if len(newarray) != 1:
            for str in newarray[1:]:
                retstr += ("(" + str)
        return retstr

class Affects_Others(Modifier):
    """This extra allows you to give someone else use of a personal
effect. You must touch the subject as a standard
action, and they have control over their use of the effect,
although you can withdraw it when you wish as a free action.
If you are unable to maintain the effect, it stops working,
even if someone else is using it. Both you and your
subject(s) can use the effect simultaneously.
If the effect Affects Only Others, and not you, it has a net
modifier of +0."""
    points_per_rank_modifier = points.Points_Per_Rank_X_Modifier(1)
    modifier_needs_rank = True
    modifier_name = "Affects Others"
    modifier_list_type = False
    flat_modifier = False

    def __init__(self, power, rank, starting_rank=0):
        super().__init__()
        self.link_modifier_per_rank(starting_rank, rank, power)
        self.affects_only = points.Rank_Range(0,0)
        self.affects_total = points.Rank_Range_With_Points(rank,starting_rank=starting_rank)
        self.affects_b = False

    def when_applied(self, power):
        self.when_applied_stored_in_extras(power)
        if power.range == value_enums.Power_Range.PERSONAL:
            power.range = value_enums.Power_Range.CLOSE

    def when_removed(self, power):
        self.when_removed_stored_in_extras(power)
        power.range = value_enums.Power_Range.PERSONAL


    def add_additional_level(self, rank, starting_rank=0):
        self.alter_x_modifiers(points.Points_Per_Rank_X_Modifier(1), rank, starting_rank=starting_rank)
        self.affects_total.add_rank_range(points.Rank_Range(rank, starting_rank=0))

    def affects_only_others(self, rank, starting_rank=0):
        self.alter_x_modifiers(points.Points_Per_Rank_X_Modifier(-1), rank, starting_rank=starting_rank)
        self.affects_only.add_range(starting_rank, rank)

    def represent_modifier_on_sheet_without_rank(self, power):
        self.affects_b = False
        retstr = ""
        modstr = ""
        for mod in self.modifier_modifiers:
            modstr += "%s" % (mod.represent_modifier_on_sheet_without_rank(power))
            rr = mod.get_rank_range()
            if (rr.get_min() != 0) or (rr.get_max() != power.get_rank()) or (len(rr.rank_range) != 1):
                modstr += " %s" % (str(rr))
            modstr += ", "

        empty = points.Rank_Range(0,0)
        value_rank = 0
        for (a, b) in self.affects_total.get_points():
            #a is int, b is points_per_rank_x_modifier
            mod = b.get_modifier()
            altstr = ""
            if mod != 1:
                altstr = " x%d" % mod
            rng = points.Rank_Range(a,starting_rank=value_rank)
            adj = (rng - self.affects_only)
            affects_both = False
            if (adj == rng):
                retstr += "Affects Others%s" % (altstr)
            elif(adj == empty):
                retstr += "Affects Only Others%s" % (altstr)
            else:
                retstr += "Affects Others%s %s (Affects Only Others%s %s)" % (altstr, adj, altstr, (rng-adj))
                affects_both = True
                self.affects_b = True
            if(rng != self.get_rank_range()) and affects_both == False:
                retstr += " %s" % rng
            retstr += " "

        retstr = retstr[:-1]

        if modstr != "":
            retstr = "[%s (%s)]" % (retstr, modstr[:-2])
        return retstr

    def represent_modifier_on_sheet_with_rank(self, power):
        retstr = self.represent_modifier_on_sheet_without_rank(power)
        if self.affects_b == True:
            return retstr
        newarray = retstr.split("(")
        if (self.affects_only.is_empty() == True) or (self.affects_only == self.get_rank_range()):
            retstr = "%s %s" % (newarray[0], str(self.get_rank_range()))
        else:
            retstr = "%s" % (newarray[0])
        if len(newarray) != 1:
            for string in newarray[1:]:
                retstr += ("(" + string)
        return retstr


class Accurate(Modifier):
    """An effect with this extra is especially accurate; you get +2
per Accurate rank to attack checks made with it. The power
level limits maximum attack bonus with any given effect."""
    points_per_rank_modifier = points.Points_Flat_Modifier(1)
    modifier_needs_rank = True
    modifier_name = "Accurate"
    modifier_list_type = False
    flat_modifier = True

    def __init__(self, power, rank, starting_rank=0):
        super().__init__()
        self.link_modifier_flat_with_rank(starting_rank, rank, power)

    def when_applied(self, power):
        self.when_applied_stored_in_extras(power)

    def when_removed(self, power):
        self.when_removed_stored_in_extras(power)

class Insidious(Modifier):
    """This modifier is similar to the Subtle modifier (later in
this section), except Insidious makes the result of an
effect harder to detect rather than the effect itself. For
example, a target suffering from Insidious Damage isn’t
even aware he’s been damaged. Someone affected by an
Insidious Weaken feels fine until some deficiency makes
it obvious that he’s weaker, and so forth. A target of an
Insidious effect may remain unaware of the danger until
it’s too late!
An Insidious effect is detectable either by a DC 20 skill
check (usually Perception, although skills like Expertise,
Insight, or Treatment may apply in other cases) or a
particular unusual sense, such as an Insidious magical
effect noticeable by Detect Magic or Magical Awareness.
Note that Insidious does not make the effect itself harder
to notice; apply the Subtle modifier for that. So it is possible
for an active Insidious effect to be noticeable: the target
can perceive the use of the effect, but not its results:
the effect appears “harmless” or doesn’t seem to “do
anything” since the target cannot detect the results."""
    points_per_rank_modifier = points.Points_Flat_Modifier(1)
    modifier_needs_rank = True
    modifier_name = "Insidious"
    modifier_list_type = False
    flat_modifier = True
    modifier_pyramid_type = True

    def __init__(self, power, rank, starting_rank=0):
        super().__init__()
        self.link_modifier_flat_with_rank(starting_rank, rank, power)

    def when_applied(self, power):
        self.when_applied_stored_in_extras(power)

    def when_removed(self, power):
        self.when_removed_stored_in_extras(power)


class Subtle(Modifier):
    """Subtle effects are not as noticeable. A subtle effect may
be used to catch a target unaware and may in some cases
qualify for a surprise attack. Rank 1 makes an effect difficult
to notice; a DC 20 Perception check is required, or the effect
is noticeable only to certain exotic senses (at the GM’s discretion).
Rank 2 makes the effect completely undetectable"""
    points_per_rank_modifier = points.Points_Flat_Modifier(1)
    modifier_needs_rank = True
    modifier_name = "Subtle"
    modifier_list_type = False
    flat_modifier = True
    modifier_pyramid_type = True

    def __init__(self, power, rank, starting_rank=0):
        super().__init__()
        self.link_modifier_flat_with_rank(starting_rank, rank, power)

    def when_applied(self, power):
        self.when_applied_stored_in_extras(power)

    def when_removed(self, power):
        self.when_removed_stored_in_extras(power)

class Noticeable(Modifier):
    """A continuous or permanent effect with this modifier is
noticeable in some sort of way (see Noticing Power Effects
at the start of the chapter). Choose a noticeable
display for the effect. For example Noticeable Protection
may take the form of armored plates or a tough, leathery-looking
hide, making it clear the character is tougher
than normal."""
    points_per_rank_modifier = points.Points_Flat_Modifier(1)
    modifier_needs_rank = True
    modifier_name = "Noticeable"
    modifier_list_type = False
    flat_modifier = True
    modifier_pyramid_type = True
    modifier_is_flaw = True

    def __init__(self, power, rank, starting_rank=0):
        super().__init__()
        self.link_modifier_flat_with_rank(starting_rank, rank, power)

    def when_applied(self, power):
        self.when_applied_stored_in_extras(power)

    def when_removed(self, power):
        self.when_removed_stored_in_extras(power)

class Split(Modifier):
    """With this modifier, a resistible effect that works on one target
can split between two. The attacker chooses how many
ranks to apply to each target up to the effect’s total rank. So
a rank 10 effect could be split 5/5, 4/6, 2/8, or any other total
adding up to 10. If an attack check is required, the attacker
makes one, comparing the results against each target. The
effect works on each target at its reduced rank.
Each additional rank of this modifier allows the power
to split an additional time, so rank 2 allows an effect to
split among three targets, then four, and so forth. An effect
cannot split to less than 1 rank per target, and cannot
apply more than one split to the same target. Thus maximum
Split rank equals the effect’s rank."""
    points_per_rank_modifier = points.Points_Flat_Modifier(1)
    modifier_needs_rank = True
    modifier_name = "Split"
    modifier_list_type = False
    flat_modifier = True

    def __init__(self, power, rank, starting_rank=0):
        super().__init__()
        self.link_modifier_flat_with_rank(starting_rank, rank, power)

    def when_applied(self, power):
        self.when_applied_stored_in_extras(power)

    def when_removed(self, power):
        self.when_removed_stored_in_extras(power)

class Triggered(Modifier):
    """You can “set” an instant duration effect with this modifier
to activate under particular circumstances, such as in re196
Mutants & Master Mutants & Mastermminds D Deluxe Hero’s Handbook eluxe Hero’s Handbook
Chapter 6: Powers Chapter 6: Powers
sponse to a particular danger, after a set amount of time,
in response to a particular event, and so forth—chosen
when you apply the modifier. Once chosen, the trigger
cannot be changed.
The circumstances must be detectable by your senses.
You can acquire Senses Limited and Linked to Triggered
effects, if desired. Setting the effect requires the same action
as using it normally.
A Triggered effect lying in wait may be detected with a
Perception check (DC 10 + effect rank) and in some cases
disarmed with a successful skill or power check (such as
Sleight of Hand, Technology, Nullify or another countering
effect) with a DC of (10 + effect rank).
A Triggered effect is good for one use per rank in this
modifier. After its last activation, it stops working.
You can apply an additional rank of Triggered to have a
Variable Trigger, allowing you to change the effect’s trigger
each time you set it."""
    points_per_rank_modifier = points.Points_Flat_Modifier(1)
    modifier_needs_rank = True
    modifier_name = "Triggered"
    modifier_list_type = False
    flat_modifier = True

    def __init__(self, power, rank, starting_rank=0):
        super().__init__()
        self.link_modifier_flat_with_rank(starting_rank, rank, power)

    def when_applied(self, power):
        self.when_applied_stored_in_extras(power)

    def when_removed(self, power):
        self.when_removed_stored_in_extras(power)

class Variable_Descriptor(Modifier):
    """You can change the descriptors of an effect with this modifier,
varying them as a free action once per round. With rank
1, you can apply any of a closely related group of descriptors,
such as weather, electromagnetic, temperature, and
so forth. With rank 2, you can apply any of a broad group,
such as any mental, magical, or technological descriptor.
The GM decides if a given descriptor is appropriate in conjunction
with a particular effect and this modifier."""
    points_per_rank_modifier = points.Points_Flat_Modifier(1)
    modifier_needs_rank = True
    modifier_name = "Variable_Descriptor"
    modifier_list_type = False
    flat_modifier = True

    def __init__(self, power, rank, starting_rank=0):
        super().__init__()
        self.link_modifier_flat_with_rank(starting_rank, rank, power)

    def when_applied(self, power):
        self.when_applied_stored_in_extras(power)

    def when_removed(self, power):
        self.when_removed_stored_in_extras(power)

class Impervious:
    """A defense with this modifier is highly resistant. Any effect
with a resistance difficulty modifier equal to or less than
half the Impervious rank (rounded up) has no effect. So,
for example, Impervious Toughness 9 ignores any Damage
with a rank of 5 or less. Penetrating effects can overcome
Impervious Resistance (see the Penetrating extra
description).
Impervious is primarily intended for Toughness resistance
checks, to handle characters immune to a certain threshold
of damage, but it can be applied to other defenses
with the GM’s permission, to reflect characters with certain
reliable capabilities in terms of resisting particular effects
or hazards."""
    points_per_rank_modifier = points.Points_Flat_Modifier(1)
    modifier_needs_rank = True
    modifier_name = "Impervious"
    modifier_list_type = False
    flat_modifier = True

    def __init__(self, power, rank, starting_rank=0):
        super().__init__()
        self.link_modifier_flat_with_rank(starting_rank, rank, power)

    def when_applied(self, power):
        self.when_applied_stored_in_extras(power)

    def when_removed(self, power):
        self.when_removed_stored_in_extras(power)

class Ricochet:
    """You can ricochet or bounce an attack effect with this
modifier off of a solid surface to change its direction. This
allows you to attack around corners, overcome cover and
possibly make a surprise attack against an opponent. It
does not allow you to affect multiple targets. The “bounce”
has no effect apart from changing the attack’s direction.
You must be able to define a clear path for your attack,
which must follow a straight line between each ricochet.
Each rank in Ricochet allows you to bounce the attack
once before it hits. Ricochet may grant a bonus to hit due
to surprise, at the GM’s discretion."""
    points_per_rank_modifier = points.Points_Flat_Modifier(1)
    modifier_needs_rank = True
    modifier_name = "Ricochet"
    modifier_list_type = False
    flat_modifier = True

    def __init__(self, power, rank, starting_rank=0):
        super().__init__()
        self.link_modifier_flat_with_rank(starting_rank, rank, power)

    def when_applied(self, power):
        self.when_applied_stored_in_extras(power)

    def when_removed(self, power):
        self.when_removed_stored_in_extras(power)

class Reversible:
    """You can remove conditions caused by a Reversible effect at
will as a free action, so long as the subject is within the effect’s
range. Examples include removing the damage conditions
caused by a Damage effect, repairing damage done by
Weaken Toughness, or removing an Affliction instantly. Normally,
you have no control over the results of such effects."""
    points_per_rank_modifier = points.Points_Flat_Modifier(1)
    modifier_needs_rank = False
    modifier_name = "Reversible"
    modifier_list_type = False
    flat_modifier = True

    def __init__(self, power, rank=1, starting_rank=0):
        super().__init__()
        self.link_modifier_flat_with_rank(0, 1, power)

    def when_applied(self, power):
        self.when_applied_stored_in_extras(power)

    def when_removed(self, power):
        self.when_removed_stored_in_extras(power)

    def represent_modifier_on_sheet_with_rank(self, power):
        return self.represent_modifier_on_sheet_without_rank(power)

class Reach:
    """Each time you apply this modifier to a close range effect,
you extend its reach by 5 feet. This may represent a shortranged
effect or one with a somewhat greater reach, like a
whip, spear, or similar weapon."""
    points_per_rank_modifier = points.Points_Flat_Modifier(1)
    modifier_needs_rank = True
    modifier_name = "Reach"
    modifier_list_type = False
    flat_modifier = True

    def __init__(self, power, rank, starting_rank=0):
        super().__init__()
        self.link_modifier_flat_with_rank(starting_rank, rank, power)

    def when_applied(self, power):
        self.when_applied_stored_in_extras(power)

    def when_removed(self, power):
        self.when_removed_stored_in_extras(power)

class Precise(Modifier):
    """You can use a Precise effect to perform tasks requiring
delicacy and fine control, such as using Precise Damage
to spot-weld or carve your initials, Precise Move Object to
type or pick a lock, Precise Environment to match a particular
temperature exactly, and so forth. The GM has final
say as to what tasks can be performed with a Precise effect
and may require an ability, skill, or power check to determine
the degree of precision with any given task."""
    points_per_rank_modifier = points.Points_Flat_Modifier(1)
    modifier_needs_rank = True
    modifier_name = "Precise"
    modifier_list_type = False
    flat_modifier = True
    modifier_pyramid_type = True

    def __init__(self, power, rank=1, starting_rank=0):
        super().__init__()
        self.link_modifier_flat_with_rank(starting_rank, rank, power)

    def when_applied(self, power):
        self.when_applied_stored_in_extras(power)

    def when_removed(self, power):
        self.when_removed_stored_in_extras(power)

class Penetrating(Modifier):
    """Your effect overcomes Impervious Resistance to a degree;
the target must make a resistance check against an effect
rank equal to your Penetrating rank. So, if a rank 4 (Penetrating
2) effect hits a target with Impervious 9, the target
must resist a rank 2 effect (equal to the Penetrating rank).
If the effect were rank 6, the target would have to resist
the full effect anyway, since its rank is greater than half
the Impervious rank. You cannot have a Penetrating rank
greater than your effect rank."""
    points_per_rank_modifier = points.Points_Flat_Modifier(1)
    modifier_needs_rank = True
    modifier_name = "Penetrating"
    modifier_list_type = False
    flat_modifier = True

    def __init__(self, power, rank, starting_rank=0):
        super().__init__()
        self.link_modifier_flat_with_rank(starting_rank, rank, power)

    def when_applied(self, power):
        self.when_applied_stored_in_extras(power)

    def when_removed(self, power):
        self.when_removed_stored_in_extras(power)

class Linked(Modifier):
    """This modifier applies to two or more effects, linking them
together so they only work in conjunction as one.
The Linked effects must operate at the same range.
The action required to use the combined effects is the
longest of its components and they use a single attack
check (if one is required) and resistance check (if both
effects use the same type of check). If the effects have
different resistances, targets check against each effect
separately. Different Alternate Effects cannot be Linked
since they can’t be used at the same time by definition.
Generally, the same effect cannot be Linked to itself to
“multiply” the results of a failed resistance check (such as
two Linked Damage effects causing “double damage” on
a failed check).
This modifier does not change the cost of the component
effects; simply add their costs together to get the combined
effect’s cost."""
    pass

class Innate(Modifier):
    """An effect with this modifier is an innate part of your na
ture and unaffected by Nullify (see the Nullify effect in
this chapter). Gamemasters should exercise caution in
allowing the application of Innate; the effect must be a
truly inborn or essential trait, such as an elephant’s size or
a ghost’s incorporeal nature. If the effect is not something
normal to the character’s species or type, it probably isn’t
innate."""
    points_per_rank_modifier = points.Points_Flat_Modifier(1)
    modifier_needs_rank = False
    modifier_name = "Innate"
    modifier_list_type = False
    flat_modifier = True

    def __init__(self, power, rank=1, starting_rank=0):
        super().__init__()
        self.link_modifier_flat_with_rank(0, 1, power)

    def when_applied(self, power):
        self.when_applied_stored_in_extras(power)

    def when_removed(self, power):
        self.when_removed_stored_in_extras(power)

    def represent_modifier_on_sheet_with_rank(self, power):
        return self.represent_modifier_on_sheet_without_rank(power)

class Incurable(Modifier):
    """Effects such as Healing and Regeneration cannot heal the
damage caused by an effect with this modifier; the target
must recover at the normal rate. Effects with the Persistent
extra can heal Incurable damage."""
    points_per_rank_modifier = points.Points_Flat_Modifier(1)
    modifier_needs_rank = False
    modifier_name = "Incurable"
    modifier_list_type = False
    flat_modifier = True

    def __init__(self, power, rank=1, starting_rank=0):
        super().__init__()
        self.link_modifier_flat_with_rank(0, 1, power)

    def when_applied(self, power):
        self.when_applied_stored_in_extras(power)

    def when_removed(self, power):
        self.when_removed_stored_in_extras(power)

    def represent_modifier_on_sheet_with_rank(self, power):
        return self.represent_modifier_on_sheet_without_rank(power)

class Indirect(Modifier):
    """A ranged effect with this modifier can originate from a
point other than the user, ignoring cover between the
user and the target, such as walls and other intervening
barriers, so long as they do not provide cover between
the effect’s origin point and the target. An Indirect effect
normally originates from a fixed point directed away from
you. In some cases, an Indirect effect may count as a surprise
attack (see Surprise Attack, page 251).
• Indirect 1: the effect originates from a fixed point
away from you.
• Indirect 2: the effect can come from any point away
from you or a fixed point in a fixed direction (notaway
from you).
• Indirect 3: The effect can come from any point in a
fixed direction (not away from you) or a fixed
point in any direction.
•Indirect 4: The effect can originate from any point
and aim in any direction, including towards you
(hitting a target in front of you from behind, for example)."""
    points_per_rank_modifier = points.Points_Flat_Modifier(1)
    modifier_needs_rank = True
    modifier_name = "Indirect"
    modifier_list_type = False
    flat_modifier = True

    def __init__(self, power, rank, starting_rank=0):
        super().__init__()
        self.link_modifier_flat_with_rank(starting_rank, rank, power)

    def when_applied(self, power):
        self.when_applied_stored_in_extras(power)

    def when_removed(self, power):
        self.when_removed_stored_in_extras(power)

class Increased_Mass(Modifier):
    """This modifier may apply to an effect that allows you to
carry or affect a set amount of mass, typically a movement
effect like Dimensional Travel or Teleport. Each rank of this
extra increases the mass rank you can carry or move with
the effect by 1. So Increased Mass 3 on Teleport allows you
to carry up to 400 lbs. of extra mass with you when you
teleport, for example."""
    points_per_rank_modifier = points.Points_Flat_Modifier(1)
    modifier_needs_rank = True
    modifier_name = "Increased Mass"
    modifier_list_type = False
    flat_modifier = True

    def __init__(self, power, rank, starting_rank=0):
        super().__init__()
        self.link_modifier_flat_with_rank(starting_rank, rank, power)

    def when_applied(self, power):
        self.when_applied_stored_in_extras(power)

    def when_removed(self, power):
        self.when_removed_stored_in_extras(power)

class Homing(Modifier):
    """This modifier grants a ranged effect an additional opportunity
to hit. If an attack check with a Homing effect fails, it
attempts to hit again on the start of your next turn, requiring
only a free action to maintain and allowing you to take
other actions, including making another attack. Each rank
in Homing grants the effect one additional attack check,
but it still only gets one check per round.
The Homing effect uses the same accurate sense as the
original attack to “track” its target, so concealment effective
against that sense may confuse the effect and cause
it to miss. If a Homing attack misses due to concealment,
it has lost its “lock” on the target and does not get any
further chances to hit. You can take Senses Linked to
the Homing effect, if desired (to create things like radarguided
or heat-seeking missiles, for example). If a Homing
attack is countered before it hits, it loses any remaining
chances to hit. The same is true if it hits a different target."""
    points_per_rank_modifier = points.Points_Flat_Modifier(1)
    modifier_needs_rank = True
    modifier_name = "Homing"
    modifier_list_type = False
    flat_modifier = True

    def __init__(self, power, rank, starting_rank=0):
        super().__init__()
        self.link_modifier_flat_with_rank(starting_rank, rank, power)

    def when_applied(self, power):
        self.when_applied_stored_in_extras(power)

    def when_removed(self, power):
        self.when_removed_stored_in_extras(power)

class Extended_Range(Modifier):
    """This modifier extends the distance over which a ranged effect
works. Each rank of Extended Range doubles all of the
effect’s range categories. So 1 rank makes short range (rank
x 50 ft.), medium range (rank x 100 ft.) and long range (rank
x 200 ft.). Each additional rank further doubles range.
The GM may set limits on the maximum Extended Range
an effect can have; as a general guideline, effects used on
a planetary surface are limited to the distance to the horizon
(beyond which the curvature of the planet makes it
impossible to see anything to target it). On Earth at sea
level, this is roughly three miles (distance rank 10)."""
    points_per_rank_modifier = points.Points_Flat_Modifier(1)
    modifier_needs_rank = True
    modifier_name = "Extended Range"
    modifier_list_type = False
    flat_modifier = True

    def __init__(self, power, rank, starting_rank=0):
        super().__init__()
        self.link_modifier_flat_with_rank(starting_rank, rank, power)

    def when_applied(self, power):
        self.when_applied_stored_in_extras(power)

    def when_removed(self, power):
        self.when_removed_stored_in_extras(power)

class Dimensional(Modifier):
    """This modifier allows an effect to work on targets in other
dimensions (if any exist in the series). You affect your
proximate location in the other dimension as if you were
actually there, figuring range modifiers from that point.
One rank in Dimensional can affect a single other dimension.
Two ranks can affect any of a related group of dimensions
(mythic dimensions, mystic dimensions, fiendish
planes, and so forth). Three ranks can reach into any other
dimension in the setting.
For many effects, you may need a Dimensional Remote
Sensing effect to target them. Targets in other dimensions
you cannot sense have total concealment from you."""
    points_per_rank_modifier = points.Points_Flat_Modifier(1)
    modifier_needs_rank = True
    modifier_name = "Dimensional"
    modifier_list_type = False
    flat_modifier = True

    def __init__(self, power, rank, starting_rank=0):
        super().__init__()
        self.link_modifier_flat_with_rank(starting_rank, rank, power)

    def when_applied(self, power):
        self.when_applied_stored_in_extras(power)

    def when_removed(self, power):
        self.when_removed_stored_in_extras(power)


class Feature(Modifier):
    """The Feature effect (see page 160) can also serve as an effect
modifier, essentially adding on some minor additional
capability or benefit to a basic effect. Although listed here
as an extra, this is essentially the same as having the Feature
Linked to the base effect (see the Linked modifier
later in this section); the Feature is an intrinsic part of the
overall power, rather than separate.
As with the Feature effect, a Feature extra should be significant
enough to be worth at least 1 power point and
not solely based on the power’s descriptors. So, for example,
a fiery Ranged Damage effect does not need a Feature
to ignite fires; doing so is part of its “fire” descriptor and
can be equally advantageous and problematic. A Ranged
Damage effect that consistently “brands” its target with a
visible and traceable mark, on the other hand, is an effect
with an added Feature."""
    points_per_rank_modifier = points.Points_Flat_Modifier(1)
    modifier_needs_rank = True
    modifier_name = "Feature"
    modifier_list_type = False
    flat_modifier = True

    def __init__(self, power, rank, starting_rank=0):
        super().__init__()
        self.link_modifier_flat_with_rank(starting_rank, rank, power)

    def when_applied(self, power):
        self.when_applied_stored_in_extras(power)

    def when_removed(self, power):
        self.when_removed_stored_in_extras(power)

class Area(Modifier):
    """This extra allows an effect that normally works on a single
target to affect an area. No attack check is needed; the
effect simply fills the designated area, based on the type
of modifier. Potential targets in the area are permitted
a Dodge resistance check (DC 10 + effect rank) to avoid
some of the effect (reflecting ducking for cover, dodging
out of the way, and so forth). A successful resistance check
reduces the Area effect to half its normal rank against that
target (round down, minimum of 1 rank).
Shape
Choose one of the following options:
• Burst: The effect fills a sphere with a 30-foot radius
(distance rank 0). Bursts on level surfaces (like the
ground) create hemispheres 30 feet in radius and
height.
• Cloud: The effect fills a sphere with a 15-foot radius
(distance rank –1) that lingers in that area for one
round after its duration expires (affecting any targets
in the area normally during the additional round).
Clouds on level surfaces (like the ground) create
hemispheres 15 feet in radius and height.
• Cone: The effect fills a cone with a length, width,
and height of 60 feet (distance rank 1), spreading out
from the effect’s starting point. Cones on a level surface
halve their final height.
• Cylinder: The effect fills a cylinder 30 feet in radius
and height (distance rank 0).
• Line: The effect fills a path 6 feet wide and 30 feet
long (distance ranks -2 and 0, respectively) in a
straight line. Additional ranks of area increases the
length. To increase the width, purchase additional
ranks for that.
• Perception: The effect works on anyone able to perceive
the target point with a particular sense, chosen
when you apply this extra, like a Sense-Dependent effect
(see the Sense-Dependent modifier). Targets get
a Dodge resistance check, as usual, but if the check is
successful suffer no effect (rather than half). Concealment
that prevents a target from perceiving the effect
also blocks it. This modifier includes the Sense-Dependent
flaw (see Flaws) so it cannot be applied again. If
it is applied to an already Sense-Dependent effect, it
costs 2 points per rank rather than 1.
• Shapeable: The effect fills a volume of 30 cubic feet
(volume rank 5), and you may shape the volume as
you wish, so long as it all remains contiguous. Affecting
an average-sized human requires 4 cubic feet
(volume rank 2).
Each +1 point increase in cost per rank moves the area’s
distance rank up by 1. So a Burst Area with +2 cost per
rank has a 60-foot radius (distance rank 1), a 120-foot radius
at +3 cost per rank (distance rank 2), and so forth.
Range
The Area modifier interacts with different ranges as follows:
• Close: An effect must be at least close range in order
to apply Area (personal range effects work only on the
user by definition). A Close Area effect originates from
the user and expands to fill the affected area; the user
is not affected by it. So, for example, Close Burst Area
Damage does not damage the user, who is at the center
 of the burst. This immunity does not apply to other
effects, nor does it extend to anyone else: for that, apply
the Selective extra. If the user wants to be affected
at the same time, increase cost per rank by +1. An example
would be a Close Burst Area Healing effect that
included the user along with everyone else in the area.
This is the equivalent of the +1 Affects Others modifier.
• Ranged: A ranged area effect can be placed anywhere
within the effect’s range, extending to fill the
area’s volume from the origin point.
• Perception: A perception area effect can be placed
anywhere the user can accurately perceive. Perception
area effects neither require an attack check nor
allow a Dodge resistance check, although targets still
get a normal resistance check against the effect. Perception
area effects are blocked by either concealment
or cover; choose one when acquiring the effect.
For concealment, if the attacker can’t accurately perceive
a target in the area, it is unaffected. Thus even
heavy smoke or darkness can block the effect. Effects
blocked by cover are much like conventional area effects:
solid barriers interfere with the effect, even if
they are transparent, but the effect ignores concealment
like darkness, shadows, or smoke. Only targets
behind total cover are unaffected.
Example: Mastermind has a Burst Area Affliction, allowing
him to seize control of the minds of everyone
in the affected area. He must be able to accurately
perceive a target to control it; an invisible foe or one
out of his line of sight, for example, would be unaffected,
even if they were within the area of the burst. On
the other hand, targets behind a glass wall or invisible
force field are affected, since Mastermind can perceive
them. Conversely, Fear-Master has a Burst Area Affliction
as well—his fear-inducing gas. Targets behind a
solid barrier (such as on the other side of that glass
wall or invisible shield) are unaffected, but the unseen
or concealed target is, even though Fear-Master can’t
perceive him, since the gas still reaches them."""
    points_per_rank_modifier = points.Points_Per_Rank_X_Modifier(1)
    modifier_needs_rank = True
    modifier_name = "Area"
    modifier_list_type = False
    flat_modifier = False

    modifier_plain_text = value_enums.Power_Area_Names.name_list
    modifier_values = value_enums.Power_Area_Names.val_list

    modifier_options = Modifier_Options(modifier_plain_text,modifier_values)

    def __init__(self, power, rank, starting_rank=0, area_val=value_enums.Power_Area.BURST):
        super().__init__()
        self.link_modifier_per_rank(starting_rank, rank, power)
        self.area_total = points.Rank_Range_With_Points(rank,starting_rank=starting_rank)
        self.area_type = area_val

    def when_applied(self, power):
        self.when_applied_stored_in_extras(power)

    def when_removed(self, power):
        self.when_removed_stored_in_extras(power)

    def set_area_type(self, area_type):
        self.area_type = area_type

    def add_additional_level(self, rank, starting_rank=0):
        self.alter_x_modifiers(points.Points_Per_Rank_X_Modifier(1), rank, starting_rank=starting_rank)
        self.area_total.add_rank_range(points.Rank_Range(rank, starting_rank=0))

    def represent_modifier_on_sheet_without_rank(self, power):
        self.rank_included = False
        retstr = ""
        modstr = ""
        for mod in self.modifier_modifiers:
            modstr += "%s" % (mod.represent_modifier_on_sheet_without_rank(power))
            rr = mod.get_rank_range()
            if (rr.get_min() != 0) or (rr.get_max() != power.get_rank()) or (len(rr.rank_range) != 1):
                modstr += " %s" % (str(rr))
            modstr += ", "

        empty = points.Rank_Range(0,0)
        value_rank = 0
        for (a, b) in self.area_total.get_points():
            #a is int, b is points_per_rank_x_modifier
            mod = b.get_modifier()
            altstr = ""
            if mod != 1:
                altstr = " x%d" % mod
            rng = points.Rank_Range(a,starting_rank=value_rank)
            retstr += "Area %s%s" % (type(self).modifier_options.get_plaintext_from_value(self.area_type),altstr)
            if(rng != self.get_rank_range()):
                retstr += " %s" % rng
                self.rank_included = True
            retstr += " "

        retstr = retstr[:-1]

        if modstr != "":
            retstr = "[%s (%s)]" % (retstr, modstr[:-2])
        return retstr

    def represent_modifier_on_sheet_with_rank(self, power):
        retstr = self.represent_modifier_on_sheet_without_rank(power)
        if self.rank_included == True:
            return retstr
        newarray = retstr.split("(")
        if (self.affects_only.is_empty() == True) or (self.affects_only == self.get_rank_range()):
            retstr = "%s %s" % (newarray[0], str(self.get_rank_range()))
        else:
            retstr = "%s" % (newarray[0])
        if len(newarray) != 1:
            for string in newarray[1:]:
                retstr += ("(" + string)
        return retstr

class Attack(Modifier):
    """This extra applies to personal range effects, making
them into attack effects. Examples include Shrinking and
Teleport, causing a target to shrink or teleport away, respectively.
Unlike most extras, the effect’s cost does not
change, although it does work differently.
The effect no longer works on you (so a Teleport Attack
can’t be used to teleport yourself, for example). It affects
one creature of any size or 50 lbs. of inanimate mass. The
effect has close range and requires a standard action and
an attack check to touch the subject. Its range can be improved
with the Range extra while its required action can
be changed with the Action modifier. The target gets a resistance
check, determined when the effect is made into
an attack. Generally Dodge or Will is the most appropriate.
A successful check negates the effect.
You must also define reasonably common circumstances
that negate an Attack effect entirely, such as force fields or the
ability to teleport blocking a Teleport Attack. You control the
effect, and maintain it, if it has a duration longer than instant.
If you want both versions of an Attack effect, such as being
able to Teleport yourself and Teleport others as an attack,
take both as Alternate Effects. For the ability to use
both options simultaneously—to teleport a target and
yourself at the same time, for example—take the effects
as separate powers."""
    pass

class Alternate_Resistance(Modifier):
    """An effect with this modifier has a different resistance
than usual. The resistance check difficulty class remains
the same, only the resistance differs. If the change is to
a generally lower (and therefore more advantageous) resistance,
this extra increases cost per rank by +1. If, in the
GM’s opinion, there is no real increase in effectiveness, just
a chance to the resistance, it has a net modifier of +0."""
    points_per_rank_modifier = points.Points_Per_Rank_X_Modifier(1)
    modifier_needs_rank = True
    modifier_name = "Alternate Resistance"

    modifier_list_type = False

    def __init__(self, power, rank, starting_rank=0, res_ptr=None, res_name="Fortitude"):
        super().__init__()
        self.link_modifier_per_rank(starting_rank, rank, power)
        self.resistance_pointer = res_ptr
        self.resistance_name = res_name

    def when_applied(self, power):
        self.when_applied_stored_in_extras(power)

    def when_removed(self, power):
        self.when_removed_stored_in_extras(power)

    def adjust_value_of_resistance(self, adjval):
        self.alter_x_modifiers(points.Points_Per_Rank_X_Modifier(adjval),self.get_rank(),self.get_starting_rank())

    def set_new_resistance(self, resistance_pointer):
        self.resistance_pointer = resistance_pointer

    def represent_modifier_on_sheet_without_rank(self, power):
        retstr = ""
        modstr = ""
        for mod in self.modifier_modifiers:
            modstr += "%s" % (mod.represent_modifier_on_sheet_without_rank(power))
            rr = mod.get_rank_range()
            if (rr.get_min() != 0) or (rr.get_max() != power.get_rank()) or (len(rr.rank_range) != 1):
                modstr += " %s" % (str(rr))
            modstr += ", "
        retstr += "%s (%s)" % (type(self).modifier_name,self.resistance_name)
        if modstr == "":
            pass
        else:
            retstr = "[%s (%s)]" % (retstr, modstr[:-2])
        return retstr

    def represent_modifier_on_sheet_with_rank(self, power):
        retstr = self.represent_modifier_on_sheet_without_rank(power)
        retstr = "%s %s" % (retstr,self.get_rank_range())
        return retstr


extras = """XXX Accurate 1 flat per rank +2 attack check bonus per rank XXX
XXX Affects Corporeal 1 flat per rank Effect works on corporeal beings with rank equal to extra rank. XXX
XXX Affects Insubstantial 1-2 flat points Effect works on insubstantial beings at half (1 rank) or full (2 ranks) effect. XXX
XXX Affects Objects +0-1 per rank Fortitude resisted effect works on objects. XXX
XXX Affects Others +0-1 per rank Personal effect works on others. XXX
Alternate Effect 1-2 flat points Substitute one effect for another in a power.
XXX Alternate Resistance +0-1 per rank Effect uses a different resistance. XXX
XXX Area +1 per rank Effect works on an area. XXX
Attack +0 per rank Personal effect works on others as an attack.
XXX Contagious +1 per rank Effect works on anyone coming into contact with its target. XXX
XXX Dimensional 1-3 flat points Effect works on targets in other dimensions. XXX
XXX Extended Range 1 flat per rank Doubles ranged effect’s distances per rank. XXX
XXX Feature 1 flat per rank Adds a minor capability or benefit to an effect. XXX
XXX Homing 1 flat per rank Attack effect gains additional chances to hit. XXX
XXX Impervious +1 per rank Resistance ignores effects with difficulty modifier of half extra rank or less. XXX
XXX Increased Duration +1 per rank Improves effect’s duration. XXX
XXX Increased Mass 1 flat per rank Effect can carry a greater amount of mass. XXX
XXX Increased Range +1 per rank Improves effect’s range. XXX
XXX Incurable 1 flat point Effect cannot be countered or removed using Healing or Regeneration. XXX
XXX Indirect 1 flat per rank Effect can originate from a point other than the user. XXX
XXX Innate 1 flat point Effect cannot be Nullified. XXX
XXX Insidious 1 flat point Result of the effect is more difficult to detect. XXX
Linked 0 flat points Two or more effects work together as one.
XXX Multiattack +1 per rank Effect can hit multiple targets or a single target multiple times. XXX
XXX Penetrating 1 flat per rank Effect overcomes Impervious Resistance. XXX
XXX Precise 1 flat point Effect can perform delicate and precise tasks. XXX
XXX Reach 1 flat per rank Extend effect’s reach by 5 feet per rank. XXX
XXX Reaction +1 or 3 per rank Changes effect’s required action to reaction. XXX
XXX Reversible 1 flat point Effect can be removed at will as a free action. XXX
XXX Ricochet 1 flat per rank Attacker can bounce effect to change direction. XXX
XXX Secondary Effect +1 per rank Instant effect works on the target twice. XXX
XXX Selective +1 per rank Resistible effect works only on the targets you choose. XXX
XXX Sleep +0 per rank Effect leaves targets asleep rather than incapacitated. XXX
XXX Split 1 flat per rank Effect can split into multiple, smaller, effects. XXX
XXX Subtle 1-2 flat points Effect is less noticeable (1 point) or not noticeable (2 points). XXX
XXX Sustained +0 per rank Makes a permanent effect sustained. XXX
XXX Triggered 1 flat per rank Effect can be set for later activation. XXX
XXX Variable Descriptor 1-2 flat points Effect can change descriptors XXX"""

flaws = """Activation –1-2 flat points Effect requires a move (1 point) or standard (2 points) action to activate.
Check Required –1 flat per rank Must succeed on a check to use effect.
Concentration –1 per rank Sustained effect becomes concentration duration.
Diminished Range –1 flat per rank Reduces short, medium, and long ranges for the effect.
Distracting –1 per rank Vulnerable while using effect.
XXX Fades –1 per rank Effect loses 1 rank each time it is used. XXX
Feedback –1 per rank Suffer damage when your effect’s manifestation is damaged.
Grab-Based –1 per rank Effect requires a successful grab attack to use.
Increased Action –1-3 per rank Increases action required to use effect.
Limited –1 per rank Effect loses about half its effectiveness.
XXX Noticeable –1 flat point Continuous or permanent effect is noticeable. XXX
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



class Modifier_Description:
    mods_dict = {"Increased Range": Increased_Range,
                 "Increased Duration": Increased_Duration,
                 "Secondary Effect": Secondary_Effect,
                 "Increased Action": Increased_Action,
                 "Multiattack": Multiattack,
                 "Selective": Selective,
                 "Contagious": Contagious,
                 "Fades": Fades,
                 "Sustained": Sustained,
                 "Sleep": Sleep,
                 "Accurate": Accurate,
                 "Insidious": Insidious,
                 "Subtle": Subtle,
                 "Noticeable": Noticeable,
                 "Split": Split,
                 "Triggered": Triggered,
                 "Variable_Descriptor": Variable_Descriptor}

    def __init__(self, dict_input):
        self.modifier_name = dict_input['modifier']
        self.modifier_class = type(self).mods_dict[self.modifier_name]
        if modifier_class.modifier_needs_rank == True:
            self.modifier_rank = dict_input['rank']
            if 'starting rank' in dict_input:
                self.modifier_starting_rank = dict_input['starting rank']
            else:
                self.modifier_starting_rank = 0

if __name__ == "__main__":
    for i in range(4,2,-1):
        print(i)