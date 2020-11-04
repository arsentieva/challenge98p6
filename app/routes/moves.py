from app.models import db, Move, Game
from app.bi.board import Board
from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import ( jwt_required, get_jwt_identity)
from flask_cors import CORS, cross_origin

api = Namespace('moves', description="Game's activities")

model = api.model("Move", {
                            "column": fields.Integer( description="Specify column number for your move.", example=1),
                          }
                )

@api.route("/moves")
class GetMove(Resource):
    @api.response(200, 'OK')
    @api.response(400, ' Malformed request.')
    @api.response(404, ' Game/moves not found.')
    def get(self, gameId):
        '''Get (sub) list of the moves played.'''
        moves = Move.query.filter(Move.gameId==gameId).all()
        if (moves == None):
            return {"message": "Game/moves not found."}, 404
        
        moves = [move.to_dictionary() for move in moves]
        return {"games":moves}


@api.route("/<int:playerId>")
class GetMove(Resource):
    @api.expect(model)
    @api.response(200, 'OK')
    @api.response(400, ' Malformed input. Illegal move.')
    @api.response(404, ' Game not found or player is not a part of it.')
    @api.response(409, " Player tried to post when it's not their turn.")
    def post(self, gameId, playerId):
        '''Post a move.'''
        moves = Move.query.filter(Move.gameId==gameId).order_by(Move.movedOn.desc()).all()
        print("moves:", moves)
        if (len(moves) == 0):
            game = Game.query.get(gameId)
            if (game == None):
                return {"message":"Game not found or player is not a part of it"}, 404
            
            board = Board(gameId)
            columnIdx = api.payload["column"]  
            board.handleMove(columnIdx, playerId)  
            print(board.layout)      


            # else:
                # check that is this players turn
            
        return {"games":"TODO"}