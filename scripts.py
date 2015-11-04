from gameboard import *

def wallsToPoints(walls):
    maxX = 0
    maxY = 0
    for wall in walls:
        if wall.direction == 'h':
            maxX = max([wall.eastPoint[0], wall.westPoint[0], maxX])
            maxY = max([wall.eastPoint[1], wall.westPoint[1], maxY])
        else:
            maxX = max([wall.northPoint[0], wall.southPoint[0], maxX])
            maxY = max([wall.northPoint[1], wall.southPoint[1], maxY])

    matrix = [['.' for j  in range(maxX + 1)] for i in range(maxY + 1)]
    for wall in walls:
        if wall.direction == 'h':
            y = wall.eastPoint[1]
            for x in range(wall.eastPoint[0], wall.westPoint[0] + 1):
                matrix[y][x] = '#'

        else:
            x = wall.northPoint[0]
            for y in range(wall.northPoint[1], wall.southPoint[1] + 1):
                matrix[y][x] = '#'

    return matrix

map = mapToBoard('./test_map1.map')
#map.boxes.add((1, 9))

matrix = wallsToPoints(map.walls)

lines = ["".join(line) for line in matrix]
for line in lines:
    print line

for p in map.playArea:
    matrix[p[1]][p[0]] = ' '

print ''
lines = ["".join(line) for line in matrix]
for line in lines:
    print line

for trap in map.traps:
    for p in trap.positions:
        matrix[p[1]][p[0]] = str(trap.capacity())

print ''
lines = ["".join(line) for line in matrix]
for line in lines:
    print line

for p in map.deadPositions:
    matrix[p[1]][p[0]] = 'D'

print ''
lines = ["".join(line) for line in matrix]
for line in lines:
    print line
