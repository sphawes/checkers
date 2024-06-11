import time

from board import Board
from machine import Machine
from runner import Runner
from graveyard import Graveyard

# make singletons
machine = Machine()
board = Board(machine)
redGY = Graveyard(7, 91.5, 178, -1)
blackGY = Graveyard(7, 390.5, 178, 1)

runner = Runner(machine, board, redGY, blackGY)

machine.home()

print("ambient: " + str(machine.readLeftVac()))

try:
    while True:
        runner.playGame()
except KeyboardInterrupt:
    machine.safeZ()
    runner.discard()
    machine.pump(False)
    machine.park()


