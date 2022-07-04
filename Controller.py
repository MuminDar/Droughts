from Board import board

def MovePiece(CurrentX,CurrentY,Direction):
  if Direction == 'UpLeft':
    temp = board[CurrentX][CurrentY]
    board[CurrentX-1][CurrentY-1] = temp
    board[CurrentX][CurrentY] = 0
  elif Direction == 'UpRight':
    temp = board[CurrentX][CurrentY]
    board[CurrentX-1][CurrentY+1] = temp
    board[CurrentX][CurrentY] = 0
  elif Direction == 'DownLeft':
    temp = board[CurrentX][CurrentY]
    board[CurrentX+1][CurrentY-1] = temp
    board[CurrentX][CurrentY] = 0
  elif Direction == 'DownRight':
    temp = board[CurrentX][CurrentY]
    board[CurrentX+1][CurrentY+1] = temp
    board[CurrentX][CurrentY] = 0

def ValidateMove(CurrentX,CurrentY,Direction):
  if board[CurrentX][CurrentY] == 0:
    print('Incorrect Move: Not a Piece')
  else:
    if Direction == 'UpLeft':
      if board[CurrentX-1][CurrentY-1] == 0:
        MovePiece(CurrentX,CurrentY,Direction)
      else:
        print("Invalid move")
    if Direction == 'UpRight':
      if board[CurrentX-1][CurrentY+1] == 0:
        MovePiece(CurrentX,CurrentY,Direction)
      else:
        print("Invalid move")
    if Direction == 'DownLeft':
      if board[CurrentX+1][CurrentY-1] == 0:
        MovePiece(CurrentX,CurrentY,Direction)
      else:
        print("Invalid move")
    if Direction == 'DownRight':
      if board[CurrentX+1][CurrentY+1] == 0:
        MovePiece(CurrentX,CurrentY,Direction)
      else:
        print("Invalid move")
    
  

