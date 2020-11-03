from app.models import db, Move, Game
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
        moves = Move.query.filter(Move.gameId==gameId).all()
        if moves == None:
            return {"message": "Game/moves not found."}, 404
        
        moves = [move.to_dictionary() for move in moves]
        return {"games":moves}