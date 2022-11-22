from sympy import symbols, Eq, solve
from Entities import Vessel

x, y = symbols('x y')
X = "x"
Y = "y"

VECTOR = "vector"
POINT = "point"
KEY = "key"
VALUE = "value"

NUMBER_INCREASE = 0.5

CLASS_0 = [[0, 0, 0, 0]]
CLASS_1 = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
CLASS_2 = [[1, 1, 0, 0], [1, 0, 1, 0], [1, 0, 0, 1],
           [0, 1, 1, 0], [0, 1, 0, 1], [0, 0, 1, 1]]
CLASS_3 = [[1, 1, 1, 0], [1, 1, 0, 1], [1, 0, 1, 1], [0, 1, 1, 1]]
CLASS_4 = [[1, 1, 1, 1]]

CLASS_1_VERTEX_HOLE = [[1, 0, 0, 0], [0, 0, 0, 1]]
CLASS_3_VERTEX_HOLE_1 = [[1, 0, 1, 1], [1, 1, 0, 1]]
CLASS_3_VERTEX_HOLE_2 = [[1, 1, 1, 0], [0, 1, 1, 1]]
CLASS_2_VERTEX_HOLE = [[1, 0, 1, 0], [0, 1, 0, 1]]
CLASS_2_VERTEX_HOLE_SPLIT_1 = [[0, 0, 1, 0], [1, 0, 0, 0]]
CLASS_2_VERTEX_HOLE_SPLIT_2 = [[0, 1, 0, 0], [0, 0, 0, 1]]

TABLE_1_I1 = [
    {
        KEY: [[0, 1, 1, 1]],
        VALUE: [0, 0, 0, 1]
    },
    {
        KEY: [[1, 0, 1, 1]],
        VALUE: [1, 0, 0, 0]
    },
    {
        KEY: [[1, 1, 0, 1]],
        VALUE: [0, 0, 0, 1]
    },
    {
        KEY: [[1, 1, 1, 0]],
        VALUE: [1, 0, 0, 0]
    }
]

TABLE_1_I2 = [
    {
        KEY: [[1, 0, 1, 1], [1, 1, 1, 0]],
        VALUE: [1, 0, 0, 0]
    },
    {
        KEY: [[1, 1, 0, 1], [0, 1, 1, 1]],
        VALUE: [0, 0, 0, 1]
    }
]


def convertKeySymbolToString(point):
    return {X: point[x], Y: point[y]}


def getAllNode(vessel, locationVessels, S, T):
    """
    params:
    vessel: Vessel
    locationVessels: list([int, int])
    """
    arrivalTime = vessel.arrival_time
    result = []
    oY = Eq(x, 0)
    maxT = Eq(x, T)
    maxS = Eq(y, S)
    haveMaxT = False
    haveMaxS = False
    oX = Eq(y, 0)
    lines = [oX]
    for location in locationVessels:
        for i in range(len(location)):
            indexNextPoint = i + 1
            if indexNextPoint >= len(location):
                indexNextPoint = 0
            if location[i][0] == location[indexNextPoint][0]:
                newLine = Eq(x, location[i][0])
                if (not (newLine in lines)) and (newLine != oY):
                    lines.append(newLine)
                    if newLine == maxT:
                        haveMaxT = True
                continue
            if location[i][1] == location[indexNextPoint][1]:
                newLine = Eq(y, location[i][1])
                if not (newLine in lines):
                    lines.append(newLine)
                    if newLine == maxS:
                        haveMaxS = True

    if (arrivalTime > 0) and (Eq(x, arrivalTime) not in lines):
        lines.append(Eq(x, arrivalTime))
    if arrivalTime == 0:
        lines.append(oY)
    if not haveMaxT:
        lines.append(maxT)
    if not haveMaxS:
        lines.append(maxS)
    for i in range(len(lines)):
        for j in range((i + 1), len(lines)):
            intersection = solve([lines[i], lines[j]])
            if len(intersection) == 0:
                continue
            result.append(convertKeySymbolToString(intersection))
    return result


def getRangeOfVessel(location):
    minX = location[0][0]
    maxX = location[0][0]
    minY = location[0][1]
    maxY = location[0][1]
    for i in range(1, len(location)):
        if location[i][0] < minX:
            minX = location[i][0]
        if location[i][0] > maxX:
            maxX = location[i][0]
        if location[i][1] < minY:
            minY = location[i][1]
        if location[i][1] > maxY:
            maxY = location[i][1]
    return [[minX, maxX], [minY, maxY]]


def getRangeOfVesselWithXY(location):
    minX = location[0][X]
    maxX = location[0][X]
    minY = location[0][Y]
    maxY = location[0][Y]
    for i in range(1, len(location)):
        if location[i][X] < minX:
            minX = location[i][X]
        if location[i][X] > maxX:
            maxX = location[i][X]
        if location[i][Y] < minY:
            minY = location[i][Y]
        if location[i][Y] > maxY:
            maxY = location[i][Y]
    return [[minX, maxX], [minY, maxY]]


def getValueOfVector(vessel, intersection, rangeOfVessels, numberIncreaseX, numberIncreaseY, S, T):
    arrivalTime = vessel.arrival_time
    valueX = intersection[X] + numberIncreaseX
    valueY = intersection[Y] + numberIncreaseY
    if (valueX >= T) or (valueX <= arrivalTime):
        return 0
    if (valueY >= S) or (valueY <= 0):
        return 0
    for rang in rangeOfVessels:
        if (rang[0][0] <= valueX <= rang[0][1]) and (rang[1][0] <= valueY <= rang[1][1]):
            return 0
    return 1


def getVector(vessel, intersections, locationVessel, S, T):
    rangeOfVessels = []
    result = []
    for location in locationVessel:
        rangeOfVessels.append(getRangeOfVessel(location))
    for intersection in intersections:
        vectorOfIntersection = [getValueOfVector(vessel,
                                                 intersection, rangeOfVessels, NUMBER_INCREASE, NUMBER_INCREASE, S, T),
                                getValueOfVector(vessel,
                                                 intersection, rangeOfVessels, -NUMBER_INCREASE, NUMBER_INCREASE, S, T),
                                getValueOfVector(vessel,
                                                 intersection, rangeOfVessels, -NUMBER_INCREASE, -NUMBER_INCREASE, S,
                                                 T), getValueOfVector(vessel,
                                                                      intersection, rangeOfVessels, NUMBER_INCREASE,
                                                                      -NUMBER_INCREASE, S, T)]
        result.append({POINT: intersection, VECTOR: vectorOfIntersection})

    return result


def getVertexOfHole(vertexes):
    result = []
    for vertex in vertexes:
        if (vertex[VECTOR] in CLASS_1) or (vertex[VECTOR] in CLASS_3):
            result.append(vertex)
        if vertex[VECTOR] in CLASS_2_VERTEX_HOLE:
            if vertex[VECTOR] == CLASS_2_VERTEX_HOLE[0]:
                result.append({POINT: vertex[POINT], VECTOR: CLASS_2_VERTEX_HOLE_SPLIT_1[0]})
                result.append(
                    {POINT: vertex[POINT], VECTOR: CLASS_2_VERTEX_HOLE_SPLIT_1[1]})
            if vertex[VECTOR] == CLASS_2_VERTEX_HOLE[1]:
                result.append(
                    {POINT: vertex[POINT], VECTOR: CLASS_2_VERTEX_HOLE_SPLIT_2[0]})
                result.append(
                    {POINT: vertex[POINT], VECTOR: CLASS_2_VERTEX_HOLE_SPLIT_2[1]})

    return result


def handleVertexInClass(hole, point, vector, vertexOfHoles, classNumber, visited):
    result = []
    if (vector == [1, 0, 0, 0] and classNumber == 1) or (vector == [0, 1, 1, 1] and classNumber == 3):
        for vertex in vertexOfHoles:
            if (vertex[POINT][X] == point[X]) and (vertex[POINT][Y] > point[Y]) and (
                    vertex[VECTOR][2] == 1 or vertex[VECTOR][3] == 1):
                result.append(vertex)
            if (vertex[POINT][Y] == point[Y]) and (vertex[POINT][X] > point[X]) and (
                    vertex[VECTOR][1] == 1 or vertex[VECTOR][2] == 1):
                result.append(vertex)
    if (vector == [0, 1, 0, 0] and classNumber == 1) or (vector == [1, 0, 1, 1] and classNumber == 3):
        for vertex in vertexOfHoles:
            if (vertex[POINT][X] == point[X]) and (vertex[POINT][Y] > point[Y]) and (
                    vertex[VECTOR][2] == 1 or vertex[VECTOR][3] == 1):
                result.append(vertex)
            if (vertex[POINT][Y] == point[Y]) and (vertex[POINT][X] < point[X]) and (
                    vertex[VECTOR][0] == 1 or vertex[VECTOR][3] == 1):
                result.append(vertex)
    if (vector == [0, 0, 1, 0] and classNumber == 1) or (vector == [1, 1, 0, 1] and classNumber == 3):
        for vertex in vertexOfHoles:
            if (vertex[POINT][X] == point[X]) and (vertex[POINT][Y] < point[Y]) and (
                    vertex[VECTOR][0] == 1 or vertex[VECTOR][1] == 1):
                result.append(vertex)
            if (vertex[POINT][Y] == point[Y]) and (vertex[POINT][X] < point[X]) and (
                    vertex[VECTOR][0] == 1 or vertex[VECTOR][3] == 1):
                result.append(vertex)
    if (vector == [0, 0, 0, 1] and classNumber == 1) or (vector == [1, 1, 1, 0] and classNumber == 3):
        for vertex in vertexOfHoles:
            if (vertex[POINT][X] == point[X]) and (vertex[POINT][Y] < point[Y]) and (
                    vertex[VECTOR][0] == 1 or vertex[VECTOR][1] == 1):
                result.append(vertex)
            if (vertex[POINT][Y] == point[Y]) and (vertex[POINT][X] > point[X]) and (
                    vertex[VECTOR][1] == 1 or vertex[VECTOR][2] == 1):
                result.append(vertex)
    resultX = None
    resultY = None
    for vertex in result:
        if (vertex in hole) or (vertex in visited):
            continue
        if vertex[POINT][X] == point[X]:
            if resultY == None:
                resultY = vertex
            else:
                if abs(vertex[POINT][Y] - point[Y]) < abs(resultY[POINT][Y] - point[Y]):
                    resultY = vertex
            continue
        if vertex[POINT][Y] == point[Y]:
            if resultX == None:
                resultX = vertex
            else:
                if abs(vertex[POINT][X] - point[X]) < abs(resultX[POINT][X] - point[X]):
                    resultX = vertex
    if resultX == None and resultY == None:
        return False
    if resultX != None:
        return resultX
    if resultY != None:
        return resultY


def getHoles(vertexOfHoles):
    result = []
    visited = []
    for vertex in vertexOfHoles:
        if vertex in visited:
            continue
        loop = True
        hole = []
        targetVertex = vertex
        while loop:
            if len(hole) == 0:
                hole.append(vertex)
                visited.append(vertex)
            if targetVertex[VECTOR] in CLASS_1:
                newVertex = handleVertexInClass(
                    hole, targetVertex[POINT], targetVertex[VECTOR], vertexOfHoles, 1, visited)
                if not newVertex:
                    loop = False
                    continue
                hole.append(newVertex)
                visited.append(newVertex)
                targetVertex = newVertex
                continue
            if targetVertex[VECTOR] in CLASS_3:
                newVertex = handleVertexInClass(
                    hole, targetVertex[POINT], targetVertex[VECTOR], vertexOfHoles, 3, visited)
                if not newVertex:
                    loop = False
                    continue
                hole.append(newVertex)
                visited.append(newVertex)
                targetVertex = newVertex
                continue
        result.append(hole)
    return result


def getVectorOfVertexHole(vertex3_1, vertex3_2):
    for mapping in TABLE_1_I2:
        if (vertex3_1[VECTOR] in mapping[KEY]) and (vertex3_2[VECTOR] in mapping[KEY]):
            return mapping[VALUE]
    return False


def getVectorOfVertexHoleWithEdge(vertex):
    for mapping in TABLE_1_I1:
        if vertex[VECTOR] in mapping[KEY]:
            return mapping[VALUE]
    return False


def getPositionAvailable(holes):
    result = []
    for hole in holes:
        resultHole = []
        vertexClass3_1 = []
        vertexClass3_2 = []
        for vertex in hole:
            if vertex[VECTOR] in CLASS_1_VERTEX_HOLE:
                resultHole.append(vertex)
                continue
            if vertex[VECTOR] in CLASS_3_VERTEX_HOLE_1:
                vertexClass3_1.append(vertex)
                continue
            if vertex[VECTOR] in CLASS_3_VERTEX_HOLE_2:
                vertexClass3_2.append(vertex)
        for vertex3_1 in vertexClass3_1:
            lineX = Eq(x, vertex3_1[POINT][X])
            for vertex3_2 in vertexClass3_2:
                lineY = Eq(y, vertex3_2[POINT][Y])
                intersection = solve([lineX, lineY])
                if len(intersection) == 0:
                    continue
                intersection = convertKeySymbolToString(intersection)
                vector = getVectorOfVertexHole(vertex3_1, vertex3_2)
                if vector == False:
                    continue
                if intersection[X] > vertex3_2[POINT][X]:
                    continue
                resultHole.append({POINT: intersection, VECTOR: vector})
        for vertex3_1 in vertexClass3_1:
            for i in range(len(hole)):
                indexNextVertex = i + 1
                if indexNextVertex == len(hole):
                    indexNextVertex = 0
                if hole[i][POINT][Y] != hole[indexNextVertex][POINT][Y]:
                    continue
                if (hole[i][POINT][X] < vertex3_1[POINT][X] < hole[indexNextVertex][POINT][X]) or (
                        hole[i][POINT][X] > vertex3_1[POINT][X] > hole[indexNextVertex][POINT][X]):
                    intersection = {X: vertex3_1[POINT][X], Y: hole[i][POINT][Y]}
                    if intersection[Y] > vertex3_1[POINT][Y]:
                        continue
                    vector = getVectorOfVertexHoleWithEdge(vertex3_1)
                    resultHole.append({POINT: intersection, VECTOR: vector})
        for vertex3_2 in vertexClass3_2:
            for i in range(len(hole)):
                indexNextVertex = i + 1
                if indexNextVertex == len(hole):
                    indexNextVertex = 0
                if hole[i][POINT][X] != hole[indexNextVertex][POINT][X]:
                    continue
                if (hole[i][POINT][Y] < vertex3_2[POINT][Y] < hole[indexNextVertex][POINT][Y]) or (
                        hole[i][POINT][Y] > vertex3_2[POINT][Y] > hole[indexNextVertex][POINT][Y]):
                    intersection = {Y: vertex3_2[POINT][Y], X: hole[i][POINT][X]}
                    if intersection[X] > vertex3_2[POINT][X]:
                        continue
                    vector = getVectorOfVertexHoleWithEdge(vertex3_2)
                    resultHole.append(
                        {POINT: intersection, VECTOR: vector})
        result.append(resultHole)
    return result


def handlePositionWithVector(vessel, position):
    departureTime = vessel.process_time
    size = vessel.size
    if position[VECTOR] == [0, 0, 0, 1]:
        firstPoint = {X: position[POINT][X], Y: position[POINT][Y]}
        secondPoint = {X: position[POINT][X] + departureTime, Y: position[POINT][Y]}
        thirdPoint = {X: position[POINT][X] + departureTime, Y: position[POINT][Y] - size}
        fourthPoint = {X: position[POINT][X], Y: position[POINT][Y] - size}
        return [firstPoint, secondPoint, thirdPoint, fourthPoint]
    if position[VECTOR] == [1, 0, 0, 0]:
        firstPoint = {X: position[POINT][X], Y: position[POINT][Y] + size}
        secondPoint = {X: position[POINT][X] + departureTime, Y: position[POINT][Y] + size}
        thirdPoint = {X: position[POINT][X] + departureTime, Y: position[POINT][Y]}
        fourthPoint = {X: position[POINT][X], Y: position[POINT][Y]}
        return [firstPoint, secondPoint, thirdPoint, fourthPoint]


def getLocationVessel(vessel, availablePosition):
    result = []
    for hole in availablePosition:
        resultHole = []
        for position in hole:
            resultHole.append(handlePositionWithVector(vessel, position))
        result.append(resultHole)

    return result


def getValidLocationVessel(hole_locations, locationVessel):
    result = []
    rangeOfVessels = []
    for location in locationVessel:
        rangeOfVessels.append(getRangeOfVessel(location))
    for hole in hole_locations:
        for position in hole:
            valid = True
            rangeOfPosition = getRangeOfVesselWithXY(position)
            for rangeOfVessel in rangeOfVessels:
                if ((rangeOfVessel[0][0] < rangeOfPosition[0][0] < rangeOfVessel[0][1]) or (
                        rangeOfPosition[0][0] < rangeOfVessel[0][0] < rangeOfPosition[0][1])) and (
                        (rangeOfVessel[1][0] < rangeOfPosition[1][0] < rangeOfVessel[1][1]) or (
                        rangeOfPosition[1][0] < rangeOfVessel[1][0] < rangeOfPosition[1][1])):
                    valid = False
                    break
            if valid:
                result.append(position)

    return result


memmorize_location = {}


def covertBreakToVessel(breaks, locationVessel, T):
    for breakPoint in breaks:
        locationVessel.append(
            ((0, breakPoint), (T, breakPoint), (T, breakPoint), (0, breakPoint)))


def GetPossibleLocations(vessel, vessel_locations, S, T, breaks):
    if memmorize_location.get((vessel, vessel_locations)) is not None:
        return memmorize_location.get((vessel, vessel_locations))

    list_vessel_locations = list(list(list(vl) for vl in v) for v in vessel_locations)
    covertBreakToVessel(breaks, list_vessel_locations, T)
    nodes = getAllNode(vessel, list_vessel_locations, S, T)
    vertexes = getVector(vessel, nodes, list_vessel_locations, S, T)
    vertexOfHoles = getVertexOfHole(vertexes)
    holes = getHoles(vertexOfHoles)
    availablePosition = getPositionAvailable(holes)
    locations = getLocationVessel(vessel, availablePosition)
    validLocations = getValidLocationVessel(locations, list_vessel_locations)

    memmorize_location[(vessel, vessel_locations)] = validLocations
    return validLocations


if __name__ == "__main__":
    T = 9999999999
    S = 12

    vessel_locations = [
        ([0, 12], [5, 12], [5, 9], [0, 9]),
        ([2, 9], [5, 9], [5, 7], [2, 7]),
        ([5, 12], [8, 12], [8, 10], [5, 10]),
        ([0, 3], [6, 3], [6, 0], [0, 0]),
        ([6, 4], [8, 4], [8, 0], [6, 0]),
        ([8, 10], [11, 10], [11, 0], [8, 0])
    ]
    vessels = [
        Vessel(10, 10, 10),
        Vessel(15, 5, 9, 2),
        Vessel(6, 0, 5),
        Vessel(20, 2, 10, 3),
        Vessel(5, 15, 5),
        Vessel(15, 12, 8)
    ]
    a = GetPossibleLocations(Vessel(4, 1, 3), vessel_locations, S, T)
    for i in a:
        print(i)
