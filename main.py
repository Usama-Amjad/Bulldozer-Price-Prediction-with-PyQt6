import sys
from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QDialog , QApplication , QWidget , QStackedWidget, QMessageBox , QTableWidget , QTableWidgetItem
from PyQt6.QtGui import QIcon 
from model_run import get_prediction
import mysql.connector as c

# Main Screen
class welcomeScreen(QDialog):
    def __init__(self):
        super(welcomeScreen , self ).__init__() 
        loadUi('./userInterface/mainPage.ui' , self)
        self.setWindowIcon(QIcon('./bulldozer-icon.png'))
        self.Calculate.clicked.connect(self.calculation)
        # self.Clear.clicked.connect(self.close())
    
    def calculation(self):
        self.modID=int(self.modelID.text())
        self.year=int(self.YearMade.text())
        self.meter=int(self.MeterReading.text())
        self.result=get_prediction(modelid=self.modID,YearMade=self.year,meterReading=self.meter)

        with open("./static_data/files/data.csv" , "a") as data:
            data.write(f"{self.modID},{self.year},{self.meter},{self.result}\n")
            data.close()
        

        output=priceOutput()
        widget.addWidget(output)
        widget.setCurrentIndex(widget.currentIndex()+1)
        self.result=str(self.result)
        output.Price.setText(self.result)

        con=c.connect(host='localhost',user='root',passwd='usama78630mirzas',database='priceprediction')
        cursor=con.cursor()
        query='insert into Prediction values({},{},{},{})'.format(self.modID,self.year,self.meter,self.result)
        cursor.execute(query)
        con.commit()

        output.goBack.clicked.connect(self.goBackF)

    def goBackF(self):
        welcome = welcomeScreen()
        widget.addWidget(welcome)
        widget.setCurrentIndex(widget.currentIndex()+1)


# Output Class
class priceOutput(QDialog):
    def __init__(self):
        super(priceOutput , self).__init__()
        loadUi('./userInterface/priceOutput.ui' , self)    




app = QApplication(sys.argv)
welcome = welcomeScreen()
widget = QStackedWidget()
widget.addWidget(welcome)
widget.setFixedHeight(500)
widget.setFixedWidth(650)
widget.setWindowTitle("Price Predictor")
widget.show()
sys.exit(app.exec())

