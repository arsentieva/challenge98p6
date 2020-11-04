from app.models import db, Game

class Board:
    layout =[]
    gameId = None

    def __init__(self, gameId=None):
        if(gameId == None):
            self.getNewBoard()
        else :
            self.layout = self.getBoard(gameId)

    def handleMove(self):
        pass

    def checkForWinner(self):
        pass

    def switchPlayer(self):
        pass

    def isValidMove(self):
        pass

    def getNewBoard(self):
        self.layout = ["____" for i in range(4)] 

    def getBoard(self, gameId):
        game = Game.query.get(gameId)
        if (game == None):
            return "No game found for the provided game id"

        return game.board

