# Specifikation
## inledning
Jag ska programmera ett enkelt ritprogram som använder sig av Gtk och Cario för att rita ut bilderna. 
Man ska kunna välja mellan olika verktyg för att kunna rita oilka saker samnt ha möjligheten att ångrasitt val.
Programmet ska slutligen kunna spara ned ritningen till fil som ska kunna användas i andra ritprogram.

## Användarscenarier
Programmet är riktat mot personer som vill ha ett gratis ritprogram och inte har hittat Incscape^(tm) eller annat gratis vector program.

## Programskelettet
### src/main.py 

```python
class SaveDialog(object):
    """
    This is a popup window for some simple save settings
    """

class ColorDialog(object):
    """
    Simple color picker
    """

class Drawer(object):
    """
    This is the main window object, controlls the user flow
    and the lay of hte land. Passes information forward to
    the nessesary places and handles the responces.
    """
    def __init__(self):
    """ Initializes the obejct """

    def run(self):
    """ Starts the Gtk loop (static) """

    def save(self, name):
    """ Saves the current picture to file as a png """

    def on_all_events(self, widget, ctx):
    """ There are may different on_**** that handels mostly mouse and keyboard """

    def kill_action(self):
    """ Helper function to restart a tool """

    def on_keyboard(self, widget, event):
    """ Example of event handler """
        # On some key
        if (event.keyval == Gdk.KEY_someKey):
            # Do some action
            doAction()

```

### src/drawables.py

```python
# Abtract classes for the drawable and action classes
class Action(object):
    """
    Specifies all the functions to e implemented by action
    classes. This will be used to create a drawable obejct
    later on save()
    """
    def on_mouse_release(self, coord, right, left):

    def on_mouse_press(self, coord, right, left):

    def on_mouse_move(self, *args):

    def on_keyboard(self, *args):

    def on_draw(self, ctx):

    def save(self):


class Drawable(object):
    """
    This is an object meant to be able to be drawn to a
    Cairo context. It is used to store the important information
    nessesary to draw.
    """
    def draw(self, context):

```

### src/util.py

```python
class Color(Enum):
    """ Enum Color class for easy access to different colors. """
    Red = [1, 0, 0, 1]
    Green = [0, 1, 0, 1]
    Blue = [0, 0, 1, 1]
    Black = [0, 0, 0, 1]
    White = [1, 1, 1, 1]


class Coords(object):
    """
    Helper function for working with coordinates
    """
    def __init__(self, x, y):

    def dist(self, other):

    def length(self):

    def dot(self, other):

    def __sub__(self, other):

    def __rsub__(self, other):

    def __mul__(self, scale):

class DoList(object):
    """
    A class to be able to do, undo and redo.
    """

    class Iter:
    """ Itterator class to help with for x in y: loops """
        def __init__(self, li, end):

        def __next__(self):

    def __init__(self):

    def do(self, action):

    def undo(self):

    def redo(self):


    def __iter__(self):
    """ Creates an instace of the iterator for this class """
```

# Programflöde och dataflöde
Vid programmets start så skapas ett Drawer object som initierar en del Gtk delar. Sedan körs Gtk loopen från main metoden och startar programmet.
Efter det hamnar allt i event hanteringen. Där hanteras rit instruktioner från pekdonet och instruktioner från tangentbordet.
En av ritklasserna instancieras och används för att skapa ritobejct som kan renderas av Cairo.
