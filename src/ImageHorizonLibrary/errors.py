# -*- coding: utf-8 -*-
class ImageHorizonLibraryError(ImportError):
    pass


class ImageNotFoundException(Exception):
    def __init__(self, image_name):
        self.image_name = image_name

    def __str__(self):
        return 'Reference image "%s" was not found on screen' % self.image_name


class InvalidImageException(Exception):
    pass


class KeyboardException(Exception):
    pass


class MouseException(Exception):
    pass


class OSException(Exception):
    pass


class ReferenceFolderException(Exception):
    pass


class ScreenshotFolderException(Exception):
    pass
