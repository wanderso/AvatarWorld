import heapq
import enum
import sys

class Round_Schedule(enum.IntEnum):
    BEFORE = sys.maxsize
    AFTER = -sys.maxsize -1


class Timeline:
    def __init__(self):
        self.current_time = Game_Round(0)
        self.last_event = Timeline_Entry(0, Round_Schedule.BEFORE, Round_Schedule.BEFORE)
        self.heap_timeline = []

    def add_event_with_time(self, time, event):
        te = Timeline_Event.from_time_event(time, event)
        heapq.heappush(self.heap_timeline, te)

    def add_event(self, timeline_event):
        heapq.heappush(self.heap_timeline, timeline_event)

    def pop_event(self):
        if len(self.heap_timeline) > 0:
            datum = heapq.heappop(self.heap_timeline)
            self.last_event = datum.get_time()
            return datum
        else:
            return None

    def top_event(self):
        if len(self.heap_timeline) > 0:
            return self.heap_timeline[0]
        else:
            return None

    def get_time(self):
        return self.last_event


class Timeline_Event:
    @classmethod
    def from_time_event(cls, ti, ev):
        datum = cls(0,0,None)
        datum.time = ti
        datum.event = ev
        return datum

    def __eq__(self, other):
        return (self.time == other.time)

    def __gt__(self, other):
        return (self.time > other.time)

    def __lt__(self, other):
        return (self.time < other.time)

    def __init__(self, initiative, rnd, eve, tiebreaker=Round_Schedule.AFTER):
        self.time = Timeline_Entry(initiative, rnd, tiebreaker=tiebreaker)
        self.event = eve

    def get_event(self):
        return self.event

    def get_time(self):
        return self.time


class Timeline_Entry:
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

    def __init__(self, initiative, rnd, tiebreaker=Round_Schedule.AFTER):
        self.tiebreaker = tiebreaker
        if type(initiative) == Initiative:
            self.initiative = Initiative.cpy(initiative)
        else:
            self.initiative = Initiative(initiative)
        if type(rnd) == Game_Round:
            self.round = Game_Round.cpy(rnd)
        else:
            self.round = Game_Round(rnd)

    def get_round(self):
        return self.round

    def get_initiative_count(self):
        return self.initiative

    def get_tiebreaker(self):
        return self.tiebreaker


class Game_Round:
    def __eq__(self, other):
        return self.round_number == other.round_number

    def __gt__(self, other):
        return (self.round_number > other.round_number)

    def __lt__(self, other):
        return (self.round_number < other.round_number)

    def __init__(self, rnd):
        self.round_number = rnd

    def __add__(self, other):
        if type(other) == Game_Round:
            return type(self)(self.round_number + other.round_number)
        else:
            return type(self)(self.round_number + other)

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

    e1 = Timeline_Event(Initiative("Before"), Game_Round(1),"e1")
    e2 = Timeline_Event(Initiative("After"), Game_Round(0), "e2")
    e3 = Timeline_Event(Initiative(8), Game_Round(1), "e3")
    e4 = Timeline_Event(Initiative(24), Game_Round(1), "e4")
    e5 = Timeline_Event(Initiative(24), Game_Round(1), "e5", tiebreaker=8)
    e6 = Timeline_Event(Initiative(24), Game_Round(1), "e6", tiebreaker=55)

    ti.add_event(e1)
    ti.add_event(e2)
    ti.add_event(e3)
    ti.add_event(e4)
    ti.add_event(e5)
    ti.add_event(e6)

    print(ti.pop_event().get_event())
    print(ti.pop_event().get_event())
    print(ti.pop_event().get_event())
    print(ti.pop_event().get_event())
    print(ti.pop_event().get_event())
    print(ti.pop_event().get_event())



