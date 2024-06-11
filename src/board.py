from spot import Spot

spot_offset = 27.5

x_start = 144.5
y_start = 371.5

# column X positions
a = x_start
b = x_start + (spot_offset)
c = x_start + (spot_offset * 2)
d = x_start + (spot_offset * 3)
e = x_start + (spot_offset * 4)
f = x_start + (spot_offset * 5)
g = x_start + (spot_offset * 6)
h = x_start + (spot_offset * 7)

# row Y positions
one = y_start
two = y_start - spot_offset
three = y_start - (spot_offset * 2)
four = y_start - (spot_offset * 3)
five = y_start - (spot_offset * 4)
six = y_start - (spot_offset * 5)
seven = y_start - (spot_offset * 6)
eight = y_start - (spot_offset * 7)

spotLUT = [
    ["b1", b, one],["d1", d, one],["f1", f, one],["h1", h, one],
    ["a2", a, two],["c2", c, two],["e2", e, two],["g2", g, two],
    ["b3", b, three],["d3", d, three],["f3", f, three],["h3", h, three],
    ["a4", a, four],["c4", c, four],["e4", e, four],["g4", g, four],
    ["b5", b, five],["d5", d, five],["f5", f, five],["h5", h, five],
    ["a6", a, six],["c6", c, six],["e6", e, six],["g6", g, six],
    ["b7", b, seven],["d7", d, seven],["f7", f, seven],["h7", h, seven],
    ["a8", a, eight],["c8", c, eight],["e8", e, eight],["g8", g, eight]
]

class Board:
    def __init__(self, machine):
        self.spots = []
        self.machine = machine
        self.z = 7
        

        for i in range(32):
            spot = Spot(id=spotLUT[i][0], x_coord=spotLUT[i][1], y_coord=spotLUT[i][2])
            self.spots.append(spot)

    def get(self, id):
        for spot in self.spots:
            if spot.id == id:
                return spot.loaded