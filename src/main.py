import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import cairo
from util import Color, Coords
from drawables import DrawLine, DrawPolygon, DrawCircle


class SaveDialog(Gtk.Window):

    def __init__(self, name, width, height, doli, cb):
        self.name = name
        self.height = height
        self.width = width
        self.doli = doli
        self.cb = cb

        Gtk.Window.__init__(self, title="Save Dialog")
        self.set_default_size(200, 100)
        self.set_type_hint(Gtk.WindowType.POPUP)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        label = Gtk.Label(label="Save As:")
        vbox.add(label)

        hbox = Gtk.Box(spacing=6)
        vbox.add(hbox)

        text_in = Gtk.Entry()
        text_in.set_text(name)
        hbox.add(text_in)

        save_button = Gtk.Button(label="Save")
        save_button.connect("clicked", self.save)
        hbox.add(save_button)

        self.text_in = text_in
        self.show_all()

    def save(self, widget):
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.width, self.height)
        ctx = cairo.Context(surface)
        # Draw a white background
        ctx.set_source_rgba(1,1,1,1)
        ctx.move_to(0, 0)
        ctx.line_to(self.width, 0)
        ctx.line_to(self.width, self.height)
        ctx.line_to(0, self.height)
        ctx.line_to(0, 0)
        ctx.fill()


        for drawable in self.doli:
            drawable.draw(ctx)

        surface.write_to_png(self.text_in.get_text() + ".png")
        self.destroy()
        self.cb()


class ColorDialog(Gtk.Window):

    def __init__(self, cb):
        self.cb = cb

        Gtk.Window.__init__(self, title="Color Picker")
        self.set_default_size(300, 200)
        self.set_type_hint(Gtk.WindowType.POPUP)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        label = Gtk.Label(label="Set color as hex")
        vbox.add(label)

        hbox = Gtk.Box(spacing=6)
        vbox.add(hbox)

        poundLabel = Gtk.Label(label="#")
        hbox.add(poundLabel)
        text_in = Gtk.Entry()
        hbox.add(text_in)

        set_button = Gtk.Button(label="Set Color")
        set_button.connect("clicked", self.set_color)
        hbox.add(set_button)

        self.text_in = text_in
        self.show_all()

    def set_color(self, widget):
        color = self.text_in.get_text()
        c = Color(color)
        self.destroy()
        self.cb(c)


class Drawer(object):

    def __init__(self):
        # self.__doli = DoList()
        self.__doli = []

        self.__primary = Color(Color.Black)
        self.__secondary = Color(Color.White)
        self.__fill = True

        self.__selected_action = DrawLine
        self.new_action()

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

    def save(self, name, width, height):
        def cb():
            self.sd.destroy()
            self.sd = None

        self.sd = SaveDialog(name, width, height, self.__doli, cb)

    def select_color(self):
        def cb(color):
            self.__primary = color
            self.new_action()
            self.cd = None

        self.cd = ColorDialog(cb)

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
            self.new_action()

        self.__draw_area.queue_draw()

    def on_mouse_press(self, widget, event):
        ret = self.__action.on_mouse_press(Coords(event.x, event.y),
                                     event.button == Gdk.BUTTON_PRIMARY,
                                     event.button == Gdk.BUTTON_SECONDARY)
        if (ret is not None):
            self.__doli.append(ret)
            self.new_action()

        self.__draw_area.queue_draw()

    def new_action(self):
        self.__action = self.__selected_action(self.__primary,
                                               self.__secondary,
                                               self.__fill)

    def on_keyboard(self, widget, event):
        if (event.keyval == Gdk.KEY_Escape):
            # renew the current action
            self.new_action()

        if (event.keyval == Gdk.KEY_q):
            Gtk.main_quit()

        if (event.keyval == Gdk.KEY_p):
            self.__selected_action = DrawPolygon
            self.new_action()

        if (event.keyval == Gdk.KEY_l):
            self.__selected_action = DrawLine
            self.new_action()

        if (event.keyval == Gdk.KEY_c):
            self.__selected_action = DrawCircle
            self.new_action()

        if (event.keyval == Gdk.KEY_f):
            self.__fill = not self.__fill
            self.new_action()

        if (event.keyval == Gdk.KEY_z and
            event.state & Gdk.ModifierType.CONTROL_MASK):
            if (len(self.__doli) != 0):
                del self.__doli[-1]

        if (event.keyval == Gdk.KEY_s and
            event.state & Gdk.ModifierType.CONTROL_MASK):
            self.save("best_picture", 1920, 1080)

        if (event.keyval == Gdk.KEY_d and
            event.state & Gdk.ModifierType.CONTROL_MASK):
            self.select_color()

        self.__draw_area.queue_draw()


def main():
    app = Drawer()
    app.run()

if __name__ == '__main__':
    main()
