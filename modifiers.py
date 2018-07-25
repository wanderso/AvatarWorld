import powers

class Modifier:
    points_per_rank_modifier = None
    modifier_name = None
    def __init__(self, power):
        self.associated_powers = [power]

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
    points_per_rank_modifier = 1.0
    modifier_name = "Increased Range"
    def __init__(self, power):
        super().__init__(power)
        apply()

    def apply(self):
        for power in self.associated_powers:
            if power.range < powers.Power_Range.PERCEPTION:
                power.range += 1
                power.adjust_points_per_rank(points_per_rank_modifier)

    def remove(self):
        for power in self.associated_powers:
            if power.range > powers.Power_Range.PERSONAL:
                power.range -= 1
                power.adjust_points_per_rank(points_per_rank_modifier)


extras = """Accurate 1 flat per rank +2 attack check bonus per rank
Affects Corporeal 1 flat per rank Effect works on corporeal beings with rank equal to extra rank.
Affects Insubstantial 1-2 flat points Effect works on insubstantial beings at half (1 rank) or full (2 ranks) effect.
Affects Objects +0-1 per rank Fortitude resisted effect works on objects.
Affects Others +0-1 per rank Personal effect works on others.
Alternate Effect 1-2 flat points Substitute one effect for another in a power.
Alternate Resistance +0-1 per rank Effect uses a different resistance.
Area +1 per rank Effect works on an area.
Attack +0 per rank Personal effect works on others as an attack.
Contagious +1 per rank Effect works on anyone coming into contact with its target.
Dimensional 1-3 flat points Effect works on targets in other dimensions.
Extended Range 1 flat per rank Doubles ranged effect’s distances per rank.
Feature 1 flat per rank Adds a minor capability or benefit to an effect.
Homing 1 flat per rank Attack effect gains additional chances to hit.
Impervious +1 per rank Resistance ignores effects with difficulty modifier of half extra rank or less.
Increased Duration +1 per rank Improves effect’s duration.
Increased Mass 1 flat per rank Effect can carry a greater amount of mass.
Increased Range +1 per rank Improves effect’s range.
Incurable 1 flat point Effect cannot be countered or removed using Healing or Regeneration.
Indirect 1 flat per rank Effect can originate from a point other than the user.
Innate 1 flat point Effect cannot be Nullified.
Insidious 1 flat point Result of the effect is more difficult to detect.
Linked 0 flat points Two or more effects work together as one.
Multiattack +1 per rank Effect can hit multiple targets or a single target multiple times.
Penetrating 1 flat per rank Effect overcomes Impervious Resistance.
Precise 1 flat point Effect can perform delicate and precise tasks.
Reach 1 flat per rank Extend effect’s reach by 5 feet per rank.
Reaction +1 or 3 per rank Changes effect’s required action to reaction.
Reversible 1 flat point Effect can be removed at will as a free action.
Ricochet 1 flat per rank Attacker can bounce effect to change direction.
Secondary Effect +1 per rank Instant effect works on the target twice.
Selective +1 per rank Resistible effect works only on the targets you choose.
Sleep +0 per rank Effect leaves targets asleep rather than incapacitated.
Split 1 flat per rank Effect can split into multiple, smaller, effects.
Subtle 1-2 flat points Effect is less noticeable (1 point) or not noticeable (2 points).
Sustained +0 per rank Makes a permanent effect sustained.
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