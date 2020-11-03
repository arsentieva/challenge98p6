from app.models import db, Game, Player
from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import create_access_token
from flask_cors import CORS, cross_origin

api = Namespace('games', description='Create and update user operations')

create_model = api.model("Game", {
                            "players": fields.List(fields.Integer(), required=True, description = "Specify all the player ids", example = [1,2]),
                            "columns": fields.Integer(required=True, description="Specify number of columns.", example=4),
                            "rows": fields.Integer(required=True, description="Specify number of rows.", example=4),
                          }
                )

@api.route("/")
class GetDropToken(Resource):
    @api.response(200, 'OK')
    @api.response(404, 'No Games found in progress')
    def get(self):
        '''Return all in-progress games.'''
        games = Game.query.filter(Game.status=="IN_PROGRESS").all()
        if games == None:
            return {"message": "No games in progress state found"}, 404
        # TODO format the output in an array
        return {"games":"TODO"}


@api.route("/")
class CreateDropToken(Resource):
    @api.expect(create_model)
    @api.response(200, 'OK')
    @api.response(400, 'Malformed request')
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
            player_one.name = "TODO"
            player_one.color = "TODO"
            db.session.add(player_one)
            db.session.commit()

        player_two = Player.query.get(player_two) 
        if player_two == None:
            player_two = Player()
            player_two.id = players[1]
            player_two.name = "TODO"
            player_two.color = "TODO"
            db.session.add(player_two)
            db.session.commit()

        game = Game()
        game.player_one_id = player_one.id
        game.player_two_id = player_two.id
        game.status = "IN_PROGRESS" #TODO consider creating a const or an enum for the game status
        db.session.add(game)
        db.session.commit()
        token = create_access_token(identity=game.id)

        #TODO create a new empty board , 2D array

        return {"gameId": token }


@api.route("/<int:game_id>")
class GetDropTokenByGameId(Resource):
    @api.response(200, 'OK')
    @api.response(400, 'Malformed request.') # TODO when the key is a not a number
    @api.response(404, 'Game/moves not found.')
    def get(self, game_id):
        '''Get the state of the game.'''
        game = Game.query.get(Game.id==game_id)
        if game == None:
            return {"message": "No games in progress state found"}, 404
        # TODO format the output 
        return {"players":"TODO"}