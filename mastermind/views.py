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


def detail(request):
	return JsonResponse({})

def guess(request):
	return JsonResponse({})
