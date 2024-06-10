
class Graveyard:
    def __init__(self, z, x_start, y_start, flip):
        self.z = z
        self.x_start = x_start
        self.y_start = y_start
        self.flip = flip

        self.count = 0

        self.y_offset = 27
        self.row2_x = 23.5
        self.row2_y = 14

    def getCoords(self):
        if self.count > 5:
            return self.x_start + (self.row2_x * self.flip), self.y_start + ((self.count-6) * self.y_offset) + self.row2_y
        else:
            return self.x_start, self.y_start + (self.count * self.y_offset)

    def increment(self):
        if self.count < 11:
            self.count = self.count + 1

    def decrement(self):
        if self.count > 0:
            self.count = self.count - 1