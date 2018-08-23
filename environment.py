import character
import timeline
import rooms
import powers

class Environment:
    def __init__(self):
        self.room_list = []
        self.clock = timeline.Timeline()


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

    men.add_power(vm)
    cer.add_power(mf)

    men.print_character_sheet()
    print(men.print_character_sheet())

    cer.print_character_sheet()
    print(cer.print_character_sheet())

    vm.execute_power(None)