board = [[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]]

class piece:
  def __init__(self,colour):
    self.PieceColour = colour
    self.queen = False

def initialise():
  for x in range (10):
    for y in range(10):
      if (x+y)% 2 == 0:
        if x<=3:
          board[x][y] = piece('w')
        elif x>=6:
          board[x][y] = piece('b')
  
def SaveBoard():
  BoardFile = open('board.txt','w')
  for x in range (10):
    row = ""
    for y in range (10):
      if board[x][y] == 0:
        row = row + " " + str(board[x][y])
      else:
        if board[x][y].PieceColour == 'w':
          row = row + " " + 'w'
        else:
          row = row + " " + 'b'
    BoardFile.write(row + "\n")