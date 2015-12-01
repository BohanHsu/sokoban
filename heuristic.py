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

def gameHeuristic2(gameboard):
    #find the min-distance for all boxes to the nearest goals
    boxes = set(gameboard.boxes)
    goals = list(gameboard.goals)
    robot = gameboard.robot
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
    # find the total distance from robot to all boxes
    temp_boxes = set(gameboard.boxes)
    distanceToBoxes = 0
    while len(temp_boxes) > 0:
        cur_box = temp_boxes.pop()
        temp_distance = abs(cur_box[0]-robot[0]) + abs(cur_box[1]-robot[1])
        distanceToBoxes += temp_distance
    total_distance += distanceToBoxes
    return total_distance

def gameHeuristic3(gameboard):
    #find the min-distance for all boxes to the nearest goals
    boxes = set(gameboard.boxes)
    goals = list(gameboard.goals)
    robot = gameboard.robot
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
    #find the nearest box to the robot
    temp_boxes = set(gameboard.boxes)
    near_box = float('inf')
    for box in temp_boxes:
        temp_distance = abs(box[0]-robot[0]) + abs(box[1]-robot[1])
        if temp_distance < near_box:
            near_box = temp_distance
    total_distance += near_box
    return total_distance