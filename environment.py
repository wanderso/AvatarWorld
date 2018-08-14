import heapq

class Environment:
    def __init__(self):
        self.room_list = []
        self.clock = Timeline()

class Room:
    def __init__(self):
        self.x_total = 0
        self.y_total = 0
        self.z_total = 0
        self.objects_inside = []

class Timeline:
    def __init__(self):
        self.current_time = Round(0)
        self.heap_timeline = []

    def add_event(self, time, event):
        heapq.heappush(self.heap_timeline,(time, event))

    def top_event(self):
        if len(self.heap_timeline > 0):
            return self.heap_timeline[0]
        else:
            return None

class Round:
    def __init__(self, rnd):
        self.round_number = rnd


class Initiative:
    def __eq__(self, other):
        return self.initiative_count == other.initiative_count

    def __gt__(self, other):
        if (self.initiative_count == "Before") != (other.initiative_count == "Before"):
            return (other.initiative_count == "Before")
        elif (self.initiative_count == "After") != (other.initiative_count == "After"):
            return (self.initiative_count == "After")
        else:
            return (self.initiative_count > other.initiative_count)

    def __lt__(self, other):
        if (self.initiative_count == "Before") != (other.initiative_count == "Before"):
            return (self.initiative_count == "Before")
        elif (self.initiative_count == "After") != (other.initiative_count == "After"):
            return (other.initiative_count == "After")
        else:
            return (self.initiative_count < other.initiative_count)

    def __init__(self, clk):
        self.initiative_count = clk

if __name__ == "__main__":
    i1 = Initiative("Before")
    i2 = Initiative(25)
    i3 = Initiative("Before")
    if i1 != i2:
        print("This works!")
        print(i2 < i1)

    print(i1 == i3)