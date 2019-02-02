import character
import timeline
import rooms
import powers
from senses import senses
import artificial_intelligence

class Environment:
    def __init__(self):
        self.room_list = []
        self.character_list = []
        self.object_list = []
        self.clock = timeline.Timeline()

    def add_character(self, chara):
        self.character_list.append(chara)

    def advance_clock(self):
        e = self.clock.pop_event()
        self.execute_event(e)

    def add_event(self, timeline_event):
        self.clock.add_event(timeline_event)

    def execute_event(self, event):
        event.get_event().execute_event()

    def get_time(self):
        return self.clock.get_time()

class Event:
    def __init__(self, event_dict):
        self.event_information = event_dict

    def add_to_environment(self, env):
        cnt = timeline.Initiative(timeline.Round_Schedule.AFTER)
        rnd = None
        tie = timeline.Round_Schedule.AFTER
        if 'Initiative Count' in self.event_information:
            cnt = self.event_information['Initiative Count']
        if 'Initiative Tiebreaker' in self.event_information:
            tie = self.event_information['Initiative Tiebreaker']
        if 'Initiative Round' in self.event_information:
            rnd = self.event_information['Initiative Round']
        else:
            rnd = env.get_time().get_round()
            self.event_information['Initiative Round'] = rnd
        tent = timeline.Timeline_Entry(cnt, rnd, tiebreaker=tie)
        teve = timeline.Timeline_Event.from_time_event(tent, self)
        env.add_event(teve)
        self.event_information['Environment'] = env
        
    def execute_event(self):
        pass

class Character_Turn(Event):
    def __init__(self, init_count, init_tiebreak, character):
        super().__init__({})
        self.event_information['Initiative Count'] = init_count
        self.event_information['Initiative Tiebreaker'] = init_tiebreak
        self.event_information['Power User'] = character
        
    def execute_event(self):
        turn = self.event_information['Power User'].generate_turn()
        turn.execute_actions()
        self.event_information['Initiative Round'] += 1
        self.add_to_environment(self.event_information['Environment'])


if __name__ == "__main__":
    r1 = rooms.Room()

    men = character.CharacterGenerators.default_char("Doctor Menlo", 10, "Defense")
    cer = character.CharacterGenerators.default_char("Cerulean", 10, "Toughness")

    men_loc = rooms.Room_Object(0,0,0,men,r1)
    cer_loc = rooms.Room_Object(0,0,0,cer,r1)

    vm = powers.Attack("Voltaic Manipulator", "Ranged Combat: Hypersuit Blasters", 10, "Dodge",
                       character.Character.get_toughness, character.Character.get_toughness,
                       modifier_values={'Ranged':'default'})
    mf = powers.Attack("Metal Flow", "Melee Combat: Martial Arts", 10, "Parry", character.Character.get_toughness,
                       character.Character.get_toughness)

    og = powers.Senses("Omniglasses", {})



    tv = senses.Tracking()
    tv.set_sense_type(senses.Sense_Type_Designation.VISUAL)
    og.add_sense_flag(tv)

    ta = senses.Tracking()
    ta.set_sense_type(senses.Sense_Type_Designation.AUDITORY)
    og.add_sense_flag(ta)

    aa = senses.Accurate(modifiers={"Flag Type": "Auditory"})
    og.add_sense_flag(aa)

    ms = senses.Microscopic_Vision(modifiers={"Flag Type": "Visual", "Rank":4})
    og.add_sense_flag(ms)

    av = senses.Analytical(modifiers={"Flag Type": "Visual", "Rank":1})
    og.add_sense_flag(av)

    dt = senses.Detect(modifiers={"Flag Type": "Mental", "Rank":2, "Descriptor":"Electricity"})
    og.add_sense_flag(dt)

    iv = senses.Infravision(modifiers={})
    og.add_sense_flag(iv)

    print("Sense type: %s [%s]" % (av.get_sense_type(), av.get_narrow()))

    men.set_skill_ranks("Ranged Combat: Hypersuit Blasters", 10)
    cer.set_skill_ranks("Melee Combat: Martial Arts", 10)

    men.add_power(vm)
    men.add_power(og)
    cer.add_power(mf)

    men.print_character_sheet()
    cer.print_character_sheet()

    print(men.print_character_sheet())
    print(cer.print_character_sheet())

    men_init = men.roll_initiative()
    cer_init = cer.roll_initiative()

    print("%s initiative count: %d" % (men.get_name(), men_init))
    print("%s initiative count: %d" % (cer.get_name(), cer_init))

    men_turn = Character_Turn(men_init, men.get_initiative(), men)
    cer_turn = Character_Turn(cer_init, cer.get_initiative(), cer)

    en = Environment()

    men_turn.add_to_environment(en)
    cer_turn.add_to_environment(en)

    men_ai = artificial_intelligence.Artificial_Intelligence(men, en)
    cer_ai = artificial_intelligence.Artificial_Intelligence(cer, en)

    men_ob = artificial_intelligence.Objective({'Type':artificial_intelligence.Objective_Type.DEFEAT_TARGET,
                                                'Target':cer, 'Weight':1})
    cer_ob = artificial_intelligence.Objective({'Type':artificial_intelligence.Objective_Type.DEFEAT_TARGET,
                                                'Target':men, 'Weight':1})

    men_ai.add_objective(men_ob)
    cer_ai.add_objective(cer_ob)

    men_wins = 0
    cer_wins = 0

    print(men.get_sense_cluster())

    execute_data = powers.Power_Execution_Data({"Self": men, "Target": men})

    og.execute_power(execute_data)

    print(men.get_sense_cluster())

    print(men.get_sense_cluster().get_total_senses()[senses.Sense_Type_Designation.VISUAL]['Ordinary Frequencies'].get_mask_tag())


