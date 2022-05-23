# MessageDTO
from datetime import datetime


class GameDto:
    def __init__(self, name, gender):
        self._name = name
        self._gender = gender

    @property
    def time(self):
        return self._time

    @property
    def name(self):
        return self._name

    @property
    def gender(self):
        return self._gender

    def __str__(self):
        return f"Nombre: \t{self._name}" \
               f"\nGénero: \t{self._gender}"
