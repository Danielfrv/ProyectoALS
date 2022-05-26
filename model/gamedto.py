# MessageDTO
from PIL import Image
import PIL


class GameDto:
    def __init__(self, name, gender, image, description):
        self._name = name
        self._gender = gender
        self._image = image
        self._description = description

    @property
    def name(self):
        return self._name

    @property
    def gender(self):
        return self._gender

    @property
    def image(self):
        return self._image

    @property
    def description(self):
        return self._description

    def __str__(self):
        return f"Nombre: \t{self._name}" \
               f"\nGénero: \t{self._gender}"
