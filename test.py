import unittest

from newgameboard import *
from solver import *

class TestGameBoard(unittest.TestCase):
    def setUp(self):
        self.gameBoard = mapToBoard('./map/test_map3.map')

    def test_initObstacles(self):
        expectedObstacle = set()
        for j in range(0, 5):
            expectedObstacle.add((0, j))
            expectedObstacle.add((4, j))

        expectedObstacle.add((4,5))

        for i in range(1,4):
            expectedObstacle.add((i, 0))
            expectedObstacle.add((i, 5))

        expectedObstacle.add((1, 4))
        self.assertEqual(self.gameBoard.obstacles, expectedObstacle)

    def test_initBoxes(self):
        expectedBoxed = set()
        expectedBoxed.add((2, 2))
        self.assertEqual(self.gameBoard.boxes, expectedBoxed)

    def test_initGoals(self):
        expectedGoals = set()
        expectedGoals.add((1, 2))
        self.assertEqual(self.gameBoard.goals, expectedGoals)

    def test_initRobot(self):
        expectedRobot = (3, 2)
        self.assertEqual(self.gameBoard.robot, expectedRobot)

    def test_initPlayArea(self):
        expectedPlayArea = set()
        for j in range(1, 4):
            expectedPlayArea.add((1, j))

        for i in range(2, 4):
            for j in range(1, 5):
                expectedPlayArea.add((i, j))

        self.assertEqual(self.gameBoard.playArea, expectedPlayArea)

    def test_initDeadPoint(self):
        expectedDeadPoint = set()
        expectedDeadPoint.add((1, 1))
        expectedDeadPoint.add((1, 3))
        expectedDeadPoint.add((2, 4))
        expectedDeadPoint.add((3, 1))
        expectedDeadPoint.add((3, 4))
        self.assertEqual(self.gameBoard.deadPoints, expectedDeadPoint)

    def test_initWalls(self):
        expectedWalls = set()
        expectedWalls.add(str(Wall({'n': (0, 0), 's': (4, 0)})))
        expectedWalls.add(str(Wall({'n': (0, 4), 's': (1, 4)})))
        expectedWalls.add(str(Wall({'n': (1, 5), 's': (4, 5)})))
        expectedWalls.add(str(Wall({'w': (0, 0), 'e': (0, 4)})))
        expectedWalls.add(str(Wall({'w': (1, 4), 'e': (1, 5)})))
        expectedWalls.add(str(Wall({'w': (4, 0), 'e': (4, 5)})))
        realWalls = set([str(w) for w in self.gameBoard.walls])
        self.assertEqual(len(self.gameBoard.walls), 6)
        self.assertEqual(realWalls, expectedWalls)

    def test_initTraps(self):
        expectedTraps = set()
        expectedTraps.add(((1,1), (1,2), (1,3)))
        expectedTraps.add(((3,1), (3,2), (3,3), (3,4)))
        expectedTraps.add(((1,1), (2,1), (3,1)))
        expectedTraps.add(((2,4), (3,4)))

        realPoints = set()
        for t in self.gameBoard.traps:
            nl = list(t.points)
            nl.sort()
            realPoints.add(tuple(nl))

        self.assertEqual(len(self.gameBoard.traps), 4)
        self.assertEqual(expectedTraps, realPoints)

        capacities = set([t.capacity() for t in self.gameBoard.traps])
        realCapacities = set([1,0,0,0])
        self.assertEqual(capacities, realCapacities)

    def test_initCouldMove(self):
        self.assertEqual(self.gameBoard.couldMove('s'), None)
        self.assertEqual(self.gameBoard.couldMove('e'), {'oldRobot': (3,2), 'newRobot': (3,3)})
        self.assertEqual(self.gameBoard.couldMove('w'), {'oldRobot': (3,2), 'newRobot': (3,1)})
        self.assertEqual(self.gameBoard.couldMove('n'), {'oldRobot': (3,2), 'newRobot': (2,2), 'oldBox': (2,2), 'newBox': (1,2)})

    def test_initMoveRobot(self):
        self.assertEqual(self.gameBoard.moveRobot('s'), None)
        moveEastBoard = self.gameBoard.moveRobot('e')
        self.assertEqual(self.gameBoard.obstacles, moveEastBoard.obstacles)
        self.assertEqual(self.gameBoard.boxes, moveEastBoard.boxes)
        self.assertEqual(self.gameBoard.goals, moveEastBoard.goals)
        self.assertEqual(moveEastBoard.robot, (3,3))
        self.assertEqual(self.gameBoard.walls, moveEastBoard.walls)
        self.assertEqual(self.gameBoard.playArea, moveEastBoard.playArea)
        self.assertEqual(self.gameBoard.deadPoints, moveEastBoard.deadPoints)
        trapPoints1 = set()
        for t in self.gameBoard.traps:
            nl = list(t.points)
            nl.sort()
            trapPoints1.add(tuple(nl))

        trapPoints2 = set()
        for t in moveEastBoard.traps:
            nl = list(t.points)
            nl.sort()
            trapPoints2.add(tuple(nl))

        self.assertEqual(trapPoints1, trapPoints2)

        capacities1 = set([t.capacity() for t in self.gameBoard.traps])
        capacities2 = set([t.capacity() for t in moveEastBoard.traps])
        self.assertEqual(capacities1, capacities2)

        moveNorthBoard = self.gameBoard.moveRobot('n')
        self.assertEqual(moveNorthBoard.boxes, set([(1,2)]))
        capacities3 = set([t.capacity() for t in moveNorthBoard.traps])
        realCapacities = set([0 for i in range(0, 4)])
        self.assertEqual(capacities3, realCapacities)

    def test_isWin(self):
        self.assertEqual(self.gameBoard.isWin(), False)
        self.assertEqual(self.gameBoard.moveRobot('n').isWin(), True)

    def test_isGameOver(self):
        self.assertEqual(self.gameBoard.isGameOver(), False)
        gameOverBoard1 = mapToBoard('./map/test_map4.map')
        gameOverBoard2 = mapToBoard('./map/test_map5.map')
        self.assertEqual(gameOverBoard1.isGameOver(), True)
        self.assertEqual(gameOverBoard2.isGameOver(), True)

    def test_hashMethods(self):
        s = set()
        s.add(self.gameBoard)
        moveE = self.gameBoard.moveRobot('e')
        s.add(moveE)
        self.assertEqual(len(s), 2)
        moveEW = moveE.moveRobot('w')
        s.add(moveEW)
        self.assertEqual(len(s), 2)

class TestSolver(unittest.TestCase):
    def setUp(self):
        self.gameBoard = mapToBoard('./map/test_map3.map')
        self.solver = Solver(self.gameBoard)

    def test_dfs(self):
        pass

class TestMove(unittest.TestCase):
    def test_moveNorth(self):
        self.assertEqual(move('n')((1, 1)), (0, 1))

    def test_moveSouth(self):
        self.assertEqual(move('s')((1, 1)), (2, 1))

    def test_moveEase(self):
        self.assertEqual(move('e')((1, 1)), (1, 2))

    def test_moveWest(self):
        self.assertEqual(move('w')((1, 1)), (1, 0))

if __name__ == '__main__':
    unittest.main()
