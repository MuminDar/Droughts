from Board import board

def MovePiece(CurrentX,CurrentY,Direction):
  if Direction == 'UL':
    temp = board[CurrentX][CurrentY]
    board[CurrentX-1][CurrentY-1] = temp
    board[CurrentX][CurrentY] = 0
  elif Direction == 'UR':
    temp = board[CurrentX][CurrentY]
    board[CurrentX-1][CurrentY+1] = temp
    board[CurrentX][CurrentY] = 0
  elif Direction == 'DL':
    temp = board[CurrentX][CurrentY]
    board[CurrentX+1][CurrentY-1] = temp
    board[CurrentX][CurrentY] = 0
  elif Direction == 'DR':
    temp = board[CurrentX][CurrentY]
    board[CurrentX+1][CurrentY+1] = temp
    board[CurrentX][CurrentY] = 0

def ValidateMove(CurrentX,CurrentY,Direction):
  if board[CurrentX][CurrentY] == 0:
    print('Incorrect Move: Not a Piece')
  else:
    if board[CurrentX][CurrentY].PieceColour == 'b' or board[CurrentX][CurrentY].queen == True:
      if Direction == 'UpLeft':
        if board[CurrentX-1][CurrentY-1] == 0:
          return(True)
        else:
          print("Invalid move")
      if Direction == 'UpRight':
        if board[CurrentX-1][CurrentY+1] == 0:
          return(True)
        else:
          print("Invalid move")
    if board[CurrentX][CurrentY].PieceColour == 'w' or board[CurrentX][CurrentY].queen == True:
      if Direction == 'DownLeft':
        if board[CurrentX+1][CurrentY-1] == 0:
          return(True)
        else:
          print("Invalid move")
      if Direction == 'DownRight':
        if board[CurrentX+1][CurrentY+1] == 0:
          return(True)
        else:
          print("Invalid move")

def findMoves(CurrentX,CurrentY):
  UpLeft = ValidateMove(CurrentX,CurrentY,'UpLeft')
  UpRight = ValidateMove(CurrentX,CurrentY,'UpRight')
  DownLeft = ValidateMove(CurrentX,CurrentY,'DownLeft')
  DownRight = ValidateMove(CurrentX,CurrentY,'DownRight')

  ValidMove = False
  
  while ValidMove == False:
    print('You can move')
    if UpLeft:
      print('Up Left (UL)')
    if UpRight:
      print('Up Right (UR)')
    if DownLeft:
      print('Down Left (DL)')
    if DownRight:
      print('Down Right (DR)')
    Move = input('Type your Move Here: ')

    if Move == 'UL' and not UpLeft:
      print('Invalid Choice, Cant Move there.')
    elif Move == 'UR' and not UpRight:
      print('Invalid Choice, Cant Move there.')
    elif Move == 'DL' and not DownLeft:
      print('Invalid Choice, Cant Move there.')
    elif Move == 'DR'and not DownLeft:
      print('Invalid Choice, Cant Move there.')
    elif Move not in ['UL','UR','DL','DR']:
      print('Invlaid Input')
    else:
      MovePiece(CurrentX, CurrentY, Move)
      ValidMove = True
      
  
  
  return UpLeft, UpRight, DownLeft, DownRight
