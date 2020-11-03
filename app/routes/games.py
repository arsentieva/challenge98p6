from app.models import db, Game
from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import ( jwt_required, get_jwt_identity)
from flask_cors import CORS, cross_origin

api = Namespace('games', description='Create and update user operations')

model = api.model("Game", {
                            "name": fields.String( description="User first name.", example="John"),
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