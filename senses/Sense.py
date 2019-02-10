from senses.SenseConstants import Sense_Type_Narrow, Sense_Type_Designation


class Sense:
    def __init__(self, designation, sense_narrow="", with_flags=[]):
        self.sense_modifiers = []
        self.sense_type = designation
        self.name = Sense_Type_Description.sense_type_dict[designation]
        self.sense_narrow = sense_narrow
        if sense_narrow == "":
            self.sense_narrow = Sense_Type_Narrow.default_narrow_senses[self.sense_type][0]
        self.sense_flags = []
        self.sense_mask = {}
        self.active = True
        for flag in with_flags:
            flag.set_sense_type(self.sense_type)
            flag.set_narrow(self.sense_narrow)
            self.add_flag(flag)

    def __eq__(self, other):
        if self.sense_type != other.sense_type:
            return False
        if self.sense_narrow != other.sense_narrow:
            return False
        if self.sense_mask != other.sense_mask:
            return False
        if self.sense_modifiers != other.sense_modifiers:
            return False
        return True

    def __str__(self):
        ret_val = self.name + " Sense"
        if self.sense_narrow != "":
            ret_val = ret_val + " [" + self.sense_narrow + "]"
        ret_val = ret_val + ": "
        for entry in self.sense_mask:
            if type(self.sense_mask[entry]) != type({}):
                if self.sense_mask[entry] == 1:
                    ret_val += entry + ", "
                elif self.sense_mask[entry] > 0:
                    ret_val += entry + " " + str(self.sense_mask[entry]) + ", "
            else:
                for value in self.sense_mask[entry]:
                    if self.sense_mask[entry][value] == 1:
                        ret_val += value + " " + entry + ", "
                    elif self.sense_mask[entry][value] > 0:
                        ret_val += value + " " + entry + " " + str(self.sense_mask[entry][value]) + ", "
        return ret_val[:-2]

    def get_type(self):
        return self.sense_type

    def get_narrow(self):
        return self.sense_narrow

    def add_flag(self, sense_flag):
        sense_flag.apply_flag_to_sense(self)

    def remove_flag(self, sense_flag):
        sense_flag.remove_flag_from_sense(self)

    def change_mask_flag(self, mask_tag, change_value=1):
        if mask_tag in self.sense_mask:
            self.sense_mask[mask_tag] += change_value
        else:
            self.sense_mask[mask_tag] = change_value

    def change_mask_flag_dict(self, mask_tag, dict_tag, change_value=1):
        if mask_tag in self.sense_mask:
            if dict_tag in self.sense_mask[mask_tag]:
                self.sense_mask[mask_tag] += change_value
            else:
                self.sense_mask[mask_tag][dict_tag] = change_value
        else:
            self.sense_mask[mask_tag] = {dict_tag: change_value}

    def get_mask_tag(self):
        return self.sense_mask

    def has_mask_tag(self, mask_tag):
        return (not ((mask_tag in self.sense_mask) or (self.sense_mask[mask_tag] == 0)))

    def get_active(self):
        return self.active

    def set_active(self, status):
        self.active = status


class Sense_Type_Description:
    sense_type_dict = {Sense_Type_Designation.VISUAL: "Visual",
                       Sense_Type_Designation.AUDITORY: "Auditory",
                       Sense_Type_Designation.OLFACTORY: "Olfactory",
                       Sense_Type_Designation.TACTILE: "Tactile",
                       Sense_Type_Designation.MENTAL: "Mental",
                       Sense_Type_Designation.RADIO: "Radio"}