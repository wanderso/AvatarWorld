import enum

class Advantage_Type(enum.Enum):
    COMBAT_ADVANTAGE = 1
    FORTUNE_ADVANTAGE = 2
    GENERAL_ADVANTAGE = 3
    SKILL_ADVANTAGE = 4

class Cost_Type(enum.Enum):
    FLAT_RANK = 1
    PYRAMID_RANK = 2
    NO_RANK = 3



class Advantage:
    def __init__(self, name):
        self.advantage_name = name
        self.advantage_cost = 0
        self.advantage_cost_type = Cost_Type.FLAT_RANK
        self.advantage_rank = 0
        self.advantage_func_list = None

    def calculate_cost(self):
        print("Will we ever reach this?")
        if self.advantage_cost_type == Cost_Type.FLAT_RANK:
            return self.advantage_rank
        elif self.advantage_cost_type == Cost_Type.PYRAMID_RANK:
            ret_val = 0
            for i in range (1, self.advantage_rank+1):
                ret_val += i
            return ret_val
        elif self.advantage_cost_type == Cost_Type.NO_RANK:
            return 1

    def pyramid_cost(self):
        ret_val = 0
        for i in range(1, self.advantage_rank + 1):
            ret_val += i
        return ret_val

    def flat_cost(self):
        return self.advantage_rank

    def no_rank_cost(self):
        return 1

    def init_flat(self,rank):
        self.advantage_cost = rank
        self.advantage_cost_type = Cost_Type.FLAT_RANK
        self.advantage_rank = rank
        self.advantage_func_list = None
        self.calculate_cost = self.flat_cost

    def init_no(self):
        self.advantage_cost = 1
        self.advantage_cost_type = Cost_Type.NO_RANK
        self.advantage_rank = 1
        self.advantage_func_list = None
        self.calculate_cost = self.no_rank_cost

    def init_pyramid(self,rank):
        self.advantage_cost = 0
        self.advantage_cost_type = Cost_Type.PYRAMID_RANK
        self.advantage_rank = rank
        self.advantage_func_list = None
        self.calculate_cost = self.pyramid_cost



class Accurate_Attack(Advantage):
    """When you make an accurate attack (see Maneuvers, page
    249) you can take a penalty of up to –5 on the effect modifier
    of the attack and add the same number (up to +5) to
    your attack bonus."""
    def __init__(self, rank):
        super().__init__("Accurate Attack")
        self.init_pyramid(rank)

class Agile_Feint(Advantage):
    """You can use your Acrobatics bonus or movement speed
    rank in place of Deception to feint and trick in combat as if
    your skill bonus or speed rank were your Deception bonus
    (see the Deception skill description). Your opponent opposes
    the attempt with Acrobatics or Insight (whichever
    is better)."""
    def __init__(self):
        super().__init__("Agile Feint")
        self.init_no()

class All_Out_Attack(Advantage):
    """When you make an all-out attack (see Maneuvers, page
249) you can take a penalty of up to –5 on your active defenses
(Dodge and Parry) and add the same number (up
to +5) to your attack bonus."""
    def __init__(self, rank):
        super().__init__("All Out Attack")
        self.init_pyramid(rank)

class Animal_Empathy(Advantage):
    """You have a special connection with animals. You can use
interaction skills on animals normally, and do not have to
speak a language the animal understands; you communicate
your intent through gestures and body language
and learn things by studying animal behavior. Characters
normally have a –10 circumstance penalty to use interaction
skills on animals, due to their Intellect and lack of language."""
    def __init__(self):
        super().__init__("Animal Empathy")
        self.init_no()

class Artificer(Advantage):
    """You can use the Expertise: Magic skill to create temporary
magical devices. See Magical Inventions, page 212, for
details"""
    def __init__(self):
        super().__init__("Artificer")
        self.init_no()


class Assessment(Advantage):
    """You’re able to quickly size up an opponent’s combat capabilities.
Choose a target you can accurately perceive and
have the GM make a secret Insight check for you as a free
action, opposed by the target’s Deception check result.
If you win, the GM tells you the target’s attack and defense
bonuses relative to yours (lower, higher, or equal). With
each additional degree of success, you learn one of the
target’s bonuses exactly.
If you lose the opposed roll, you don’t find out anything.
With more than one degree of failure, the GM may lie or
otherwise exaggerate the target’s bonuses."""
    def __init__(self):
        super().__init__("Assessment")
        self.init_no()

class Attractive(Advantage):
    """You’re particularly attractive, giving you a +2 circumstance
bonus on Deception and Persuasion checks to deceive,
seduce, or change the attitude of anyone who finds your
looks appealing. With a second rank, you are Very Attractive,
giving you a +5 circumstance bonus. This bonus does
not count as part of your regular skill bonus in terms of
the series power level, but also does not apply to people
or situations which (in the GM’s opinion) would not be influenced
by your appearance.
While superheroes tend to be a fairly good-looking lot,
this advantage is generally reserved for characters with
particularly impressive looks."""
    def __init__(self, rank):
        super().__init__("Attractive")
        self.init_flat(rank)

class Beginners_Luck(Advantage):
    """By spending a hero point, you gain an effective 5 ranks in
one skill of your choice you currently have at 4 or fewer
ranks, including skills you have no ranks in, even if they can’t
be used untrained. These temporary skill ranks last for the
duration of the scene and grant you their normal benefits."""
    def __init__(self):
        super().__init__("Beginner's Luck")
        self.init_no()

class Benefit(Advantage):
    """You have some significant perquisite or fringe benefit. The
exact nature of the benefit is for you and the Gamemaster
to determine. As a rule of thumb it should not exceed the
benefits of any other advantage, or a power effect costing
1 point (see Feature in the Powers chapter). It should also
be significant enough to cost at least 1 power point. An
example is Diplomatic Immunity (see Sample Benefits).
A license to practice law or medicine, on the other hand,
should not be considered a Benefit; it’s simply a part of
having training in the appropriate Expertise skill and has
no significant game effect.
Benefits may come in ranks for improved levels of the
same benefit. The GM is the final arbiter as to what does
and does not constitute a Benefit in the setting. Keep in
mind some qualities may constitute Benefits in some series,
but not in others, depending on whether or not they
have any real impact on the game.
Sample Benefits
The following are some potential Benefits. The GM is free
to choose any suitable Benefit for the series.
• Alternate Identity: You have an alternate identity,
complete with legal paperwork (driver’s license, birth
certificate, etc.). This is different from a costumed
identity, which doesn’t necessarily have any special
legal status (but may in some settings).
• Ambidexterity: You are equally adept using either
hand, suffering no circumstance penalty for using
your off-hand (as you don’t have one).
• Cipher: Your true history is well hidden, making it
difficult to dig up information about you. Investigation
checks concerning you are made at a –5 circumstance
penalty per rank in this benefit.
• Diplomatic Immunity: By dint of your diplomatic
status, you cannot be prosecuted for crimes in nations
other than your own. All another nation can do
is deport you to your home nation.
• Security Clearance: You have access to classified
government information, installations, and possibly
equipment and personnel.
• Status: By virtue of birth or achievement, you have
special status. Examples include nobility, knighthood,
aristocracy, and so forth.
• Wealth: You have greater than average wealth or
material resources, such as well-off (rank 1), independently
wealthy (rank 2), a millionaire (rank 3), multimillionaire
(rank 4), or billionaire (rank 5)."""
    def __init__(self, benefit_name, rank):
        super().__init__("Benefit")
        self.benefit_name = benefit_name
        self.init_flat(rank)

class Chokehold(Advantage):
    """If you successfully grab and restrain an opponent (see
Grab, page 248), you can apply a chokehold, causing your
opponent to begin suffocating for as long as you continue
to restrain your target (see Suffocation, page 238)."""
    def __init__(self):
        super().__init__("Chokehold")
        self.init_no()

class Close_Attack(Advantage):
    """You have a +1 bonus to close attacks checks per rank in
this advantage. Your total attack bonus is still limited by
power level. This advantage best suits characters with a
level of overall close combat skill (armed and unarmed).
For capability with a particular type of attack, use the
Close Combat skill."""
    def __init__(self, rank):
        super().__init__("Close Attack")
        self.init_flat(rank)

class Connected(Advantage):
    """You know people who can help you out from time to time.
It might be advice, information, help with a legal matter, or
access to resources. You can call in such favors by making a
Persuasion check. The GM sets the DC of the check, based
on the aid required. A simple favor is DC 10, ranging up to
DC 25 or higher for especially difficult, dangerous, or expensive
favors. You can spend a hero point to automatically
secure the favor, if the GM allows it. The GM has the right to
veto any request if it is too involved or likely to spoil the plot
of the adventure. Use of this advantage always requires at
least a few minutes (and often much longer) and the means
to contact your allies to ask for their help."""
    def __init__(self):
        super().__init__("Connected")
        self.init_no()

class Contacts(Advantage):
    """You have such extensive and well-informed contacts you
can make an Investigation check to gather information
in only one minute, assuming you have some means of
getting in touch with your contacts. Further Investigation
checks to gather information on the same subject require
the normal length of time, since you must go beyond your
immediate network of contacts."""
    def __init__(self):
        super().__init__("Contacts")
        self.init_no()

class Daze(Advantage):
    """You can make a Deception or Intimidation check as a
standard action (choose which skill when you acquire the
advantage) to cause an opponent to hesitate in combat.
Make a skill check as a standard action against your target’s
resistance check (the same skill, Insight, or Will defense,
whichever has the highest bonus). If you win, your
target is dazed (able to take only a standard action) until
the end of your next round. The ability to Daze with Deception
and with Intimidation are separate advantages.
Take this advantage twice in order to be able to do both."""
    def __init__(self, skill_list):
        super().__init__("Daze")
        self.list_value = skill_list
        rank = len(skill_list)
        self.init_flat(rank)

class Defensive_Attack(Advantage):
    """When you make a defensive attack (see Maneuvers, page
249), you can take a penalty of up to –5 on your attack
bonus and add the same number (up to +5) to both your
active defenses (Dodge and Parry)."""
    def __init__(self, rank):
        super().__init__("Defensive Attack")
        self.init_pyramid(rank)

class Defensive_Roll(Advantage):
    """You can avoid damage through agility and “rolling” with
an attack. You receive a bonus to your Toughness equal
to your advantage rank, but it is considered an active defense
similar to Dodge and Parry (see Active Defenses in
the Abilities chapter), so you lose this bonus whenever
you are vulnerable or defenseless. Your total Toughness,
including this advantage, is still limited by power level.
This advantage is common for heroes who lack either superhuman
speed or toughness, relying on their agility and
training to avoid harm."""
    def __init__(self, rank):
        super().__init__("Defensive Roll")
        self.init_flat(rank)

class Diehard(Advantage):
    """When your condition becomes dying (see Conditions
in the Action & Adventure chapter) you automatically
stabilize on the following round without any need for a
Fortitude check, although further damage—such as a finishing
attack—can still kill you."""
    def __init__(self):
        super().__init__("Diehard")
        self.init_no()

class Eidetic_Memory(Advantage):
    """You have perfect recall of everything you’ve experienced.
You have a +5 circumstance bonus on checks to remember
things, including resistance checks against effects that
alter or erase memories. You can also make Expertise skill
checks to answer questions and provide information as
if you were trained, meaning you can answer questions
involving difficult or obscure knowledge even without
ranks in the skill, due to the sheer amount of trivia you
have picked up."""
    def __init__(self):
        super().__init__("Eidetic Memory")
        self.init_no()

class Equipment(Advantage):
    """You have 5 points per rank in this advantage to spend on
equipment. This includes vehicles and headquarters. See
the Gadgets & Gear chapter for details on equipment and
its costs. Many heroes rely almost solely on Equipment in
conjunction with their skills and other advantages."""
    def __init__(self, rank):
        super().__init__("Defensive Roll")
        self.init_flat(rank)

class Evasion(Advantage):
    """You have a +2 circumstance bonus to Dodge resistance
checks to avoid area effects (see the Area extra in the
Powers chapter). If you have 2 ranks in this advantage,
your circumstance bonus increases to +5."""
    def __init__(self, rank):
        super().__init__("Evasion")
        self.init_pyramid(rank)

class Extraordinary_Effort(Advantage):
    """When using extra effort (see Extra Effort in The Basics
chapter), you can gain two of the listed benefits, even
stacking two of the same type of benefit. However, you
also double the cost of the effort; you’re exhausted starting
the turn after your extraordinary effort. If you are already
fatigued, you are incapacitated. If you are already
exhausted, you cannot use extraordinary effort. Spending
a hero point at the start of your next turn reduces the cost
of your extraordinary effort to merely fatigued, the same
as a regular extra effort."""
    def __init__(self):
        super().__init__("Extraordinary Effort")
        self.init_no()

class Fascinate(Advantage):
    """One of your interaction skills is so effective you can capture
and hold other’s attention with it. Choose Deception,
Intimidation, or Persuasion when you acquire this
advantage. You can also use Fascinate with an appropriate
Expertise skill, like musician or singer, at the GM’s
discretion.
You are subject to the normal guidelines for interaction
skills, and combat or other immediate danger makes this
advantage ineffective. Take a standard action and make
an interaction skill check against your target’s opposing
check (Insight or Will defense). If you succeed, the target is
entranced. You can maintain the effect with a standard action
each round, giving the target a new resistance check.
The effect ends when you stop performing, the target successfully
resists, or any immediate danger presents itself.
Like all interaction skills, you can use Fascinate on a group,
but you must affect everyone in the group in the same
way.
You may take this advantage more than once. Each time, it
applies to a different skill."""
    def __init__(self, skill_list):
        super().__init__("Fascinate")
        self.list_value = skill_list
        rank = len(skill_list)
        self.init_flat(rank)

class Fast_Grab(Advantage):
    """When you hit with an unarmed attack you can immediately
make a grab check against that opponent as a free
action (see Grab, page 248). Your unarmed attack inflicts
its normal damage and counts as the initial attack check
required to grab your opponent."""
    def __init__(self):
        super().__init__("Fast Grab")
        self.init_no()

class Favored_Environment(Advantage):
    """You have an environment you’re especially suited for
fighting in. Examples include in the air, underwater, in
space, in extreme heat or cold, in jungles or woodlands,
and so forth. While you are in your favored environment,
you gain a +2 circumstance bonus to attack checks or your
active defenses. Choose at the start of the round whether
the bonus applies to attack or defense. The choice remains
until the start of your next round. This circumstance bonus
is not affected by power level."""
    def __init__(self, environment_list):
        super().__init__("Favored Environment")
        self.list_value = environment_list
        rank = len(environment_list)
        self.init_flat(rank)

class Favored_Foe(Advantage):
    """You have a particular type of opponent you’ve studied or
are especially effective against. It may be a type of creature
(aliens, animals, constructs, mutants, undead, etc.), a profession
(soldiers, police officers, Yakuza, etc.) or any other
category the GM approves. Especially broad categories
like “humans” or “villains” are not permitted. You gain a +2
circumstance bonus on Deception, Intimidation, Insight,
and Perception checks dealing with your Favored Foe. This
circumstance bonus is not limited by power level."""
    def __init__(self, foe_list):
        super().__init__("Favored Foe")
        self.list_value = foe_list
        rank = len(self.list_value)
        self.init_flat(rank)

class Fearless(Advantage):
    """You are immune to fear effects of all sorts, essentially the
same as an Immunity to Fear effect (see Immunity in the
Powers chapter)."""
    def __init__(self):
        super().__init__("Fearless")
        self.init_no()

class Grabbing_Finesse(Advantage):
    """You can use your Dexterity bonus, rather than your
Strength bonus, to make grab attacks. You are not vulnerable
while grabbing. See Grab, page 248, for details. This
is a good advantage for skilled unarmed combatants focused
more on speed than strength."""
    def __init__(self):
        super().__init__("Grabbing Finesse")
        self.init_no()

class Great_Endurance(Advantage):
    """You have a +5 bonus on checks to avoid becoming fatigued
and checks to hold your breath, avoid damage
from starvation or thirst, avoid damage from hot or cold
environments, and to resist suffocation and drowning.
See Hazards and the Environment in the Action & Adventure
chapter for details on these checks."""
    def __init__(self):
        super().__init__("Great Endurance")
        self.init_no()

class Hide_In_Plain_Sight(Advantage):
    """You can hide (see Hiding under Stealth in the Skills
chapter) without any need for a Deception or Intimidation
check or any sort of diversion, and without penalty
to your Stealth check. You’re literally there one moment,
and gone the next. You must still have some form of cover
or concealment within range of your normal movement
speed in order to hide."""
    def __init__(self):
        super().__init__("Hide In Plain Sight")
        self.init_no()

class Improved_Aim(Advantage):
    """You have an even keener eye when it comes to ranged
combat. When you take a standard action to aim, you
gain double the normal circumstance bonus: +10 for a
close attack or ranged attack adjacent to the target, +5
for a ranged attack at a greater distance. See Aim, page
246, for details."""
    def __init__(self):
        super().__init__("Improved Aim")
        self.init_no()

class Improved_Critical(Advantage):
    """Increase your critical threat range with a particular attack
(chosen when you acquire this advantage) by 1, allowing
you to score a critical hit on a natural 19 or 20. Only
a natural 20 is an automatic hit, however, and an attack
that misses is not a critical. Each additional rank applies
to a different attack or increases your threat range with an
existing attack by one more, to a maximum threat range
of 16-20 with 4 ranks."""
    def __init__(self, skill, rank):
        super().__init__("Improved Critical")
        self.skill = skill
        self.init_pyramid(rank)

class Improved_Defense(Advantage):
    """When you take the defend action in combat (see Defend
in the Action & Adventure chapter) you gain a +2 circumstance
bonus to your active defense checks for the
round."""
    def __init__(self):
        super().__init__("Improved Defense")
        self.init_no()

class Improved_Disarm(Advantage):
    """You have no penalty to your attack check when attempting
to disarm an opponent and they do not get the opportunity
to disarm you (see Disarm in the Action & Adventure
chapter)."""
    def __init__(self):
        super().__init__("Improved Disarm")
        self.init_no()

class Improved_Grab(Advantage):
    """You can make grab attacks with only one arm, leaving
the other free. You can also maintain the grab while using
your other hand to perform actions. You are not vulnerable
while grabbing (see Grabbing in the Action & Adventure
chapter)."""
    def __init__(self):
        super().__init__("Improved Grab")
        self.init_no()

class Improved_Hold(Advantage):
    """Your grab attacks are particularly difficult to escape. Opponents
you grab suffer a –5 circumstance penalty on
checks to escape."""
    def __init__(self):
        super().__init__("Improved Hold")
        self.init_no()

class Improved_Initiative(Advantage):
    """You have a +4 bonus to your initiative checks per rank in
this advantage."""
    def __init__(self, rank):
        super().__init__("Improved Initiative")
        self.init_flat(rank)

class Improved_Smash(Advantage):
    """You have no penalty to attack checks to hit an object held
by another character (see Smash in the Action & Adventure
chapter)."""
    def __init__(self):
        super().__init__("Improved Smash")
        self.init_no()

class Improved_Trip(Advantage):
    """You have no penalty to your attack check to trip an opponent
and they do not get the opportunity to trip you.
When making a trip attack, make an opposed check of
your Acrobatics or Athletics against your opponent’s Acrobatics
or Athletics, you choose which your opponent
uses to defend, rather than the target choosing (see Trip
in the Action & Adventure chapter). This is a good martial
arts advantage for unarmed fighters."""
    def __init__(self):
        super().__init__("Improved Trip")
        self.init_no()

class Improvised_Tools(Advantage):
    """You ignore the circumstance penalty for using skills without
proper tools, since you can improvise sufficient tools
with whatever is at hand. If you’re forced to work without
tools at all, you suffer only a –2 penalty."""
    def __init__(self):
        super().__init__("Improvised Tools")
        self.init_no()

class Improvised_Weapon(Advantage):
    """When wielding an improvised close combat weapon—
anything from a chair to a telephone pole or entire car—
you use your Close Combat: Unarmed skill bonus for attack
checks with the “weapon” rather than relying on your
general Close Combat skill bonus. Additional ranks in this
advantage give you a +1 bonus to Damage with improvised
weapons per rank. Your maximum Damage bonus is
still limited by power level, as usual."""
    def __init__(self, rank):
        super().__init__("Improvised Weapon")
        self.init_flat(rank)

class Inspire(Advantage):
    """You can inspire your allies to greatness. Once per scene, by
taking a standard action and spending a hero point, allies
able to interact with you gain a +1 circumstance bonus per
Inspire rank on all checks until the start of your next round,
with a maximum bonus of +5. You do not gain the bonus,
only your allies do. The inspiration bonus ignores power
level limits, like other uses of hero points. Multiple uses of
Inspire do not stack, only the highest bonus applies."""
    def __init__(self, rank):
        super().__init__("Inspire")
        self.init_flat(rank)

class Instant_Up(Advantage):
    """You can go from prone to standing as a free action without
the need for an Acrobatics skill check."""
    def __init__(self):
        super().__init__("Instant Up")
        self.init_no()

class Interpose(Advantage):
    """Once per round, when an ally within range of your normal
movement is hit by an attack, you can choose to place
yourself between the attacker and your ally as a reaction,
making you the target of the attack instead. The attack
hits you rather than your ally, and you suffer the effects
normally. You cannot use this advantage against area effects
or perception range attacks, only those requiring an
attack check."""
    def __init__(self, rank):
        super().__init__("Interpose")
        self.init_pyramid(rank)

class Inventor(Advantage):
    """You can use the Technology skill to create inventions. See
Inventing, page 211, for details."""
    def __init__(self):
        super().__init__("Inventor")
        self.init_no()

class Jack_Of_All_Trades(Advantage):
    """You can use any skill untrained, even skills or aspects of
skills that normally cannot be used untrained, although
you must still have proper tools if the skill requires them"""
    def __init__(self):
        super().__init__("Jack-of-all-Trades")
        self.init_no()

class Languages(Advantage):
    """You can speak and understand additional languages.
With one rank in this advantage, you know an additional
language. For each additional rank, you double your additional
known languages: two at rank 2, four at rank 3,
eight at rank 4, etc. So a character with Languages 7 is fluent
in 64 languages! Characters are assumed to be fluent
in any languages they know, including being able to read
and write in them.
For the ability to understand any language, see the Comprehend
effect in the Powers chapter."""
    def __init__(self, language_list, rank):
        super().__init__("Languages")
        self.list_value = language_list
        self.init_flat(rank)

class Leadership(Advantage):
    """Your presence reassures and lends courage to your allies.
As a standard action, you can spend a hero point to remove one
of the following conditions from an ally with whom you can
interact: dazed, fatigued, or stunned."""
    def __init__(self):
        super().__init__("Leadership")
        self.init_no()

class Luck(Advantage):
    """Once per round, you can choose to re-roll a die roll, like
spending a hero point (see Hero Points, page 20), including
adding 10 to re-rolls of 10 or less. You can do this a
number of times per game session equal to your Luck
rank, with a maximum rank of half the series power level
(rounded down). Your Luck ranks refresh when your hero
points “reset” at the start of an adventure. The GM may
choose to set a different limit on ranks in this advantage,
depending on the series."""
    def __init__(self, rank):
        super().__init__("Luck")
        self.init_pyramid(rank)

class Minion(Advantage):
    """You have a follower or minion. This minion is an independent
character with a power point total of (advantage
rank x 15). Minions are subject to the normal power level
limits, and cannot have minions themselves. Your minions
(if capable of independent thought) automatically have a
helpful attitude toward you. They are subject to the normal
rules for minions (see page 245).
Minions do not earn power points. Instead, you must spend
earned power points to increase your rank in this advantage
to improve the minion’s power point total and traits.
Minions also do not have hero points. Any lost minions are
replaced in between adventures with other followers with
similar abilities at the Gamemaster’s discretion."""
    def __init__(self, minion_name, rank):
        super().__init__("Minion")
        self.minion_name = minion_name
        self.init_flat(rank)

class Move_By_Action(Advantage):
    """When taking a standard action and a move action you can
move both before and after your standard action, provided
the total distance moved isn’t greater than your normal
movement speed."""
    def __init__(self):
        super().__init__("Move-By Action")
        self.init_no()

class Power_Attack(Advantage):
    """When you make a power attack (see Maneuvers, page
250) you can take a penalty of up to –5 on your attack
bonus and add the same number (up to +5) to the effect
bonus of your attack."""
    def __init__(self, rank):
        super().__init__("Power Attack")
        self.init_pyramid(rank)

class Precise_Attack(Advantage):
    """When you make close or ranged attacks (choose one) you
ignore attack check penalties for cover or concealment
(choose one), although total cover still prevents you from
making attacks. Each additional rank in this advantage lets
you choose an additional option, so with Precise Attack 4,
all your attacks (both close and ranged) ignore penalties
for both cover and concealment."""
    def __init__(self, penalty_list):
        super().__init__("Precise_Attack")
        self.list_value = penalty_list
        rank = len(self.list_value)
        self.init_flat(rank)

class Prone_Fighting(Advantage):
    """You suffer no circumstance penalty to attack checks for
being prone, and adjacent opponents do not gain the
usual circumstance bonus for close attacks against you."""
    def __init__(self):
        super().__init__("Prone Fighting")
        self.init_no()

class Quick_Draw(Advantage):
    """You can draw a weapon from a holster or sheath as a free
action, rather than a move action."""
    def __init__(self,rank):
        super().__init__("Quick Draw")
        self.init_flat(rank)

class Ranged_Attack(Advantage):
    """You have a +1 bonus to ranged attacks checks per rank in
this advantage. Your total attack bonus is still limited by
power level."""
    def __init__(self,rank):
        super().__init__("Ranged Attack")
        self.init_flat(rank)

class Redirect(Advantage):
    """If you successfully trick an opponent (see Trick under Deception
in the Skills chapter), you can redirect a missed
attack against you from that opponent at another target
as a reaction. The new target must be adjacent to you and
within range of the attack. The attacker makes a new attack
check with the same modifiers as the first against the
new target."""
    def __init__(self, rank):
        super().__init__("Redirect")
        self.init_pyramid(rank)

class Ritualist(Advantage):
    """You can use the Expertise: Magic skill to create and cast
magical rituals (see page 212). This advantage is often a
back-up or secondary magical power for superhuman
sorcerers, and may be the only form of magic available to
some “dabbler” types."""
    def __init__(self):
        super().__init__("Ritualist")
        self.init_no()

class Second_Chance(Advantage):
    """Choose a particular hazard, such as falling, being tripped,
triggering traps, mind control (or another fairly specific
power effect, such as Damage with the fire descriptor) or
a particular skill with consequences for failure. If you fail a
check against that hazard, you can make another immediately
and use the better of the two results. You only get
one second chance for any given check, and the GM decides
if a particular hazard or skill is an appropriate focus
for this advantage. You can take this advantage multiple
times, each for a different hazard."""
    def __init__(self, chance_list):
        super().__init__("Second Chance")
        self.list_value = chance_list
        rank = len(self.list_value)
        self.init_flat(rank)

class Seize_Initiative(Advantage):
    """You can spend a hero point to automatically go first in the
initiative order. You may only do so at the start of combat,
when you would normally make your initiative check.
If more than one character uses this advantage, they all
make initiative checks normally and act in order of their
initiative result, followed by all the other characters who
do not have this advantage."""
    def __init__(self):
        super().__init__("Seize Initiative")
        self.init_no()

class Set_Up(Advantage):
    """You can transfer the benefits of a successful combat use of
an interaction skill to your teammate(s). For example, you
can feint and have your target vulnerable against one or
more allies next attack(s), rather than yours. Each rank in
the advantage lets you transfer the benefit to one ally. The
interaction skill check requires its normal action, and the
affected allies must be capable of interacting with you (or
at least seeing the set-up) to benefit from it."""
    def __init__(self, rank):
        super().__init__("Set-Up")
        self.init_pyramid(rank)

class Sidekick(Advantage):
    """You have another character serving as your partner and
aide. Create your sidekick as an independent character
with (advantage rank x 5) power points, and subject to the
series power level. A sidekick’s power point total must be
less than yours. Your sidekick is an NPC, but automatically
helpful and loyal to you. Gamemasters should generally
allow you to control your sidekick, although sidekicks remain
NPCs and the GM has final say in their actions.
Sidekicks do not earn power points. Instead, you must
spend earned power points to increase your rank in Sidekick
to improve the sidekick’s power point total and traits;
each point you spend to increase your rank in Sidekick
grants the sidekick 5 additional power points. Sidekicks
also do not have hero points, but you can spend your own
hero points on the sidekick’s behalf with the usual benefits.
Sidekicks are not minions, but full-fledged characters,
so they are not subject to the minion rules."""
    def __init__(self, sidekick_name, rank):
        super().__init__("Sidekick")
        self.sidekick_name = sidekick_name
        self.init_flat(rank)

class Skill_Mastery(Advantage):
    """Choose a skill. You can make routine checks with that skill
even when under pressure (see Routine Checks in The
Basics chapter). This advantage does not allow you to
make routine checks with skills that do not normally allow
you to do so. You can take this advantage multiple times
for different skills."""
    def __init__(self, skill_list):
        super().__init__("Skill Mastery")
        self.list_value = skill_list
        rank = len(skill_list)
        self.init_flat(rank)

class Startle(Advantage):
    """You can use Intimidation rather than Deception to feint in
combat (see Feint under the Deception skill description).
Targets resist with Insight, Intimidation, or Will defense."""
    def __init__(self):
        super().__init__("Startle")
        self.init_no()

class Takedown(Advantage):
    """If you render a minion incapacitated with an attack, you
get an immediate extra attack as a free action against another
minion within range and adjacent to the previous
target’s location. The extra attack is with the same attack
and bonus as the first. You can continue using this advantage
until you miss or there are no more minions within
range of your attack or your last target.
A second rank in this advantage allows you to attack nonadjacent
minion targets, moving between attacks if necessary
to do so. You cannot move more than your total
speed in the round, regardless of the number of attacks
you make. You stop attacking once you miss, run out of
movement, or there are no more minions within range of
your attack."""
    def __init__(self, rank):
        super().__init__("Takedown")
        self.init_pyramid(rank)

class Taunt(Advantage):
    """You can demoralize an opponent with Deception rather
than Intimidation (see Demoralize under the Intimidation
skill description), disparaging and undermining confidence
rather than threatening. Targets resist using Deception,
Insight, or Will defense."""
    def __init__(self):
        super().__init__("Taunt")
        self.init_no()

class Teamwork(Advantage):
    """You’re effective at helping out your friends. When you
support a team check (see Team Checks in The Basics
chapter) you have a +5 circumstance bonus to your
check. This bonus also applies to the Aid action and
Team Attacks."""
    def __init__(self):
        super().__init__("Teamwork")
        self.init_no()

class Throwing_Mastery(Advantage):
    """You have a +1 damage bonus with thrown weapons per
rank in this advantage. You can also throw normally harmless
objects—playing cards, pens, paper clips, and so
forth—as weapons with a damage bonus equal to your
advantage rank and range based on the higher of your
advantage rank or Strength (see Ranged in the Powers
chapter). Your maximum damage bonus with any given
weapon or attack is still limited by power level."""
    def __init__(self, rank):
        super().__init__("Throwing Mastery")
        self.init_flat(rank)

class Tracking(Advantage):
    """You can use the Perception skill to visually follow tracks
like the Tracking Senses effect (see the Powers chapter)."""
    def __init__(self):
        super().__init__("Tracking")
        self.init_no()

class Trance(Advantage):
    """Through breathing and bodily control, you can slip into a
deep trance. This takes a minute of uninterrupted meditation
and a DC 15 Awareness check. While in the trance
you add your Awareness rank to your Stamina rank to determine
how long you can hold your breath and you use
the higher of your Fortitude or Will defenses for resistance
checks against suffocation (see Suffocation, page 238).
Poison and disease effects are suspended for the duration
of the trance. It requires a Perception check with a DC
equal to your Awareness check result to determine you’re
not dead because your bodily functions are so slow. You
are aware of your surroundings while in trance and can
come out of it at any time at will. You cannot take any actions
while in the trance, but your GM may allow mental
communication while in a trance."""
    def __init__(self):
        super().__init__("Trance")
        self.init_no()

class Ultimate_Effort(Advantage):
    """You can spend a hero point on a particular check and
treat the roll as a 20 (meaning you don’t need to roll the
die at all, just apply a result of 20 to your modifier). This
is not a natural 20, but is treated as a roll of 20 in all other
respects. You choose the particular check the advantage
applies to when you acquire it and the GM must approve
it. You can take Ultimate Effort multiple times, each time,
it applies to a different check. This advantage may not
be used after you’ve rolled the die to determine if you
succeed."""
    def __init__(self, skill_list):
        super().__init__("Ultimate Effort")
        self.list_value = skill_list
        rank = len(skill_list)
        self.init_flat(rank)

class Uncanny_Dodge(Advantage):
    """You are especially attuned to danger. You are not
vulnerable when surprised or otherwise caught off-guard. You are
still made vulnerable by effects that limit your mobility."""
    def __init__(self):
        super().__init__("Uncanny Dodge")
        self.init_no()

class Weapon_Bind(Advantage):
    """If you take the defend action (see Defend in the Action
& Adventure chapter) and successfully defend against
a close weapon attack, you can make a disarm attempt
against the attacker immediately as a reaction. The disarm
attempt is carried out normally, including the attacker
getting the opportunity to disarm you."""
    def __init__(self):
        super().__init__("Weapon Bind")
        self.init_no()

class Weapon_Break(Advantage):
    """If you take the defend action (see Defend in the Action
& Adventure chapter) and successfully defend against
a close weapon attack, you can make an attack against
the attacker’s weapon immediately as a reaction. This
requires an attack check and inflicts normal damage to the
weapon if it hits (see Smash in the Action & Adventure
chapter)."""
    def __init__(self):
        super().__init__("Weapon Break")
        self.init_no()

class Well_Informed(Advantage):
    """You are exceptionally well-informed. When encountering
an individual, group, or organization for the first time, you
can make an immediate Investigation or Persuasion skill
check to see if your character has heard something about
the subject. Use the guidelines for gathering information
in the Investigation skill description to determine the level
of information you gain. You receive only one check per
subject upon first encountering them, although the GM
may allow another upon encountering the subject again
once significant time has passed."""
    def init(self):
        super().init("Well Informed")
        self.init_no()

combat_adv = """Accurate Attack Trade effect DC for attack bonus.
All-out Attack Trade active defense for attack bonus.
Chokehold Suffocate an opponent you have successfully grabbed.
Close Attack +1 bonus to close attack checks per rank.
Defensive Attack Trade attack bonus for active defense bonus.
Defensive Roll +1 active defense bonus to Toughness per rank.
Evasion Circumstance bonus to avoid area effects.
Fast Grab Make a free grab check after an unarmed attack.
Favored Environment Circumstance bonus to attack or defense in an environment.
Grabbing Finesse Substitute Dex for Str when making grab attacks.
Improved Aim Double circumstance bonuses for aiming.
Improved Critical +1 to critical threat range with an attack per rank.
Improved Defense +2 bonus to active defense when you take the defend action.
Improved Disarm No penalty for the disarm action.
Improved Grab Make grab attacks with one arm. Not vulnerable while grabbing.
Improved Hold –5 circumstance penalty to escape from your holds.
Improved Initiative +4 bonus to initiative checks per rank.
Improved Smash No penalty for the smash action.
Improved Trip No penalty for the trip action.
Improvised Weapon Use Unarmed Combat skill with improvised weapons, +1 damage bonus.
Move-by Action Move both before and after your standard action.
Power Attack Trade attack bonus for effect bonus.
Precise Attack Ignore attack check penalties for either cover or concealment.
Prone Fighting No penalties for fighting while prone.
Quick Draw Draw a weapon as a free action.
Ranged Attack +1 bonus to ranged attack checks per rank.
Redirect Use Deception to redirect a missed attack at another target.
Set-up Transfer the benefit of an interaction skill to an ally.
Takedown Free extra attack when you incapacitate a minion.
Throwing Mastery +1 damage bonus with thrown weapons per rank.
Uncanny Dodge Not vulnerable when surprised or caught off-guard.
Weapon Bind Free disarm attempt when you actively defend.
Weapon Break Free smash attack when you actively defend."""

fortune_adv = """Beginner’s Luck Spend a hero point to gain 5 temporary ranks in a skill.
Inspire Spend a hero point to grant allies a +1 circumstance bonus per rank.
Leadership Spend a hero point to remove a condition from an ally.
Luck Re-roll a die roll once per rank.
Seize Initiative Spend a hero point to go first in the initiative order.
Ultimate Effort Spend a hero point to get an effective 20 on a specific check."""

general_adv = """Assessment Use Insight to learn an opponent’s combat capabilities.
Benefit Gain a significant perquisite or fringe benefit.
Diehard Automatically stabilize when dying.
Eidetic Memory Total recall, +5 circumstance bonus to remember things.
Equipment 5 points of equipment per rank.
Extraordinary Effort Gain two benefits when using extra effort.
Fearless Immune to fear effects.
Great Endurance +5 on checks involving endurance.
Instant Up Stand from prone as a free action.
Interpose Take an attack meant for an ally.
Minion Gain a follower or minion with (15 x rank) power points.
Second Chance Re-roll a failed check against a hazard once.
Sidekick Gain a sidekick with (5 x rank) power points.
Teamwork +5 bonus to support team checks.
Trance Go into a deathlike trance that slows bodily functions."""

skill_adv = """Agile Feint Feint using Acrobatics skill or movement speed.
Animal Empathy Use interaction skills normally with animals.
Artificer Use Expertise: Magic to create temporary magical devices.
Attractive Circumstance bonus to interaction based on your looks.
Connected Call in assistance or favors with a Persuasion check.
Contacts Make an initial Investigation check in one minute.
Daze Use Deception or Intimidation to daze an opponent.
Fascinate Use an interaction skill to entrance others.
Favored Foe Circumstance bonus to checks against a type of opponent.
Hide in Plain Sight Hide while observed without need for a diversion.
Improvised Tools No penalty for using skills without tools.
Inventor Use Technology to create temporary devices.
Jack-of-all-trades Use any skill untrained.
Languages Speak and understand additional languages.
Ritualist Use Expertise: Magic to create and perform rituals.
Skill Mastery Make routine checks with one skill under any conditions.
Startle Use Intimidation to feint in combat.
Taunt Use Deception to demoralize in combat.
Tracking Use Perception to follow tracks.
Well-informed Immediate Investigation or Persuasion check to know something"""