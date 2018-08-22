import character
import timeline

class Environment:
    def __init__(self):
        self.room_list = []
        self.clock = timeline.Timeline()

class Separator:
    def __init__(self):
        self.rooms_connected = []
        self.connector_details = []

class Room:
    def __init__(self):
        self.x_total = 0
        self.y_total = 0
        self.z_total = 0
        self.objects_inside = []

    def add_object_to_room(self,r_obj):
        pass

class Room_Object:
    def __init__(self,x,y,z,obj,room):
        self.x = x
        self.y = y
        self.z = z
        room.add_object_to_room(self)

if __name__ == "__main__":

    r1 = Room()

    men = character.CharacterGenerators.default_char("Doctor Menlo", 10, "Defense")
    cer = character.CharacterGenerators.default_char("Cerulean", 10, "Toughness")

    men_loc = Room_Object(0,0,0,men,r1)
    cer_loc = Room_Object(0,0,0,cer,r1)

    men.print_character_sheet()
    print(men.print_character_sheet())

    cer.print_character_sheet()
    print(cer.print_character_sheet())