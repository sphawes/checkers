from spot import Spot

# column X positions
a = 
b = 
c = 
d = 
e = 
f = 
g = 
h = 

# row Y positions
one = 
two = 
three = 
four = 
five = 
six = 
seven = 
eight = 

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

        self.z_with_piece = 15
        self.z_empty = 10

        for i in range(32):
            spot = Spot(id=spotLUT[i][0], x_coord=spotLUT[i][1], y_coord=spotLUT[i][2])
            self.spots.append(spot)

    def get(self, id):
        for spot in self.spots:
            if spot.id == id:
                return spot.loaded