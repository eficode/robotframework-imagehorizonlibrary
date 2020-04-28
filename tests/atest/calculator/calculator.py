import eel
import os
import sys


os.chdir(os.path.dirname(__file__))

eel.init('web')


@eel.expose
def close():
    sys.exit(0)


eel.start('main.html', size=(300, 380))
