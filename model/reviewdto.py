
from datetime import datetime


class ReviewDto:
    def __init__(self, game, review):
        self._game = game
        self._review = review
        self._time = datetime.today().strftime('%d-%m-%Y')

    @property
    def game(self):
        return self._game

    @property
    def review(self):
        return self._review

    @property
    def time(self):
        return self._time

    def __str__(self):
        return f"{self._review}: {self._time}"
