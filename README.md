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

##### Methods:

`client.setKey(key)` - sets the key to connect to the Vindinium servers. It should be the same key that is given when a bot is created.

`client.setParam(key, value)` - sets client parameters when creating a game. Currently, it only supports the key `mode`, which can take the value `arena` or `training`

`client.startGame()` - starts the game that was configured with `setKey()` and `setParam()`. This marks the beginning of the 1-second time periods that you have to make a move.

`client.makeMove(move)` - submit the move you want to make to Vindinium. This will update the game and hero state.

`client.close()` - This function shuts down the connection to the client once the game has ended.
