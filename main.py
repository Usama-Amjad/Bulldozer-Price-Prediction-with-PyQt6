import sys
import pandas as pd
from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QDialog , QApplication , QWidget , QStackedWidget, QMessageBox , QTableWidget , QTableWidgetItem , QSplashScreen
from PyQt6.QtGui import QIcon ,QPixmap
from model_run import get_prediction
from csvController import *
from database import *
import time

####################################################### Main Screen ######################################################
class welcomeScreen(QDialog):
    def __init__(self):
        super(welcomeScreen , self ).__init__() 
        loadUi('./userInterface/mainPage.ui' , self)
        # self.setWindowIcon(QIcon('./bulldozer-icon.png'))
        self.Calculate.clicked.connect(self.calculation)
        self.adminButton.clicked.connect(self.admin)
        self.Clear.clicked.connect(self.closeapp)

    def closeapp(self):
        app = QApplication(sys.argv)
        sys.exit(app.exec())

    def calculation(self):
        self.modID=int(self.modelID.value())
        self.year=int(self.YearMade.value())
        self.meter=int(self.MeterReading.value())
        self.result=get_prediction(modelid=self.modID,YearMade=self.year,meterReading=self.meter)
        
        # To sql
        addData(self.modID,self.year,self.meter,self.result)
        # To csv
        writingData(self.modID,self.year,self.meter,self.result)

        output=priceOutput()
        widget.addWidget(output)
        widget.setCurrentIndex(widget.currentIndex()+1)
        self.result=str(self.result)
        output.Price.setText(self.result)

    def admin(self):
        adminP=adminLogInPage()
        widget.addWidget(adminP)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
######################################################### Output Screen #############################################################
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
    

####################################################### Admin Main-Screen ######################################################
class adminMainPage(QDialog):
    def __init__(self ):
        super(adminMainPage,self).__init__()
        loadUi('./userInterface/adminView.ui',self)
        self.delete_2.clicked.connect(self.deleteData)
        self.logOut.clicked.connect(self.logout)
        self.searchByModelId.clicked.connect(self.searchPage)
        self.add.clicked.connect(self.addRecord)
        self.updateB.clicked.connect(self.updateRecord)
        self.viewAllB.clicked.connect(self.viewAll)

        rows,cursor=showall()

        cursor.execute("select * from Prediction")
        self.adminTable.setRowCount(rows)

        rowNo=0
        for item in cursor:
            for col in range(0,4):
                data = str(item[col])
                self.adminTable.setItem(rowNo , col , QTableWidgetItem(data))
            rowNo += 1

    def deleteData(self):
        selectedRow=self.adminTable.currentRow()
        print(selectedRow)
        

        if selectedRow<0:
            return QMessageBox.warning(self, 'ERROR','Please select a record to delete')
        else:
            
            self.ModelID = self.adminTable.item(selectedRow , 0).text()
            # print(type(self.ModelID))
            btn = QMessageBox.question(self , "Confirmation" , "Are You Sure You Want To Delete The Selected Record" ,
                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                                  )

            if btn == QMessageBox.StandardButton.Yes:
                dropRow(self.ModelID)
                # self.data=pd.read_csv("static_data/files/data.csv")
                # self.data.drop(selectedRow,axis=0 ,inplace=True)
                # self.data.reset_index(drop=True, inplace=True)
                QMessageBox.information(self , "Congratulations" , "Data Has Been Deleted")
                self.viewAll()

    def viewAll(self):
        adminOBJ = adminMainPage()
        widget.addWidget(adminOBJ)
        widget.setCurrentIndex(widget.currentIndex()+1)
        viewAll()

    def logout(self):
        admin=adminLogInPage()
        widget.addWidget(admin)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def addRecord(self):
        add=welcomeScreen()
        widget.addWidget(add)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def updateRecord(self):
        update=Update()
        widget.addWidget(update)
        widget.setCurrentIndex(widget.currentIndex()+1)

    
    def searchPage(self):
        if len(self.searchID.text()) == 0 :
            QMessageBox.information(self , "Error!!" , "Please Enter Something In The Feild")

        else:
            self.id = self.searchID.text()
            rows , cursor = whereControls(self.id)
            # print(rows)
            if rows == 0:
                QMessageBox.information(self , "Error!!" , "No Record Founded")
            else:
                query = f'select * from Prediction where ModelID = "{self.id}"'
                cursor.execute(query)
                self.adminTable.setRowCount(rows)
                rowNo=0
                for item in cursor:
                    for col in range(0,4):
                        data = str(item[col])
                        self.adminTable.setItem(rowNo , col , QTableWidgetItem(data))
                    rowNo += 1
                search(self.id)

 ######################################################## Update Data ###################################################################
class Update(QDialog):
    def __init__(self ):
        super(Update,self).__init__()
        loadUi('./userInterface/updateData.ui',self)
        self.updateButton.clicked.connect(self.RecordUpdated)
        
    def RecordUpdated(self):
        if len(self.condition.text())==0 or len(self.modelID.text())==0 or len(self.yearMade.text()) == 0 or len(self.meterReading.text()) == 0:
            self.error.setText("Please Fill All Fields")
        else:
            self.model = self.modelID.value()
            self.yearM = self.yearMade.value()
            self.meterR = self.meterReading.value()
            self.con = self.condition.value()

            self.price=updateDatabase(self.model , self.yearM , self.meterR , self.con)
            if self.price=='0':
                QMessageBox.information(self,"Error!!" , "No Record Founded")
            else:
                btn = QMessageBox.information(self, "Congratulations" , "Data Has Been Updated",QMessageBox.StandardButton.Ok)
                # update_new_data(self,self.model , self.yearM , self.meterR , self.price)
                if btn==QMessageBox.StandardButton.Ok:
                    admin=adminMainPage()
                    widget.addWidget(admin)
                    widget.setCurrentIndex(widget.currentIndex()+1)

app = QApplication(sys.argv)
splash=QPixmap('./static_data/images/splashn.jpg')
splashScreen=QSplashScreen(splash)

splashScreen.setGeometry(500,110,600,600)
splashScreen.show()
time.sleep(2)
splashScreen.close()

welcome = welcomeScreen()
widget = QStackedWidget()
widget.addWidget(welcome)
widget.setFixedHeight(600)
widget.setFixedWidth(800)
widget.setWindowTitle("Price Predictor")
widget.setWindowIcon(QIcon('./static_data/images/bulldozer (1).png'))
widget.show()
sys.exit(app.exec())

