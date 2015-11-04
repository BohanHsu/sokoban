class GameBoard:
    def __init__(self, obstacles, boxes, goals, robot):
        self.obstacles = obstacles
        self.boxes = boxes
        self.goals = goals
        self.robot = robot
        self.traps = set()
        self.walls = self.findWalls()
        self.deadPositions = set()
        self.playArea = None
        self.findTraps(self.walls, self.obstacles)

    def findTraps(self, walls, obstacles):
        boundaryX = 0
        boundaryY = 0
        for obstacle in obstacles:
            if obstacle[0] > boundaryX:
                boundaryX = obstacle[0]

            if obstacle[1] > boundaryY:
                boundaryY = obstacle[1]

        boundaryX += 5
        boundaryY += 5
        northwallY = min(self.obstacles, key=lambda x: x[1])[1]
        northwall = [obstacle for obstacle in self.obstacles if obstacle[1] == northwallY]
        northwallEastObstacle = min(northwall, key=lambda x: x[0])

        srcPoint = (northwallEastObstacle[0] + 1, northwallEastObstacle[1] + 1)
        if srcPoint in obstacle:
            raise Exception('Game Board Error')

        def bfs(srcPoint, tgtPoint, obstacles):
            visitedPoints = set()
            stack = [srcPoint]
            visitedPoints.add(srcPoint)

            while len(stack) != 0:
                p = stack.pop()
                visitedPoints.add(p)
                if p == tgtPoint:
                    raise Exception('Game Board Error')

                for newP in [move(direction)(p) for direction in ['n', 's', 'w', 'e']]:
                    if not newP in visitedPoints and not newP in obstacles:
                        stack.append(newP)
            
            return visitedPoints
        
        self.playArea = bfs(srcPoint, (boundaryX, boundaryY), obstacles)

        def isDeadPosition(point):
            np = move('n')(point)
            sp = move('s')(point)
            ep = move('e')(point)
            wp = move('w')(point)
            return (np in self.obstacles or sp in self.obstacles) and (ep in self.obstacles or wp in self.obstacles)

        for p in self.playArea:
            if isDeadPosition(p) and not p in self.goals:
                self.deadPositions.add(p)

        def handleTrap(p1, p2):
            if p1[0] == p2[0]:
                x = p1[0]
                positions = [(x, y) for y in range(p1[1] + 1, p2[1])]
            else:
                y = p1[1]
                positions = [(x, y) for x in range(p1[0] + 1, p2[0])]

            if len([p for p in positions if not p in self.playArea]) > 0:
                return None
            trap = Trap(positions, self)
            #trap.capacity = len([p for p in positions if p in self.goals])
            return trap

        for wall in walls:
            if wall.direction == 'v':
                np = wall.northPoint
                sp = wall.southPoint
                if move('e')(np) in obstacles and move('e')(sp) in obstacles:
                    trap = handleTrap(move('e')(np), move('e')(sp))
                    if not trap is None:
                        self.traps.add(trap)

                if move('w')(np) in obstacles and move('w')(sp) in obstacles:
                    trap = handleTrap(move('w')(np), move('w')(sp))
                    if not trap is None:
                        self.traps.add(trap)

            else:
                ep = wall.eastPoint
                wp = wall.westPoint
                if move('n')(ep) in obstacles and move('n')(wp) in obstacles:
                    trap = handleTrap(move('n')(ep), move('n')(wp))
                    if not trap is None:
                        self.traps.add(trap)

                if move('s')(ep) in obstacles and move('s')(wp) in obstacles:
                    trap = handleTrap(move('s')(ep), move('s')(wp))
                    if not trap is None:
                        self.traps.add(trap)

    def findWalls(self):
        def isIntersection(obstacle):
            np = (obstacle[0], obstacle[1] - 1)
            sp = (obstacle[0], obstacle[1] + 1)
            ep = (obstacle[0] - 1, obstacle[1])
            wp = (obstacle[0] + 1, obstacle[1])
            return ((np in self.obstacles or sp in self.obstacles) and \
            (ep in self.obstacles or wp in self.obstacles))

        def isTerminal(obstacle, direction):
            oppo_dir = None
            if direction == 'n':
                oppo_dir = 's'
            elif direction == 's':
                oppo_dir = 'n'
            elif direction == 'e':
                oppo_dir = 'w'
            elif direction == 'w':
                oppo_dir = 'e'

            for dir in ['n', 's', 'e', 'w']:
                if oppo_dir != dir:
                    if move(dir)(obstacle) in self.obstacles:
                        return False
            
            return True

        northwallY = min(self.obstacles, key=lambda x: x[1])[1]
        northwall = [obstacle for obstacle in self.obstacles if obstacle[1] == northwallY]
        northwallEastObstacle = min(northwall, key=lambda x: x[0])

        walls = set()
        visitedObstacles = set()
        stack = []
        south_p = move('s')(northwallEastObstacle)
        stack.append((northwallEastObstacle, south_p, 's'))
        west_p = move('w')(northwallEastObstacle)
        stack.append((northwallEastObstacle, west_p, 'w'))
        #visitedObstacles.add(northwallEastObstacle)

        while len(stack) != 0:
            vector = stack.pop()
            point = vector[1]
            direction = vector[2]
            visitedObstacles.add(point)
            if isIntersection(point):
                if direction == 'n':
                    walls.add(Wall({'n': point, 's': vector[0]}))
                elif direction == 's':
                    walls.add(Wall({'s': point, 'n': vector[0]}))
                elif direction == 'e':
                    walls.add(Wall({'e': point, 'w': vector[0]}))
                elif direction == 'w':
                    walls.add(Wall({'w': point, 'e': vector[0]}))

                for dir in ['n', 's', 'e', 'w']:
                    movedPoint = move(dir)(point)
                    if movedPoint in self.obstacles and not movedPoint in visitedObstacles:
                        stack.append((point, movedPoint, dir))

            elif isTerminal(point, direction):
                if direction == 'n':
                    walls.add(Wall({'n': point, 's': vector[0]}))
                elif direction == 's':
                    walls.add(Wall({'s': point, 'n': vector[0]}))
                elif direction == 'e':
                    walls.add(Wall({'e': point, 'w': vector[0]}))
                elif direction == 'w':
                    walls.add(Wall({'w': point, 'e': vector[0]}))

            else:
                movedPoint = move(direction)(point)
                if not movedPoint in visitedObstacles:
                    stack.append((vector[0], movedPoint, direction))

        return walls    

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
    def __init__(self, positions, gameboard):
        self.positions = set(positions)
        self.gameboard = gameboard
    
    def capacity(self):
        count = 0
        for goal in self.gameboard.goals:
            if goal in self.positions:
                count += 1

        for box in self.gameboard.boxes:
            if box in self.positions:
                count -= 1

        if count < 0:
            return 0
        return count

def move(direction):
    def getNorthPosition(position):
        return (position[0], position[1] - 1)
    
    def getSouthPosition(position):
        return (position[0], position[1] + 1)
    
    def getEastPosition(position):
        return (position[0] - 1, position[1])
    
    def getWestPosition(position):
        return (position[0] + 1, position[1])

    if direction == 'n':
        return getNorthPosition
    if direction == 's':
        return getSouthPosition
    if direction == 'e':
        return getEastPosition
    if direction == 'w':
        return getWestPosition

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
                obstacles.add((xi, yi))
            elif char == 'b':
                boxes.add((xi, yi))
            elif char == 'g':
                goals.add((xi, yi))
            elif char == 'r':
                robot = (xi, y1)

    return GameBoard(obstacles, boxes, goals, robot)
