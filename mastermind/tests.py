from django.test import TestCase
from . import mastermind
from .models import Game, Guess

class MastermindTests(TestCase):
	def test_check_guess(self):
		"""Check the correct number of black and white key pegs is returned"""
		examples = [
			{
				'secret': [1, 1, 1, 1],
				'guess': [1, 1, 1, 1],
				'correct_position': 4,
				'correct_color': 0
			},
			{
				'secret': [0, 1, 2, 3],
				'guess': [3, 2, 1, 0],
				'correct_position': 0,
				'correct_color': 4
			},
			{
				'secret': [2, 8, 8, 2],
				'guess': [2, 2, 2, 2],
				'correct_position': 2,
				'correct_color': 0
			},
			{
				'secret': [2, 8, 8, 2],
				'guess': [8, 8, 2, 8],
				'correct_position': 1,
				'correct_color': 2
			},
			{
				'secret': [1, 3, 5, 3],
				'guess': [3, 1, 5, 0],
				'correct_position': 1,
				'correct_color': 2
			},
			{
				'secret': [0, 1],
				'guess': [1, 0],
				'correct_position': 0,
				'correct_color': 2
			},
			{
				'secret': [0, 0],
				'guess': [1, 0],
				'correct_position': 1,
				'correct_color': 0
			},
			{
				'secret': [0, 1, 2, 3, 4, 5],
				'guess': [6, 7, 8, 9, 10, 11],
				'correct_position': 0,
				'correct_color': 0
			},
		]

		for example in examples:
			correct_position, correct_color = mastermind.check_guess(example['secret'], example['guess'])
			self.assertEqual(correct_position, example['correct_position'])
			self.assertEqual(correct_color, example['correct_color'])


	def test_exceptions(self):
		with self.assertRaises(Exception):
			mastermind.create_game(num_holes=0, num_colors=0, max_guesses=0)

		with self.assertRaises(Exception):
			mastermind.create_game(num_holes=-1, num_colors=1, max_guesses=1)

		with self.assertRaises(Exception):
			game = Game(status='STARTED', secret='[1, 2, 3, 4]', num_holes=4, num_colors=6, max_guesses=12)
			guess = mastermind.guess(game, [])

		with self.assertRaises(Exception):
			game = Game(status='STARTED', secret='[1, 2, 3, 4]', num_holes=4, num_colors=6, max_guesses=12)
			guess = mastermind.guess(game, [2, 3])

		with self.assertRaises(Exception):
			game = Game(status='STARTED', secret='[1, 2, 3, 4]', num_holes=4, num_colors=6, max_guesses=12)
			guess = mastermind.guess(game, [7, 7, 7, 7])

		with self.assertRaises(Exception):
			game = Game(status='STARTED', secret='[1, 2, 3, 4]', num_holes=4, num_colors=6, max_guesses=12)
			guess = mastermind.guess(game, [-1, 0, 0, 0])


	def test_return_none_on_nonexistent_game(self):
		game = mastermind.get_game(-1)
		self.assertIsNone(game)
