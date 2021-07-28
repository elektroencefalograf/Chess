class GameState():
    def __init__(self):
        self.board = [['BR', 'BN', 'BB', 'BQ', 'BK', 'BB', 'BN', 'BR'],
                      ['BP', 'BP', 'BP', 'BP', 'BP', 'BP', 'BP', 'BP'],
                      ['--', '--', '--', '--', '--', '--', '--', '--'],
                      ['--', '--', '--', '--', '--', '--', '--', '--'],
                      ['--', '--', '--', '--', '--', '--', '--', '--'],
                      ['--', '--', '--', '--', '--', '--', '--', '--'],
                      ['WP', 'WP', 'WP', 'WP', 'WP', 'WP', 'WP', 'WP'],
                      ['WR', 'WN', 'WB', 'WQ', 'WK', 'WB', 'WN', 'WR']
                      ]
        self.whiteToStart = True
        self.moveLog = []
        self.WhiteKing = (7, 4)
        self.BlackKing = (0, 4)
        self.CheckMate = False
        self.StaleMate = False
        self.PEnpassant = ()
        self.CastlingPassible = Castling(True,True,True,True)
        self.CastlingLog = [Castling(self.CastlingPassible.WhiteKS, self.CastlingPassible.WhiteQS,
                                     self.CastlingPassible.BlackKS,self.CastlingPassible.BlackQS)]
        self.AllMoveFunctions = {'P': self.getPawnMove, 'R': self.getRookMove, 'N': self.getKnightMove,
                                 'B': self.getBishopMove, 'Q': self.getQueenMove, 'K': self.getKingMove}
    def makeMove(self, move):
        self.board[move.startRow][move.startColl] = '--'
        self.board[move.secondRow][move.secondColl] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToStart = not self.whiteToStart
        if move.pieceMoved == 'WK':
            self.WhiteKing = (move.secondRow, move.secondColl)
        elif move.pieceMoved == 'BK':
            self.BlackKing = (move.secondRow, move.secondColl)

        if move.promotion:
            self.board[move.secondRow][move.secondColl] = move.pieceMoved[0] + 'Q'

        if move.enpassant:
            self.board[move.startRow][move.secondColl] = '--'
        if move.pieceMoved[1] == 'P' and abs(move.startRow - move.secondRow) == 2:
            self.PEnpassant = ((move.startRow + move.secondRow)//2, move.startColl)
        else:
            self.PEnpassant = ()

        if move.castle:
            if move.secondColl - move.startColl == 2: #kingside
                self.board[move.secondRow][move.secondColl - 1] = self.board[move.secondRow][move.secondColl + 1]
                self.board[move.secondRow][move.secondColl + 1] = '--'
            else: #queen side
                self.board[move.secondRow][move.secondColl + 1] = self.board[move.secondRow][move.secondColl - 2]
                self.board[move.secondRow][move.secondColl - 2] = '--'
        self.CastlingRights(move)
        self.CastlingLog.append(Castling(self.CastlingPassible.WhiteKS, self.CastlingPassible.WhiteQS,
                                     self.CastlingPassible.BlackKS,self.CastlingPassible.BlackQS))


    def undo(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startColl] = move.pieceMoved
            self.board[move.secondRow][move.secondColl] = move.pieceCaptured
            self.whiteToStart = not self.whiteToStart
            if move.pieceMoved == 'WK':
                self.WhiteKing = (move.startRow, move.startColl)
            elif move.pieceMoved == 'BK':
                self.BlackKing = (move.startRow, move.startColl)

            if move.enpassant:
                self.board[move.secondRow][move.secondColl] = '--'
                self.board[move.startRow][move.secondColl] = move.pieceCaptured
                self.PEnpassant = (move.secondRow, move.secondColl)

            if move.pieceMoved[1] == 'P' and abs(move.startRow - move.secondRow) == 2:
                self.PEnpassant = ()

            self.StaleMate = False
            self.CheckMate = False

            self.CastlingLog.pop()
            self.CastlingPassible.WhiteKS = self.CastlingLog[-1].WhiteKS
            self.CastlingPassible.WhiteQS = self.CastlingLog[-1].WhiteQS
            self.CastlingPassible.BlackKS = self.CastlingLog[-1].BlackKS
            self.CastlingPassible.BlackQS = self.CastlingLog[-1].BlackQS

            if move.castle:
                if move.secondColl - move.startColl == 2:
                    self.board[move.secondRow][move.secondColl + 1] = self.board[move.secondRow][move.secondColl - 1]
                    self.board[move.secondRow][move.secondColl - 1] = '--'
                else:
                    self.board[move.secondRow][move.secondColl - 2] = self.board[move.secondRow][move.secondColl + 1]
                    self.board[move.secondRow][move.secondColl + 1] = '--'


    def CastlingRights(self,move):
        if move.pieceMoved == 'WK':
            self.CastlingPassible.WhiteKS = False
            self.CastlingPassible.WhiteQS = False
        elif move.pieceMoved == 'BK':
            self.CastlingPassible.BlackKS = False
            self.CastlingPassible.BlackQS = False
        elif move.pieceMoved == 'WR':
            if move.startRow == 7:
                if move.startColl == 0:
                    self.CastlingPassible.WhiteQS = False
                elif move.startColl == 7:
                    self.CastlingPassible.WhiteKS = False
        elif move.pieceMoved == 'BR':
            if move.startRow == 0:
                if move.startColl == 0:
                    self.CastlingPassible.BlackQS = False
                elif move.startColl == 7:
                    self.CastlingPassible.BlackKS = False

    def all_moves(self):
        moves = []
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                turn = self.board[i][j][0]
                if(turn == 'W' and self.whiteToStart) or (turn == 'B' and not self.whiteToStart):
                    piece = self.board[i][j][1]
                    self.AllMoveFunctions[piece](i, j, moves)
        return moves

    def getKingMove(self, row, coll, moves):
        direction = ((-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (0, -1), (1, 0), (0, 1))
        color = 'W' if self.whiteToStart else 'B'
        for i in range(8):
            secondRow = row + direction[i][0]
            secondColl = coll + direction[i][1]
            if 0 <= secondRow < 8 and 0 <= secondColl < 8:
                endPiece = self.board[secondRow][secondColl]
                if endPiece[0] != color:
                    moves.append(Move((row, coll), (secondRow, secondColl), self.board))

    def getCastling(self, row, coll, moves):
        if self.KAttacked(row, coll):
            return
        if (self.whiteToStart and self.CastlingPassible.WhiteKS) or (not self.whiteToStart and self.CastlingPassible.BlackKS):
            self.getKingSide(row, coll, moves)
        if (self.whiteToStart and self.CastlingPassible.WhiteQS) or (not self.whiteToStart and self.CastlingPassible.BlackQS):
            self.getQueenSide(row, coll, moves)


    def getKingSide(self,row,coll,moves):
        if self.board[row][coll + 1] == '--' and self.board[row][coll + 2] == '--':
            if not self.KAttacked(row,coll + 1) and not self.KAttacked(row,coll +2):
                moves.append(Move((row,coll),(row, coll + 2 ),self.board,castle=True))

    def getQueenSide(self,row,coll,moves):
        if self.board[row][coll-1] == '--' and self.board[row][coll-2] == '--' and self.board[row][coll-3] == '--':
            if not self.KAttacked(row,coll-1) and not self.KAttacked(row, coll-2):
                moves.append(Move((row,coll),(row, coll-2),self.board, castle=True))


    def getQueenMove(self, row, coll, moves):
        direction = ((-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (0, -1), (1, 0), (0, 1))
        color = 'B' if self.whiteToStart else 'W'
        for d in direction:
            for i in range(1, 8):
                secondRow = row + d[0] * i
                secondColl= coll + d[1] * i
                if 0 <= secondRow < 8 and 0 <= secondColl < 8:
                    endPiece = self.board[secondRow][secondColl]
                    if endPiece == '--':
                        moves.append(Move((row, coll), (secondRow, secondColl), self.board))
                    elif endPiece[0] == color:
                        moves.append(Move((row, coll), (secondRow, secondColl), self.board))
                        break
                    else:
                        break
                else:
                    break

    def getBishopMove(self, row, coll, moves):
        direction = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        color = 'B' if self.whiteToStart else 'W'
        for d in direction:
            for i in range(1,8):
                secondRow = row + d[0] * i
                secondColl= coll + d[1] * i
                if 0 <= secondRow < 8 and 0 <= secondColl < 8:
                    endPiece = self.board[secondRow][secondColl]
                    if endPiece == '--':
                        moves.append(Move((row,coll),(secondRow,secondColl), self.board))
                    elif endPiece[0] == color:
                        moves.append(Move((row,coll), (secondRow, secondColl), self.board))
                        break
                    else:
                        break
                else:
                    break

    def getKnightMove(self, row, coll, moves):
        Ls = ((-2, -1), (-2, 1), (2, 1), (2, -1), (1, -2), (1, 2), (-1, -2), (-1, 2))
        color = 'W'if self.whiteToStart else 'B'
        for l in Ls:
            secondRow = row + l[0]
            secondColl = coll + l[1]
            if 0 <= secondRow < 8 and 0 <= secondColl < 8:
                endPiece = self.board[secondRow][secondColl]
                if endPiece[0] != color:
                    moves.append(Move((row, coll), (secondRow, secondColl), self.board))


    def getRookMove(self, row, coll, moves):
        direction = ((-1, 0), (0, -1), (1, 0), (0, 1))
        color = 'B' if self.whiteToStart else 'W'
        for d in direction:
            for i in range(1,8):
                secondRow = row + d[0] * i
                secondColl= coll + d[1] * i
                if 0 <= secondRow < 8 and 0 <= secondColl < 8:
                    endPiece = self.board[secondRow][secondColl]
                    if endPiece == '--':
                        moves.append(Move((row,coll),(secondRow,secondColl), self.board))
                    elif endPiece[0] == color:
                        moves.append(Move((row,coll), (secondRow, secondColl), self.board))
                        break
                    else:
                        break
                else:
                    break
    def getPawnMove(self, row, coll, moves):
        if self.whiteToStart:#białe zaczynają
            if self.board[row - 1][coll] == '--':
                moves.append(Move((row, coll), (row - 1, coll), self.board))
                if row == 6 and self.board[row - 2][coll] == '--':
                    moves.append(Move((row, coll), (row - 2, coll), self.board))
            if coll - 1 >= 0:#bicie w lewo
                if self.board[row - 1][coll - 1][0] == 'B':
                    moves.append(Move((row, coll), (row - 1, coll - 1), self.board))
                elif (row - 1, coll - 1) == self.PEnpassant:
                    moves.append(Move((row, coll), (row - 1, coll - 1), self.board, Empassant=True))
            if coll + 1 <= 7: #bicie w prawo
                if self.board[row - 1][coll + 1][0] == 'B':
                    moves.append(Move((row, coll), (row - 1, coll + 1), self.board))
                elif (row - 1, coll + 1) == self.PEnpassant:
                    moves.append(Move((row, coll), (row-1, coll+1), self.board, Empassant=True))
        else:#czarne sie ruszają
            if self.board[row + 1][coll] == '--':
                moves.append(Move((row, coll), (row + 1, coll), self.board))
                if row == 1 and self.board[row + 2][coll] == '--':
                   moves.append(Move((row, coll), (row + 2, coll), self.board))
            if coll - 1 >= 0:#bicie w lewo
                if self.board[row + 1][coll - 1][0] == 'W':
                    moves.append(Move((row, coll), (row + 1, coll - 1), self.board))
                elif (row + 1, coll - 1) == self.PEnpassant:
                    moves.append(Move((row,coll),(row+1,coll-1),self.board, Empassant=True))
            if coll + 1 <= 7: #bicie w prawo
                if self.board[row + 1][coll + 1][0] == 'W':
                    moves.append(Move((row, coll), (row + 1, coll + 1), self.board))
                elif (row + 1, coll + 1) == self.PEnpassant:
                    moves.append(Move((row, coll), (row + 1, coll + 1), self.board, Empassant=True))


    def getValidMove(self):
        TempEnpassant = self.PEnpassant
        tempCastling = Castling(self.CastlingPassible.WhiteKS, self.CastlingPassible.WhiteQS,
                                     self.CastlingPassible.BlackKS,self.CastlingPassible.BlackQS)
        moves = self.all_moves()
        if self.whiteToStart:
            self.getCastling(self.WhiteKing[0],self.WhiteKing[1],moves)
        else:
            self.getCastling(self.BlackKing[0],self.BlackKing[1],moves)
        for i in range(len(moves)-1, -1, -1):
            self.makeMove(moves[i])
            self.whiteToStart = not self.whiteToStart

            if self.inCheck():
                moves.remove(moves[i])
            self.whiteToStart = not self.whiteToStart
            self.undo()
        if len(moves) == 0:
            if self.inCheck():
                self.CheckMate = True
            else:
                self.StaleMate = True
        else:
            self.CheckMate = False
            self.StaleMate = False
        self.PEnpassant = TempEnpassant
        self.CastlingPassible = tempCastling
        return moves

    def inCheck(self):
        if self.whiteToStart:
            return self.KAttacked(self.WhiteKing[0], self.WhiteKing[1])
        else:
            return self.KAttacked(self.BlackKing[0], self.BlackKing[1])

    def KAttacked(self, row, coll):
        self.whiteToStart = not self.whiteToStart
        enemyMoves = self.all_moves()
        self.whiteToStart = not self.whiteToStart
        for move in enemyMoves:
            if move.secondRow == row and move.secondColl == coll:
                return True
        return False

class Move():
    ranksToRows = {'1': 7, '2': 6, '3': 5, '4': 4,
                   '5': 3, '6': 2, '7': 1, '8': 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}

    filesToCols = {'a': 0, 'b': 1, 'c': 2, 'd': 3,
                   'e': 4, 'f': 5, 'g': 6, 'h': 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, firstK, secondK, board, Empassant=False, castle=False):
        self.startRow = firstK[0]
        self.startColl = firstK[1]
        self.secondRow = secondK[0]
        self.secondColl = secondK[1]
        self.pieceMoved = board[self.startRow][self.startColl]
        self.pieceCaptured = board[self.secondRow][self.secondColl]
        self.moveNum = self.startRow * 1000 + self.startColl * 100 + self.secondRow * 10 + self.secondColl
        self.promotion = False
        if (self.pieceMoved == 'WP' and self.secondRow == 0) or (self.pieceMoved == 'BP' and self.secondRow == 7):
            self.promotion = True

        self.enpassant = Empassant
        self.castle = castle
        if self.enpassant:
            self.pieceCaptured = 'WP' if self.pieceMoved == 'BP' else 'BP'
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveNum == other.moveNum
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.secondColl) + self.getRankFile(self.secondRow, self.secondColl)

    def getRankFile(self, row, collum):
        return self.colsToFiles[collum] + self.rowsToRanks[row]
class Castling():
    def __init__(self, WhiteKS,WhiteQS,BlackKS,BlackQS):
        self.WhiteKS = WhiteKS
        self.WhiteQS = WhiteQS
        self.BlackKS = BlackKS
        self.BlackQS = BlackQS
