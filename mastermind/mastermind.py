from django.utils import timezone
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


def get_game(game_id):
	"""Returns the Game instance with the specified id, or None if the game does not exist

	Keyword arguments:
	game_id -- The integer representing the game ID in the database
	"""
	try:
		game = Game.objects.get(id=game_id)
		return game
	except:
		return None


def guess(game, guess_list):
	"""Makes a Guess for the specified Game. 
	If the game is already finished, it raises a GameFinishedException.
	If the guess is invalid (that is, the length of the guess is different from
	the number of holes in the game, or there is a number that exceeds the number
	of colors in the game), it raises an InvalidGuessException.
	Otherwise, it persists the newly created Guess to the database
	and returns the newly created Guess.

	Keyword arguments:
	game -- The Game instance
	guess_list -- An array containing the numbers of the guess
	"""
	if game.status == 'FINISHED':
		raise exceptions.GameFinishedException('Game is already finished')

	if len(guess_list) != game.num_holes or max(guess_list) >= game.num_colors:
		raise exceptions.InvalidGuessException('Invalid guess')

	secret_list = json.loads(game.secret)
	guess_str = json.dumps(guess_list)

	correct_position, correct_color = check_guess(secret_list, guess_list)

	guess = Guess(game=game, guess=guess_str, correct_position=correct_position, correct_color=correct_color)
	guess.save()

	# Check whether the game has finished
	update_game_status(game)

	return guess


def check_guess(secret, guess):
	"""Checks a guess array against a secret array.
	Returns two values corresponding to the number of black key pegs
	and the number of white key pegs.

	Keyword arguments:
	secret -- An array containing the numbers of the secret
	guess -- An array containing the numbers of the guess
	"""
	correct_position = sum(1 for k, v in enumerate(guess) if guess[k] == secret[k])

	# secret_not_matched contains items not matched by position by the guess
	secret_not_matched = [secret[k] for k, v in enumerate(secret) if guess[k] != secret[k]]

	# guess_not_matched contains items that did not match by position
	guess_not_matched = [guess[k] for k, v in enumerate(secret) if guess[k] != secret[k]]

	correct_color = 0
	for v in guess_not_matched:
		if v in secret_not_matched:
			correct_color = correct_color + 1
			del secret_not_matched[secret_not_matched.index(v)]

	return correct_position, correct_color


def update_game_status(game):
	"""Updates the status and winner of the specified game if necessary.

	Keyword arguments:
	game -- The Game instance to update
	"""
	if game.status == 'STARTED' and game.guess_set.count() > 0:
		last_guess = game.guess_set.order_by('-created_at')[0]
		if last_guess.correct_position == game.num_holes:
			# the codebreaker won
			game.status = 'FINISHED'
			game.winner = 'CODEBREAKER'
			game.finished_at = timezone.now()
			game.save()
		elif game.max_guesses <= game.guess_set.count():
			# the codemaker won
			game.status = 'FINISHED'
			game.winner = 'CODEMAKER'
			game.finished_at = timezone.now()
			game.save()


def game_to_dict(game):
	"""Returns a dictionary created from the specified game, in order to return it
	to the user. The secret is not included unless the game has finished.

	Keyword arguments:
	game -- The Game instance for which to return the dictionary
	"""
	game_dict = {
		'started_at': game.started_at,
		'finished_at': game.finished_at,
		'status': game.status,
		'winner': game.winner,
		'num_holes': game.num_holes,
		'num_colors': game.num_colors,
		'max_guesses': game.max_guesses,
		'guesses': []
	}

	if (game.status == 'FINISHED'):
		game_dict['secret'] = json.loads(game.secret)

	for guess in game.guess_set.order_by('created_at'):
		game_dict['guesses'].append({
			'id': guess.id,
			'created_at': guess.created_at,
			'guess': json.loads(guess.guess),
			'correct_position': guess.correct_position,
			'correct_color': guess.correct_color
		})

	return game_dict
