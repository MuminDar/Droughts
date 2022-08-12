board = [[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]]

# code later for counting black white pieces on load board

class Board:   
  class piece:
    def __init__(self,colour,Queen):
      self.PieceColour = colour
      self.queen = Queen
  
  def __init__(self):
    for x in range (10):
      for y in range(10):
        if (x+y)% 2 == 0:
          if x<=3:
            board[x][y] = self.piece("w",False)
          elif x>=6:
            board[x][y] = self.piece("b",False)
    
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

  def LoadSave(self):
    row = 0
    BoardFile = open("board.txt","r")
    for line in BoardFile:
      column = 0
      for char in line.strip():
        if char == '0':
          board[row][column] = 0
        elif char.lower() == 'w' or char.lower() == 'b':
          if char == char.lower():
            board[row][column] = self.piece(char.lower(),False)
          else:
            board[row][column] = self.piece(char.lower(),True)
        column += 1
      row += 1
  
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
  def __init__(self):
    self.MorT = ""
    self.PieceCountW = 20
    self.PieceCountB = 20

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
    if self.MorT == "T" :
      x = x*2
      y = y*2  
    temp = board[CurrentX][CurrentY]
    board[CurrentX+x][CurrentY+y] = temp
    board[CurrentX][CurrentY] = 0

  def ValidateMove(self,CurrentX,CurrentY,Direction):
    valid = False 
    if board[CurrentX][CurrentY] == 0:
      valid = False 
    else:
      if self.MorT == "T": 
        m = 2
      else:
        m = 1
      if board[CurrentX][CurrentY].PieceColour == "b" or board[CurrentX][CurrentY].queen == True:
        if CurrentY != 0 and CurrentX != 0 and Direction == "UpLeft" and board[CurrentX-m][CurrentY-m] == 0:    
          valid = True
        if CurrentY != 9 and CurrentX != 0 and Direction == "UpRight" and board[CurrentX-m][CurrentY+m] == 0:
          valid = True
        if self.MorT == "T":
          valid = self.CheckTakePossible(CurrentX, CurrentY, Direction)
      if board[CurrentX][CurrentY].PieceColour == "w" or board[CurrentX][CurrentY].queen == True:
        if CurrentY != 0 and CurrentX != 9 and Direction == "DownLeft" and board[CurrentX+m][CurrentY-m] == 0:
          valid = True
        if CurrentY != 9 and CurrentX != 9 and Direction == "DownRight" and board[CurrentX+m][CurrentY+m] == 0 :
          valid = True
        if self.MorT == "T":
          valid = self.CheckTakePossible(CurrentX, CurrentY, Direction)
    return valid 
  
  def findMoves(self,CurrentX,CurrentY):
    print(self.MorT)
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
          elif Move == "DR"and not DownRight:
            print("Invalid Choice, Cant Move there.")
          elif Move not in ["UL","UR","DL","DR"]:
            print("Invlaid Input")
          else:
            self.MovePiece(CurrentX, CurrentY, Move)
            ValidMove = True
            if self.MorT == "T":
              self.TakePiece(CurrentX, CurrentY, Move)
      return ValidMove
      
  def CheckTakePossible(self, CurrentX, CurrentY, Direction):
    if board[CurrentX][CurrentY].PieceColour == "b":
      if Direction == "UpLeft" and board[CurrentX-1][CurrentY-1] != 0:
        if board[CurrentX-1][CurrentY-1].PieceColour == "w":
          return True
      if Direction == "UpRight" and board[CurrentX-1][CurrentY+1] != 0:
        if board[CurrentX-1][CurrentY+1].PieceColour == "w":
          return True
      if Direction == "DownLeft" and board[CurrentX+1][CurrentY-1] != 0:
        if board[CurrentX+1][CurrentY-1].PieceColour == "w":
          return True
      if Direction == "DownRight" and board[CurrentX+1][CurrentY+1] != 0:
        if board[CurrentX+1][CurrentY+1].PieceColour == "w":
          return True
    if board[CurrentX][CurrentY].PieceColour == "w":
      if Direction == "UpLeft" and board[CurrentX-1][CurrentY-1] != 0:
        if board[CurrentX-1][CurrentY-1].PieceColour == "b":
          return True
      if Direction == "UpRight" and board[CurrentX-1][CurrentY+1] != 0:
        if board[CurrentX-1][CurrentY+1].PieceColour == "b":
          return True
      if Direction == "DownLeft" and board[CurrentX+1][CurrentY-1] != 0:
        if board[CurrentX+1][CurrentY-1].PieceColour == "b":
          return True
      if Direction == "DownRight" and board[CurrentX+1][CurrentY+1] != 0:
        if board[CurrentX+1][CurrentY+1].PieceColour == "b":
          return True
    return False
      
  def TakePiece(self, CurrentX, CurrentY, Direction):
    if Direction == "UL" :
      board[CurrentX-1][CurrentY-1] = 0
    elif Direction == "UR":
      board[CurrentX-1][CurrentY+1] = 0
    elif Direction == "DL" :
      board[CurrentX+1][CurrentY-1] = 0
    elif Direction == "DR":
      board[CurrentX+1][CurrentY+1] = 0
    
    if turn == "w":
      self.PieceCountB -= 1 
    else:
      self.PieceCountW -= 1 

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
    Controller_OBJ.MorT = input("Would you like to move or take (M/T)").upper()
    if board[X][Y] == 0 :
      X = int(input("what X position: "))
      Y = int(input("what Y position: "))
      Controller_OBJ.MorT = input("Would you like to move or take (M/T)").upper()
    elif board[X][Y].PieceColour == turn:
      ValidMove = Controller_OBJ.findMoves(X,Y)
      GUI_OBJ.DisplayBoard()
      Board_OBJ.SaveBoard()
      if turn == "w" and ValidMove:
        turn = "b"
      elif turn == "b" and ValidMove:
        turn = "w"

#commented