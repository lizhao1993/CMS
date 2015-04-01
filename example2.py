from PyQt5.QtWidgets import QMainWindow
from CMS1 import Ui_MainWindow
import sys
from PyQt5.QtWidgets import (QMainWindow, QTextEdit, 
    QAction, QFileDialog, QApplication)
from PyQt5.QtGui import QIcon

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        self.ui = Ui_MainWindow()
        
        self.ui.setupUi(self)
 #       pushButton.clicked.connect(pushButton_Clicked())
#        self.initUI()
        
 #   def initUI(self):      

 #   def pushButton_Clicked(self):
 #       print ("hello")
        

           
        #self.setGeometry(300, 300, 350, 300)
        #self.setWindowTitle('File dialog')
        #self.show()
        
        
    #def showDialog(self):

    #    fname = QFileDialog.getOpenFileName()
        
     #   f = open(fname, 'r')
        
     #   with f:        
      #      data = f.read()
       #     self.textEdit.setText(data) 
                                
#if __name__ == '__main__':
    
 #   app = QApplication(sys.argv)
  #  ex = MainWindow()
   # sys.exit(app.exec_())
       
