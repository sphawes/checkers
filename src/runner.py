
class Runner:
    def __init__(self, machine, board, redGY, blackGY):
        self.machine = machine
        self.board = board
        self.redGY = redGY
        self.blackGY = blackGY

        self.blackInit = ["b1", "d1", "f1", "h1", "a2", "c2", "e2", "g2", "b3", "d3", "f3", "h3"]
        self.emptyInit = ["a4", "c4", "e4", "g4", "b5", "d5", "f5", "h5"]
        self.redInit = ["a6", "c6", "e6", "g6", "b7", "d7", "f7", "h7", "a8", "c8", "e8", "g8"]
        

    def pick(self, id):
        if self.machine.loaded is None:
            for spot in self.board.spots:
                if spot.id == id:
                    self.machine.goto(x=spot.x_coord, y=spot.y_coord)
                    self.machine.goto(z=self.board.z)
                    self.machine.pump(True)
                    #any delay needed
                    self.machine.send("G4 P300")
                    self.machine.safeZ()
                    self.machine.send("G4 P10")
                    vac = self.machine.readLeftVac()
                    if vac > -700000:
                        print("low vac, retry")
                        self.machine.goto(z=self.board.z + 0.2)
                        self.machine.send("G4 P400")
                        self.machine.safeZ()

                    self.machine.loaded = spot.loaded
                    spot.loaded = None

    def place(self, id):
        if self.machine.loaded is not None:
            for spot in self.board.spots:
                if spot.id == id and spot.loaded == None:
                    self.machine.goto(x=spot.x_coord, y=spot.y_coord)
                    self.machine.goto(z=self.board.z)
                    self.machine.pump(False)
                    #any delay needed
                    self.machine.send("G4 P200")
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
            self.machine.send("G4 P200")
            self.machine.safeZ()
            gy.decrement()
            self.machine.loaded = None

    def dance(self):
        self.machine.park()
        self.machine.goto(z=3)
        self.machine.goto(z=60)
        self.machine.goto(z=3)
        self.machine.goto(z=60)
        self.machine.safeZ()

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
            self.machine.send("G4 P350")
            self.machine.safeZ()
            self.machine.send("G4 P10")
            vac = self.machine.readLeftVac()
            if vac > -700000:
                print("low vac, retry")
                self.machine.goto(z=gy.z + 0.2)
                self.machine.send("G4 P400")
                self.machine.safeZ()
            gy.increment()
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
            
    def playGame(self):
        # prep the board for a game
        self.initGame()

        moves = [
            ["c6", "d5"],
            ["b3", "a4"],
            ["g6", "f5"],
            ["c2", "b3"],
            ["h7", "g6"],
            ["d1", "c2"],
            ["f5", "g4"],
            ["h3", "f5"],
            ["f5", "h7"],
            ["g4", "d"],
            ["g6", "d"],
            ["e6", "f5"],
            ["f3", "e4"],
            ["d5", "f3"],
            ["e4", "d"],
            ["e2", "g4"],
            ["f3", "d"],
            ["f5", "h3"],
            ["g4", "d"],
            ["b3", "c4"],
            ["a6", "b5"],
            ["c4", "a6"],
            ["b5", "d"],
            ["b7", "c6"],
            ["d3", "c4"],
            ["c6", "d5"],
            ["c4", "e6"],
            ["e6", "g4"],
            ["d5", "d"],
            ["f5", "d"],
            ["d7", "c6"],
            ["a4", "b5"],
            ["c6", "a4"],
            ["b5", "d"],
            ["g4", "f5"],
            ["a4", "b3"],
            ["a2", "c4"],
            ["b3", "d"],
            ["c8", "d7"],
            ["c4", "d5"],
            ["a8", "b7"],
            ["a6", "c8"],
            ["c8", "e6"],
            ["b7", "d"],
            ["d7", "d"],
            ["e8", "d7"],
            ["e6", "c8"],
            ["d7", "d"],
            ["f7", "e6"],
            ["f5", "d7"],
            ["e6", "d"],
            ["g8", "f7"],
            ["h7", "g6"],
            ["f7", "e6"],
            ["d5", "f7"],
            ["e6", "d"]       
        ]


        for move in moves:
            self.pick(move[0])
            if move[1] == "d":
                self.discard()
            else:
                self.place(move[1])

        self.dance()

        self.clearBoard()


    

