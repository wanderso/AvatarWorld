import character
import timeline
import rooms
import powers
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
        print("%s's turn" % self.event_information['Power User'].get_name())
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

    men.set_skill_ranks("Ranged Combat: Hypersuit Blasters", 10)
    cer.set_skill_ranks("Melee Combat: Martial Arts", 10)


    men.add_power(vm)
    cer.add_power(mf)

    men.print_character_sheet()
    print(men.print_character_sheet())

    cer.print_character_sheet()
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

    print(vm.get_name())


    men_wins = 0
    cer_wins = 0

    for _ in range(0,1000):
        men.generate_health_classic()
        cer.generate_health_classic()
        while not men.has_condition("Incapacitated") and not cer.has_condition("Incapacitated"):
            en.advance_clock()
        if men.has_condition("Incapacitated"):
            cer_wins += 1
        if cer.has_condition("Incapacitated"):
            men_wins += 1

    print("Menlo wins: %d, Cerulean wins: %d" % (men_wins, cer_wins))




    