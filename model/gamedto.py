# MessageDTO
from datetime import datetime


class GameDto:
    def __init__(self, review, name, gender):
        self._review = review
        self._time = datetime.today().strftime('%d-%m-%Y')
        self._name = name
        self._gender = gender

    @property
    def review(self):
        return self._review

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
               f"\nGénero: \t{self._gender}" \
               f"\nReseña: \t{self._review}" \
               f"\nFecha de reseña: \t{self._time}"
