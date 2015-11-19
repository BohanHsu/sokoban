def gameHeuristic1(gameboard):
    #find the min-distance for all boxes to the nearest goals
    boxes = set(gameboard.boxes)
    goals = list(gameboard.goals)
    total_distance = 0
    while boxes:
        cur_box = boxes.pop()
        min_distance = float('inf')
        cur_goal = []
        for i in goals:
            distance = abs(i[0]-cur_box[0]) + abs(i[1]-cur_box[1])
            if distance<min_distance:
                min_distance = distance
                cur_goal = i
        total_distance += min_distance
        goals.remove(cur_goal)
    return total_distance
