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


@api.route("/moves/<int:move_number>")
class GetMove(Resource):
    @api.response(200, 'OK')
    @api.response(400, ' Malformed request.')
    @api.response(404, ' Game/moves not found.')
    def get(self, gameId, move_number):
        '''Get (sub) list of the moves played.'''
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
        moves = Move.query.filter(Move.gameId==gameId).order_by(Move.movedOn.desc()).all()
        print("moves:", moves)
        if (len(moves) == 0):
            game = Game.query.get(gameId)
            if (game == None):
                return {"message":"Game not found or player is not a part of it"}, 404
            
            print("board: ", game.board)
            updateBoard = db.session.query(Game).filter(Game.id==gameId).first()
            board = Board(gameId)
            columnIdx = api.payload["column"]  
            print(columnIdx)
            moved = board.handleMove(columnIdx, playerId)  
            newBoard = [column for column in board.layout]
            # print("new board", newBoard)
            print(type(board.layout))
            print(type(newBoard))
            if(moved) :
                # game.board = board.layout
                updateBoard.id = game.id
                updateBoard.playerOneId = game.playerOneId
                updateBoard.playerTwoId = game.playerTwoId
                updateBoard.status = game.status
                updateBoard.board.append(board.layout[0]) 
                updateBoard.board.append(board.layout[1]) 
                updateBoard.board.append(board.layout[2]) 
                updateBoard.board.append(board.layout[3])
                # updateBoard.board = [column for column in board.layout]
                updateBoard.winner = game.winner
                # setattr(updateBoard, board, board.layout)
                db.session.commit()

                move = Move()
                move.gameId = gameId
                move.playerId = playerId
                move.column = columnIdx
                move.type = "MOVE"
                db.session.add(move)
                db.session.commit()


            # else:
                # check that is this players turn
            
        return {"games":"TODO"}