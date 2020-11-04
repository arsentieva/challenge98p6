from app.models import db, Game

class Board:
    matrix = []
    gameId = None
    winner = None
    layout = None

    def __init__(self, gameId=None):
        if(gameId == None):
            self.getNewBoard()
            self.layout = "_"*16 #string representation of the board
        else :
            self.layout = self.getBoard(gameId)

    def handleMove(self, columnIdx, playerSymbol ):
        if(self.isColumnFull(columnIdx) == False):

            columnToUpdate = self.matrix[columnIdx-1]
            cells = [cell for cell in columnToUpdate]
            for i in range(len(cells)):
                cell = cells[i]
                if(cell== "_"):
                    cells[i]=playerSymbol
                    break

            self.matrix[columnIdx-1] = [cell for cell in cells]
            self.layout = "".join(str(cell) for cells in self.matrix for cell in cells)
            self.checkForWinner(columnIdx)
            return True
        
        return False


    def checkForWinner(self, columnIdx):
        symbol  = self.checkColumnWin(columnIdx)
        print("return", symbol)
        if(symbol != None):
            self.winner = symbol
            return 
        
        symbol = self.checkForRowWin()
        if(symbol != None):
            self.winner = symbol
            return 

        symbol = self.checkForDiagonalWin()
        if(symbol != None):
            self.winner = symbol
            return 


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

    def checkColumnWin(self, columnIdx):
        column = self.matrix[columnIdx-1]
        print("C:" , column)
        columnSymbol = set(column[0])
        if( column[0] == "_"):
            return None

        for i in range(len(column)-1):
            symbol = column[i+1]
            print("s:" , columnSymbol)
            print("sb:" , symbol)
            if(symbol not in columnSymbol):
                return None
        
        return columnSymbol.pop()

    def checkForRowWin(self):
        row = set()
        j = 0
        while( j <= (len(self.matrix)-1)):
            for i in range(len(self.matrix)):
                symbol = self.matrix[i][j]
                row.add(symbol)
            
            if (len(row)== 1 and "_" not in row):
                return row.pop()

            j+=1
            row.clear()
        
        return None

    
    def checkForDiagonalWin(self):
        diagonal = set ()
        diagonal2 = set ()
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if(i == j):
                    diagonal.add(self.matrix[i][j])
                if(i+j == (len(self.matrix)-1)):
                    diagonal2.add(self.matrix[i][j])
        
        if (len(diagonal)== 1 and "_" not in diagonal):
                return diagonal.pop()

        if (len(diagonal2)== 1 and "_" not in diagonal2):
                return diagonal2.pop()

        return None
        











