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