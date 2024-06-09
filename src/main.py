from board import Board
from machine import Machine
from runner import Runner
from graveyard import Graveyard

# make singletons
machine = Machine()
board = Board(machine)
redGY = Graveyard(15, 100, 100, 1)
blackGY = Graveyard(15, 200, 100, -1)

runner = Runner(machine, board, redGY, blackGY)

machine.home()

#runner.initGame()
#runner.clearBoard()

