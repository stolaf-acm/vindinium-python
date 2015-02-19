#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Example ai using the vindinium package
#   This ai rushes to get as many mines as possible, without regards
#   for anything else (including walls in its way)

import vindinium

client = vindinium.client()

# Initialization / Configuration of the game goes here
client.setKey('your_key')
client.setParam('mode', 'training')

# Begin the game
client.startGame()

# This is the main loop of the game
while not client.game.finished:

    # Loop over all of the mines to find the closest one
    closest = None
    direction = None
    for mine in client.game.board.mines:

        # Ignore mines that we already own
        if client.game.board[mine[0]][mine[1]] == 'r':
            continue

        distance = (client.hero.pos[0] - mine[0], client.hero.pos[1] - mine[1])

        if closest == None or abs(distance[0]) + abs(distance[1]) < closest:
            closest = abs(distance[0]) + abs(distance[1])
            direction = distance

    # Find the direction to move closer to the closest mine
    move = None
    if abs(direction[0]) < abs(direction[1]):
        if direction[1] < 0:
            move = 'East'
        else:
            move = 'West'
    else:
        if direction[0] < 0:
            move = 'South'
        else:
            move = 'North'

    # Make the chosen move
    client.makeMove(move)

# See the results of the game
print(client.game.results())

# Close the client
client.close()
