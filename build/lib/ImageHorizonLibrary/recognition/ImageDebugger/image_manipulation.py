from PIL import Image, ImageTk
from enum import Enum, unique
import numpy as np


@unique
class ImageFormat(Enum):
    PILIMG = 0
    NUMPYARRAY = 1
    IMAGETK = 2         # ImageTk PhotoImage
    PATHSTR = 3

class ImageContainer:
    """Store and retrieve haystack and needle images of different formats."""
    def save_to_img_container(self, img, is_haystack_img=False):
        """Save haystack and needle images.

        Args:
        - ``img (str/PIL.Image)``: Path (str) or object (PIL.Image) to haystack/needle image.
        - ``is_haystack_img (bool, optional)``: If to be saved img is a haystack image.
        """
        if isinstance(img, str):
            _PIL_img = Image.open(img)
        else:
            _PIL_img = img

        if is_haystack_img:
            self._haystack_image_orig_size = _PIL_img
            self._haystack_image = _PIL_img.resize((384, 216), Image.ANTIALIAS)
        else:
            self._needle_image = {'Path': img, 'Obj': _PIL_img}

    def get_haystack_image(self, format: ImageFormat):
        if format == ImageFormat.PILIMG:
            return self._haystack_image
        elif format == ImageFormat.NUMPYARRAY:
            return np.array(self._haystack_image)
        elif format == ImageFormat.IMAGETK:
            return ImageTk.PhotoImage(self._haystack_image)

    def get_haystack_image_orig_size(self, format: ImageFormat):
        if format == ImageFormat.PILIMG:
            return self._haystack_image_orig_size
        elif format == ImageFormat.NUMPYARRAY:
            return np.array(self._haystack_image_orig_size)
        elif format == ImageFormat.IMAGETK:
            return ImageTk.PhotoImage(self._haystack_image_orig_size)

    def get_needle_image(self, format: ImageFormat):
        if format == ImageFormat.PILIMG:
            return self._needle_image['Obj']
        elif format == ImageFormat.PATHSTR:
            return self._needle_image['Path']
        elif format == ImageFormat.NUMPYARRAY:
            return np.array(self._needle_image['Obj'])
        elif format == ImageFormat.IMAGETK:
            return ImageTk.PhotoImage(self._needle_image['Obj'])

