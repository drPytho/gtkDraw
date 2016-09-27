import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from enum import Enum
import math
# from dolist import DoList


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


class Action(object):
    def on_mouse_release(self, coord, right, left):
        raise NotImplemented()

    def on_mouse_press(self, coord, right, left):
        raise NotImplemented()

    def on_mouse_move(self, *args):
        raise NotImplemented()

    def on_keyboard(self, *args):
        raise NotImplemented()

    def on_draw(self, ctx):
        raise NotImplemented()

    def save(self):
        raise NotImplemented()


class Drawable(object):
    def draw(self, context):
        raise NotImplemented()


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


class Polygon(Drawable):

    def __init__(self, coords, primColor, altColor, fill):
        self.coords = coords
        self.primColor = primColor
        self.altColor = altColor
        self.fill = fill

    def draw(self, ctx):
        if (len(self.coords) == 0):
            return
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
        self.poly = Polygon([], primColor, altColor, fill)

    def save(self):
        return self.poly

    def on_mouse_release(self, coord, right, left):
        if (right):
            self.poly.coords.append(coord)
        elif (left):
            return self.save()

    def on_draw(self, ctx):
        self.poly.draw(ctx)

    def on_mouse_move(self, *args):
        pass

    def on_keyboard(self, *args):
        pass

    def on_mouse_press(self, coord, right, left):
        pass


class Drawer(object):

    def __init__(self):
        # self.__doli = DoList()
        self.__doli = []

        self.__primary = Color.Black
        self.__secondary = Color.White

        self.__selected_action = DrawPolygon
        self.__action = DrawPolygon(self.__primary, self.__secondary, True)

        self.__init_window()

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
        self.__draw_area = draw_area
        w.add(draw_area)

    def run(self):
        self.__window.show_all()
        Gtk.main()

    def on_draw(self, widget, ctx):
        # Draw the stack
        print("Drawing")
        for drawable in self.__doli:
            drawable.draw(ctx)

        self.__action.on_draw(ctx)

    def on_mouse_move(self, widget, event):
        # print("Move", event.x, event.y)
        self.__action.on_mouse_move(event)

    def on_mouse_release(self, widget, event):
        # print("Release", event.x, event.y)
        ret = self.__action.on_mouse_release(Coords(event.x, event.y),
                                       event.button == 1, event.button == 3)
        if (ret is not None):
            self.__doli.append(ret)
            self.__action = DrawPolygon(self.__fg, self.__bg, True)

        self.__draw_area.queue_draw()

    def on_mouse_press(self, widget, event):
        # print("Press", event.x, event.y)
        self.__action.on_mouse_release(Coords(event.x, event.y),
                                       event.button == 3, event.button == 1)


def main():
    app = Drawer()
    app.run()

if __name__ == '__main__':
    main()
