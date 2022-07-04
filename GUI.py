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
          if board[x][y].queen == False:
            row = row + " " + 'w'
          else:
            row = row + " " + 'W'
        else:
          if board[x][y].queen == False:
            row = row + " " + 'b'
          else:
            row = row + " " + 'B'
    print(row)