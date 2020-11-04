from app.models import db, Game, Player
from app.bi.board import Board
from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import create_access_token
from flask_cors import CORS, cross_origin


api = Namespace('drop_token', description='Create and play drop token game aka connect four')

create_model = api.model("Game", {
                            "players": fields.List(fields.Integer(), required=True, description = "Specify all the player ids", example = [1,2]),
                            "columns": fields.Integer(required=True, description="Specify number of columns.", example=4),
                            "rows": fields.Integer(required=True, description="Specify number of rows.", example=4),
                          }
                )

@api.route("/")
class DropToken(Resource):
    @api.response(200, 'OK')
    @api.response(404, 'No Games found in progress')
    def get(self):
        '''Return all in-progress games.'''
        games = Game.query.filter(Game.status=="IN_PROGRESS").all()
        if games == None:
            return {"message": "No games in progress state were found"}, 404
        
        gameIds = [game.id for game in games]

        return {"games": gameIds}


    @api.expect(create_model)
    @api.response(200, 'OK')
    @api.response(400, 'Malformed request')
    @api.response(404, '404 - Game/moves not found')
    def post(self):
        '''Create a new game.'''
        players = api.payload["players"]
        columns = api.payload["columns"]
        rows = api.payload["rows"]
        if(len(players)<= 1 or len(players)>2 or (columns != 4) or (rows != 4) ):
            return {"message": "Malformed request"}, 400
        

        player_one = players[0]
        player_two = players[1]

        player_one = Player.query.get(player_one) 
        if player_one == None:
            player_one = Player()
            player_one.id = players[0]
            player_one.symbol = "X"
            db.session.add(player_one)
            db.session.commit()

        player_two = Player.query.get(player_two) 
        if player_two == None:
            player_two = Player()
            player_two.id = players[1]
            player_two.symbol = "O"
            db.session.add(player_two)
            db.session.commit()

        game = Game()
        game.playerOneId = player_one.id
        game.playerTwoId = player_two.id
        game.status = "IN_PROGRESS" #TODO consider creating a const or an enum for the game status
        board = Board()
        game.board = board.layout
        db.session.add(game)
        db.session.commit()
        token = create_access_token(identity=game.id)

        return {"gameId": token }

@api.route("/<int:gameId>")
class GetDropTokenByGameId(Resource):
    @api.response(200, 'OK')
    @api.response(400, 'Malformed request.')
    @api.response(404, 'Game/moves not found.')
    def get(self, gameId):
        '''Get the state of the game.'''
        game = Game.query.get(gameId)
        print(game)
        if game == None:
            return {"message": "Game/moves not found"}, 404
        game_state = {
            "players": [game.playerOneId, game.playerTwoId],
            "state": game.status,
        }
        
        if(game.status == "DONE"):
            game_state["winner"]= game.winner

        return game_state