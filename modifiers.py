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
            self.points_in_modifier.adjust_x_for_ranks(points.Points_Per_Rank_X_Modifier(-1), rank, starting_rank=starting_rank, pos=True)
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
            retstr = "%s (%s)" % (retstr, modstr[:-2])
        return retstr

    def represent_modifier_on_sheet_with_rank(self, power):
        retstr = self.represent_modifier_on_sheet_without_rank(power)
        newarray = retstr.split("(")
        retstr = "%s %s" % (newarray[0], self.get_rank_range())
        if len(newarray) != 1:
            for str in newarray[1:]:
                retstr += ("(" + str)
        return retstr

    # def represent_modifier_on_sheet_with_rank(self, power):
    #     #TODO - this is also broken
    #     retstr = ""
    #     modstr = ""
    #     for mod in self.modifier_modifiers:
    #         modstr += " %s%s " % (mod.represent_modifier_on_sheet_with_rank(power), type(mod).get_class_plaintext_name())
    #     if type(self).modifier_list_type == True:
    #         retstr += "%s" % type(self).modifier_options.get_plaintext_from_value(self.power_new_value)
    #     if self.get_starting_rank() != 0:
    #         retstr = "%s %d-%d" % (retstr, self.get_starting_rank(), self.get_rank())
    #     else:
    #         retstr = "%s %d" % (retstr, self.get_rank())
    #     if modstr == "":
    #         pass
    #     else:
    #         retstr = "%s (%s)" % (retstr, modstr)
    #     return retstr


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
        if power.range < type(self).modifier_values[-1]:
            power.range += 1

    def when_removed(self, power):
        if power.range > type(self).modifier_values[1]:
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
            if type(mod) == Limited:
                only_val = True
            else:
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
            retstr = "%s" (newarray[0])
        if len(newarray) != 1:
            for str in newarray[1:]:
                retstr += ("(" + str)
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


extras = """XXX Accurate 1 flat per rank +2 attack check bonus per rank XXX
XXX Affects Corporeal 1 flat per rank Effect works on corporeal beings with rank equal to extra rank. XXX
XXX Affects Insubstantial 1-2 flat points Effect works on insubstantial beings at half (1 rank) or full (2 ranks) effect. XXX
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