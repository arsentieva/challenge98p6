class Board:
    layout =[]

    def __init__(self, layout=[]):
        if(len(layout)== 0):
            self.getNewBoard(self)
        else :
            this.layout = layout

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

    def getBoard(self, currentLayout):
        pass