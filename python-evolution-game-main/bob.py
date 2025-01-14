class Bob:
    def __init__(self, id_bob, x, y, e_spawn=100, speed=1,mass=1, maman=0):
        self.id_bob = id_bob
        self.energy = e_spawn
        self.e_spawn = e_spawn
        self.maman = maman
        self.fils = []
        self.x = x
        self.y = y
        self.speed = speed
        self.speed_buffer = 0
        self.mass = mass

    def set_energy(self, energy):
        self.energy = energy

    def set_pos(self, x, y):
        self.x = x
        self.y = y

    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y

    def get_pos(self):
        return (self.x, self.y)

    def get_energy(self):
        return self.energy

    def get_id(self):
        return self.id_bob

    def get_speed(self):
        return self.speed

    def get_mass(self):
        return self.mass
    
    def set_mass(self, new_mass):
        self.mass = new_mass
        
    def set_speed(self, new_speed):
        self.speed = new_speed

    def get_speed_buffer(self):
        return self.speed_buffer

    def set_speed_buffer(self,new_buffer):
        self.speed_buffer = round(new_buffer,1)
    
    def get_maman(self):
        return self.maman
    
    def set_maman(self, new_maman):
        self.maman = new_maman
    
    def get_fils(self):
        return self.fils
    
    def set_fils(self,new_fils):
        self.fils.append(new_fils)
    
    def move_bob(self, x, y):
        self.x = x
        self.y = y
