from django.db import models

GAME_STATUSES = (
	('STARTED', 'Started'),
	('FINISHED', 'Finished'),
)

GAME_WINNERS = (
	('CODEMAKER', 'Codemaker'),
	('CODEBREAKER', 'Codebreaker'),
)

class Game(models.Model):
	started_at = models.DateTimeField(auto_now_add=True)
	finished_at = models.DateTimeField(blank=True, null=True)
	status = models.CharField(max_length=64, choices=GAME_STATUSES)
	winner = models.CharField(max_length=64, choices=GAME_WINNERS, blank=True, null=True)
	secret = models.TextField()
	num_holes = models.IntegerField()
	num_colors = models.IntegerField()
	max_guesses = models.IntegerField()

class Guess(models.Model):
	game = models.ForeignKey(Game, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	guess = models.TextField()
	correct_position = models.IntegerField()
	correct_color = models.IntegerField()
