class Board:

    def __init__(self):
        self.board = [0 for _ in range(9)]
        self.winner = None

    def place(self, pos:int, player:int):
        self.board[pos] = player
        self.check_winner()

    def get_board(self):
        return self.board

    def check_winner(self):
        b = self.board
        winPositions = [(b[0], b[1], b[2]), (b[3], b[4], b[5]), (b[6], b[7], b[8]), (b[0], b[3], b[6]), (b[1], b[4], b[7]), (b[2], b[5], b[8]), (b[0], b[4], b[8]), (b[2], b[4], b[6])]
        
        if len(list(filter(lambda x : x != 0, self.board))) == 9:
            self.winner = 2

        for position in winPositions:
            if sum(position) == -3:
                self.winner = -1
            if sum(position) == 3:
                self.winner = 1

    def get_winner(self):
        return self.winner
    
class Game:

    def __init__(self):
        self.running = True
        self.player = 1
        self.mainBoard = Board()
        self.boards = [Board() for _ in range(9)]
        self.activeBoards = list(range(9))

    def place(self, boardIndex, posIndex):
        board = self.boards[boardIndex]
        board.place(posIndex, self.player)
        if board.get_winner() is not None:
            self.mainBoard.place(boardIndex, board.get_winner())
        if self.mainBoard.get_winner() is not None:
            self.running = False
            self.activeBoards.clear()
            return
        if self.mainBoard.get_board()[posIndex] != 0:
            self.activeBoards = []
            for i in range(9):
                if self.boards[i].get_winner() is None:
                    self.activeBoards.append(i)
            #self.activeBoards = list(filter(lambda x : x is not None, [i if self.boards[i].get_winner() is None else None for i in range(9)]))
        else:
            self.activeBoards = [posIndex]
        self.player *= -1

    def get_active_boards(self):
        return self.activeBoards
        