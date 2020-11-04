from app.models import db, Game

class Board:
    layout =[]
    gameId = null

    def __init__(self, gameId=null):
        if(gameId == null):
            self.getNewBoard()
        else :
            this.layout = self.getBoard(gameId)

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

        storedBoard = gameBoard.board
        print(storedBoard)
