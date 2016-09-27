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
class Drawer(object):
    """
    This is the main window object, controlls the user flow
    and the lay of hte land. Passes information forward to
    the nessesary places and handles the responces
    """
    def __init__(self):
    """ Initializes the obejct """

    def __init_window(self):
    """ Does most if not all of the window working """

    def run(self):
    """ Starts the Gtk loop """

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
