
import timeline

class Environment:
    def __init__(self):
        self.room_list = []
        self.clock = timeline.Timeline()

class Seperator:
    def __init__(self):
        self.rooms_connected = []
        self.connector_details = []

class Room:
    def __init__(self):
        self.x_total = 0
        self.y_total = 0
        self.z_total = 0
        self.objects_inside = []
