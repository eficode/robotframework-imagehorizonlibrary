import eel
import os
import sys


os.chdir(os.path.dirname(__file__))

eel.init('web')


@eel.expose
def close():
    sys.exit(0)


mode = 'edge' if os.name == 'nt' else 'chrome'

eel.start('main.html', size=(300, 380), mode=mode)
