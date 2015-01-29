#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import webbrowser
import sys

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

        if response == None:
            print('Error: game could not be initialized')
            sys.exit(1)

        self.game = Game(response['game'])
        self.hero = Hero(response['hero'])
        self.viewUrl = response['viewUrl']
        self.playUrl = response['playUrl']

        # Print a message that the game has started
        print(str('Game Started at:'), str(self.viewUrl))
        webbrowser.open(self.viewUrl)

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
                sys.exit(1)
        except requests.exceptions.RequestException as e:
            print('Error in request:', str(e))

class Game:
    """A class representing the vindinium game object"""
    def __init__(self, state):
        # Set the default values of the game
        self.state = state
        self.heroes = []
        self.turn = state['turn']
        self.maxTurns = state['maxTurns']
        self.finished = state['finished']
        self.board = Board(state['board'])

        for i in range(0, len(state['heroes'])):
            self.heroes.append(Hero(state['heroes'][i]))

    def results(self):
        print('Finished.')

class Board:
    """A class representing the board of the game"""
    def __init__(self, board):
        self.size = None
        self.map = []

        self.process(board)

    def process(self, board):
        self.size = board['size']

        # Loop through the tiles to add locations to the map
        # y is the row number, x is the col number
        for y in range(0, len(board['tiles']), self.size * 2):
            maprow = []

            for x in range(0, self.size * 2, 2):
                tile = board['tiles'][x+y]
                if tile == ' ':
                    # empty space
                    maprow.append(' ')

                elif tile == '#':
                    # wall
                    maprow.append('#')

                elif tile == '$':
                    # mine
                    next_tile = board['tiles'][x+y+1]
                    if next_tile == '1':
                        maprow.append('r')
                    elif next_tile == '2':
                        maprow.append('b')
                    elif next_tile == '3':
                        maprow.append('g')
                    elif next_tile == '4':
                        maprow.append('y')
                    elif next_tile == '-':
                        maprow.append('$')

                elif tile == '[':
                    # tavern
                    maprow.append('T')

                elif tile == '@':
                    # player
                    next_tile = board['tiles'][x+y+1]
                    if next_tile == '1':
                        maprow.append('R')
                    elif next_tile == '2':
                        maprow.append('B')
                    elif next_tile == '3':
                        maprow.append('G')
                    elif next_tile == '4':
                        maprow.append('Y')

            self.map.append(maprow)

    def __getitem__(self, index):
        return self.map[index]

    def __str__(self):
        result = ''
        for row in range(0, len(self.map)):
            result += ''.join(self.map[row]) + '\n'
        return result

class Hero:
    """A class representing the vindinium hero object"""
    def __init__(self, hero):
        try:
            self.lastDir = hero['lastDir']
        except KeyError:
            self.lastDir = None
        self.pos = (hero['pos']['x'], hero['pos']['y'])
        self.life = hero['life']
        self.gold = hero['gold']
        self.mineCount = hero['mineCount']
        self.spawnPos = (hero['spawnPos']['x'], hero['spawnPos']['y'])
        self.crashed = hero['crashed']

if __name__ == '__main__':
    pass
