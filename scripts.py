from solver import *
from newgameboard import *
from ui import *

initialGameBoard = mapToBoard('./map/game1.map')

solver = Solver(initialGameBoard)

result = solver.dfs()

boards = result['boards']

Ui(boards)
