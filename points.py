import math
import fractions
import decimal


class Rank_Range:
    def __init__(self, rank, starting_rank=0):
        self.rank_range = [[starting_rank, rank]]

    def add_range(self, starting_rank, ending_rank):
        rank_index = 0
        edited = False
        for entry in self.rank_range:
            start_entry = entry[0]
            end_entry = entry[1]
            if starting_rank > end_entry:
                pass
            elif starting_rank < start_entry:
                if ending_rank < start_entry:
                    self.rank_range.insert(rank_index,[starting_rank,ending_rank])
                    edited = True
                    break
                elif ending_rank < end_entry:
                    self.rank_range[rank_index][0] = starting_rank
                    edited = True
                    break
                else:
                    self.rank_range[rank_index][0] = starting_rank
                    self.rank_range[rank_index][1] = ending_rank
                    edited = True
                    break
            elif starting_rank > start_entry:
                if ending_rank > end_entry:
                    self.rank_range[rank_index][1] = ending_rank
                    edited = True
                    break
            rank_index += 1
        if edited == False:
            self.rank_range.append([starting_rank,ending_rank])
        self.clean_range()

    def remove_range(self, starting_rank, ending_rank):
        rank_index = 0
        restart_loop = True
        while restart_loop == True:
            for entry in self.rank_range:
                print (self.rank_range)
                start_entry = entry[0]
                end_entry = entry[1]
                if starting_rank > start_entry:
                    if starting_rank > end_entry:
                        pass
                    elif ending_rank >= end_entry:
                        self.rank_range[rank_index][1] = starting_rank
                    else:
                        self.rank_range[rank_index][1] = starting_rank
                        self.rank_range.pop(rank_index)
                        self.add_range(ending_rank,end_entry)
                        restart_loop = True
                        break
                elif starting_rank < start_entry:
                    if ending_rank > start_entry:
                        if ending_rank > end_entry:
                            self.rank_range.pop(rank_index)
                            restart_loop = True
                            break
                        else:
                            self.rank_range[rank_index][0] = ending_rank
                rank_index += 1

        self.clean_range()

    def clean_range(self):
        cleanup_progress = True
        while cleanup_progress:
            edited_this_run = False
            for index in range(0,len(self.rank_range)-1):
                i2 = index+1
                if self.rank_range[index][1] > self.rank_range[i2][0]:
                    if self.rank_range[index][1] >= self.rank_range[i2][1]:
                        self.rank_range.pop(i2)
                        edited_this_run = True
                        break
                    else:
                        self.rank_range[index][1] = self.rank_range[i2][1]
                        self.rank_range.pop(i2)
                        edited_this_run = True
                        break
                elif self.rank_range[index][1] == self.rank_range[i2][0]:
                    self.rank_range[index][1] = self.rank_range[i2][1]
                    self.rank_range.pop(i2)
                    edited_this_run = True
                    break
            if edited_this_run == False:
                cleanup_progress = False


class Points_Per_Rank:
    def __init__(self, x=1):
        self.x = x

    def __add__(self, other):
        if hasattr(other, 'x'):
            return Points_Per_Rank(self.x + other.x)
        else:
            return Points_Per_Rank(self.x + other)

    def __sub__(self, other):
        if hasattr(other, 'x'):
            return Points_Per_Rank(self.x - other.x)
        else:
            return Points_Per_Rank(self.x - other)

    @classmethod
    def from_ppr(cls, ppr_old):
        return cls(ppr_old.get_x())

    @classmethod
    def from_int(cls, int):
        return cls(x=int)

    def adjust_points_per_rank(self, modifier):
        self.x += modifier

    def get_points_per_rank_float(self):
        return self.get_y()

    def get_x(self):
        return self.x

    def get_y(self):
        if self.x >= 1:
            return self.x
        else:
            return 1.0/(2.0-self.x)

    def __str__(self):
        return "%f" % self.get_points_per_rank_float()

    def __repr__(self):
        return fractions.Fraction(decimal.Decimal(self.get_y())).__repr__()

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

    def adjust_ppr_for_range(self, range_start, range_end, ppr_modifier, pos=True):
        self.add_ppr_break_point(range_start)
        self.add_ppr_break_point(range_end)
        current_index = 0
        adjust_start = (range_start == 0)
        for entry in self.rank_list:
            if adjust_start == True:
                if pos == True:
                    self.ppr_list[current_index] = self.ppr_list[current_index] + (ppr_modifier)
                else:
                    self.ppr_list[current_index] = self.ppr_list[current_index] - (ppr_modifier)
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

    def __repr__(self):
        return str(self.rank_list) + " " + str(self.ppr_list)

if __name__ == "__main__":
    ppr_1 = Points_Per_Rank()
    ppr_flat = Points_Per_Rank.from_int(-2)
    ppr_1.adjust_points_per_rank(-1)
    print("Current points_per_rank in ppr1: %f" % ppr_1.get_points_per_rank_float())
    ppr_2 = Points_Per_Rank.from_ppr(ppr_1)
    print("Current points_per_rank in ppr2: %f" % ppr_2.get_points_per_rank_float())

    print("Current points_per_rank in ppr_flat: %f" % ppr_flat.get_points_per_rank_float())

    ppr_1.adjust_points_per_rank(3)
    print("Current points_per_rank in ppr1: %f" % ppr_1.get_points_per_rank_float())
    print("Current points_per_rank in ppr2: %f" % ppr_2.get_points_per_rank_float())

    pip = Points_In_Power(10,Points_Per_Rank())

    print(pip.rank_list)
    print(pip.ppr_list)

    pip.add_ppr_break_point(5)
    pip.add_ppr_break_point(3)
    pip.add_ppr_break_point(8)

    pip.adjust_ppr_for_range(0,7,-3)

    print(pip.rank_list)
    print(pip.ppr_list)

    print(pip.get_points_total())



    rnge = Rank_Range(5,starting_rank=3)
    rnge.add_range(1,2)
    rnge.add_range(7,10)
    print (rnge.rank_range)
    rnge.add_range(0,10)
    print (rnge.rank_range)
    rnge.add_range(5,13)
    print (rnge.rank_range)
    rnge.add_range(15,18)
    print (rnge.rank_range)
    rnge.add_range(12,15)
    print (rnge.rank_range)
    rnge.remove_range(12,15)
    print (rnge.rank_range)
