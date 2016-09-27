import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from util import Color, Coords
from drawables import DrawLine, DrawPolygon, DrawCircle


class Drawer(object):

    def __init__(self):
        # self.__doli = DoList()
        self.__doli = []

        self.__primary = Color.Black
        self.__secondary = Color.White
        self.__fill = True

        self.__selected_action = DrawLine
        self.__action = DrawLine(self.__primary, self.__secondary, self.__fill)

        self.__init_window()

    def __init_window(self):
        self.__window = Gtk.Window()
        w = self.__window

        w.add_events(Gdk.EventMask.KEY_PRESS_MASK)
        w.connect('delete-event', Gtk.main_quit)
        w.connect("key-press-event", self.on_keyboard)
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
        for drawable in self.__doli:
            drawable.draw(ctx)

        self.__action.on_draw(ctx)

    def on_mouse_move(self, widget, event):
        # print("Move", event.x, event.y)
        self.__action.on_mouse_move(Coords(event.x, event.y))
        self.__draw_area.queue_draw()

    def on_mouse_release(self, widget, event):
        # print("Release", event.x, event.y)
        ret = self.__action.on_mouse_release(Coords(event.x, event.y),
                                             event.button == Gdk.BUTTON_PRIMARY,
                                             event.button == Gdk.BUTTON_SECONDARY)
        if (ret is not None):
            self.__doli.append(ret)
            self.__action = self.__selected_action(self.__primary, self.__secondary, self.__fill)

        self.__draw_area.queue_draw()

    def on_mouse_press(self, widget, event):
        ret = self.__action.on_mouse_press(Coords(event.x, event.y),
                                     event.button == Gdk.BUTTON_PRIMARY,
                                     event.button == Gdk.BUTTON_SECONDARY)
        if (ret is not None):
            self.__doli.append(ret)
            self.__action = self.__selected_action(self.__primary, self.__secondary, self.__fill)

        self.__draw_area.queue_draw()

    def kill_action(self):
        self.__action = self.__selected_action(self.__primary,
                                               self.__secondary,
                                               self.__fill)

    def on_keyboard(self, widget, event):
        if (event.keyval == Gdk.KEY_Escape):
            # Kill the current action
            self.kill_action()

        if (event.keyval == Gdk.KEY_q):
            Gtk.main_quit()

        if (event.keyval == Gdk.KEY_p):
            self.__selected_action = DrawPolygon
            self.kill_action()

        if (event.keyval == Gdk.KEY_l):
            self.__selected_action = DrawLine
            self.kill_action()

        if (event.keyval == Gdk.KEY_c):
            self.__selected_action = DrawCircle
            self.kill_action()

        if (event.keyval == Gdk.KEY_f):
            self.__fill = not self.__fill
            self.kill_action()

        if (event.keyval == Gdk.KEY_z and
            event.state & Gdk.ModifierType.CONTROL_MASK):
            print("<CTRL>z")
            if (len(self.__doli) != 0):
                del self.__doli[-1]

        self.__draw_area.queue_draw()


def main():
    app = Drawer()
    app.run()

if __name__ == '__main__':
    main()
