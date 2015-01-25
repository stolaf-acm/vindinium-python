#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import pprint

CONFIG_KEYS = ['mode']
DIRECTIONS = ['Stay', 'North', 'South', 'East', 'West']
TIMEOUT = 15

# This is the class that a program interacts with
class client:
    """A client for interacting with the vindinium server"""
    def __init__(self):
        self.key = None
        self.game = None
        self.hero = None
        self.viewUrl = None
        self.playUrl = None
        self.config = {}
        self.session = None

    def setKey(self, key):
        self.key = key

    def setParam(self, key, value):
        # Apply checks to make sure the key is a valid setting
        if key in CONFIG_KEYS:
            self.config[key] = value
        else:
            print('Skipping', key, 'because it is not a valid config parameter.')

    def startGame(self):
        self.session = requests.session()

        server_url = 'http://vindinium.org'
        if self.config['mode'] == 'arena':
            api_url = '/api/arena'
        else:
            api_url = '/api/training'

        response = self._request({'key': self.key}, server_url + api_url)

        self.game = Game(response['game'])
        self.hero = Hero(response['hero'])
        self.viewUrl = response['viewUrl']
        self.playUrl = response['playUrl']

        # Print a message that the game has started
        print('Game Started at:', self.viewUrl)

    def makeMove(self, move):
        """Make a move and update the client's state"""
        if move not in DIRECTIONS:
            move = 'Stay'
        response = self._request({'dir': move})

        self.game = Game(response['game'])
        self.hero = Hero(response['hero'])


    def close(self):
        self.session.close()

    def _request(self, params = {}, url = None):
        """Send a move to the vindinium server"""
        if url == None:
            url = self.playUrl

        try:
            response = self.session.post(url, params, timeout=TIMEOUT)
            if response.status_code == 200:
                # HTTP OK
                return response.json()
            else:
                print("HTTP Error", str(response.status_code), ":", response.text)
        except requests.exceptions.RequestException as e:
            print('Error in request:', str(e))

class Game:
    """A class representing the vindinium game object"""
    def __init__(self, state):
        # Set the default values of the game
        self.state = state
        self.turn = None
        self.maxTurns = None
        self.heroes = []
        self.board_size = None
        self.board_tiles = []
        self.finished = None

        self.process(self.state)

    def process(self, game):
        """Parse the game's state"""
        self.turn = game['turn']
        self.maxTurns = game['maxTurns']
        self.finished = game['finished']
        self.board_size = game['board']['size']
        self.board_tiles = game['board']['tiles']

    def results(self):
        print('Finished.')

class Hero:
    """A class representing the vindinium hero object"""
    def __init__(self, hero = None):
        pass

if __name__ == '__main__':
    pass
