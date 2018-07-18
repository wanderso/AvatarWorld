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


class Accurate_Attack(Advantage):
    """When you make an accurate attack (see Maneuvers, page
    249) you can take a penalty of up to –5 on the effect modifier
    of the attack and add the same number (up to +5) to
    your attack bonus."""

    def __init__(self, rank):
        super().__init__("Accurate Attack")
        self.advantage_cost = 0
        self.advantage_cost_type = Cost_Type.PYRAMID_RANK
        self.advantage_rank = rank
        self.advantage_func_list = None
        self.calculate_cost = self.pyramid_cost





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