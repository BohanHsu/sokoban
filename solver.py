import heapq
from collections import deque

class Solver:
    def __init__(self, gameBoard):
        self.gameBoard = gameBoard

    def bfs(self):
        """
            naive bfs
        """
        count = 0
        queue = deque([self.gameBoard])
        parents = {self.gameBoard: None}

        while len(parents) != 0:
            gb = queue.popleft()
            count += 1
            if gb.isWin():
                path = []
                boards = []
                curGb = gb
                while curGb in parents and not parents[curGb] is None:
                    boards.insert(0, curGb)
                    path.insert(0, parents[curGb].direction)
                    curGb = parents[curGb].parent

                boards.insert(0, curGb)
                return {'path': path, 'boards': boards, 'count': count}

            if gb.isGameOver():
                continue

            for direction in ['n', 's', 'e', 'w']:
                movedGB = gb.moveRobot(direction)
                if not movedGB is None and not movedGB in parents:
                    queue.append(movedGB)
                    parents[movedGB] = Parent(gb, direction)

    def dfs(self):
        """
            naive dfs
        """
        count = 0
        stack = [self.gameBoard]
        parents = {self.gameBoard: None}

        while len(parents) != 0:
            gb = stack.pop()
            count += 1
            if gb.isWin():
                path = []
                boards = []
                curGb = gb
                while curGb in parents and not parents[curGb] is None:
                    boards.insert(0, curGb)
                    path.insert(0, parents[curGb].direction)
                    curGb = parents[curGb].parent

                boards.insert(0, curGb)
                return {'path': path, 'boards': boards, 'count': count}

            if gb.isGameOver():
                continue

            for direction in ['n', 's', 'e', 'w']:
                movedGB = gb.moveRobot(direction)
                if not movedGB is None and not movedGB in parents:
                    stack.append(movedGB)
                    parents[movedGB] = Parent(gb, direction)

    def Astar(self, heuristic):
        """
            naive bfs
        """
        count = 0
        queue = PriorityQueue()
        queue.push(self.gameBoard, heuristic(self.gameBoard))
        parents = {self.gameBoard: None}
        origin = list(self.gameBoard.robot)

        while len(parents) != 0:
            gb = queue.pop()
            count += 1
            if gb.isWin():
                path = []
                boards = []
                curGb = gb
                while curGb in parents and not parents[curGb] is None:
                    boards.insert(0, curGb)
                    path.insert(0, parents[curGb].direction)
                    curGb = parents[curGb].parent

                boards.insert(0, curGb)
                return {'path': path, 'boards': boards, 'count': count}

            if gb.isGameOver():
                continue

            for direction in ['n', 's', 'e', 'w']:
                movedGB = gb.moveRobot(direction)
                if not movedGB is None:
                    cur_robot = list(movedGB.robot)
                    dis_to_origin = abs(cur_robot[0]-origin[0])+abs(cur_robot[1]-origin[1])
                    cost = dis_to_origin + heuristic(movedGB)
                    if not movedGB in parents:
                        queue.push(movedGB,cost)
                        parents[movedGB] = Parent(gb, direction)

class Parent:
    def __init__(self, parent, direction):
        self.parent = parent
        self.direction = direction

class PriorityQueue:
    def  __init__(self):
        self.heap = []
        self.count = 0

    def push(self, item, priority):
        # FIXME: restored old behaviour to check against old results better
        # FIXED: restored to stable behaviour
        entry = (priority, self.count, item)
        # entry = (priority, item)
        heapq.heappush(self.heap, entry)
        self.count += 1

    def pop(self):
        (_, _, item) = heapq.heappop(self.heap)
        #  (_, item) = heapq.heappop(self.heap)
        return item

    def isEmpty(self):
        return len(self.heap) == 0
