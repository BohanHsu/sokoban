from solver import *
from newgameboard import *
from ui import *

initialGameBoard = mapToBoard('./map/game2.map')

solver = Solver(initialGameBoard)

result = solver.dfs()
#result = solver.bfs()

boards = result['boards']
print "explored:", result['count'], 'states'
print "solution length:", len(result['path'])

Ui(boards)
