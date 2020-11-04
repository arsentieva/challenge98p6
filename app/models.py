from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class Game(db.Model):
    __tablename__="games"

    id = db.Column(db.Integer, primary_key=True)
    playerOneId = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    playerTwoId = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    playerQuit = db.Column(db.Integer, db.ForeignKey('players.id'))
    status = db.Column(db.String(20), nullable=False)
    board = db.Column(db.String(40), nullable=False)
    winner = db.Column(db.String(20))


class Player(db.Model):
    __tablename__ = 'players'

    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(1), nullable=False)
    # name = db.Column(db.String(50), nullable=False)

class Move(db.Model):
    __tablename__= "moves"

    id = db.Column(db.Integer, primary_key=True)
    playerId = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    gameId = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)
    column = db.Column(db.Integer)
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