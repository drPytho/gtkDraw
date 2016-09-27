
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
