from app.models import db, Game

class Board:
    layout =[]
    gameId = None
    winner = None

    def __init__(self, gameId=None):
        if(gameId == None):
            self.getNewBoard()
        else :
            self.layout = self.getBoard(gameId)

    def handleMove(self, columnIdx, playerId ):
        if(self.isColumnFull(columnIdx) == False):
            columnToUpdate = self.layout[columnIdx-1]
            cells = [cell for cell in columnToUpdate]

            for i in range(len(cells)):
                cell = cells[i]
                print(cell)
                if(cell== "_"):
                    cells[i]=playerId
                    break

            self.layout[columnIdx-1] = " ".join([str(cell) for cell in cells])
            self.updateGame()
            self.checkForWinner()
            return True
        
        return False


    def checkForWinner(self):
        pass
    # TODO check column
    # TODO check row
    # TODO check diagonales



    # check if the column is full for the passed in column index
    def isColumnFull(self, columnIdx):
        columnToUpdate = self.layout[columnIdx-1]
        if(columnToUpdate[-1]!= '_'):
            print("is full")
            return True
        return False

    # initialize the board for a new game
    def getNewBoard(self):
        self.layout = ["____" for i in range(4)] 

    # get the state of the board from the database by the provided game id
    def getBoard(self, gameId):
        game = Game.query.get(gameId)
        if (game != None):
            return game.board

    def updateGame(self):
        pass



