import pygame as pyg
import chessStorage

Width = Height = 512
dim = 8
KSize = Height // dim
Fps = 20
Images = {}


def load_images():
    pieces = ['WP', 'BP', 'WR', 'BR', 'WB', 'BB', 'WN', 'BN', 'WQ', 'BQ', 'WK', 'BK']
    for piece in pieces:
        Images[piece] = pyg.transform.scale(pyg.image.load('chesspieces/' + piece + '.png'), (KSize, KSize))


def main():
    pyg.init()
    screen = pyg.display.set_mode((Width, Height))
    clock = pyg.time.Clock()
    screen.fill(pyg.Color('white'))
    gameState = chessStorage.GameState()
    validMoves = gameState.getValidMove()
    moveDone = False
    GameOver = False
    load_images()
    run = True
    KSelected = ()
    PlayerClick = []
    while run:
        for e in pyg.event.get():
            if e.type == pyg.QUIT:
                run = False
            elif e.type == pyg.MOUSEBUTTONDOWN:
                location = pyg.mouse.get_pos()
                coll = location[0]//KSize
                row = location[1]//KSize
                print(coll,row)
                if KSelected == (row, coll):
                    KSelected = ()
                    PlayerClick = []
                else:
                    KSelected = (row, coll)
                    PlayerClick.append(KSelected)
                if len(PlayerClick) == 2:
                    move = chessStorage.Move(PlayerClick[0], PlayerClick[1], gameState.board)
                    for i in range(len(validMoves)):
                        if move == validMoves[i]:
                            gameState.makeMove(validMoves[i])
                            moveDone = True
                            print(move.getChessNotation())
                            KSelected =()
                            PlayerClick = []
                    if not moveDone:
                        PlayerClick = [KSelected]
            elif e.type == pyg.KEYDOWN:
                if e.key == pyg.K_u:
                    gameState.undo()
                    moveDone = True
        if moveDone:
            validMoves = gameState.getValidMove()
            moveDone = False
            
            
        if gameState.CheckMate:
            GameOver = True
            if gameState.whiteToStart:
                messages(screen,'Black wins by checkmate')
            else:
                messages(screen,'White wins by checkmate')
        elif gameState.StaleMate:
            GameOver = True
            messages(screen,'Draw by stalemate')
        clock.tick(Fps)
        pyg.display.flip()
        drawGame(screen, gameState, validMoves, KSelected)
def highlightSquare(screen, gameState, validMoves, KSelected):
    if KSelected != ():
        row, coll = KSelected
        if gameState.board[row][coll][0] == ('W' if gameState.whiteToStart else 'B'):
            s = pyg.Surface((KSize, KSize))
            s.set_alpha(100)
            s.fill(pyg.Color('blue'))
            screen.blit(s, (coll * KSize, row * KSize))
            s.fill(pyg.Color('yellow'))
            for move in validMoves:
                if move.startRow == row and move.startColl == coll:
                    screen.blit(s, (move.secondColl * KSize, move.secondRow * KSize))

def drawGame(screen, gameState, validMoves, KSelected):
    drawBoard(screen)
    drawPieces(screen, gameState.board)
    highlightSquare(screen, gameState, validMoves, KSelected)

def drawBoard(screen):
    colors = [pyg.Color('white'), pyg.Color('Dark green')]
    for i in range(dim):
        for j in range(dim):
            color = colors[(i+j)%2]
            pyg.draw.rect(screen, color, pyg.Rect(j*KSize, i*KSize, KSize, KSize))

def drawPieces(screen, board):
    for i in range(dim):
        for j in range(dim):
            piece = board[i][j]
            if piece != '--':
                screen.blit(Images[piece], pyg.Rect(j*KSize, i*KSize, KSize, KSize))


def messages(screen,text):
    font = pyg.font.SysFont('Arial', 32, True, False)
    message = font.render(text, 0, pyg.Color('Black'))
    location = pyg.Rect(0,0,Width,Height).move(Width/2 - message.get_width()/2,Height/2 - message.get_height()/2)
    screen.blit(message,location)






if __name__ == '__main__':
    main()




















