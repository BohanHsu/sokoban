from Tkinter import *

class Ui:
    def __init__(self, gameBoards):
        self.sizeUnit = 30.0
        self.idx = 0
        gameBoard = gameBoards[0]
        maxI = 0
        maxJ = 0
        for obstacle in gameBoard.obstacles:
            if obstacle[0] > maxI:
                maxI = obstacle[0]

            if obstacle[1] > maxJ:
                maxJ = obstacle[1]

        root = Tk()
        canvas = Canvas(root, width=(maxJ + 3) * self.sizeUnit, height=(maxI + 3) * self.sizeUnit)
        canvas.pack()
    
        def task():
            canvas.delete('all')
            self.drawCanvas(canvas, gameBoards[self.idx])
            self.idx += 1
            if self.idx < len(gameBoards):
                root.after(200, task)
        
        self.drawCanvas(canvas, gameBoards[self.idx])
        self.idx += 1
        root.after(1000, task)
        mainloop()


    def drawCanvas(self, canvas, gameBoard):
        matrix = gameBoardToMatrix(gameBoard)
        for i in range(0, len(matrix)):
            for j in range(0, len(matrix[0])):
                self.drawBox(canvas, i, j, matrix[i][j])

    def drawBox(self, canvas, i, j, type):
        color = {'.': 'white', ' ': 'gray', '#': 'black', 'B': 'red', 'b': 'blue', 'g': 'green', 'r': 'yellow'}
        canvas.create_rectangle((j + 1) * self.sizeUnit, (i + 1)  * self.sizeUnit, (j + 2) * self.sizeUnit, (i + 2) * self.sizeUnit, fill=color[type])
        if type == 'r':
            canvas.create_rectangle((j + 1) * self.sizeUnit + self.sizeUnit / 10, (i + 1)  * self.sizeUnit + self.sizeUnit / 10, (j + 2) * self.sizeUnit - self.sizeUnit / 10, (i + 2) * self.sizeUnit - self.sizeUnit / 10, fill='red')
        
        if type == 'B' or type == 'b':
            canvas.create_line((j + 1) * self.sizeUnit + self.sizeUnit / 5, (i + 1)  * self.sizeUnit + self.sizeUnit / 5, (j + 2) * self.sizeUnit - self.sizeUnit / 5, (i + 2) * self.sizeUnit - self.sizeUnit / 5, fill='white')
            canvas.create_line((j + 1) * self.sizeUnit + self.sizeUnit / 5, (i + 2)  * self.sizeUnit - self.sizeUnit / 5, (j + 2) * self.sizeUnit - self.sizeUnit / 5, (i + 1) * self.sizeUnit + self.sizeUnit / 5, fill='white')


def gameBoardToMatrix(gameBoard):
    maxI = 0
    maxJ = 0
    for obstacle in gameBoard.obstacles:
        if obstacle[0] > maxI:
            maxI = obstacle[0]

        if obstacle[1] > maxJ:
            maxJ = obstacle[1]

    matrix = [[' ' for j in range(0, maxJ + 1)] for i in range(0, maxI + 1)]
    for obstacle in gameBoard.obstacles:
        matrix[obstacle[0]][obstacle[1]] = '#'

    for point in gameBoard.playArea:
        matrix[point[0]][point[1]] = '.'

    for goal in gameBoard.goals:
        matrix[goal[0]][goal[1]] = 'g'

    for box in gameBoard.boxes:
        if matrix[box[0]][box[1]] == 'g':
            matrix[box[0]][box[1]] = 'B'
        else:
            matrix[box[0]][box[1]] = 'b'

    matrix[gameBoard.robot[0]][gameBoard.robot[1]] = 'r'

    return matrix
