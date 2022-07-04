from Board import board

def DisplayBoard():
  for x in range (10):
    row = ""
    for y in range (10):
      if board[x][y] == 0:
        if (x+y)% 2 == 0:
          row = row + " " + "■"
        else:
          row = row + " " + "□"
      else:
        if board[x][y].PieceColour == 'w':
          row = row + " " + 'w'
        else:
          row = row + " " + 'b'
    print(row)