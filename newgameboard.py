import random

class GameBoard:
    """
    game board of sokoban, redesign from gameboard
    """
    def __init__(self, obstacles, boxes, goals, robot, hsh={}):
        #self.key = GameBoardKey()
        if 'genesis' in hsh:
            self.stamp = hsh['genesis']
        else:
            self.stamp = random.randint(0, 10000)

        self.obstacles = obstacles
        self.boxes = boxes
        self.goals = goals
        self.robot = robot
        if 'traps' in hsh and 'walls' in hsh and 'playArea' in hsh and 'deadPoints' in hsh:
            self.walls = hsh['walls']
            self.playArea = hsh['playArea']
            self.deadPoints = hsh['deadPoints']
            self.traps = set([trap.clone(self) for trap in hsh['traps']])
        else:
            self.playArea = self.findPlayArea()
            self.deadPoints = self.findDeadPoints()
            self.walls = self.findWalls()
            self.traps = self.findTraps()

    def isWin(self):
        return len(self.boxes - self.goals) == 0

    def isGameOver(self):
        if self.isWin():
            return False

        if len(self.boxes & self.deadPoints) > 0:
            return True

        for trap in self.traps:
            if trap.capacity() < 0:
                return True

        return False

    def moveRobot(self, direction):
        moveResult = self.couldMove(direction)
        if moveResult is None:
            return None

        newBoxes = set(self.boxes)
        if 'oldBox' in moveResult and 'newBox' in moveResult:
            newBoxes.remove(moveResult['oldBox'])
            newBoxes.add(moveResult['newBox'])

        hsh = {'genesis': self.stamp}
        hsh['walls'] = self.walls
        hsh['playArea'] = self.playArea
        hsh['deadPoints'] = self.deadPoints
        hsh['traps'] = self.traps
        return GameBoard(self.obstacles, newBoxes, self.goals, moveResult['newRobot'], hsh)

    def couldMove(self, direction):
        """
            check if a direcrtion of move to the robot is valid
        """
        newPosition = move(direction)(self.robot)
        if newPosition in self.obstacles:
            return None

        result = {'oldRobot': self.robot, 'newRobot': newPosition}
        if newPosition in self.boxes:
            boxNewPosition = move(direction)(newPosition)
            if boxNewPosition in self.boxes or boxNewPosition in self.obstacles:
                return None
            else:
                result['oldBox'] = newPosition
                result['newBox'] = boxNewPosition

        return result


    def findTraps(self):
        """
            find all traps in gameboard
        """
        def createTrap(p1, p2):
            points = None
            if p1[0] == p2[0]:
                i = p1[0]
                points = set([(i, j) for j in range(p2[1] + 1, p1[1])])
            else:
                j = p1[1]
                points = set([(i, j) for i in range(p1[0] + 1, p2[0])])

            if len([p for p in points if p not in self.playArea]) > 0:
                return None

            return Trap(points, self)

        traps = set()
        for wall in self.walls:
            if wall.direction == 'v':
                np = wall.northPoint
                sp = wall.southPoint
                if move('e')(np) in self.obstacles and move('e')(sp) in self.obstacles:
                    trap = createTrap(move('e')(np), move('e')(sp))
                    if not trap is None:
                        traps.add(trap)

                if move('w')(np) in self.obstacles and move('w')(sp) in self.obstacles:
                    trap = createTrap(move('w')(np), move('w')(sp))
                    if not trap is None:
                        traps.add(trap)

            else:
                ep = wall.eastPoint
                wp = wall.westPoint
                if move('n')(ep) in self.obstacles and move('n')(wp) in self.obstacles:
                    trap = createTrap(move('n')(ep), move('n')(wp))
                    if not trap is None:
                        traps.add(trap)

                if move('s')(ep) in self.obstacles and move('s')(wp) in self.obstacles:
                    trap = createTrap(move('s')(ep), move('s')(wp))
                    if not trap is None:
                        traps.add(trap)

        return traps


    def findWalls(self):
        def isIntersection(p):
            if not p in self.obstacles:
                return False

            np = move('n')(p)
            sp = move('s')(p)
            ep = move('e')(p)
            wp = move('w')(p)
            return (np in self.obstacles or sp in self.obstacles) and (ep in self.obstacles or wp in self.obstacles)

        def isTerminal(p, direction):
            oppositeDirection = {'n': 's', 's': 'n', 'e': 'w', 'w': 's'}[direction]

            for dir in ['n', 's', 'e', 'w']:
                if dir != oppositeDirection:
                    if move(dir)(p) in self.obstacles:
                        return False

            return True

        northWallI = min(self.obstacles, key=lambda x: x[0])[0]
        northWall = [obstacle for obstacle in self.obstacles if obstacle[0] == northWallI]
        northWestObstacle = min(northWall, key=lambda x: x[1])

        walls = set()
        visitedObstacles = set()
        stack = []
        southP = move('s')(northWestObstacle)
        stack.append((northWestObstacle, southP, 's'))
        eastP = move('e')(northWestObstacle)
        stack.append((northWestObstacle, eastP, 'e'))

        while len(stack) != 0:
            vector = stack.pop()
            point = vector[1]
            direction = vector[2]
            visitedObstacles.add(point)
            if isIntersection(point) or isTerminal(point, direction):
                if direction == 'n':
                    walls.add(Wall({'n': point, 's': vector[0]}))
                elif direction == 's':
                    walls.add(Wall({'s': point, 'n': vector[0]}))
                elif direction == 'e':
                    walls.add(Wall({'e': point, 'w': vector[0]}))
                elif direction == 'w':
                    walls.add(Wall({'w': point, 'e': vector[0]}))

                if isIntersection(point):
                    for dir in ['n', 's', 'e', 'w']:
                        movedPoint = move(dir)(point)
                        if movedPoint in self.obstacles and not movedPoint in visitedObstacles:
                            stack.append((point, movedPoint, dir))

            else:
                movedPoint = move(direction)(point)
                if not movedPoint in visitedObstacles:
                    stack.append((vector[0], movedPoint, direction))

        return walls


    def findDeadPoints(self):
        if len(self.playArea) == 0:
            raise Exception('PlayArea not calculated')

        def isDeadPoint(p):
            np = move('n')(p)
            sp = move('s')(p)
            ep = move('e')(p)
            wp = move('w')(p)
            return (np in self.obstacles or sp in self.obstacles) and (ep in self.obstacles or wp in self.obstacles) and not p in self.goals

        result = set()
        for point in self.playArea:
            if isDeadPoint(point):
                result.add(point)

        return result


    def findPlayArea(self):
        maxI = max(self.obstacles, key=lambda x: x[0])[0] + 2
        maxJ = max(self.obstacles, key=lambda x: x[1])[1] + 2

        northWallI = min(self.obstacles, key=lambda x: x[0])[0]
        northWall = [obstacle for obstacle in self.obstacles if obstacle[0] == northWallI]
        northWestObstacle = min(northWall, key=lambda x: x[1])

        srcPoint = (northWestObstacle[0] + 1, northWestObstacle[1] + 1)

        def bfs(src):
            visitedPoints = set()
            stack = [src]
            visitedPoints.add(src)

            while len(stack) != 0:
                p = stack.pop()
                visitedPoints.add(p)
                if (p[0] < 0 or p[0] > maxI or p[1] < 0 or p[1] > maxJ):
                    raise Exception('Game Board Error')

                for newP in [move(direction)(p) for direction in ['n', 's', 'w', 'e']]:
                    if not newP in visitedPoints and not newP in self.obstacles:
                        stack.append(newP)

            return visitedPoints

        if srcPoint in self.obstacles:
            raise Exception('Game Board Error')

        return bfs(srcPoint)

    def __hash__(self):
        return self.stamp + sum([hash(box) for box in self.boxes]) + hash(self.robot)

    def __cmp__(self, other):
        if self.stamp != other.stamp:
            return self.stamp - other.stamp

        if self.boxes == other.boxes and self.robot == other.robot:
            return 0
        else:
            return cmp(self.boxes, other.boxes) + cmp(self.robot, other.robot)

    def __eq__(self, other):
        return self.stamp == other.stamp and self.boxes == other.boxes and self.robot == other.robot

    def __ne__(self, other):
        return not self.__eq__(other)

class Wall:
    def __init__(self, points):
        if 'n' in points and 's' in points:
            self.direction = 'v'
            self.northPoint = points['n']
            self.southPoint = points['s']
        elif 'e' in points and 'w' in points:
            self.direction = 'h'
            self.eastPoint = points['e']
            self.westPoint = points['w']
    
    def __str__(self):
        if self.direction == 'h':
            return "horizontal: " + str(self.eastPoint) + '--' + str(self.westPoint)
        if self.direction == 'v':
            return "vertical: " + str(self.northPoint) + '--' + str(self.southPoint)


class Trap:
    def __init__(self, points, gameboard):
        self.points = points
        self.gameboard = gameboard

    def clone(self, gameboard):
        return Trap(self.points, gameboard)

    def capacity(self):
        count = 0
        for goal in self.gameboard.goals:
            if goal in self.points:
                count += 1

        for box in self.gameboard.boxes:
            if box in self.points:
                count -= 1

        return count


def move(direction):
    def getNorthPosition(position):
        return (position[0] - 1, position[1])
    
    def getSouthPosition(position):
        return (position[0] + 1, position[1])
    
    def getEastPosition(position):
        return (position[0], position[1] + 1)
    
    def getWestPosition(position):
        return (position[0], position[1] - 1)

    if direction == 'n':
        return getNorthPosition
    if direction == 's':
        return getSouthPosition
    if direction == 'e':
        return getEastPosition
    if direction == 'w':
        return getWestPosition

class GameBoardKey:
    def __init__(self):
        pass

def mapToBoard(path):
    obstacles = set([])
    boxes = set([])
    goals = set([])
    robot = None
    file = open(path)
    lines = file.read().split("\n")
    for yi, line in enumerate(lines):
        for xi, char in enumerate(line):
            if char == '#':
                obstacles.add((yi, xi))
            elif char == 'b':
                boxes.add((yi, xi))
            elif char == 'g':
                goals.add((yi, xi))
            elif char == 'r':
                robot = (yi, xi)
            elif char == 'B':
                boxes.add((yi, xi))
                goals.add((yi, xi))
            elif char == 'R':
                robot = (yi, xi)
                goals.add((yi, xi))

    return GameBoard(obstacles, boxes, goals, robot)
