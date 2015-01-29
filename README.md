# A Python 3 client for Vindinium

This client requires the [requests](http://docs.python-requests.org/en/latest/) module.

To use this client, simply import the `vindinium.py` module like this:

```python
import vindinium.py
```

See [example.py](example.py) for an example program that uses the module.  Or see below for the documentation:

## Documentation

### class client
This class represents the Vindinium client.  It is also how you will interact with the library:

##### Data Members:
`game` - A Game object

`hero` - A Hero object representing the current player

`viewUrl` - A string containing the URL that the game can be viewed at

##### Methods:

`client.setKey(key)` - sets the key to connect to the Vindinium servers. It should be the same key that is given when a bot is created.

`client.setParam(key, value)` - sets client parameters when creating a game. Currently, it only supports the key `mode`, which can take the value `arena` or `training`

`client.startGame()` - starts the game that was configured with `setKey()` and `setParam()`. This marks the beginning of the 1-second time periods that you have to make a move.

`client.makeMove(move)` - submit the move you want to make to Vindinium. This will update the game and hero state.

`client.close()` - This function shuts down the connection to the client once the game has ended.

### class Game
This class stores all the information represented in the Vindinium Game object. It also handles parsing of the JSON received.

##### Data Members:
`turn` - The current turn of the game

`maxTurns` - The maximum number of turns in the game

`heroes` - An array of Hero objects including the current player

`board` - A Board object

`finished` - A boolean value indicating whether or not the game has finished

##### Methods:
`Game.results` - Print the results of the game

### class Board
This class represents the board of the game

##### Data Members:
`size` - the length of one side of a board. All boards are square.

`map` - A two-dimensional array of characters representing the game board. The following table lists all the characters and their meanings:

| Character | Description |
| --------- | ----------- |
| `' '`     | An empty tile |
| `'#'`     | An impassable tile |
| `'T'`     | A tavern |
| `'R', 'B', 'G', 'Y'` | A hero (you are `'R'`) |
| `'r', 'b', 'g', 'y'` | A mine owned by a hero |
| `'$'`     | An empty mine |

##### Methods:
`Board[]` - returns the map row that is indexed. Allows for `Board[]` rather than `Board.map[]`

### class Hero
This class represents a hero in Vindinium

##### Data Members:
`pos` - A tuple representing the hero's current position

`lastDir` - The last direction that the hero moved

`life` - The health of a hero (max 100)

`gold` - How much gold the hero owns

`mineCount` - How many mines are in the hero's posession

`spawnPos` - A tuple representing the hero's spawn position

`crashed` - A boolean value representing whether or not the hero has timed out

##### Methods:
The Hero object currently has no methods
