from . import exceptions
from .models import Game, Guess
import random
import json

def create_game(num_holes, num_colors, max_guesses):
	"""Creates a new Game with a randomly generated secret
	according to the specified arguments, and persists the game
	to the database. Returns the newly created Game.
	Raises an exceptions.InvalidGameParameter exception if any of
	the specified arguments is <=0.
	Colors are represented by numbers in order to allow more complex games.

	Keyword arguments:
	num_holes -- The number of holes of the code.
	num_colors -- The number of distinct colors allowed in this game
	max_guesses -- The maximum number of guesses in this game
	"""
	if num_holes <= 0 or num_colors <= 0 or max_guesses <= 0:
		raise exceptions.InvalidGameParameter('Number of holes, colors and max guesses must be positive integers')

	secret = []
	for i in range(num_holes):
		secret.append(random.randrange(0, num_colors))

	secret_str = json.dumps(secret)

	game = Game(status='STARTED', secret=secret_str, num_holes=num_holes, num_colors=num_colors, max_guesses=max_guesses)
	game.save()

	return game

def guess(game, guess):
	"""Makes a Guess for the specified Game. 
	If the game is already finished, it raises a GameFinishedError.
	If the game does not exist, it raises a GameDoesNotExistError.
	Otherwise, it persists the newly created Guess to the database
	and returns the newly created Guess.
	"""
	pass

def check_guess(secret, guess):
	"""Checks a guess array against a secret array.
	Returns two values corresponding to the number of black key pegs
	and the number of white key pegs.
	"""
	pass
