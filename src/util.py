import math
from enum import Enum


class Color(Enum):
    """
    Enum Color class for easy access to different
    colors.
    """
    Red = [1, 0, 0, 1]
    Green = [0, 1, 0, 1]
    Blue = [0, 0, 1, 1]
    Black = [0, 0, 0, 1]
    White = [1, 1, 1, 1]


class Coords(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def dist(self, other):
        return (self - other).length()

    def length(self):
        return math.sqrt(self.dot(self))

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def __sub__(self, other):
        return Coords(self.x - other.x, self.y - other.y)

    def __rsub__(self, other):
        return Coords(other.x - self.x, other.y - self.y)

    def __mul__(self, scale):
        return Coords(self.x * scale, self.y * scale)

    __rmul__ = __mul__


class DoList(object):

    class Iter:
        def __init__(self, li, end):
            self.__li = li
            if (end is not None and end < len(li)):
                self.__end = end
            else:
                self.__end = len(li)-1
            self.__current = 0

        def __next__(self):
            self.__current += 1
            if (self.__current >= self.__end):
                raise StopIteration()
            else:
                return self.__li[self.__current]

    def __init__(self):
        self.__actions = []
        self.__pointer = -1

    def do(self, action):

        if (self.__pointer < len(self.__actions)-1):
            self.__actions = self.__actions[:self.__pointer+1]

        self.__actions.append(action)
        self.__pointer = len(self.__actions)

    def undo(self):
        if (self.__pointer < 0):
            return False
        else:
            self.__pointer -= 1
            return True

    def redo(self):
        if (self.__pointer == len(self.__actions)-1):
            return False
        else:
            self.__pointer += 1
            return True

    def __iter__(self):
        return self.Iter(self.__actions, self.__pointer)
