from PIL import ImageDraw
from abc import ABC, abstractmethod
from .image_manipulation import ImageFormat, ImageContainer


class TemplateMatchingStrategy(ABC):
    @abstractmethod
    def find_num_of_matches(self) -> int: pass

    # Match place is highlighted with a red rectangle
    def highlight_matches(self):
        haystack_img = self.image_container.get_haystack_image_orig_size(ImageFormat.PILIMG)
        draw = ImageDraw.Draw(haystack_img, "RGBA")

        for loc in self.coord:
            draw.rectangle([loc[0], loc[1], loc[0]+loc[2], loc[1]+loc[3]], fill=(256, 0, 0, 127))
            draw.rectangle([loc[0], loc[1], loc[0]+loc[2], loc[1]+loc[3]], outline=(256, 0, 0, 127), width=3)
            
        self.image_container.save_to_img_container(img=haystack_img, is_haystack_img=True)

class Pyautogui(TemplateMatchingStrategy):
    def __init__(self, image_container: ImageContainer, image_horizon_instance):
        self.image_container = image_container
        self.image_horizon_instance = image_horizon_instance

    def find_num_of_matches(self):
        self.coord = list(self.image_horizon_instance._locate_all(
            self.image_container.get_needle_image(ImageFormat.PATHSTR),
            self.image_container.get_haystack_image_orig_size(ImageFormat.PILIMG)
        ))
        return self.coord


class Skimage(TemplateMatchingStrategy):
    def __init__(self, image_container: ImageContainer, image_horizon_instance):
        self.image_container = image_container
        self.image_horizon_instance = image_horizon_instance
    
    def find_num_of_matches(self):
        self.coord = list(self.image_horizon_instance._locate_all(
            self.image_container.get_needle_image(ImageFormat.PATHSTR),
            self.image_container.get_haystack_image_orig_size(ImageFormat.NUMPYARRAY)
        ))
        return self.coord
