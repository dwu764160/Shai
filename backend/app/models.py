# -*- coding: utf-8 -*-
"""Contains models related to stats"""
from django.db import models

class Team(models.Model):
    """Model representing a team"""
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class Game(models.Model):
    """Model representing a game"""
    date = models.DateField()

    def __str__(self):
        return f"Game on {self.date}"
    
class Player(models.Model):
    # specify primary_key=True because the JSON data uses 'player_id' as the key
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='players')

    def __str__(self):
        return self.name
    
class Event(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='events')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='events')
    
    # An Event can be of type 'shot', 'pass', or 'turnover'
    EVENT_TYPE_CHOICES = [
        ('shot', 'Shot'),
        ('pass', 'Pass'),
        ('turnover', 'Turnover'),
    ]
    event_type = models.CharField(max_length=10, choices=EVENT_TYPE_CHOICES)
    action_type = models.CharField(max_length=50)

    # Shot-event fields (can be null if the event is not a shot)
    points = models.IntegerField(null=True, blank=True)
    is_shooting_foul = models.BooleanField(null=True, blank=True)
    shot_loc_x = models.FloatField(null=True, blank=True)
    shot_loc_y = models.FloatField(null=True, blank=True)

    # Pass-event fields
    is_pass_completed = models.BooleanField(null=True, blank=True)
    is_potential_assist = models.BooleanField(null=True, blank=True)
    pass_start_loc_x = models.FloatField(null=True, blank=True)
    pass_start_loc_y = models.FloatField(null=True, blank=True)
    pass_end_loc_x = models.FloatField(null=True, blank=True)
    pass_end_loc_y = models.FloatField(null=True, blank=True)

    # Turnover-event fields
    turnover_loc_x = models.FloatField(null=True, blank=True)
    turnover_loc_y = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.player.name} - {self.event_type} in Game {self.game.id}"
    