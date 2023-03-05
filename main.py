import sys
from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QDialog , QApplication , QWidget , QStackedWidget, QMessageBox , QTableWidget , QTableWidgetItem
from PyQt6.QtGui import QIcon 
from model_run import get_prediction
from database import *

####################################################### Main Screen ######################################################
class welcomeScreen(QDialog):
    def __init__(self):
        super(welcomeScreen , self ).__init__() 
        loadUi('./userInterface/mainPage.ui' , self)
        self.setWindowIcon(QIcon('./bulldozer-icon.png'))
        self.Calculate.clicked.connect(self.calculation)
        self.adminButton.clicked.connect(self.admin)
    
    def calculation(self):
        self.modID=int(self.modelID.text())
        self.year=int(self.YearMade.text())
        self.meter=int(self.MeterReading.text())
        self.result=get_prediction(modelid=self.modID,YearMade=self.year,meterReading=self.meter)

        with open("./static_data/files/data.csv" , "a") as data:
            data.write(f"{self.modID},{self.year},{self.meter},{self.result}\n")
            data.close()
        
        addData(self.modID,self.year,self.meter,self.result)

        output=priceOutput()
        widget.addWidget(output)
        widget.setCurrentIndex(widget.currentIndex()+1)
        self.result=str(self.result)
        output.Price.setText(self.result)

    def admin(self):
        adminP=adminLogInPage()
        widget.addWidget(adminP)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
####################################################### Output Screen ######################################################
class priceOutput(QDialog):
    def __init__(self):
        super(priceOutput , self).__init__()
        loadUi('./userInterface/priceOutput.ui' , self)    
        self.goBack.clicked.connect(self.goBackF)

    def goBackF(self):
        welcome = welcomeScreen()
        widget.addWidget(welcome)
        widget.setCurrentIndex(widget.currentIndex()+1)


####################################################### Admin LogIn Screen ######################################################
class adminLogInPage(QDialog):
    def __init__(self ):
        super(adminLogInPage,self).__init__()
        loadUi('./userInterface/adminOutput.ui',self)
        self.signin.clicked.connect(self.adminMain)
        
        
    def adminMain(self):
        if self.username.text()=='admin' and self.password.text()=='admin':    
            adminM=adminMainPage()
            widget.addWidget(adminM)
            widget.setCurrentIndex(widget.currentIndex()+1)
        else:
            msg = QMessageBox.critical(self,'Invalid Information','Enter Valid Credentials')
    

####################################################### Admin Main Screen ######################################################
class adminMainPage(QDialog):
    def __init__(self ):
        super(adminMainPage,self).__init__()
        loadUi('./userInterface/mainPage.ui',self)




app = QApplication(sys.argv)
welcome = welcomeScreen()
widget = QStackedWidget()
widget.addWidget(welcome)
widget.setFixedHeight(500)
widget.setFixedWidth(650)
widget.setWindowTitle("Price Predictor")
widget.show()
sys.exit(app.exec())

