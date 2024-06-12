import time

from board import Board
from machine import Machine
from runner import Runner
from graveyard import Graveyard

# make singletons
machine = Machine()
board = Board(machine)
redGY = Graveyard(6.8, 91.5, 178, -1)
blackGY = Graveyard(6.8, 390.5, 178, 1)

runner = Runner(machine, board, redGY, blackGY)

machine.home()

print("ambient: " + str(machine.readLeftVac()))

try:
    runner.probeBoard()
    while True:
        runner.playGame()
except KeyboardInterrupt:
    runner.gracefulExit()


