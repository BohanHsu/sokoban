from solver import *
from newgameboard import *
from ui import *
from heuristic import *
from newgameboard import *


def helper():
    lines = [
            "Sokoban is the search ai program for solving sokoban game.",
            "This program supports dfs, bfs and A* search aglorithm.",
            "",
            "Usage:",
            "python sokoban.py help             show Help",
            "python sokoban.py h                show Help",
            "python sokoban.py -ng              Not show graphic animation after",
            "                                   solve the path.",
            "python sokoban.py -dfs             Use Depth first search as searching",
            "                                   algorithm, if not search algorithm is",
            "                                   selected, A* will be use as default",
            "python sokoban.py -bfs             Use Beardth first search as searching",
            "                                   algorithm, if not search algorithm is",
            "                                   selected, A* will be use as default",
            "python sokoban.py -p <path>        Required, set path of sokoban game",
            "                                   map.",
            "python sokoban.py -h <heuristic>   Required if using A* algorithm, set name",
            "                                   of heuristic, heurictic name can be found",
            "                                   in './heuristic.py' file.",
            "python sokoban.py -map <path>      Show graph of the map.",
            "",
            "Output:",
            "explored: [number of states expended] states: show how much states",
            "was explored by find the solution.",
            "solution length: [length of path]: show how much steps does solution",
            "take to win the game.",
            "If not given '-ng' argument, there will be a pop up window show each",
            "step of solution",
            "",
            "Example:",
            "python sokoban.py -p ./map/game1.map -h gameHeuristic1",
            ""
            ]

    for line in lines:
        print (line)

def visialize_map(path):
    initialGameBoard = mapToBoard(path)
    Ui([initialGameBoard])

def main():
    i = 1
    arguments = {'ng': False, 'dfs': False, 'bfs': False, 'path': None, 'map': False}
    
    while i < len(sys.argv):
        if sys.argv[i] in ['help', 'h']:
            helper()
            return
        if sys.argv[i] == '-p':
            if i+1 <= len(sys.argv):
                arguments['path'] = sys.argv[i+1]
                i += 2
            else:
                helper()
                return
        elif sys.argv[i] == '-h':
            if i + 1 <= len(sys.argv):
                arguments['heuristic'] = eval(sys.argv[i+1])
                i += 2
            else:
                helper()
                return
        elif sys.argv[i] == '-dfs':
            arguments['dfs'] = True
            i += 1
        elif sys.argv[i] == '-bfs':
            arguments['bfs'] = True
            i += 1
        elif sys.argv[i] == '-ng':
            arguments['ng'] = True
            i += 1
        elif sys.argv[i] == '-map':
            arguments['map'] = True
            if i+1 <= len(sys.argv):
                arguments['path'] = sys.argv[i+1]
                i += 2
            else:
                helper()
                return
        else:
            helper()
            return

    if not arguments['path']:
        helper()
        return

    if arguments['map']:
        visialize_map(arguments['path'])
        return

    initialGameBoard = mapToBoard(arguments['path'])
    
    solver = Solver(initialGameBoard)

    if arguments['bfs']:
        result = solver.bfs()
    elif arguments['dfs']:
        result = solver.dfs()
    else:
        result = solver.Astar(arguments['heuristic'])
    
    boards = result['boards']
    print "explored:", result['count'], 'states'
    print "solution length:", len(result['path'])
    
    if not arguments['ng']:
        Ui(boards)

main()
