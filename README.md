#Application deployed and live [here](https://drop-token-98p6.herokuapp.com/)

<details>
  <summary> 🔻 Database schema </summary>
  <img align="left" alt="GIF" src="https://github.com/arsentieva/challenge98p6/blob/master/drop_token.png" />

</details>


<details>
  <summary>:zap: Set up information</summary>

  This challenge was implemented using the following packages and libraries:
  * Flask 
  * python-dotenv
  * psycopg2-binary
  * SQLAlchemy
  * flask-restx
  * alembic
  * Flask-Migrate
  * python_version = "3.8"

  * PostgreSQL database for data storage

  ### Database set up
  - create a user named 'drop_token_admin' with password "password"
  - create a database named 'drop_token_db' and "drop_token_admin" as owner
  

  ### Application setup
    - in the application root folder enter ``` pipenv install ```
    - in the application root folder  create a .env file and copy the setup from .env.example and paste it into .env

  ### Create and migrate database tables
    -  from the application root folder run ``` pipenv shell ```  to enter the virtual environment
 
    ``` pipenv run flask db upgrade ```

    - after this your database should be ready to play the game

  ### Running the application
    -  from the application root folder run ``` pipenv shell ```  to enter the virtual environment if it is not still active 
    - ``` flask run ``` to run the application 
    - open the browser and navigate to http://127.0.0.1:5000/
    - on a successful setup you should get access to the game API routes that have been implemented and can be tested from the browser


  
<details>
  <summary>:zap: Flask Back end and PostogreSQL database deployment to Heroku</summary>

  ** Perquisites have a heroku account
  ## app configuration
  * in your .env file define a variable DATABASE_URL and set it to your local db connection
  * in your config file make sure to use DATABASE_URL (this var will be dynamically populated when run in development vs production )

  ## heroku configuration
  * in your application install gunicorn by running ``` pipenv install gunicorn ```
  * in the root directory add a file named Procfile and add the following code to it : ``` web: gunicorn app:app ```

  * in the terminal type ``` heroku login ``` to make sure you are logged in
  * run ``` heroku create drop-token-98p6 ``` to create an application in heroku named "drop-token-98p6"
  * run ``` git push heroku master ```

  ## Install Heroku Postgres add-on for the database
  * From the Heroku account select your project ad under the Overview and Install add-ons section click Configure Add-Ons
   this will redirect to Resources page, select Find more add-ons and search for Heroku Postgres (choose a plan, i used Hobby Dev which is free) then specify which project/app you want the database to be attached to as a result a new "DATABASE_URL" will be automatically created for the project that will point to this database ( this config var can be found in the Setting tab/ Reveal Config Vars, if you have other vars that you need to add now it is a good time to do that) 

  I installed the add-on for the database via Heroku UI but here is the equivalent command for the terminal :
  *  ``` heroku addons:create heroku-postgresql:hobby-dev ``` 

  ## Migrate and Create your tables
  * run ``` heroku run flask db upgrade ``` this should create all the tables for your application
  * if you have seed data in a file like databse.py you can runn it ``` heroku run python database.py ```

  You are all set

</details>



</details>


<br/>
<br/>

<details>
  <summary>:zap: Challenge Requirements</summary>

# Drop-Token
implement a backend (REST web-service) that allows playing the game of 9dt, or 98point6 drop token. This should allow the players to create games, post moves, query moves and get state of games.

##  Rules of the Game
[ X ] Drop Token takes place on a 4x4 grid.
[ X ] A token is dropped along a column and said token goes to the lowest unoccupied row of the board.
[ X ] A player wins when they have 4 tokens next to each other either along a row, in a column, or on a diagonal.
[ X ] If the board is filled, and nobody has won then the game is a draw.
[ X ] Each player takes a turn, starting with player 1, until the game reaches either win or draw.
[ X ] If a player tries to put a token in a column that is already full, that results in an error state, and the player must play again until the play a valid move.

## Requirements
[ X ] Each game is between *k = 2* individuals
[ X ] basic board size is 4x4 (number of columns x number of rows)
[ X ] A player can quit a game at every moment while the game is still in progress. The game will continue as long as there are 2 or more active players and the game is not done. In case only a single player is left, that player is considered the winner.
[ X ] The backend should validate that a move is valid (it's the player's turn, column is not already full)
[ X ] The backend should identify a winning state.
[ X ] Multiple games may be running at the same time.

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
 => {
      "column" : 2
    }

 <=> {
        "move": "{gameId}/moves/{move_number}"
     }

    * #### Status codes ####
    * 200 - OK. On success
    * 400 - Malformed input. Illegal move
    * 404 - Game not found or player is not a part of it.
    * 409 - Player tried to post when it's not their turn.
 

#### GET /drop_token/{gameId}/moves/{move_number} - Return the move.
 <=>  {
        "type" : "MOVE",
        "player": "player1",
        "column": 2
      }

    * #### Status codes ####
    * 200 - OK. On success
    * 400 - Malformed request
    * 404 - Game/moves not found.


#### DELETE /drop_token/{gameId}/{playerId} - Player quits from game.
 <=> 
   * #### Status codes ####
   * 202 - OK. On success
   * 404 - Game not found or player is not a part of it.
   * 410 - Game is already in DONE state
   

</details>


