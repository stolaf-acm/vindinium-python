#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Example program using the vindinium package
import vindinium

client = vindinium.client()

# Initialization / Configuration of the game goes here
client.setKey('your_key')
client.setParam('mode', 'training')

# Begin the game
client.startGame()

# This is the main loop of the game, where you will decide how to move
while not client.game.finished:

    # Code here to decide how to make a move
    print(client.game.board)

    # Make the chosen move - this function will update client's game and state
    client.makeMove('dir')

# See the results of the game
print(client.game.results())

# Close the client
client.close()
