import tkinter as tk
from random import randint
from time import sleep
import pandas as pd
board = [[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]]


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
          else:
            board[x][y] = 0
        else:
          board[x][y] = 0
    
  def SaveBoard(self):
    BoardFile = open("board.txt","w")
    for x in range (10):
      row = ""
      for y in range (10):
        if board[x][y] == 0:
          row = row + str(board[x][y])
        else:
          if board[x][y].PieceColour == "w":
            if board[x][y].queen == True:
              row = row +  "W"
            else:
              row = row +  "w"
          else:
            if board[x][y].queen == True:
              row = row +  "B"
            else:
              row = row + "b"
      BoardFile.write(row + "\n")
    BoardFile.write(Game_OBJ.turn)

  def LoadSave(self):
    Game_OBJ.PieceCountW = 0
    Game_OBJ.PieceCountB = 0
    row = 0
    BoardFile = open("board.txt","r")
    for line in BoardFile:
      column = 0
      if line == 'w' or line =='b':
        if line == 'w':
          Game_OBJ.turn = 'w'
          GUI_OBJ.DisplayTurn('White')
        else:
          Game_OBJ.turn = 'b'
          GUI_OBJ.DisplayTurn('Black')
      else:
        for char in line.strip():
          if char == '0':
            board[row][column] = 0
          elif char.lower() == 'w' or char.lower() == 'b':
            if char == char.lower():
              board[row][column] = self.piece(char.lower(),False)
            else:
              board[row][column] = self.piece(char.lower(),True)
            if char.lower() == 'w':
              Game_OBJ.PieceCountW += 1
            elif char.lower() == 'b':
              Game_OBJ.PieceCountB += 1
          column += 1
        row += 1
    GUI.displayBoard(GUI_OBJ)
    GUI.displayScores(GUI_OBJ)

class Controller:
  def __init__(self):
    self.MorT = ""
    self.multimove = False

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
    #updating only the tiles changed
    GUI.updateTile(GUI_OBJ, CurrentX, CurrentY)
    GUI.updateTile(GUI_OBJ, CurrentX+x, CurrentY+y)
    if self.MorT == 'T':
      GUI.updateTile(GUI_OBJ, CurrentX+int(x/2), CurrentY+int(y/2))

    UL = self.CheckTakePossible(CurrentX+x,CurrentY+y, 'UL')
    UR = self.CheckTakePossible(CurrentX+x,CurrentY+y, 'UR')
    DL = self.CheckTakePossible(CurrentX+x,CurrentY+y, 'DL')
    DR = self.CheckTakePossible(CurrentX+x,CurrentY+y, 'DR')
    
    if (not DL and not DR and not UL and not UR) or self.MorT != 'T':
      GUI.displayButtons(GUI_OBJ,False,False,False,False)
      if self.multimove == True:
        GUI.displayBoard(GUI_OBJ)
        self.multimove = False
      if Game_OBJ.turn == "w":
        Game_OBJ.turnChange()
      elif Game_OBJ.turn == "b":
        Game_OBJ.turnChange()
      GUI.MorT_Switch(GUI_OBJ)
    else:
      GUI.updateXY(GUI_OBJ, CurrentX+x, CurrentY+y)
      GUI.displayButtons(GUI_OBJ,UL,UR,DL,DR)
      GUI.disableMorT(GUI_OBJ)
      if self.multimove == False:
        GUI.disableBoard(GUI_OBJ)
      self.multimove = True
    
    Game_OBJ.WinCheck()
      

  def ValidateMove(self,CurrentX,CurrentY,Direction):
    valid = False 
    if board[CurrentX][CurrentY] == 0:
      valid = False 
    elif board[CurrentX][CurrentY].PieceColour.lower() != Game_OBJ.turn:
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
    
    if Game_OBJ.turn == "w":
      Game_OBJ.PieceCountB -= 1 
    else:
      Game_OBJ.PieceCountW -= 1 
    GUI_OBJ.displayScores()

  def QueenCheck(self,CurrentX, CurrentY):
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
    self.WhiteTile = tk.PhotoImage(file='Icons/WhiteTile.png')
    self.BlackTile = tk.PhotoImage(file='Icons/BlackTile.png')
    self.WhitePiece = tk.PhotoImage(file='Icons/WhitePiece.png')
    self.BlackPiece = tk.PhotoImage(file='Icons/BlackPiece.png')
    self.WhiteQueen = tk.PhotoImage(file='Icons/WhiteQueen.png')
    self.BlackQueen = tk.PhotoImage(file='Icons/BlackQueen.png')
    self.ROW = 0
    self.COLUMN = 0
    
  def displayBoard(self):
    def click(row,column):
      Controller.findMoves(Controller_OBJ,row,column)
      self.ROW = row
      self.COLUMN = column
    
    for row in range(10):
      for column in range(10):
        self.updateTile(row,column)

  def updateTile(self, row, column):
    def click(row,column):
      Controller.findMoves(Controller_OBJ,row,column)
      self.ROW = row
      self.COLUMN = column
    
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
        tk.Button(self.canvas, image=self.BlackTile, relief= 'sunken').grid(row=row,column=column)
      else:
        tk.Button(self.canvas, image=self.WhiteTile, relief= 'sunken').grid(row=row,column=column)
    tk.Label(self.canvas, text='    ').grid(row=5,column=10)
    tk.Label(self.canvas, text='    ').grid(row=5,column=15)
  
  def displayButtons(self, UpLeft, UpRight, DownLeft, DownRight):
    if UpLeft:
      tk.Button(self.canvas, bg= 'green', text= '↖', command=lambda:Controller_OBJ.MovePiece(self.ROW, self.COLUMN, 'UL')).grid(row=4,column=12)
    else:
      tk.Button(self.canvas, bg= 'grey', text= '↖', state= tk.DISABLED).grid(row=4,column=12)
    if UpRight:
      tk.Button(self.canvas, bg= 'green', text= '↗', command=lambda:Controller_OBJ.MovePiece(self.ROW, self.COLUMN, 'UR')).grid(row=4,column=14)
    else:
      tk.Button(self.canvas, bg= 'grey', text= '↗', state= tk.DISABLED).grid(row=4,column=14)
    if DownLeft:
      tk.Button(self.canvas, bg= 'green', text= '↙', command=lambda:Controller_OBJ.MovePiece(self.ROW, self.COLUMN, 'DL')).grid(row=6,column=12)
    else:
      tk.Button(self.canvas, bg= 'grey', text= '↙', state= tk.DISABLED).grid(row=6,column=12)
    if DownRight:
      tk.Button(self.canvas, bg= 'green', text= '↘', command=lambda:Controller_OBJ.MovePiece(self.ROW, self.COLUMN, 'DR')).grid(row=6,column=14)
    else:
      tk.Button(self.canvas, bg= 'grey', text= '↘', state= tk.DISABLED).grid(row=6,column=14)

  def MorT_Switch(self):
    #Mort Switch
    def switch():
      # Determine is on or off
      if Controller_OBJ.MorT == 'M':
        tk.Button(self.canvas, bg= 'red', text= 'Take', command= switch).grid(row=5,column=13)
        Controller_OBJ.MorT = 'T'
      else:
        tk.Button(self.canvas, bg= 'blue', text= 'Move', command= switch).grid(row=5,column=13)
        Controller_OBJ.MorT = 'M'
      self.displayButtons(False,False,False,False)
    tk.Button(self.canvas, bg= 'blue', text= 'Move', command= switch).grid(row=5,column=13)
    Controller_OBJ.MorT = 'M'

  def disableMorT(self):
    tk.Button(self.canvas, bg= 'red', text= 'Take', relief= 'sunken').grid(row=5,column=13)

  def SaveLoadButtons(self):
    tk.Button(self.canvas, bg= 'red', text= 'Save', command=lambda:Board.SaveBoard(Board_OBJ)).grid(row=9,column=13)
    tk.Button(self.canvas, bg= 'red', text= 'Load', command=lambda:Board.LoadSave(Board_OBJ)).grid(row=8,column=13)
  
  def disableBoard(self):
    for row in range(10):
      for column in range(10):
        if board[row][column] != 0:
          if board[row][column].PieceColour == 'w':
            if board[row][column].queen == False:
              tk.Button(self.canvas, image=self.WhitePiece, relief= 'sunken').grid(row=row,column=column)
            else:
              tk.Button(self.canvas, image=self.WhiteQueen, relief= 'sunken').grid(row=row,column=column)
          else:
            if board[row][column].queen == False:
              tk.Button(self.canvas, image=self.BlackPiece, relief= 'sunken').grid(row=row,column=column)
            else:
              tk.Button(self.canvas, image=self.BlackQueen, relief= 'sunken').grid(row=row,column=column)
        else:
          if (row+column)%2 == 0:
            tk.Button(self.canvas, image=self.BlackTile,relief= 'sunken').grid(row=row,column=column)
          else:
            tk.Button(self.canvas, image=self.WhiteTile,relief= 'sunken').grid(row=row,column=column)

  def updateXY(self, newROW, newCOLUMN):
    self.ROW = newROW
    self.COLUMN = newCOLUMN
  
  def DisplayTurn(self, turn):
    tk.Label(self.canvas, text=turn).grid(row=3,column=13)

  def ClearScreen(self):
    self.canvas.destroy()
    self.canvas = tk.Canvas(self.window, width=600, height=400)
    self.canvas.grid()

  def displayScores(self):
    tk.Label(self.canvas, text=f'W : {Game_OBJ.PieceCountW} ').grid(row=0,column=13)
    tk.Label(self.canvas, text=f'B : {Game_OBJ.PieceCountB} ').grid(row=1,column=13)
  
  def WinScreen(self, winner):
    def click():
      self.ClearScreen()
      self.Menu()
    self.ClearScreen()
    tk.Label(self.canvas, text=f'{winner} is the Winner !!!', font=("Times New Roman", 25)).grid(row=1,column=1, padx = 50, pady = 140)
    tk.Button(self.canvas, text='Menu', command=click, bg='green').grid(row=2,column=1)

  def Menu(self):
    def PVP():
      self.ClearScreen()
      Game_OBJ.PVP()
    def PVE():
      self.ClearScreen()
      Game_OBJ.PVE()
    def EVE():
      self.ClearScreen()
      Game_OBJ.EVE()
    def Leaderbaord():
      print(Accounts_OBJ.df)
    tk.Button(self.canvas, bg= 'green', text= '   PVP   ', command= PVP).grid(row=0,column=0, padx = 50, pady = 5)
    tk.Button(self.canvas, bg= 'blue', text= '   PVE   ', command= PVE).grid(row=1,column=0, padx = 50, pady = 5)
    tk.Button(self.canvas, bg= 'red', text= '   EVE   ', command= EVE).grid(row=2,column=0, padx = 50, pady = 5)
    tk.Button(self.canvas, bg= 'red', text= 'Leaderboard', command= Leaderbaord).grid(row=3,column=0, padx = 50, pady = 5)
    
    tk.mainloop()
    
  def InputAccounts(self,players):
    WhiteAccount=tk.StringVar()
    BlackAccount=tk.StringVar()
    def click():
      WAccount = WhiteAccount.get()
      BAccount = BlackAccount.get()
      Game_OBJ.WhiteAccount = WAccount
      Game_OBJ.BlackAccount = BAccount
      self.canvas.quit()
      self.ClearScreen()
    if players ==2:
      tk.Label(self.canvas,text='White').grid(row=0,column=0)
      tk.Entry(self.canvas,textvariable=WhiteAccount).grid(row=0,column=1)
      tk.Label(self.canvas,text='Black').grid(row=1,column=0)
      tk.Entry(self.canvas,textvariable=BlackAccount).grid(row=1,column=1)
      tk.Button(self.canvas,text='Start Game', command=click).grid(row=3,column=0)
      tk.mainloop()
    elif players ==1:
      tk.Label(self.canvas,text='White').grid(row=0,column=0)
      tk.Entry(self.canvas, text= 'White',textvariable=WhiteAccount).grid(row=0,column=1)
      tk.Button(self.canvas,text='Start Game', command=click).grid(row=3,column=0)
      tk.mainloop()

class AI(Controller):
  def __init__(self, colour):
    Controller.__init__(self)
    self.BestX = []
    self.BestY = []
    self.BestMove = []
    self.moves = ['UL', 'UR', 'DL', 'DR']
    self.bestMorT = 'M'
    self.colour = colour

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
    #updating only the tiles changed
    GUI.updateTile(GUI_OBJ, CurrentX, CurrentY)
    GUI.updateTile(GUI_OBJ, CurrentX+x, CurrentY+y)
    if self.MorT == 'T':
      GUI.updateTile(GUI_OBJ, CurrentX+int(x/2), CurrentY+int(y/2))

    UL = self.CheckTakePossible(CurrentX+x,CurrentY+y, 'UL')
    UR = self.CheckTakePossible(CurrentX+x,CurrentY+y, 'UR')
    DL = self.CheckTakePossible(CurrentX+x,CurrentY+y, 'DL')
    DR = self.CheckTakePossible(CurrentX+x,CurrentY+y, 'DR')
    
    if (not DL and not DR and not UL and not UR) or self.MorT != 'T':
      GUI.displayButtons(GUI_OBJ,False,False,False,False)
      if Game_OBJ.turn == "w":
        Game_OBJ.turnChange()
      elif Game_OBJ.turn == "b":
        Game_OBJ.turnChange()
      GUI.MorT_Switch(GUI_OBJ)
    else:
      possibleMoves = []
      if UL:
        possibleMoves.append('UL')
      if UR:
        possibleMoves.append('UR')
      if DL:
        possibleMoves.append('DL')
      if DR:
        possibleMoves.append('DR')
      rand = randint(0,(len(possibleMoves)-1))
      move = possibleMoves[rand]
      self.MovePiece(CurrentX+x,CurrentY+y,move)
      
    Game_OBJ.WinCheck()

  
  def MakeMove(self):
    self.BestX = []
    self.BestY = []
    self.BestMove = []
    self.moves = ['UL', 'UR', 'DL', 'DR']
    self.bestMorT = 'M'
    if self.colour == Game_OBJ.turn:
      for row in range(10):
        for column in range(10):
          if board[row][column] != 0:
            if board[row][column].PieceColour == Game_OBJ.turn:
              for move in self.moves:
                self.MorT = 'M'
                if self.ValidateMove(row,column,move) == True and self.bestMorT == 'M':
                  if self.bestMorT == 'M':
                    self.BestX.append(row)
                    self.BestY.append(column)
                    self.BestMove.append(move)
                else:
                  self.MorT = 'T'
                  if self.ValidateMove(row,column,move) == True:
                    if self.bestMorT == 'M':
                      self.BestX = [row]
                      self.BestY = [column]
                      self.BestMove = [move]
                      self.bestMorT = 'T'
                    else:
                      self.BestX.append(row)
                      self.BestY.append(column)
                      self.BestMove.append(move)
                    
  
      #randomize if there are multiple possible moves
      rand = randint(0, (len(self.BestX)-1))
      self.BestX = self.BestX[rand]
      self.BestY = self.BestY[rand]
      self.BestMove = self.BestMove[rand]
      
      self.MorT = self.bestMorT
      self.MovePiece(self.BestX, self.BestY, self.BestMove)
        


class Game:
  def __init__(self):
    self.PieceCountW = 20
    self.PieceCountB = 20
    self.turn = "w"
    self.AICount = 0
    self.WhiteAccount = ''
    self.BlackAccount = ''

  def WinCheck(self):
    if Game_OBJ.PieceCountB == 0:
      GUI.WinScreen(GUI_OBJ, 'White')
      Accounts_OBJ.AddWin(self.WhiteAccount)
      Accounts_OBJ.AddLoss(self.BlackAccount)
    elif Game_OBJ.PieceCountW == 0:
      GUI.WinScreen(GUI_OBJ, 'Black')
      Accounts_OBJ.AddWin(self.BlackAccount)
      Accounts_OBJ.AddLoss(self.WhiteAccount)

  def turnChange(self):
    if self.turn == "w":
      self.turn = "b"
      GUI.DisplayTurn(GUI_OBJ, 'Black')
    elif self.turn == "b":
      self.turn = "w"
      GUI.DisplayTurn(GUI_OBJ, 'White')
    if self.AICount > 0 and Game_OBJ.PieceCountB > 0:
      AI_OBJ.MakeMove()
    if self.AICount > 1 and Game_OBJ.PieceCountW > 0:
      AI_OBJ2.MakeMove()

  def setup(self):
    GUI_OBJ.DisplayTurn('White')
    GUI_OBJ.displayBoard()
    GUI_OBJ.displayScores()
    GUI_OBJ.displayButtons(False,False,False,False)
    GUI_OBJ.SaveLoadButtons()
    GUI_OBJ.MorT_Switch()

  def PVP(self):
    global Board_OBJ
    global Controller_OBJ
    Board_OBJ = Board()
    Controller_OBJ = Controller()

    GUI_OBJ.InputAccounts(2)
    if Accounts_OBJ.FindAccount(self.WhiteAccount) == -1:
      Accounts_OBJ.AddAccount(self.WhiteAccount)
    if Accounts_OBJ.FindAccount(self.BlackAccount) == -1:
      Accounts_OBJ.AddAccount(self.BlackAccount)
    
    self.setup()
    
    tk.mainloop()

  def PVE(self):
    global Board_OBJ
    global Controller_OBJ
    global AI_OBJ
    Board_OBJ = Board()
    Controller_OBJ = Controller()
    AI_OBJ = AI('b')
    self.AICount = 1
    
    GUI_OBJ.InputAccounts(1)
    self.BlackAccount = 'AI'
    
    if Accounts_OBJ.FindAccount(self.WhiteAccount) == -1:
      Accounts_OBJ.AddAccount(self.WhiteAccount)
    self.setup()

    tk.mainloop()

  def EVE(self):
    global Board_OBJ
    global Controller_OBJ
    global AI_OBJ
    global AI_OBJ2
    Board_OBJ = Board()
    Controller_OBJ = Controller()
    AI_OBJ = AI('b')
    AI_OBJ2 = AI('w')

    self.AICount = 2
    self.WhiteAccount = 'AI'
    self.BlackAccount = 'AI'
    
    AI_OBJ2.MakeMove()
    
    self.setup()

    tk.mainloop()
class Accounts:
  def __init__(self):
    self.PATH = 'accounts.csv'
    self.df = pd.read_csv(self.PATH)
  def AddAccount(self,NewName):
    NewRow = [NewName, 0, 0, 0]
    self.df.loc[len(self.df)] = NewRow
    self.SaveToCSV()
  
  def FindAccount(self,Name):
    Found = False
    for i in range(len(self.df)):
      tempName = self.df.loc[i,'name']
      if tempName == Name:
        Found = True
        break
    if Found == False:
      i = -1
    return(i)
  
  def SaveToCSV(self):
    self.df.to_csv(self.PATH, index=False)
  def AddWin(self,Name):
    i = self.FindAccount(Name)
    if i != -1:
      self.df.loc[i,'games'] = self.df.loc[i,'games'] + 1
      self.df.loc[i,'wins'] = self.df.loc[i,'wins'] + 1
    self.SaveToCSV()
  def AddLoss(self,Name):
    i = self.FindAccount(Name)
    if i != -1:
      self.df.loc[i,'games'] = self.df.loc[i,'games'] + 1
      self.df.loc[i,'losses'] = self.df.loc[i,'losses'] + 1
    self.SaveToCSV()

Accounts_OBJ = Accounts()
Game_OBJ = Game()
GUI_OBJ = GUI()

GUI_OBJ.Menu()