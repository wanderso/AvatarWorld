"""Measurements Table
Rank Mass Time Distance Volume
–5 1.5 lb. 1/8 second 6 inches 1/32 cft.
–4 3 lbs. 1/4 second 1 foot 1/16 cft.
–3 6 lbs. 1/2 second 3 feet 1/8 cft.
–2 12 lbs. 1 second 6 feet 1/4 cft.
–1 25 lbs. 3 seconds 15 feet 1/2 cft.
0 50 lbs. 6 seconds 30 feet 1 cubic ft. (cft.)
1 100 lbs. 12 seconds 60 feet 2 cft.
2 200 lbs. 30 seconds 120 feet 4 cft.
3 400 lbs. 1 minute 250 feet 8 cft.
4 800 lbs. 2 minutes 500 feet 15 cft.
5 1,600 lbs. 4 minutes 900 feet 30 cft.
6 3,200 lbs. 8 minutes 1,800 feet 60 cft.
7 3 tons 15 minutes 1/2 mile 125 cft.
8 6 tons 30 minutes 1 mile 250 cft.
9 12 tons 1 hour 2 miles 500 cft.
10 25 tons 2 hours 4 miles 1,000 cft.
11 50 tons 4 hours 8 miles 2,000 cft.
12 100 tons 8 hours 16 miles 4,000 cft.
13 200 tons 16 hours 30 miles 8,000 cft.
14 400 tons 1 day 60 miles 15,000 cft.
15 800 tons 2 days 120 miles 32,000 cft.
16 1,600 tons 4 days 250 miles 65,000 cft.
17 3.2 ktons 1 week 500 miles 125,000 cft.
18 6 ktons 2 weeks 1,000 miles 250,000 cft.
19 12 ktons 1 month 2,000 miles 500,000 cft.
20 25 ktons 2 months 4,000 miles 1 million cft.
21 50 ktons 4 months 8,000 miles 2 million cft.
22 100 ktons 8 months 16,000 miles 4 million cft.
23 200 ktons 1.5 years 32,000 miles 8 million cft.
24 400 ktons 3 years 64,000 miles 15 million cft.
25 800 ktons 6 years 125,000 miles 32 million cft.
26 1,600 ktons 12 years 250,000 miles 65 million cft.
27 3,200 ktons 25 years 500,000 miles 125 million cft.
28 6,400 ktons 50 years 1 million miles 250 million cft.
29 12,500 ktons 100 years 2 million miles 500 million cft.
30 25,000 ktons 200 years 4 million miles 1 billion cft.
+1 x2 x2 x2 x2"""

class Measurement:
    rank_offset = 5
    value_list = []
    multiplier_after = 2
    multiplier_before = 0.5
    unit_list = []

    def __add__(self,other):
        return type(self).from_value(self.get_value() + other.get_value())

    def __sub__(self, other):
        return type(self).from_value(self.get_value() - other.get_value())

    def __init__(self):
        self.value = 0

    @classmethod
    def from_rank(cls,rank):
        retval = cls()
        r_new = rank + cls.rank_offset
        if (r_new >= 0) and (r_new < len(cls.value_list)):
            retval.value = cls.value_list[r_new]
        elif(r_new < 0):
            r_diff = 0 - r_new
            retval.value = cls.value_list[0]
            retval.value = retval.value * pow(cls.multiplier_before,r_diff)
        else:
            r_diff = r_new + 1 - len(cls.value_list)
            retval.value = cls.value_list[-1]
            retval.value = retval.value * pow(cls.multiplier_after,r_diff)
        return retval

    @classmethod
    def from_value(cls,val):
        retval = cls()
        retval.value = val
        return retval

    def get_value(self):
        return self.value

    def get_rank(self):
        rank_start = -type(self).rank_offset
        for val in type(self).value_list:
            if val < self.value:
                rank_start += 1
            else:
                break
        return rank_start

    def __str__(self):
        val = self.get_value()
        value_marker = type(self).unit_list[0][0]
        name_singleton = type(self).unit_list[0][1]
        name_plural = type(self).unit_list[0][2]
        for entry in type(self).unit_list:
            if val > entry[0]:
                value_marker = entry[0]
                name_singleton = entry[1]
                name_plural = entry[2]
        num_target = self.value/value_marker
        name_target = name_plural
        if num_target >= 1 and num_target < 2:
            name_target = name_singleton
        if num_target == int(num_target):
            return "{:,d} {}".format(int(num_target), name_target)
        else:
            return "{:,g} {}".format(num_target, name_target)

class Mass(Measurement):
    value_list = [1.5,3,6,12,25,50,100,200,400,800,1600,3200,6000,12000,24000,50000,100000,200000,400000,800000,
                  800*2000,1600*2000,3200*2000,6*2000000,12*2000000,25*2000000,50*2000000,100*2000000,200*2000000,
                  400*2000000,800*2000000,1600*2000000,3200*2000000,6400*2000000,12500*2000000,25000*2000000]
    unit_list = [(1,'lb.','lbs.'),(2000,'ton','tons'),(2000000,'kiloton','kilotons')]

class Time(Measurement):
    value_list = [1.0/8,1.0/4,0.5,1,3,6,12,30,1*60,2*60,4*60,8*60,15*60,30*60,1*60*60,2*60*60,4*60*60,8*60*60,16*60*60,
                  24*60*60,2*24*60*60,4*24*60*60,7*24*60*60,2*7*24*60*60,30*24*60*60,2*30*24*60*60,4*30*24*60*60,
                  8*30*24*60*60,3*365*12*60*60,3*365*24*60*60,6*365*24*60*60,12*365*24*60*60,25*365*24*60*60,
                  50*365*24*60*60,100*365*24*60*60,200*365*24*60*60]
    unit_list = [(1,'second','seconds'),(60,'minute','minutes'),(60*60,'hour','hours'),(24*60*60,'day','days'),
                 (7*24*60*60,'week','weeks'),(30*24*60*60,'month','months'),(365*24*60*60,'year','years')]

class Distance(Measurement):
    value_list = [0.5,1,3,6,15,30,60,120,250,500,900,1800,2640,5280,2*5280,4*5280,8*5280,16*5280,30*5280,60*5280,
                  120*5280,250*5280,500*5280,1000*5280,2000*5280,4000*5280,8000*5280,16000*5280,32000*5280,64000*5280,
                  125000*5280,250000*5280,500000*5280,1000000*5290,2*1000000*5290,4*1000000*5290]
    unit_list = [(1,'foot','feet'),(5280,'mile','miles'),(5280*1000000,'million miles','million miles')]


class Volume(Measurement):
    value_list = [1.0/32,1.0/16,1.0/8,1.0/4,1.0/2,1,2,4,8,15,30,60,125,250,500,1000,2000,4000,80000,15000,32000,
                  65000,125000,250000,500000,1000000,2*1000000,4*1000000,8*1000000,15*1000000,32*1000000,65*1000000,
                  125*1000000,250*1000000,500*1000000,1000*1000000]
    unit_list = [(1, 'cubic ft.', 'cft.'),(1000000,'million cft.','million cft.'),
                 (1000000000,'billion cft.','billion cft.')]

if __name__ == "__main__":
    m1 = Mass.from_rank(2)
    m2 = Mass.from_rank(5)
    m3 = Mass.from_rank(0)


    print(m1)

    print(m1.get_value())
    print(m2.get_value())
    print(m3.get_value())

    print(len(Mass.value_list))
    print(len(Time.value_list))
    print(len(Distance.value_list))
    print(len(Volume.value_list))

    print(Mass.from_rank(-5))
    print(Mass.from_rank(30))
    print(Mass.from_rank(31))

    print(Mass.from_value(50).get_rank())


