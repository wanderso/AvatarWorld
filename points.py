import math
import fractions
import decimal


class Rank_Range:
    def __init__(self, rank, starting_rank=0):
        if starting_rank > rank:
            self.rank_range = [[rank, starting_rank]]
        elif rank > starting_rank:
            self.rank_range = [[starting_rank, rank]]
        else:
            self.rank_range = []

    def __add__(self, other):
        rr_new = Rank_Range(0)
        for entry in self.rank_range:
            rr_new.add_range(entry[0],entry[1])
        for entry in other.rank_range:
            rr_new.add_range(entry[0],entry[1])
        return rr_new

    def __sub__(self, other):
        rr_new = Rank_Range(0)
        for entry in self.rank_range:
            rr_new.add_range(entry[0], entry[1])
        for entry in other.rank_range:
            rr_new.remove_range(entry[0], entry[1])
        return rr_new

    def __eq__(self, other):
        return (self.rank_range == other.rank_range)

    def __str__(self):
        ret_str = ""
        for entry in self.rank_range:
            ret_str += "%d-%d, " % (entry[0], entry[1])
        if len(ret_str) == 0:
            pass
        elif ret_str[0] == "0":
            ret_str = ret_str[2:-2]
        else:
            ret_str = ret_str[:-2]
        return ret_str

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index >= len(self.rank_range):
            raise StopIteration
        self.index += 1
        return self.rank_range[self.index-1]

    def get_min(self):
        return self.rank_range[0][0]

    def get_max(self):
        return self.rank_range[-1][-1]

    def add_range(self, starting_rank_var, ending_rank_var):
        starting_rank = starting_rank_var
        ending_rank = ending_rank_var
        if starting_rank > ending_rank:
            starting_rank = ending_rank_var
            ending_rank = starting_rank_var
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

    def remove_range(self, starting_rank_var, ending_rank_var):
        starting_rank = starting_rank_var
        ending_rank = ending_rank_var
        if starting_rank > ending_rank:
            starting_rank = ending_rank_var
            ending_rank = starting_rank_var
        restart_loop = True
        while restart_loop == True:
            rank_index = 0
            edited_this_run = False
            for entry in self.rank_range:
                start_entry = entry[0]
                end_entry = entry[1]
                if starting_rank > start_entry:
                    if starting_rank >= end_entry:
                        pass
                    elif ending_rank >= end_entry:
                        self.rank_range[rank_index][1] = starting_rank
                        self.add_range(start_entry,starting_rank)
                        edited_this_run = True
                    else:
                        self.rank_range[rank_index][1] = starting_rank
                        self.rank_range.pop(rank_index)
                        self.add_range(ending_rank,end_entry)
                        self.add_range(start_entry,starting_rank)
                        edited_this_run = True
                        restart_loop = True
                        break
                elif starting_rank < start_entry:
                    if ending_rank > start_entry:
                        if ending_rank > end_entry:
                            self.rank_range.pop(rank_index)
                            restart_loop = True
                            edited_this_run = True
                            break
                        else:
                            self.rank_range[rank_index][0] = ending_rank
                            edited_this_run = True
                rank_index += 1
            if edited_this_run == False:
                restart_loop = False

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

class Rank_Range_With_Points():
    def __init__(self, rank, starting_rank=0, starting_ppr=1):
        self.points = Points_Modifier_Adjuster(rank)
        self.points.adjust_x_for_ranks(Points_Per_Rank_X_Modifier(starting_ppr), rank, starting_rank, pos=True)

    def add_rank_range(self, rr):
        for entry in rr.rank_range:
            starting_val = entry[0]
            ending_val = entry[1]
            self.points.adjust_x_for_ranks(Points_Per_Rank_X_Modifier(1),ending_val,starting_val,pos=True)

    def return_max_int(self):
        ret_val = 0
        for entry in self.points.point_adjust_list:
            if ret_val < entry.get_modifier():
                ret_val = entry.get_modifier()
        return int(ret_val) - 1

    def __repr__(self):
        return str(self.points)

class Points_Per_Rank:
    def __init__(self, x=1):
        self.x = x

    @classmethod
    def from_ppr(cls, ppr_old):
        return cls(ppr_old.get_x())

    @classmethod
    def from_int(cls, int):
        return cls(x=int)

    def adjust_points_per_rank_by_x(self, modifier, pos=True):
        mod = None
        if type(modifier) == Points_Per_Rank:
            mod = modifier.get_x()
        else:
            mod = modifier
        if self.x is None:
            self.x = 0
        if pos == False:
            self.x -= mod.xmod
        else:
            self.x += mod.xmod

    def adjust_points_per_rank_by_y(self, modifier, pos=True):
        modifier_y_val = modifier.get_y()
        self_y_val = self.get_y()
        if pos == False:
            target_y_val = self_y_val - modifier_y_val
        else:
            target_y_val = self_y_val + modifier_y_val
        if target_y_val >= 1:
            self.x = target_y_val
        elif target_y_val > 0:
            self.x = (((2*target_y_val)-1)/target_y_val)
        else:
            print("Cannot create y for modifier")
            raise IndexError

    def get_points_per_rank_float(self):
        return self.get_y()

    def get_points_per_rank_fraction(self):
        return fractions.Fraction(decimal.Decimal(self.get_y()))

    def get_x(self):
        return self.x

    def get_y(self):
        if self.x is None:
            return 0.0
        elif self.x >= 1:
            return self.x
        else:
            return 1.0/(2.0-self.x)

    def __str__(self):
        return "%f" % self.get_points_per_rank_float()

    def __repr__(self):
        return fractions.Fraction(decimal.Decimal(self.get_y())).__repr__()

class Points_Per_Rank_X_Modifier:
    def __init__(self, xmod):
        self.xmod = xmod

    def __add__(self, other):
        return Points_Per_Rank_X_Modifier(self.xmod + other.xmod)

    def __sub__(self, other):
        return Points_Per_Rank_X_Modifier(self.xmod - other.xmod)

    def __eq__(self, other):
        return self.xmod == other.xmod

    def __str__(self):
        return str(self.xmod)

    def __repr__(self):
        return repr(self.xmod)

    def get_modifier(self):
        return self.xmod

class Points_Flat_Modifier:
    def __init__(self, flat_points):
        self.flat_points = flat_points

    def __add__(self, other):
        return Points_Flat_Modifier(self.flat_points + other.flat_points)

    def __sub__(self, other):
        return Points_Flat_Modifier(self.flat_points - other.flat_points)

    def __eq__(self, other):
        return self.flat_points == other.flat_points

class Flat_Points:
    def __init__(self, flat):
        self.flat_points = flat

    def get_points_total(self):
        return self.flat_points

    def __str__(self):
        return str(self.flat_points)

class Points_Modifier_Adjuster:
    def __init__(self, max_ranks):
        self.rank_list = [max_ranks]
        self.point_adjust_list = [Points_Per_Rank_X_Modifier(0)]

    def __add__(self, other):
        retpma = Points_Modifier_Adjuster(max(self.rank_list[-1],other.rank_list[-1]))
        value = 0
        index = 0
        for entry in self.rank_list:
            retpma.adjust_x_for_ranks(self.point_adjust_list[index],entry,value,True)
            value = entry
        value = 0
        index = 0
        for entry in other.rank_list:
            retpma.adjust_x_for_ranks(self.point_adjust_list[index],entry,value,True)
            value = entry
        return retpma

    def __repr__(self):
        return str(self.rank_list) + " * " + str(self.point_adjust_list)

    def adjust_x_for_ranks(self, x_modifier, rank, starting_rank=0, pos=True):
        self.add_ppr_break_point(rank)
        self.add_ppr_break_point(starting_rank)
        current_index = 0
        adjust_start = (starting_rank == 0)
        for entry in self.rank_list:
            if adjust_start == True:
                if pos == True:
                    self.point_adjust_list[current_index] += x_modifier
                else:
                    self.point_adjust_list[current_index] -= x_modifier
            if entry == starting_rank:
                adjust_start = True
            if entry == rank:
                adjust_start = False
            current_index += 1

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
                self.point_adjust_list.insert(current_index,Points_Per_Rank_X_Modifier(self.point_adjust_list[current_index].get_modifier()))
                return
        self.rank_list.append(break_point)
        self.point_adjust_list.append(Points_Per_Rank_X_Modifier(0))


class Points_In_Power:
    def __init__(self, power_ranks, starting_ppr):
        self.rank_list = [power_ranks]
        self.ppr_list = [Points_Per_Rank.from_ppr(starting_ppr)]
        self.flat_list = []

    def __add__(self, other):
        retpip = Points_In_Power(0, Points_Per_Rank.from_int(0))
        retpip.rank_list = list(self.rank_list)
        retpip.ppr_list = list(self.ppr_list)
        retpip.flat_list = list(self.flat_list)

        if type(other) is Points_In_Power:
            current_value = 0
            current_index = 0
            for entry in other.rank_list:
                retpip.add_ppr_break_point(entry)
                retpip.adjust_ppr_for_range(current_value,entry,other.ppr_list[current_index],True,pos=True)
                current_value = entry
                current_index += 1

            for entry in other.flat_list:
                retpip.add_flat_points(entry)
        elif type(other) is Flat_Points:
            retpip.add_flat_points(other)
        elif type(other) is Points_Modifier_Adjuster:
            current_value = 0
            current_index = 0
            for entry in other.rank_list:
                retpip.add_ppr_break_point(entry)
                retpip.adjust_ppr_for_range(current_value,entry,other.point_adjust_list[current_index],True,pos=True)
                current_value = entry
                current_index += 1
        return retpip


    def __sub__(self, other):
        retpip = Points_In_Power(0,Points_Per_Rank.from_int(0))

        retpip.rank_list = list(self.rank_list)
        retpip.ppr_list = list(self.ppr_list)
        retpip.flat_list = list(self.flat_list)

        if type(other) == Points_In_Power:
            current_value = 0
            current_index = 0
            for entry in other.rank_list:
                retpip.add_ppr_break_point(entry)
                retpip.adjust_ppr_for_range(current_value,entry,other.ppr_list[current_index],pos=False)
                current_value = entry
                current_index += 1

            for entry in other.flat_list:
                if entry in retpip.flat_list:
                    retpip.remove_flat_points(entry)
                else:
                    retpip.add_flat_points(Flat_Points(-entry.get_points_total()))
        elif type(other) == Flat_Points:
            if other in retpip.flat_list:
                retpip.remove_flat_points(other)
            else:
                retpip.add_flat_points(Flat_Points(-other.get_points_total()))
        elif type(other) == Points_Per_Rank_X_Modifier:
            current_value = 0
            current_index = 0
            for entry in other.rank_list:
                retpip.add_ppr_break_point(entry)
                retpip.adjust_ppr_for_range(current_value,entry,other.point_adjust_list[current_index],True,pos=False)
                current_value = entry
                current_index += 1
        return retpip

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index > len(self.rank_list):
            raise StopIteration
        elif self.index == len(self.rank_list):
            self.index += 1
            return ("Flat Values", self.flat_list)
        self.index += 1
        return (self.rank_list[self.index-1],self.ppr_list[self.index-1])

    def dictify(self):
        return {
                "rank_list": self.rank_list,
                "ppr_list": self.ppr_list,
                "flat_list": self.flat_list
                }

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
#        self.ppr_list.append(Points_Per_Rank.from_ppr(self.ppr_list[-1]))
        self.ppr_list.append(Points_Per_Rank.from_int(0))

    def adjust_ppr_for_range(self, range_start, range_end, ppr_modifier, by_x, pos=True):
        if range_end > self.rank_list[-1]:
            print("Overextending PPR!")
            print("Overextending PPR!")
            print("Overextending PPR!")
            print("Overextending PPR!")
            print(type(ppr_modifier))

        self.add_ppr_break_point(range_start)
        self.add_ppr_break_point(range_end)

        current_index = 0
        adjust_start = (range_start == 0)
        for entry in self.rank_list:
            if adjust_start == True:
                if pos == True:
                    if by_x == True:
                        self.ppr_list[current_index].adjust_points_per_rank_by_x(ppr_modifier)
                    elif by_x == False:
                        self.ppr_list[current_index].adjust_points_per_rank_by_y(ppr_modifier)
                    else:
                        raise ValueError
                else:
                    if by_x == True:
                        self.ppr_list[current_index].adjust_points_per_rank_by_x(ppr_modifier, pos=False)
                    elif by_x == False:
                        self.ppr_list[current_index].adjust_points_per_rank_by_y(ppr_modifier, pos=False)
                    else:
                        raise ValueError
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
            current_total += entry.get_points_total()
        return math.ceil(current_total)

    def add_flat_points(self, fp):
        self.flat_list.append(fp)

    def remove_flat_points(self, fp):
        self.flat_list.remove(fp)

    def __repr__(self):
        retstr = str(self.rank_list) + " * " + str(self.ppr_list)
        if len(self.flat_list)!= 0:
            retstr = retstr + " + ["
            for entry in self.flat_list:
                e = entry.get_points_total()
                if e < 0:
                    retstr = retstr[:-2] + "- " + str(e*-1) + " + "
                else:
                    retstr = retstr + str(e) + " + "
            retstr = retstr[:-3] + "]"
        return retstr

if __name__ == "__main__":
    pip1 = Points_In_Power(10, Points_Per_Rank())
    pip2 = Points_In_Power(10, Points_Per_Rank.from_int(0))

    print (pip1)

    print (pip2)

    print (pip1 + pip2)

    ppr1 = Points_Per_Rank()
    ppr2 = Points_Per_Rank.from_int(-1)

    print (ppr1)
    print (ppr2)
    print (ppr1 + ppr2)

    # ppr_1 = Points_Per_Rank()
    # ppr_flat = Points_Per_Rank.from_int(-2)
    # ppr_1.adjust_points_per_rank(-1)
    # print("Current points_per_rank in ppr1: %f" % ppr_1.get_points_per_rank_float())
    # ppr_2 = Points_Per_Rank.from_ppr(ppr_1)
    # print("Current points_per_rank in ppr2: %f" % ppr_2.get_points_per_rank_float())
    #
    # print("Current points_per_rank in ppr_flat: %f" % ppr_flat.get_points_per_rank_float())
    #
    # ppr_1.adjust_points_per_rank(3)
    # print("Current points_per_rank in ppr1: %f" % ppr_1.get_points_per_rank_float())
    # print("Current points_per_rank in ppr2: %f" % ppr_2.get_points_per_rank_float())
    #
    # pip = Points_In_Power(10,Points_Per_Rank())
    #
    # print(pip.rank_list)
    # print(pip.ppr_list)
    #
    # pip.add_ppr_break_point(5)
    # pip.add_ppr_break_point(3)
    # pip.add_ppr_break_point(8)
    #
    # pip.adjust_ppr_for_range(0,7,-3)
    #
    # print(pip.rank_list)
    # print(pip.ppr_list)
    #
    # print(pip.get_points_total())
    #
    # pip2 = Points_In_Power(10, Points_Per_Rank())
    # print(pip2.get_points_total())
    #
    # pip3 = pip2 - pip2
    # print("DEADBEEF")
    # print(pip3.get_points_total())
    # print(pip3.rank_list)
    # print(pip3.ppr_list)
    #
    #
    #
    #
    # rnge = Rank_Range(5,starting_rank=3)
    # rnge.add_range(1,2)
    # rnge.add_range(7,10)
    # print (rnge.rank_range)
    # rnge.add_range(0,10)
    # print (rnge.rank_range)
    # rnge.add_range(5,13)
    # print (rnge.rank_range)
    # rnge.add_range(15,18)
    # print(str(rnge))
    # rnge.add_range(12,15)
    # print(str(rnge))
    # rnge.remove_range(12,15)
    # print(str(rnge))
    # rnge.remove_range(10,16)
    # print(str(rnge))
    # rnge.remove_range(12,15)
    # print(str(rnge))
    # rnge.remove_range(5,12)
    # print (str(rnge))
    # rnge2 = Rank_Range(8,starting_rank=10)
    # print (str(rnge2))
    # rnge3 = rnge + rnge2
    # print (str(rnge3))
    #
    # rrpr = Rank_Range_With_Points(12)
    # print(rrpr)
    #
    # rrpr.add_rank_range(rnge3)
    # print(rrpr)
    # rrpr.add_rank_range(rnge)
    # print(rrpr)
    # print(rrpr.return_max_int())


