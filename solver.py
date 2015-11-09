class Solver:
    def __init__(self, gameBoard):
        self.gameBoard = gameBoard

    def dfs(self):
        """
            naive dfs
        """
        stack = [self.gameBoard]
        parents = {self.gameBoard: None}

        while len(parents) != 0:
            gb = stack.pop()
            if gb.isWin():
                path = []
                boards = []
                curGb = gb
                while curGb in parents and not parents[curGb] is None:
                    boards.insert(0, curGb)
                    path.insert(0, parents[curGb].direction)
                    curGb = parents[curGb].parent

                boards.insert(0, curGb)
                return {'path': path, 'boards': boards}

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
