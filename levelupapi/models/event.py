import datetime
from django.db import models
from .game import Game
from .gamer import Gamer

class Event(models.Model):
    
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    description = models.CharField(max_length=50)
    date = models.DateField(default=datetime.date(2024, 5, 13))
    time = models.TimeField(default=datetime.time(12, 0, 0))
    organizer = models.ForeignKey(Gamer, on_delete=models.CASCADE)
