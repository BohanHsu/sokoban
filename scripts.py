from solver import *
from newgameboard import *
from ui import *

initialGameBoard = mapToBoard('./map/game2.map')

solver = Solver(initialGameBoard)

#result = solver.dfs()
result = solver.bfs()

boards = result['boards']

Ui(boards)
