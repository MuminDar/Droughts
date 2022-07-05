import Board
import GUI
import Controller

Board.initialise()
GUI.DisplayBoard()

loop = True

while True:
  X = int(input('what X position: '))
  Y = int(input('what Y position: '))
  if X == 'STOP':
    loop = False
  Controller.findMoves(X,Y)
  GUI.DisplayBoard()
Board.SaveBoard()

#commented