import Board
import GUI
import Controller
Board.initialise()
GUI.DisplayBoard()

print('---------------------')

Controller.ValidateMove(3,3,'DownRight')
GUI.DisplayBoard()

print('---------------------')

Controller.ValidateMove(6,8,'UpLeft')
GUI.DisplayBoard()

print('---------------------')

Controller.ValidateMove(1,1,'UpLeft')
GUI.DisplayBoard()
Board.SaveBoard()

#commented