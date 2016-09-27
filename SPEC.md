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

    def __init_window(self):

    def run(self):

    def on_all_events(self, widget, ctx):

    def kill_action(self):

    def on_keyboard(self, widget, event):
        if (event.keyval == Gdk.KEY_someKey):
            doAction()

```

### src/util.py

```python

```
