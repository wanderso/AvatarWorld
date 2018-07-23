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
        super().__init__("Eidetic Memory")
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