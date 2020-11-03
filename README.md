# Drop-Token
implement a backend (REST web-service) that allows playing the game of 9dt, or 98point6 drop token. This should allow the players to create games, post moves, query moves and get state of games.

##  Rules of the Game
[ ] Drop Token takes place on a 4x4 grid.
[ ] A token is dropped along a column and said token goes to the lowest unoccupied row of the board.
[ ] A player wins when they have 4 tokens next to each other either along a row, in a column, or on a diagonal.
[ ] If the board is filled, and nobody has won then the game is a draw.
[ ] Each player takes a turn, starting with player 1, until the game reaches either win or draw.
[ ] If a player tries to put a token in a column that is already full, that results in an error state, and the player must play again until the play a valid move.

## Requirements
[ ] Each game is between *k = 2* individuals
[ ] basic board size is 4x4 (number of columns x number of rows)
[ ] A player can quit a game at every moment while the game is still in progress. The game will continue as long as there are 2 or more active players and the game is not done. In case only a single player is left, that player is considered the winner.
[ ] The backend should validate that a move is valid (it's the player's turn, column is not already full)
[ ] The backend should identify a winning state.
[ ] Multiple games may be running at the same time.

## API

#### POST /drop_token - Create a new game.

 => { 
     "players": ["player1", "player2"],
      "columns": 4,
      "rows":4
    }

 <=> { "gameId": "some_string_token"}
    
    * #### Status codes ####
    * 200 - OK. On success
    * 400 - Malformed request


#### GET /drop_token - Return all in-progress games.

 <=> { "games" : ["gameid1", "gameid2"] }
    
    *  #### Status codes ####
    * 200 - OK. On success


#### GET /drop_token/{gameId} - Get the state of the game.
 <=> { "players" : ["player1", "player2"], # Initial list of players.
       "state": "DONE/IN_PROGRESS",
       "winner": "player1", # in case of draw, winner will be null, state will be DONE.
                       # in case game is still in progess, key should not exist. // ??? in the response
     }

    * #### Status codes ####
    * 200 - OK. On success
    * 400 - Malformed request
    * 404 - Game/moves not found.
    


#### GET /drop_token/{gameId}/moves- Get (sub) list of the moves played.
 <=> {
      "moves": 
      [
          {"type": "MOVE", "player": "player1", "column":1}, 
          {"type": "QUIT", "player": "player2"}
      ]
    }

    * #### Status codes ####
    * 200 - OK. On success
    * 400 - Malformed request
    * 404 - Game/moves not found.


#### POST /drop_token/{gameId}/{playerId} - Post a move.
#### GET /drop_token/{gameId}/moves/{move_number} - Return the move.
#### DELETE /drop_token/{gameId}/{playerId} - Player quits from game.



