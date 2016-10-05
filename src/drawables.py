import math


# Abtracts
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


# Shapes

class Polygon(Drawable):

    def __init__(self, coords, primColor, altColor, fill):
        self.coords = coords
        self.primColor = primColor
        self.altColor = altColor
        self.fill = fill

    def draw(self, ctx):
        if (len(self.coords) == 0):
            return
        ctx.set_source_rgba(*self.primColor.val)
        ctx.set_line_width(2)
        ctx.move_to(self.coords[0].x, self.coords[0].y)
        for coord in self.coords:
            ctx.line_to(coord.x, coord.y)
        ctx.line_to(self.coords[0].x, self.coords[0].y)
        if (self.fill):
            ctx.fill()
        else:
            ctx.stroke()


class Line(Drawable):

    def __init__(self, coords, color):
        self.coords = coords
        self.color = color

    def draw(self, ctx):
        if (len(self.coords) != 2):
            return
        ctx.set_source_rgba(*self.color.val)
        ctx.set_line_width(2)
        ctx.move_to(self.coords[0].x, self.coords[0].y)
        ctx.line_to(self.coords[1].x, self.coords[1].y)
        ctx.stroke()


class Circle(Drawable):

    def __init__(self, prim, alt, fill, center=None, rad=None):
        self.color = prim
        self.center = center
        self.rad = rad
        self.fill = fill

    def draw(self, ctx):
        ctx.set_source_rgba(*self.color.val)
        ctx.set_line_width(2)
        ctx.arc(self.center.x, self.center.y, self.rad, 0, 2*math.pi)
        if (self.fill):
            ctx.fill()
        else:
            ctx.stroke()


# Drawing tools
class DrawLine(object):

    def __init__(self, primColor, altColor, fill):
        self.line = Line([], primColor)
        self.tmp_coords = None

    def on_mouse_release(self, coord, right, left):
        if (right):
            self.line.coords.append(coord)
            if (len(self.line.coords) == 2):
                return self.save()

    def on_mouse_press(self, coord, right, left):
        pass

    def on_mouse_move(self, coord):
        self.tmp_coords = coord

    def on_keyboard(self, *args):
        pass

    def on_draw(self, ctx):
        if (len(self.line.coords) == 1):
            self.line.coords.append(self.tmp_coords)
            self.line.draw(ctx)
            del self.line.coords[-1]

    def save(self):
        return self.line


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


class DrawCircle(object):

    def __init__(self, primColor, altColor, fill):
        self.circle = Circle(primColor, altColor, fill)
        self.tmp_coords = None

    def on_mouse_release(self, coord, right, left):
        if (right):
            if (self.circle.center is None):
                self.circle.center = coord
            else:
                rad = coord.dist(self.circle.center)
                self.circle.rad = rad
                return self.save()

    def on_mouse_press(self, coord, right, left):
        pass

    def on_mouse_move(self, coord):
        self.tmp_coords = coord

    def on_keyboard(self, *args):
        pass

    def on_draw(self, ctx):
        if (self.circle.center is not None and self.circle.rad is None):
            rad = self.tmp_coords.dist(self.circle.center)
            self.circle.rad = rad
            self.circle.draw(ctx)
            self.circle.rad = None

    def save(self):
        return self.circle


