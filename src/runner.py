
class Runner:
    def __init__(self, machine, board, redGY, blackGY):
        self.machine = machine
        self.board = board
        self.redGY = redGY
        self.blackGY = blackGY

        self.blackInit = ["a1", "b1", "c1", "d1", "a2", "b2", "c2", "d2", "a3", "b3", "c3", "d3"]
        self.redInit = ["a6", "b6", "c6", "d6", "a7", "b7", "c7", "d7", "a8", "b8", "c8", "d8"]
        self.emptyInit = ["a4", "b4", "c4", "d4", "a5", "b5", "c5", "d5"]

    def pick(self, id):
        if not self.machine.hasPart:
            for spot in self.board.spots:
                if spot.id == id:
                    self.machine.goto(x=spot.x_coord, y=spot.y_coord)
                    self.machine.goto(z=self.board.z_with_piece)
                    self.machine.pump(True)
                    #any delay needed
                    self.machine.safeZ()

                    self.machine.loaded = spot.loaded
                    spot.loaded = None

    def place(self, id):
        if self.machine.loaded is not None:
            for spot in self.board.spots:
                if spot.id == id and spot.piece == None:
                    self.machine.goto(x=spot.x_coord, y=spot.y_coord)
                    self.machine.goto(z=self.board.z_with_piece)
                    self.machine.pump(False)
                    #any delay needed
                    self.machine.safeZ()
                    #assigning the spot the loaded part
                    spot.loaded = self.machine.loaded
                    #assigning the machine no part
                    self.machine.loaded = None

    def discard(self):
        if self.machine.loaded is not None:
            if self.machine.loaded == "BLACK":
                # discard to black graveyard
                gy = self.blackGY
            else:
                # discard to black graveyard
                gy = self.redGY

            x, y = gy.getCoords()
            self.machine.goto(x=x, y=y)
            self.machine.goto(z=gy.z)
            self.machine.pump(False)
            self.machine.safeZ()
            gy.increment()
            self.machine.loaded = None

    def draw(self, color):

        if self.machine.loaded is None:
            if color == "BLACK":
                # discard to black graveyard
                gy = self.blackGY
            else:
                # discard to black graveyard
                gy = self.redGY

            x, y = gy.getCoords()
            self.machine.goto(x=x, y=y)
            self.machine.goto(z=gy.z)
            self.machine.pump(True)
            self.machine.safeZ()
            gy.decrement()
            self.machine.loaded = color

    def clearBoard(self):
        for spot in self.board.spots:
            if spot.loaded != None:
                self.pick(spot.id)
                self.discard()

    def initGame(self):
        for i in self.blackInit:
            if self.board.get(i) == None:
                #load with black
                self.draw("BLACK")
                self.place(i)
            elif self.board.get(i) == "RED":
                #unload red, load black
                self.pick(i)
                self.discard()
                self.draw("BLACK")
                self.place(i)
        
        for i in self.redInit:
            if self.board.get(i) == None:
                #load with black
                self.draw("RED")
                self.place(i)
            elif self.board.get(i) == "BLACK":
                #unload red, load black
                self.pick(i)
                self.discard()
                self.draw("RED")
                self.place(i)

        for i in self.emptyInit:
            if self.board.get(i) != None:
                self.pick(i)
                self.discard()
            