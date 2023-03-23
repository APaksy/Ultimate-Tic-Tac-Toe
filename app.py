import UI, game

class App:

    def __init__(self):
        self.game = game.Game()
        self.boards = []
        self.mainBoard = UI.MainBoard_UI(20, 20, 810, self.game.mainBoard)
        for i in range(3):
            for j in range(3):
                self.boards.append(UI.Board_UI(20 + j*277, 20 + i*277, 253, self.game.boards[3*i+j]))

    def mouseClick(self, pos):
        activeBoards = self.game.get_active_boards()
        for boardIndex in activeBoards:
            posIndex = self.boards[boardIndex].check_press(pos)
            if posIndex is not None:
                self.place(boardIndex, posIndex)
                return

    def place(self, boardIndex, posIndex):
        self.game.place(boardIndex, posIndex)
        activeBoards = self.game.get_active_boards()
        for i in range(9):
            if i in activeBoards:
                self.boards[i].set_active(True)
            else:
                self.boards[i].set_active(False)

    def display(self, screen):
        
        for board in self.boards:
            board.display(screen)
        self.mainBoard.display(screen)
        