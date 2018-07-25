import math

class Points_Per_Rank:
    def __init__(self):
        self.points_per_rank_numerator = 1
        self.points_per_rank_denominator = 1

    @classmethod
    def from_ppr(cls, ppr_old):
        ppr_new = cls()
        ppr_new.points_per_rank_numerator = ppr_old.points_per_rank_numerator
        ppr_new.points_per_rank_denominator = ppr_old.points_per_rank_denominator
        return ppr_new


    @classmethod
    def from_int(self, int):
        ppr_new = cls()
        if int >= 1:
            ppr_new.points_per_rank_numerator = int
        else:
            ppr_new.points_per_rank_denominator = 2 - int
        return ppr_new

    def adjust_points_per_rank(self, modifier):
        if self.points_per_rank_denominator > 1:
            if modifier > 0:
                point_test = self.points_per_rank_denominator - modifier
                if point_test <= 0:
                    self.points_per_rank_denominator = 1
                    self.points_per_rank_numerator = (1 - point_test)
                else:
                    self.points_per_rank_denominator = point_test
            else:
                self.points_per_rank_denominator -= modifier
        elif self.points_per_rank_denominator < 1:
            if modifier > 0:
                self.points_per_rank_numerator += modifier
            else:
                point_test = self.points_per_rank_numerator + modifier
                if point_test <= 0:
                    self.points_per_rank_numerator = 1
                    self.points_per_rank_denominator = (1 - point_test)
                else:
                    self.points_per_rank_numerator = point_test
        else:
            if modifier > 0:
                self.points_per_rank_numerator += modifier
            elif modifier < 0:
                self.points_per_rank_denominator -= modifier

    def get_points_per_rank_numerator(self):
        return self.points_per_rank_numerator

    def get_points_per_rank_denominator(self):
        return self.points_per_rank_numerator

    def get_points_per_rank_float(self):
        return self.points_per_rank_numerator/self.points_per_rank_denominator

    def __str__(self):
        return "%f" % self.get_points_per_rank_float()

    def __repr__(self):
        return "%d/%d" % (self.points_per_rank_numerator, self.points_per_rank_denominator)

class Flat_Points:
    def __init__(self, flat):
        self.flat_points = flat

    def get_points(self):
        return self.flat_points

class Points_In_Power:
    def __init__(self, power_ranks, starting_ppr):
        self.rank_list = [power_ranks]
        self.ppr_list = [Points_Per_Rank.from_ppr(starting_ppr)]
        self.flat_list = []

    def add_ppr_break_point(self, break_point):
        if break_point in self.rank_list or break_point == 0:
            return
        current_entry = 0
        current_index = 0
        for entry in self.rank_list:
            if entry < break_point:
                current_entry = entry
                current_index += 1
            elif break_point < entry:
                self.rank_list.insert(current_index,break_point)
                self.ppr_list.insert(current_index,Points_Per_Rank.from_ppr(self.ppr_list[current_index]))
                return
        self.rank_list.append(break_point)
        self.ppr_list.append(Points_Per_Rank.from_ppr(self.ppr_list[-1]))

    def adjust_ppr_for_range(self, range_start, range_end, ppr_modifier):
        self.add_ppr_break_point(range_start)
        self.add_ppr_break_point(range_end)
        current_index = 0
        adjust_start = (range_start == 0)
        for entry in self.rank_list:
            if adjust_start == True:
                self.ppr_list[current_index].adjust_points_per_rank(ppr_modifier)
            if entry == range_start:
                adjust_start = True
            if entry == range_end:
                adjust_start = False
            current_index += 1

    def get_points_total(self):
        current_entry = 0
        current_index = 0
        current_total = 0
        for entry in self.rank_list:
            range_val = entry-current_entry
            current_total += (self.ppr_list[current_index].get_points_per_rank_float()*range_val)
            current_entry = entry
            current_index += 1
        for entry in self.flat_list:
            current_total += entry.get_points()
        return math.ceil(current_total)

if __name__ == "__main__":
    ppr_1 = Points_Per_Rank()
    ppr_1.adjust_points_per_rank(-1)
    print("Current points_per_rank in ppr1: %f" % ppr_1.get_points_per_rank_float())
    ppr_2 = Points_Per_Rank.from_ppr(ppr_1)
    print("Current points_per_rank in ppr2: %f" % ppr_2.get_points_per_rank_float())
    ppr_1.adjust_points_per_rank(3)
    print("Current points_per_rank in ppr1: %f" % ppr_1.get_points_per_rank_float())
    print("Current points_per_rank in ppr2: %f" % ppr_2.get_points_per_rank_float())

    pip = Points_In_Power(10,Points_Per_Rank())

    print(pip.rank_list)
    print(pip.ppr_list)

    pip.add_ppr_break_point(5)
    pip.add_ppr_break_point(3)
    pip.add_ppr_break_point(8)

    pip.adjust_ppr_for_range(0,10,3)

    print(pip.rank_list)
    print(pip.ppr_list)

    print(pip.get_points_total())