from django.db import models

# Create your models here.

# Table for 1955-2023 UCL performance CSV data
class UCL_history_performance(models.Model):
    rank = models.IntegerField(default=0)
    team = models.CharField(default="Unknown Team", max_length=50)
    matches_played = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    goals_for = models.IntegerField(default=0)
    goals_against = models.IntegerField(default=0)
   
# Table for 1955-2023 UCL finals CSV data 
class UCL_history_finals(models.Model):
    season = models.CharField(default="Unknown Season", max_length=50)
    team = models.CharField(default="Unknown Team", max_length=50)
    goals_for = models.IntegerField(default=0)
    goals_against = models.IntegerField(default=0)
    match_venue = models.CharField(default="Unknown Venue", max_length=50)
    match_notes = models.CharField(default="No Notes", max_length=50)
    result = models.CharField(default="Unknown Result", max_length=50)   
    