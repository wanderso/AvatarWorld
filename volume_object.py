import measurements

class PhysicsObject:
    def __init__(self, vol_size, modifiers={}):
        self.volume_object = vol_loc
        self.velocity = [0,0,0] # I don't expect this to get used

    def get_x_velocity(self):
        return self.velocity[0]

    def get_y_velocity(self):
        return self.velocity[1]

    def get_z_velocity(self):
        return self.velocity[2]

class VolumeLocation:
    def __init__(self, x, y, z):
        self.x_loc = x
        self.y_loc = y
        self.z_loc = z

class VolumeSize:
    def __init__(self, leng, wid, hei):
        self.length = leng
        self.width = wid
        self.height = hei

