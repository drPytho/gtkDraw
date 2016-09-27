import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from enum import Enum
import math
from dolist import DoList

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


class Action(object):
    def on_mouse_press(self, coord, right, left):
        raise NotImplemented()

    def on_mouse_move(self, *args):
        raise NotImplemented()

    def on_keyboard(self, *args):
        raise NotImplemented()

    def on_draw(self, ctx):
        raise NotImplemented()


class Drawable(object):
    def draw(self, context):
        raise NotImplemented()


class Polygon(Drawable):

    def __init__(self, coords, primColor, altColor, fill):
        self.coords = coords
        self.primColor = primColor
        self.altColor = altColor
        self.fill = fill

    def draw(self, ctx):
        ctx.set_source_rgba(*self.primColor.value)
        ctx.set_line_width(2)
        ctx.move_to(self.coords[0].x, self.coords[0].y)
        for coord in self.coords:
            ctx.line_to(coord.x, coord.y)
        ctx.line_to(self.coords[0].x, self.coords[0].y)
        if (self.fill):
            ctx.fill()
        else:
            ctx.stroke()


class DrawPolygon(Action):

    def __init__(self, primColor, altColor, fill):
        self.primColor = primColor
        self.altColor = altColor
        self.fill = fill
        self.coords = []

    def on_mouse_press(self, coord, right, left):
        if (right):
            self.coords.append(coord)
        elif (left):
            return Polygon(self.coords, self.primColor, self.altColor, self.fill)


    def on_draw(self, ctx):
        Polygon(self.coords, self.primColor, self.altColor, self.fill).draw(ctx)

    def on_mouse_move(self, *args):
        pass

    def on_keyboard(self, *args):
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
                            Coords(300, 300)],
                            Color.Red, Color.Blue, True)

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
