import tkinter as tk
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

class Controller:
  def __init__(self):
    self.MorT = ""
    self.PieceCountW = 20
    self.PieceCountB = 20
    self.turn = "w"

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
      self.TakePiece(CurrentX,CurrentY,Direction)
    temp = board[CurrentX][CurrentY]
    board[CurrentX+x][CurrentY+y] = temp
    self.QueenCheck(CurrentX+x,CurrentY+y)
    board[CurrentX][CurrentY] = 0
    GUI.displayBoard(GUI_OBJ)
    GUI.displayButtons(GUI_OBJ,False,False,False,False)
    if self.turn == "w":
      self.turn = "b"
      GUI.DisplayTurn(GUI_OBJ, 'Black')
    elif self.turn == "b":
      self.turn = "w"
      GUI.DisplayTurn(GUI_OBJ, 'White')

  def ValidateMove(self,CurrentX,CurrentY,Direction):
    valid = False 
    if board[CurrentX][CurrentY] == 0:
      valid = False 
    elif board[CurrentX][CurrentY].PieceColour.lower() != self.turn:
      valid = False
    else:
      if self.MorT == "T": 
        valid = self.CheckTakePossible(CurrentX, CurrentY, Direction)
      else:
        if board[CurrentX][CurrentY].PieceColour == "b" or board[CurrentX][CurrentY].queen == True:
          if CurrentY != 0 and CurrentX != 0 and Direction == "UL" and board[CurrentX-1][CurrentY-1] == 0:    
            valid = True
          if CurrentY != 9 and CurrentX != 0 and Direction == "UR" and board[CurrentX-1][CurrentY+1] == 0:
            valid = True
        if board[CurrentX][CurrentY].PieceColour == "w" or board[CurrentX][CurrentY].queen == True:
          if CurrentY != 0 and CurrentX != 9 and Direction == "DL" and board[CurrentX+1][CurrentY-1] == 0:
            valid = True
          if CurrentY != 9 and CurrentX != 9 and Direction == "DR" and board[CurrentX+1][CurrentY+1] == 0:
            valid = True
    return valid 
  
  def findMoves(self,CurrentX,CurrentY):
    if CurrentX > 9 or CurrentY > 9:
      print("Coordintes out of range")
      return False
    else:
      UpLeft = self.ValidateMove(CurrentX,CurrentY,"UL")
      UpRight = self.ValidateMove(CurrentX,CurrentY,"UR")
      DownLeft = self.ValidateMove(CurrentX,CurrentY,"DL")
      DownRight = self.ValidateMove(CurrentX,CurrentY,"DR")
    
      GUI.displayButtons(GUI_OBJ,UpLeft,UpRight,DownLeft,DownRight)
      return True
      
  def CheckTakePossible(self, CurrentX, CurrentY, Direction):
    if Direction[0] == 'U' and (CurrentX == 0 or CurrentX == 1):
      return False
    elif Direction[0] == 'D' and (CurrentX == 9 or CurrentX == 8):
      return False
    elif Direction[1] == 'L' and (CurrentY == 0 or CurrentY == 1):
      return False
    elif Direction[1] == 'R' and (CurrentY == 9 or CurrentY == 8):
      return False
    
    if board[CurrentX][CurrentY].PieceColour == "b":
      opposite = 'w'
    elif board[CurrentX][CurrentY].PieceColour == "w":
      opposite = 'b'
    
    if board[CurrentX][CurrentY].PieceColour == "b" or board[CurrentX][CurrentY].queen == True:
      if Direction == "UL" and board[CurrentX-1][CurrentY-1] != 0 and board[CurrentX-2][CurrentY-2] == 0:
        if board[CurrentX-1][CurrentY-1].PieceColour == opposite:
          return True
      if Direction == "UR" and board[CurrentX-1][CurrentY+1] != 0 and board[CurrentX-2][CurrentY+2] == 0:
        if board[CurrentX-1][CurrentY+1].PieceColour == opposite:
          return True
    if board[CurrentX][CurrentY].PieceColour == "w" or board[CurrentX][CurrentY].queen == True:
      if Direction == "DL" and board[CurrentX+1][CurrentY-1] != 0 and board[CurrentX+2][CurrentY-2] == 0:
        if board[CurrentX+1][CurrentY-1].PieceColour == opposite:
          return True
      if Direction == "DR" and board[CurrentX+1][CurrentY+1] != 0 and board[CurrentX+2][CurrentY+2] == 0:
        if board[CurrentX+1][CurrentY+1].PieceColour == opposite:
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
    
    if self.turn == "w":
      self.PieceCountB -= 1 
    else:
      self.PieceCountW -= 1 

  def QueenCheck (self,CurrentX, CurrentY):
    if board[CurrentX][CurrentY].PieceColour == "w" and CurrentX == 9: 
      board[CurrentX][CurrentY].queen = True 
    elif board[CurrentX][CurrentY].PieceColour == "b" and CurrentX == 0: 
      board[CurrentX][CurrentY].queen = True

class GUI:
  def __init__(self):
    self.window = tk.Tk()
    self.window.title('Draughts')
    self.canvas = tk.Canvas(self.window, width=600, height=400)
    self.canvas.grid()
    self.WhiteTile = tk.PhotoImage(file='WhiteTile.png')
    self.BlackTile = tk.PhotoImage(file='BlackTile.png')
    self.WhitePiece = tk.PhotoImage(file='WhitePiece.png')
    self.BlackPiece = tk.PhotoImage(file='BlackPiece.png')
    self.WhiteQueen = tk.PhotoImage(file='WhiteQueen.png')
    self.BlackQueen = tk.PhotoImage(file='BlackQueen.png')
    self.ROW = 0
    self.COLUMN = 0
    self.is_on = True
    
  def displayBoard(self):
    def click(row,column):
      Controller.findMoves(Controller_OBJ,row,column)
      self.ROW = row
      self.COLUMN = column
    
    for row in range(10):
      for column in range(10):
        if board[row][column] != 0:
          if board[row][column].PieceColour == 'w':
            if board[row][column].queen == False:
              tk.Button(self.canvas, image=self.WhitePiece, command=lambda row=row, column=column: click(row, column)).grid(row=row,column=column)
            else:
              tk.Button(self.canvas, image=self.WhiteQueen, command=lambda row=row, column=column: click(row, column)).grid(row=row,column=column)
          else:
            if board[row][column].queen == False:
              tk.Button(self.canvas, image=self.BlackPiece, command=lambda row=row, column=column: click(row, column)).grid(row=row,column=column)
            else:
              tk.Button(self.canvas, image=self.BlackQueen, command=lambda row=row, column=column: click(row, column)).grid(row=row,column=column)
        else:
          if (row+column)%2 == 0:
            tk.Button(self.canvas, image=self.BlackTile, state=tk.DISABLED).grid(row=row,column=column)
          else:
            tk.Button(self.canvas, image=self.WhiteTile, state=tk.DISABLED).grid(row=row,column=column)
  
  def displayButtons(self, UpLeft, UpRight, DownLeft, DownRight):
    
    if UpLeft:
      tk.Button(self.canvas, bg= 'green', text= 'UL', command=lambda:Controller.MovePiece(Controller_OBJ,self.ROW, self.COLUMN, 'UL')).grid(row=4,column=12)
    else:
      tk.Button(self.canvas, bg= 'grey', text= 'UL', state= tk.DISABLED).grid(row=4,column=12)
    if UpRight:
      tk.Button(self.canvas, bg= 'green', text= 'UR', command=lambda:Controller.MovePiece(Controller_OBJ,self.ROW, self.COLUMN, 'UR')).grid(row=4,column=14)
    else:
      tk.Button(self.canvas, bg= 'grey', text= 'UR', state= tk.DISABLED).grid(row=4,column=14)
    if DownLeft:
      tk.Button(self.canvas, bg= 'green', text= 'DL', command=lambda:Controller.MovePiece(Controller_OBJ,self.ROW, self.COLUMN, 'DL')).grid(row=6,column=12)
    else:
      tk.Button(self.canvas, bg= 'grey', text= 'DL', state= tk.DISABLED).grid(row=6,column=12)
    if DownRight:
      tk.Button(self.canvas, bg= 'green', text= 'DR', command=lambda:Controller.MovePiece(Controller_OBJ,self.ROW, self.COLUMN, 'DR')).grid(row=6,column=14)
    else:
      tk.Button(self.canvas, bg= 'grey', text= 'DR', state= tk.DISABLED).grid(row=6,column=14)

  def MorT_Switch(self):
    #Mort Switch
    def switch():
      # Determine is on or off
      if self.is_on:
        self.is_on = False
        tk.Button(self.canvas, bg= 'red', text= 'Take', command= switch).grid(row=5,column=13)
        Controller_OBJ.MorT = 'T'
      else:
        self.is_on = True
        tk.Button(self.canvas, bg= 'blue', text= 'Move', command= switch).grid(row=5,column=13)
        Controller_OBJ.MorT = 'M'
      self.displayButtons(False,False,False,False)
    tk.Button(self.canvas, bg= 'blue', text= 'Move', command= switch).grid(row=5,column=13)
    Controller_OBJ.MorT = 'M'

  def DisplayTurn(self, turn):
    tk.Label(self.canvas, text=turn).grid(row=3,column=13)

Board_OBJ = Board()
GUI_OBJ = GUI()
Controller_OBJ = Controller()

GUI.DisplayTurn(GUI_OBJ, 'White')
loop = True
while loop:
  GUI_OBJ.displayBoard()
  GUI_OBJ.displayButtons(False,False,False,False)
  GUI_OBJ.MorT_Switch()
  Board_OBJ.SaveBoard()
  tk.mainloop()
#commented