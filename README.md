# Readme

This is the implementation of the Backend Technical Test for [21buttons](https://www.21buttons.com/).
The project consists of a REST API that simulates the role of the *codemaker* in the game of [Mastermind](https://en.wikipedia.org/wiki/Mastermind_(board_game)).

# Requirements
This project requires a working Python 3.x installation.
Django is a project dependency. We provide the instructions to install it inside a virtualenv. In that case, you are going to need the [virtualenv](https://virtualenv.pypa.io/en/stable/) tool and [pip](https://pypi.python.org/pypi/pip).

# How to install
1. Clone this repository into a directory of your choice:

        $ git clone https://github.com/amaneu/test21b.git

2. Create a new virtual environment:

        $ virtualenv env21b --python=python3

3. Activate the virtual environment:

        $ source env21b/bin/activate

4. Change dir to the repository's directory:

        (env21b)$ cd test21b

5. Install dependencies using pip:

        (env21b)$ pip install -r requirements.txt

6. Run migrations in order to create the database schema:

        (env21b)$ python manage.py migrate

7. Run the server:

        (env21b)$ python manage.py runserver

The server will start listening at `http://localhost:8000`.


# How to play

There are 3 endpoints:

1. An endpoint to create a new game: `/mastermind/new-game`

2. An endpoint to make a new guess: `/mastermind/game/<id>/guess`

3. An endpoint to get information about a game: `/mastermind/game/<id>`


## Start a new game

Issue a POST request to the endpoint: `http://localhost:8000/mastermind/new-game`.

The body of the request must be a json string which accepts the following optional parameters:

  * `num_holes` (defaults to 4)
  * `num_colors` (defaults to 6)
  * `max_guesses` (defaults to 12)

When any of the parameters is not specified, its default value is used.

The response is a json string with the game ID. For example:

    {"id": 7}

The server randomly generates a secret combination of numbers (*the secret*) that the codebreaker has to guess.

### Examples

Create a game with 4 holes, 6 colors and up to 12 guesses (the default values):

    curl -X POST -d '{}' "http://localhost:8000/mastermind/new-game"


Create a game with 5 holes, 6 colors and up to 12 guesses:

    curl -X POST -d '{"num_holes": 5}' "http://localhost:8000/mastermind/new-game"

Create a game with 16 holes, 16 colors and up to 16 guesses:

    curl -X POST -d '{"num_holes": 16, "num_colors": 16, "max_guesses": 16}' "http://localhost:8000/mastermind/new-game"


## Make a guess

Issue a POST request to the endpoint: `http://localhost:8000/mastermind/game/<id>/guess` where `<id>` is the game ID you received from the server when starting the game.

The server allows you to play several different games at the same time.

The body of the request must be a json string with the following parameter:

  * `guess` an array of numbers representing the guess

The colors in the original mastermind game are represented here by numbers, so for instance `[0, 1, 2, 5]` might map to `['red', 'blue', 'green', 'yellow']` in the corresponding client application.

The minimum number is always `0` and the maximum number is `num_colors - 1`.

The response is a json string indicating the values for the correct number of positions (black key peg) and correct number of colors (white key peg) for this guess. Additionally, if the game has finished as a consequence of the guess, the status and the winner are included in the response.

### Examples

Guess the combination `[0, 0, 2, 3]` for the game with id=7:

    curl -X POST -d '{"guess": [0, 0, 2, 3]}' "http://localhost:8000/mastermind/game/7/guess"

If the guess did not bring the game to an end, the response might be something like:

    {"correct_position": 1, "correct_color": 2}

indicating there is 1 peg of the correct color (number) and in the correct position, and 2 pegs with the correct color (number) but incorrect position.

If the guess brought the game to an end because it was the correct answer, the response might be:

	{
		"correct_position": 4, 
		"correct_color": 0, 
		"status": "FINISHED",
		"winner": "CODEBREAKER"
	}

If, instead, the guess brought the game to an end because it was the last possible guess (according to `max_guesses`), the response might be:

	{
		"correct_position": 1, 
		"correct_color": 0, 
		"status": "FINISHED",
		"winner": "CODEMAKER"
	}


## Check the details of a game

Issue a GET request to the endpoint: `http://localhost:8000/mastermind/game/<id>` where `<id>` is the game ID you received from the server when starting the game.

The response is a json string describing the specified game. If the game is finished, the secret code is included in the response. The details of the game also include the list of attempted guesses.

### Examples

To get the details of the game with id=7:

    curl "http://localhost:8000/mastermind/game/7"

The response might be:

	{  
	   "started_at":"2018-03-12T16:10:08.735Z",
	   "finished_at":"2018-03-12T16:11:38.651Z",
	   "status":"FINISHED",
	   "winner":"CODEBREAKER",
	   "num_holes":4,
	   "num_colors":6,
	   "max_guesses":12,
	   "guesses":[  
	      {  
	         "id":20,
	         "created_at":"2018-03-12T16:10:24.620Z",
	         "guess":[  
	            0,
	            0,
	            2,
	            3
	         ],
	         "correct_position":0,
	         "correct_color":3
	      },
	      {  
	         "id":21,
	         "created_at":"2018-03-12T16:11:03.830Z",
	         "guess":[  
	            0,
	            0,
	            2,
	            0
	         ],
	         "correct_position":1,
	         "correct_color":2
	      },
	      {  
	         "id":22,
	         "created_at":"2018-03-12T16:11:20.176Z",
	         "guess":[  
	            0,
	            2,
	            2,
	            0
	         ],
	         "correct_position":2,
	         "correct_color":2
	      },
	      {  
	         "id":23,
	         "created_at":"2018-03-12T16:11:24.790Z",
	         "guess":[  
	            2,
	            2,
	            2,
	            0
	         ],
	         "correct_position":3,
	         "correct_color":0
	      },
	      {  
	         "id":24,
	         "created_at":"2018-03-12T16:11:29.562Z",
	         "guess":[  
	            2,
	            2,
	            2,
	            2
	         ],
	         "correct_position":2,
	         "correct_color":0
	      },
	      {  
	         "id":25,
	         "created_at":"2018-03-12T16:11:33.914Z",
	         "guess":[  
	            2,
	            2,
	            0,
	            2
	         ],
	         "correct_position":3,
	         "correct_color":0
	      },
	      {  
	         "id":26,
	         "created_at":"2018-03-12T16:11:38.646Z",
	         "guess":[  
	            2,
	            2,
	            0,
	            0
	         ],
	         "correct_position":4,
	         "correct_color":0
	      }
	   ],
	   "secret":[  
	      2,
	      2,
	      0,
	      0
	   ]
	}

## Errors

If any of the requests to any endpoint result in an error (for example, trying to get details of a nonexistent game, or trying to start a game with a negative number of holes), the response is a json string with the attribute `error` and the value describing the error. For example:

    {"error": "Could not find game with the specified ID"}


## Testing

You can run the unit tests by executing:

    $ python manage.py test mastermind

