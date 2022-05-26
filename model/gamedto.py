# MessageDTO
from PIL import Image
import PIL


class GameDto:
    def __init__(self, name, gender, image):
        self._name = name
        self._gender = gender
        self._image = image

    @property
    def name(self):
        return self._name

    @property
    def gender(self):
        return self._gender

    @property
    def image(self):
        return self._image

    def __str__(self):
        return f"Nombre: \t{self._name}" \
               f"\nGénero: \t{self._gender}"
