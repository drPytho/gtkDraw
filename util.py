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



