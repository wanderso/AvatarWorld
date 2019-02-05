from senses.SenseFlags import Accurate, Acute, Radius, Ranged
from senses.SenseConstants import Sense_Type_Designation
from senses.Sense import Sense


class SenseCluster:
    def __init__(self):
        self.senses_total = {}
        self.senses_powers = []

    def __str__(self):
        if len(self.senses_total) == 0:
            return "Sense Cluster: Empty"
        ret_val = "Sense Cluster: \n"
        for value in self.senses_total:
            for entry in self.senses_total[value]:
                ret_val += "\t" + str(self.senses_total[value][entry]) + "\n"
        return ret_val[:-1]

    def get_total_senses(self):
        return self.senses_total

    def add_sense(self, sense):
        t = sense.get_type()
        if t in self.senses_total:
            n = sense.get_narrow()
            if n in self.senses_total[t]:
                pass
            else:
                self.senses_total[t][sense.get_narrow()] = sense
        else:
            self.senses_total[t] = {sense.get_narrow(): sense}

    def add_senses(self, sense_list):
        for sense in sense_list:
            self.add_sense(sense)

    def remove_sense(self, sense):
        #TODO - Fix!
        self.senses_total.remove(sense)

    def check_sense_for_existence(self, sense):
        sense_broad = sense.get_type()
        sense_narrow = sense.get_narrow()
        if (sense_broad not in self.senses_total) or (sense_narrow not in self.senses_total[sense_broad]) \
                or sense != self.senses_total[sense_broad][sense_narrow]:
            return False
        return self.senses_total[sense_broad][sense_narrow]

    def create_default_sense_cluster(self):
        visual = Sense(Sense_Type_Designation.VISUAL,
                       with_flags=[Acute(modifiers={"Rank": 1}),
                                   Ranged(modifiers={"Rank": 1}),
                                   Accurate(modifiers={"Rank": 1})])

        auditory = Sense(Sense_Type_Designation.AUDITORY,
                         with_flags=[Acute(modifiers={"Rank": 1}),
                                     Ranged(modifiers={"Rank": 1}),
                                     Radius(modifiers={"Rank": 1})])

        olfactory = Sense(Sense_Type_Designation.OLFACTORY,
                          with_flags=[Radius(modifiers={"Rank": 1})])

        tactile = Sense(Sense_Type_Designation.TACTILE,
                        with_flags=[Radius(modifiers={"Rank": 1}),
                                    Accurate(modifiers={"Rank": 1})])

        mental = Sense(Sense_Type_Designation.MENTAL)

        self.add_senses([visual, auditory, olfactory, tactile, mental])


    def get_sense_targets_from_flag(self, flag):
        flag_sense = flag.get_sense_type()
        flag_narrow = flag.get_narrow()
        sense_targets = []



        if flag_sense in self.senses_total:
            sense_type = self.senses_total[flag_sense]
            if type(flag).entire_type_option and flag.rank == 2:
                for entry in sense_type:
                    sense_targets.append(sense_type[entry])
            else:
                if flag_narrow in sense_type:
                    sense_targets.append(sense_type[flag_narrow])

        return sense_targets

    def apply_flag(self, flag):
        flag_type = type(flag)

        if flag_type.is_entire_sense:
            sns = flag.get_sense()
            exist = self.check_sense_for_existence(sns)
            if exist is not False and exist.get_active() == False:
                exist.set_active(True)
            elif exist is not False:
                pass
            else:
                self.add_sense(sns)
        else:
            for entry in self.get_sense_targets_from_flag(flag):
                entry.add_flag(flag)

    def remove_flag(self, flag):
        flag_type = type(flag)
        if flag_type.is_entire_sense:
            sns = flag.get_sense()
        else:
            for entry in self.get_sense_targets_from_flag(flag):
                entry.remove_flag(flag)