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
        return {"moves":moves}


@api.route("/moves/<int:move_number>")
class GetMove(Resource):
    @api.response(200, 'OK')
    @api.response(400, ' Malformed request.')
    @api.response(404, ' Game/moves not found.')
    def get(self, gameId, move_number):
        ''' Return the move..'''
        move = Move.query.get(move_number)
        if (move == None):
            return {"message": "Game/moves not found."}, 404
        
        elif (move.gameId != gameId):
            return {"message": " Malformed request."}, 400

        data = {
            "type": move.type,
            "player": move.playerId,
            "column": move.column
        }
        
        return data


@api.route("/<int:playerId>")
class GetMove(Resource):
    @api.expect(model)
    @api.response(200, 'OK')
    @api.response(400, ' Malformed input. Illegal move.')
    @api.response(404, ' Game not found or player is not a part of it.')
    @api.response(409, " Player tried to post when it's not their turn.")
    def post(self, gameId, playerId):
        '''Post a move.'''
        game = Game.query.get(gameId)
        if (game == None):
            return {"message":"Game not found or player is not a part of it"}, 404

        if(game.status == "DONE"):
            return {"message":"Malformed input. Illegal move"}, 400

        move = Move.query.filter(Move.gameId==gameId).order_by(Move.movedOn.desc()).first()
       
        #  if there are not moves for this game
        if (move != None and move.playerId == playerId):
            return {"message":"Player tried to post when it's not their turn."}, 409

        else :
            board = Board(gameId)
            columnIdx = api.payload["column"]  
            moved = board.handleMove(columnIdx, playerId)  

            if(moved) :
                game.board = board.layout
                if(board.winner!= None):
                    game.status = "DONE"
                    game.winder = board.winner


                move = Move()
                move.gameId = gameId
                move.playerId = playerId
                move.column = columnIdx
                move.type = "MOVE"
                db.session.add(move)
                db.session.commit()
        
        response = "{gameId}/moves/{move_number}".format(gameId=gameId, move_number=move.id)
        
        return {"move":response}


    @api.response(200, 'OK')
    @api.response(400, ' Malformed input.')
    @api.response(404, ' Game not found or player is not a part of it.')
    def delete(self, gameId, playerId):
        ''' Player quits from game.'''
        game = Game.query.get(gameId)
        
        if (game == None or  (game.playerOneId != playerId and game.playerTwoId != playerId)):
            return {"message":"Game not found or player is not a part of it"}, 404
        
        if(game.status == "DONE"):
            return {"message":"Malformed input."}, 400


        game.playerQuit = playerId
        game.status= "DONE"
        game.winner = game.playerOneId if game.playerTwoId == playerId else game.playerTwoId

        move = Move()
        move.gameId = gameId
        move.playerId = playerId
        move.type = "QUIT"

        db.session.add(move)
        db.session.commit()


    