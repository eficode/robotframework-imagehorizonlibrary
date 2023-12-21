from tkinter import *
from .image_debugger_controller import UILocatorController


class ImageDebugger:

    def __init__(self, image_horizon_instance):
        app = UILocatorController(image_horizon_instance)
        app.main()
