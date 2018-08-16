import heapq
import enum
import sys

class Round_Schedule(enum.IntEnum):
    BEFORE = sys.maxsize
    AFTER = -sys.maxsize -1

class Timeline:
    def __init__(self):
        self.current_time = Game_Round(0)
        self.heap_timeline = []

    def add_event(self, time, event):
        heapq.heappush(self.heap_timeline,(time, event))

    def pop_event(self):
        if len(self.heap_timeline) > 0:
            return heapq.heappop(self.heap_timeline)
        else:
            return None

    def top_event(self):
        if len(self.heap_timeline) > 0:
            return self.heap_timeline[0]
        else:
            return None

class Timeline_Event:
    def __eq__(self, other):
        return (self.initiative == other.initiative) and (self.round == other.round) and (self.tiebreaker == other.tiebreaker)

    def __gt__(self, other):
        if (self.round != other.round):
            return (self.round > other.round)
        elif (self.initiative != other.initiative):
            return (self.initiative > other.initiative)
        else:
            return (self.tiebreaker < other.tiebreaker)

    def __lt__(self, other):
        if (self.round != other.round):
            return (self.round < other.round)
        elif (self.initiative != other.initiative):
            return (self.initiative < other.initiative)
        else:
            return (self.tiebreaker > other.tiebreaker)

    def __init__(self, initiative, rnd, eve, tiebreaker=Round_Schedule.AFTER):
        self.event = eve
        self.tiebreaker = tiebreaker
        if type(initiative) == Initiative:
            self.initiative = Initiative.cpy(initiative)
        else:
            self.initiative = Initiative(initiative)
        if type(rnd) == Game_Round:
            self.round = Game_Round.cpy(rnd)
        else:
            self.round = Game_Round(rnd)

    def get_event(self):
        return self.event


class Game_Round:
    def __eq__(self, other):
        return self.round_number == other.round_number

    def __gt__(self, other):
        return (self.round_number > other.round_number)

    def __lt__(self, other):
        return (self.round_number < other.round_number)

    def __init__(self, rnd):
        self.round_number = rnd

    @classmethod
    def cpy(cls, rnd_cpy):
        return cls(rnd_cpy.get_round_num())

    def get_round_num(self):
        return self.round_number




class Initiative:
    def __eq__(self, other):
        return self.initiative_count == other.initiative_count

    def __gt__(self, other):
        return (self.initiative_count < other.initiative_count)

    def __lt__(self, other):
        return (self.initiative_count > other.initiative_count)

    def __init__(self, clk):
        self.adjust_init_count(clk)

    @classmethod
    def cpy(cls, init_cpy):
        return cls(init_cpy.get_init_count())

    def get_init_count(self):
        return self.initiative_count

    def adjust_init_count(self, clk):
        if clk == "Before":
            self.initiative_count = Round_Schedule.BEFORE
        elif clk == "After":
            self.initiative_count = Round_Schedule.AFTER
        else:
            self.initiative_count = clk


if __name__ == "__main__":
    i1 = Initiative("Before")
    i2 = Initiative(25)
    i3 = Initiative("Before")
    i4 = Initiative(5)
    if i1 != i2:
        print("This works!")
        print(i2 < i1)

    print(i1 == i3)
    print(i4 < i2)

    ti = Timeline()
    ti.add_event(i1,"i1")
    ti.add_event(i2,"i2")
    ti.add_event(i3,"i3")
    ti.add_event(i4,"i4")

    print(ti.pop_event())
    print(ti.pop_event())
    print(ti.pop_event())
    print(ti.pop_event())
    print(ti.pop_event())

    r1 = Game_Round(0)
    r2 = Game_Round(2)
    r3 = Game_Round(3)
    r4 = Game_Round(1)

    ti.add_event(r1,"r1")
    ti.add_event(r2,"r2")
    ti.add_event(r3,"r3")
    ti.add_event(r4,"r4")

    print(ti.pop_event())
    print(ti.pop_event())
    print(ti.pop_event())
    print(ti.pop_event())
    print(ti.pop_event())

    e1 = Timeline_Event(Initiative("Before"), Game_Round(1),"e1")
    e2 = Timeline_Event(Initiative("After"), Game_Round(0), "e2")
    e3 = Timeline_Event(Initiative(8), Game_Round(1), "e3")
    e4 = Timeline_Event(Initiative(24), Game_Round(1), "e4")
    e5 = Timeline_Event(Initiative(24), Game_Round(1), "e5", tiebreaker=8)
    e6 = Timeline_Event(Initiative(24), Game_Round(1), "e6", tiebreaker=55)


    ti.add_event(e1,e1.get_event())
    ti.add_event(e2,e2.get_event())
    ti.add_event(e3,e3.get_event())
    ti.add_event(e4,e4.get_event())
    ti.add_event(e5,e5.get_event())
    ti.add_event(e6,e6.get_event())


    print(ti.pop_event())
    print(ti.pop_event())
    print(ti.pop_event())
    print(ti.pop_event())
    print(ti.pop_event())
    print(ti.pop_event())
    print(ti.pop_event())



