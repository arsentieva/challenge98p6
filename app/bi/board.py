from app.models import db, Game

class Board:
    matrix = []
    gameId = None
    winner = None
    layout = None


    def __init__(self, gameId=None):
        if(gameId == None):
            self.getNewBoard()
        else :
            self.layout = self.getBoard(gameId)

    def handleMove(self, columnIdx, playerId ):
        if(self.isColumnFull(columnIdx) == False):

            columnToUpdate = self.matrix[columnIdx-1]
            cells = [cell for cell in columnToUpdate]
            for i in range(len(cells)):
                cell = cells[i]
                if(cell== "_"):
                    cells[i]=playerId
                    break

            self.matrix[columnIdx-1] = [cell for cell in cells]
            self.layout = "".join(str(cell) for cells in self.matrix for cell in cells)
            self.checkForWinner()
            return True
        
        return False


    def checkForWinner(self):
        pass
    # TODO check column
    # TODO check row
    # TODO check diagonales
    # TODO update the winner


    # check if the column is full for the passed in column index
    def isColumnFull(self, columnIdx):
        columnToUpdate = self.matrix[columnIdx-1] # this is the string that represents our column
        print("print",columnToUpdate)
        size = len(columnToUpdate)
        lastCell = columnToUpdate[size-1]

        if(lastCell!= '_'):
            return True
        return False

    # initialize the board for a new game
    def getNewBoard(self):
        rows, cols = (4, 4)
        self.matrix = [["_" for i in range(cols)] for j in range (rows)] 
        self.layout = "_"*12 #string representation of the board

    # get the state of the board from the database by the provided game id
    def getBoard(self, gameId):
        game = Game.query.get(gameId)
        if (game != None):
            storedLayout=game.board
            self.restoreMatrix(storedLayout)
            self.layout = storedLayout
            

    def restoreMatrix(self, layout):
        rows, cols = (4, 4)
        k = 0
        if(len(self.matrix) == 0):
            self.getNewBoard()

        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                self.matrix[i][j]= layout[k]
                k+=1










