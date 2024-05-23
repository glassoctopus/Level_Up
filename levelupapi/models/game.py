from django.db import models
from .game_type import Game_type
from .gamer import Gamer

class Game(models.Model):
    
    game_type = models.ForeignKey(Game_type, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    maker = models.CharField(max_length=50)
    gamer = models.ForeignKey(Gamer, on_delete=models.CASCADE)
    number_of_players = models.IntegerField(default=2, help_text="Max number of players")
    skill_level = models.IntegerField(default=0, help_text="game skill level")
    