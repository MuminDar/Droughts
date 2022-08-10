board = [[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]]

class Board:    
  class piece:
    def __init__(self,colour):
      self.PieceColour = colour
      self.queen = False
  
  def __init__(self):
    for x in range (10):
      for y in range(10):
        if (x+y)% 2 == 0:
          if x<=3:
            board[x][y] = self.piece("w")
          elif x>=6:
            board[x][y] = self.piece("b")
    
  def SaveBoard(self):
    BoardFile = open("board.txt","w")
    for x in range (10):
      row = ""
      for y in range (10):
        if board[x][y] == 0:
          row = row + str(board[x][y])
        else:
          if board[x][y].PieceColour == "w":
            row = row +  "w"
          else:
            row = row + "b"
      BoardFile.write(row + "\n")
  
  def QueenCheck (self,CurrentX, CurrentY):
    if board[CurrentX][CurrentY].PieceColour == "w" and CurrentX == 0: 
      board[CurrentX][CurrentY].queen == True 
    elif board[CurrentX][CurrentY].PieceColour == "b" and CurrentX == 9: 
      board[CurrentX][CurrentY].queen == True


class GUI:
  def DisplayBoard(self):
    for x in range (10):
      row = ""
      for y in range (10):
        if board[x][y] == 0:
          if (x+y)% 2 == 0:
            row = row + " " + "■"
          else:
            row = row + " " + "□"
        else:
          if board[x][y].PieceColour == "w":
            if board[x][y].queen == False:
              row = row + " " + "w"
            else:
              row = row + " " + "W"
          else:
            if board[x][y].queen == False:
              row = row + " " + "b"
            else:
              row = row + " " + "B"
      print(row)


class Controller:
  def MovePiece(self,CurrentX,CurrentY,Direction):
    x = 0
    y = 0
    if Direction[0] == "D":
      x = 1
    else:
      x = -1
    if Direction[1] == "R":
      y = 1
    else: 
      y = -1 
    temp = board[CurrentX][CurrentY]
    board[CurrentX+x][CurrentY+y] = temp
    board[CurrentX][CurrentY] = 0

  
  def ValidateMove(self,CurrentX,CurrentY,Direction):
    if board[CurrentX][CurrentY] == 0:
      return(False)
    else:
      if board[CurrentX][CurrentY].PieceColour == "b" or board[CurrentX][CurrentY].queen == True:
        if CurrentY != 0 and CurrentX != 0 and Direction == "UpLeft" and board[CurrentX-1][CurrentY-1] == 0:
          return(True)
        if CurrentY != 9 and CurrentX != 0 and Direction == "UpRight" and board[CurrentX-1][CurrentY+1] == 0:
          return(True)
      if board[CurrentX][CurrentY].PieceColour == "w" or board[CurrentX][CurrentY].queen == True:
        if CurrentY != 0 and CurrentX != 9 and Direction == "DownLeft" and board[CurrentX+1][CurrentY-1] == 0:
          return(True)
        if CurrentY != 9 and CurrentX != 9 and Direction == "DownRight" and board[CurrentX+1][CurrentY+1] == 0:
          return(True)
    return(False)
  
  def findMoves(self,CurrentX,CurrentY):
    if CurrentX > 9 or CurrentY > 9:
      print("Coordintes out of range")
      return False
    else:
      UpLeft = self.ValidateMove(CurrentX,CurrentY,"UpLeft")
      UpRight = self.ValidateMove(CurrentX,CurrentY,"UpRight")
      DownLeft = self.ValidateMove(CurrentX,CurrentY,"DownLeft")
      DownRight = self.ValidateMove(CurrentX,CurrentY,"DownRight")
    
      ValidMove = False
      NoMove = False
      
      while ValidMove == False and NoMove == False:
        if UpLeft:
          print("Up Left (UL)")
        if UpRight:
          print("Up Right (UR)")
        if DownLeft:
          print("Down Left (DL)")
        if DownRight:
          print("Down Right (DR)")
        if not UpLeft and not UpRight and not DownLeft and not DownRight:
          print("This peice can not move")
          NoMove = True
          
        else:
          Move = input("Type your Move Here: ").upper()
          if Move == "UL" and not UpLeft:
            print("Invalid Choice, Cant Move there.")
          elif Move == "UR" and not UpRight:
            print("Invalid Choice, Cant Move there.")
          elif Move == "DL" and not DownLeft:
            print("Invalid Choice, Cant Move there.")
          elif Move == "DR"and not DownLeft:
            print("Invalid Choice, Cant Move there.")
          elif Move not in ["UL","UR","DL","DR"]:
            print("Invlaid Input")
          else:
            self.MovePiece(CurrentX, CurrentY, Move)
            ValidMove = True

      return ValidMove


Board_OBJ = Board()
GUI_OBJ = GUI()
Controller_OBJ = Controller()

GUI_OBJ.DisplayBoard()

turn = "w" 

loop = True
while loop:
  print("Turn: ", turn)
  X = int(input("what X position: "))
  if X == -1 :
    loop = False
  else:
    Y = int(input("what Y position: "))
    if board[X][Y] == 0 :
      X = int(input("what X position: "))
      Y = int(input("what Y position: "))
    elif board[X][Y].PieceColour == turn:
      ValidMove = Controller_OBJ.findMoves(X,Y)
      GUI_OBJ.DisplayBoard()
      Board_OBJ.SaveBoard()
      if turn == "w" and ValidMove:
        turn = "b"
      elif turn == "b" and ValidMove:
        turn = "w"

#commented