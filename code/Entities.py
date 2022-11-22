class Vessel:
    def __init__(self, index, size, arrival_time, process_time, weight=1):
        self.index = index
        self.weight = weight
        self.size = size
        self.process_time = process_time
        self.arrival_time = arrival_time
        self.u = None
        self.v = None

    @property
    def s(self):
        return self.size

    @property
    def p(self):
        return self.process_time

    @property
    def a(self):
        return self.arrival_time

    @property
    def w(self):
        return self.weight

    def getPossiblePositions(self):
        pass


class Location:
    def __init__(self, a, b, c, d):
        self.c = c
        self.d = d
        self.b = b
        self.a = a
        

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
