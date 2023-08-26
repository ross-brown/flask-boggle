from unittest import TestCase

from app import app, games

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class BoggleAppTestCase(TestCase):
    """Test flask app of Boggle."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with self.client as client:
            response = client.get('/')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<table', html)

    def test_api_new_game(self):
        """Test starting a new game."""

        with self.client as client:
            response = client.post("/api/new-game")
            resp_json = response.get_json()

            self.assertIsInstance(resp_json["game_id"], str)
            self.assertIsInstance(resp_json["board"], list)
            self.assertIsInstance(resp_json["board"][0], list)
            self.assertIn(resp_json["game_id"], games)

            # make a post request to /api/new-game
            # get the response body as json using .get_json()
            # test that the game_id is a string
            # test that the board is a list
            # test that the game_id is in the dictionary of games (imported from app.py above)

    def test_score_word(self):
        """Test if word is valid"""

        with self.client as client:
            response = client.post("/api/new-game")
            resp_json = response.get_json()

            game_id = resp_json["game_id"]
            game = games[game_id]

            game.board = [
                ["G", "O", "T", "Y", "B"],
                ["C", "S", "U", "P", "M"],
                ["P", "I", "C", "H", "J"],
                ["E", "A", "V", "U", "S"],
                ["H", "T", "Y", "R", "W"]]

            # POST with valid word
            repsonse = client.post("/api/score-word",
                                   json={'word': 'GOT',
                                         'gameId': game_id})
            data = repsonse.get_json()

            self.assertEqual({'result': 'ok'}, data)

            # POST with valid word NOT on board
            repsonse = client.post("/api/score-word",
                                   json={'word': 'RUN',
                                         'gameId': game_id})
            data = repsonse.get_json()

            self.assertEqual({'result': 'not-on-board'}, data)

            # POST with invalid word
            repsonse = client.post("/api/score-word",
                                   json={'word': 'FDGHSJ',
                                         'gameId': game_id})
            data = repsonse.get_json()

            self.assertEqual({'result': 'not-word'}, data)

            # make a post request to /api/new-game
            # get the response body as json using .get_json()
            # find that game in the dictionary of games (imported from app.py above)

            # manually change the game board's rows so they are not random

            # test to see that a valid word on the altered board returns {'result': 'ok'}
            # test to see that a valid word not on the altered board returns {'result': 'not-on-board'}
            # test to see that an invalid word returns {'result': 'not-word'}
