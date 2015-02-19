#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Example ai using the vindinium package
#   This ai sets its own goals, and then
import vindinium
from collections import deque

# We will keep track of a goal, and how to achieve that goal
# with a path of moves
goal = None
path = deque()

# Helper functions
def check_goal(old_goal):
    global goal

    # If there is less than 20 HP, we need to heal up
    if client.hero.life - len(path) < 20 and old_goal != 'heal':
        goal = 'heal'
        recalculate_path(goal)

    # Otherwise, let's go get some gold
    if client.hero.life > 80 and old_goal != 'gold':
        goal = 'gold'
        recalculate_path(goal)

def recalculate_path(goal):
    global path

    if goal == 'heal':
        path.extend(generate_path('T'))
    elif goal == 'gold':
        path.extend(generate_path(['$', 'b', 'g', 'y']))

def generate_path(char):

    # Save board size for use in function
    boardSize = client.game.board.size

    # Perform a breadth-first search to find a path to char
    search = deque()

    # Add the first set of tiles to the deque
    search.append((client.hero.pos[0], client.hero.pos[1]+1, ['East']))
    search.append((client.hero.pos[0]+1, client.hero.pos[1], ['South']))
    search.append((client.hero.pos[0], client.hero.pos[1]-1, ['West']))
    search.append((client.hero.pos[0]-1, client.hero.pos[1], ['North']))

    # Set up the first search item
    item = search.popleft()
    tile = client.game.board[item[0]][item[1]]

    while tile not in char:
        print(tile, item)

        # if there are no characters left in the queue, uh-oh
        if len(search) == 0:
            return ['Stay']

        # if the tile is impassable, ignore it
        if tile not in [' ', 'B', 'G', 'Y']:
            item = search.popleft()
            tile = client.game.board[item[0]][item[1]]
            continue
        else:
            partial = item[2]

            # TODO: add range restriction
            if partial[-1] != 'East' and item[1]-1 in range(0,boardSize):
                partial.append('East')
                search.append((item[0], item[1]-1, partial))
                partial.pop()
            if partial[-1] != 'South' and item[0]-1 in range(0,boardSize):
                partial.append('South')
                search.append((item[0]-1, item[1], partial))
                partial.pop()
            if partial[-1] != 'West' and item[1]+1 in range(0,boardSize):
                partial.append('West')
                search.append((item[0], item[1]+1, partial))
                partial.pop()
            if partial[-1] != 'North' and item[0]+1 in range(0,boardSize):
                partial.append('North')
                search.append((item[0]+1, item[1], partial))
                partial.pop()

            item = search.popleft()
            tile = client.game.board[item[0]][item[1]]
            continue

    return item[2]

# Initialize the vindinium client
client = vindinium.client()

# Initialization / Configuration of the game goes here
client.setKey('your_key')
client.setParam('mode', 'training')

# Begin the game
client.startGame()

# This is the main loop of the game, where you will decide how to move
while not client.game.finished:

    # See what we're trying to do
    print(goal)

    # Check to see if our goal should change
    check_goal(goal)

    # If there are no items in the path
    if len(path) < 1:
        recalculate_path(goal)

    # Get a move from the path
    move = path.popleft()

    # Make the chosen move - this function will update client's game and state
    # 'dir' can be one of 'Stay', 'North', 'South', 'East', or 'West'
    client.makeMove(move)

# See the results of the game
print(client.game.results())

# Close the client
client.close()
