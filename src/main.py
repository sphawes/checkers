import time

from board import Board
from machine import Machine
from runner import Runner
from graveyard import Graveyard

# make singletons
machine = Machine()
board = Board(machine)
redGY = Graveyard(7.25, 91.5, 178, -1)
blackGY = Graveyard(7.25, 390.5, 178, 1)

runner = Runner(machine, board, redGY, blackGY)

machine.home()

print("ambient: " + str(machine.readLeftVac()))

for i in runner.blackInit:
    runner.draw("BLACK")
    runner.place(i)

for i in runner.redInit:
    runner.draw("RED")
    runner.place(i)

runner.playGame()

#runner.moveToEverySpot()

machine.pump(False)
machine.park()

#runner.initGame()
#runner.clearBoard()

