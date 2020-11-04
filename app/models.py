from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class Game(db.Model):
    __tablename__="games"

    id = db.Column(db.Integer, primary_key=True)
    playerOneId = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    playerTwoId = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    board = db.Column(db.String(100), nullable=False)
    winner = db.Column(db.String(20))


# class Board(db.Model):
#     __tablename__="boards"

#     id = db.Column(db.Integer, primary_key=True)
#     gameId = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)
#     state = db.Column(db.String(20), nullable=False)

#     game = db.relationship("Game", backref="board", lazy=True)


class Player(db.Model):
    __tablename__ = 'players'

    id = db.Column(db.Integer, primary_key=True)
    # name = db.Column(db.String(50), nullable=False)
    symbol = db.Column(db.String(10), nullable=False)

class Move(db.Model):
    __tablename__= "moves"

    id = db.Column(db.Integer, primary_key=True)
    playerId = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    gameId = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)
    column = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(20), nullable=False)
    movedOn = db.Column(db.DateTime, default=datetime.utcnow)

    game = db.relationship("Game", backref="move", lazy=True)

    def to_dictionary(self):
        data = {
            "type": self.type,
            "player": self.playerId, 
        }

        if(self.type != "QUIT"):
            data["column"]= self.column

        return data 