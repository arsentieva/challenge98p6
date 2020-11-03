from app.models import db, Move
from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import ( jwt_required, get_jwt_identity)
from flask_cors import CORS, cross_origin

api = Namespace('moves', description='Create and update user operations')

model = api.model("Move", {
                            "name": fields.String( description="User first name.", example="John"),
                          }
                )

@api.route("/")
class GetMove(Resource):
    @api.response(200, 'OK')
    @api.response(400, ' Malformed request.')
    @api.response(404, ' Game/moves not found.')
    def get(self, gameId):
        '''Get (sub) list of the moves played.'''
        games = Game.query.filter(Game.status=="IN_PROGRESS").all()
        if games == None:
            return {"message": "No games in progress state found"}, 404
        # TODO format the output in an array
        return {"games":"TODO"}