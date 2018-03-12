from django.shortcuts import render
from django.http import JsonResponse
import json
from . import mastermind

def create_game(request):
	"""Creates a new game with a random secret.
	The body must be a json string with the following format:
	{
		"num_holes": 4,
		"num_colors": 6,
		"max_guesses": 12
	}
	all keys are optional and they default to the values specified above.
	Returns a JsonRespone with a Json string depending on the result. If
	the game could be created successfully, the ID of the game is returned:
		{"id": 123}
	else, a Json string with the key "error" is returned, and the value
	is a description of the error.
		{"error": "Method not allowed"}
	"""
	if request.method != 'POST':
		return JsonResponse({'error': 'Method not allowed'}, status=405)

	try:
		request_dict = json.loads(request.body)
	except Exception as ex:
		return JsonResponse({'error': 'Invalid payload format: ' + repr(ex)}, status=400)

	try:
		num_holes = int(request_dict['num_holes']) if 'num_holes' in request_dict else 4
		num_colors = int(request_dict['num_colors']) if 'num_colors' in request_dict else 6
		max_guesses = int(request_dict['max_guesses']) if 'max_guesses' in request_dict else 12

		game = mastermind.create_game(num_holes=num_holes, num_colors=num_colors, max_guesses=max_guesses)
	except Exception as ex:
		return JsonResponse({'error': 'Could not create game: ' + repr(ex)}, status=400)

	if game is not None:
		return JsonResponse({'id': game.id})

	return JsonResponse({'error': 'Could not create game'}, status=500)


def detail(request, game_id):
	"""Returns information for the game with the specified id.
	Returns a JsonResponse with a Json string depending on the result. If the specified
	game id corresponds to a game, a game description such as the following is returned.
	Example: finished game, the codebreaker won:
		{
			"id": 2,
			"started_at": xx,
			"finished_at": xx,
			"status": "FINISHED",
			"winner": "CODEBREAKER",
			"secret": [0, 3, 4, 1],
			"num_holes": 4,
			"num_colors": 6,
			"max_guesses": 12,
			"guesses": [
				{
					"id": 4,
					"created_at": xx,
					"guess": [0, 3, 1, 2],
					"correct_position": 2
					"correct_color": 1
				},
				{
					"id": 5,
					"created_at": xx,
					"guess": [0, 3, 4, 1],
					"correct_position": 4
					"correct_color": 0
				}				
			]
		}
	Example: not finished game (note that the secret is not displayed):
		{
			"id": 2,
			"started_at": xx,
			"finished_at": null,
			"status": "STARTED",
			"winner": null,
			"num_holes": 4,
			"num_colors": 6,
			"max_guesses": 12,
			"guesses": [
				{
					"id": 4,
					"created_at": xx,
					"guess": [0, 3, 1, 2],
					"correct_position": 2
					"correct_color": 1
				},
				{
					"id": 5,
					"created_at": xx,
					"guess": [0, 3, 2, 1],
					"correct_position": 3
					"correct_color": 0
				}				
			]
		}
	If the game does not exist, a Json string with the key "error" is returned, 
	and the value is a description of the error.
		{"error": "Could not find game with the specified ID"}
	"""
	if request.method != 'GET':
		return JsonResponse({'error': 'Method not allowed'}, status=405)

	game = mastermind.get_game(game_id=game_id)

	if game is None:
		return JsonResponse({'error': 'Could not find game with the specified ID'}, status=404)

	game_dict = mastermind.game_to_dict(game=game)

	return JsonResponse(game_dict)


def guess(request, game_id):
	"""Makes a guess for the game with the specified id.
	The body must be a json string with the following format:
		{"guess": [0, 1, 2, 3]}
	where the the value for "guess" is an array with the numbers of this guess.
	Returns a JsonResponse with a Json string depending on the result. If the specified
	game id corresponds to a game and the guess is valid, the values for the correct number
	of positions (black key peg) and correct number of colors (white key peg) are returned.
		{"correct_position": 1, "correct_color": 2}
	If the game has finished as a consequence of the guess, the game status and the winner
	are returned:
		{
			"correct_position": 1, 
			"correct_color": 2, 
			"status": "FINISHED",
			"winner": "CODEMAKER"
		}
	Otherwise, a Json string with the key "error" is returned, and the value is a description
	of the error.
		{"error": "Invalid guess"}
	"""
	if request.method != 'POST':
		return JsonResponse({'error': 'Method not allowed'}, status=405)

	try:
		request_dict = json.loads(request.body)
	except Exception as ex:
		return JsonResponse({'error': 'Invalid payload format: ' + repr(ex)}, status=400)

	if not 'guess' in request_dict or not isinstance(request_dict['guess'], list):
		return JsonResponse({'error': 'Must provide the guess as an array'}, status=400)

	game = mastermind.get_game(game_id=game_id)

	if game is None:
		return JsonResponse({'error': 'Could not find game with the specified ID'}, status=404)

	try:
		guess = mastermind.guess(game=game, guess_list=request_dict['guess'])
	except Exception as ex:
		return JsonResponse({'error': 'Could not make guess: ' + repr(ex)}, status=400)

	if guess is not None:
		response_dict = {
			'correct_position': guess.correct_position, 
			'correct_color': guess.correct_color
		}

		# add information if the game has finished
		if game.status == 'FINISHED':
			response_dict['status'] = game.status
			response_dict['winner'] = game.winner

		return JsonResponse(response_dict)

	return JsonResponse({'error': 'Could not make guess'}, status=500)
