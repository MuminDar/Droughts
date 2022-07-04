import Board
import GUI
import Controller
Board.initialise()
GUI.DisplayBoard()
print('---------------------')

Controller.MovePiece(3,3,'DownRight')
GUI.DisplayBoard()

print('---------------------')

Controller.MovePiece(6,8,'UpLeft')
GUI.DisplayBoard()
Board.SaveBoard()