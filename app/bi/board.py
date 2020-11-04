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
        rows, cols = (4, 4)
        self.layout = [["_" for i in range(cols)] for j in range (rows)] 

    def getBoard(self, gameId):
        game = Game.query.get(gameId)
        if (game == None):
            return "No game found for the provided game id"

        storedBoard = game.board
        print(storedBoard)
