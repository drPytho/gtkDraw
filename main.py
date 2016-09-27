import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from enum import Enum
import math

# Undo redo stack
# Based on singaly linked list


# Undo tree
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


class Color(Enum):
    Red = "#FF0000"
    Green = "#00FF00"
    Blue = "#0000FF"
    Black = "#000000"
    White = "#FFFFFF"


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


class Action(object):
    def on_mouse(self, x, y, button, down):
        raise NotImplemented()

    def on_key(self, key, mod):
        raise NotImplemented()


class Drawable(object):
    def draw(self, context):
        raise NotImplemented()


class Polygon(Drawable):

    def __init__(self, coords):
        self.coords = coords

    def draw(self, ctx):
        print("A drawing was made")
        ctx.set_source_rgba(1, 0, 0, 1)
        ctx.set_line_width(2)
        ctx.move_to(self.coords[0].x, self.coords[0].y)
        for coord in self.coords:
            ctx.line_to(coord.x, coord.y)
        ctx.line_to(self.coords[0].x, self.coords[0].y)
        ctx.stroke()


class Pen(Action):

    def __init__(self, fg, bg):
        self.__pos = []
        self.__fg = fg
        self.__bg = bg
        self.__started = False

    def on_mouse(self, x, y, buttons):
        if (self.__started):
            return False

        if (buttons == self.MAIN_BUTTON):
            self.__started = True
            pos = self.__pos
            if (pos[len(pos)-1].dist(Coords(x, y)) > 0.1):
                pos.__append(Coords(x, y))

    def on_key(self, key, mod):
        pass


class Drawer(object):

    def __init__(self):
        self.__doli = DoList()
        self.__fg = Color.Black
        self.__bg = Color.White
        self.__curr_action = None
        self.__init_window()
        self.poly = Polygon([Coords(1, 1),
                            Coords(1, 300),
                            Coords(300, 300)])

    def __init_window(self):
        self.__window = Gtk.Window()
        w = self.__window
        w.connect('delete-event', Gtk.main_quit)
        draw_area = Gtk.DrawingArea()
        draw_area.add_events(Gdk.EventMask.BUTTON_PRESS_MASK |
                             Gdk.EventMask.BUTTON_RELEASE_MASK |
                             Gdk.EventMask.POINTER_MOTION_MASK |
                             Gdk.EventMask.POINTER_MOTION_HINT_MASK)
        draw_area.connect("motion_notify_event", self.on_mouse_move)
        draw_area.connect("button-press-event", self.on_mouse_press)
        draw_area.connect("button-release-event", self.on_mouse_release)
        draw_area.connect("draw", self.on_draw)
        w.add(draw_area)

    def run(self):
        self.__window.show_all()
        Gtk.main()

    def on_draw(self, widget, cr):
        # Draw the stack
        print("Drawing")
        self.poly.draw(cr)
        for drawable in self.__doli:
            drawable.draw(cr)

    def on_mouse_move(self, widget, event):
        print("Move", event.x, event.y)

    def on_mouse_release(self, widget, event):
        print("Release", event.x, event.y)

    def on_mouse_press(self, widget, event):
        print("Press", event.x, event.y)


def main():
    app = Drawer()
    app.run()

if __name__ == '__main__':
    main()
