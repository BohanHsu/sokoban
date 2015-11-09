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

class Parent:
    def __init__(self, parent, direction):
        self.parent = parent
        self.direction = direction
