import mysql.connector as c
from model_run import get_prediction
from PyQt6.QtWidgets import QDialog , QApplication , QWidget , QStackedWidget, QMessageBox , QTableWidget , QTableWidgetItem , QSplashScreen

mydb=c.connect(
        host='localhost',
        user='root',
        passwd='usama78630mirzas',
        database='priceprediction'
    )

# Adding to database
def addData(modId,year,meter,result):
    cursor=mydb.cursor()
    query='insert into Prediction values({},{},{},{})'.format(modId,year,meter,result)
    cursor.execute(query)
    mydb.commit()

# Deleting from database
def dropRow(modelID):
    # print(modelID)
    query = f'delete from Prediction where ModelID = "{modelID}";'
    mycursor = mydb.cursor()
    mycursor.execute(query)
    mydb.commit()

# Updating Database
def updateDatabase(modelId , yearMade , meterReading ,condition):
    
    rows , cursor =whereControls(condition)
    if rows == 0:
        return '0'
    else:
        price=get_prediction(modelid=int(modelId),YearMade=int(yearMade),meterReading=int(meterReading))
        query = f"update Prediction set ModelID='{modelId}',yearMade ='{yearMade}', meterReading ='{meterReading}', price='{price}' Where ModelID='{condition}';"
        mycursor = mydb.cursor()
        mycursor.execute(query)
        mydb.commit()
        return price

# Show All Data
def showall():
    mycursor = mydb.cursor()
    select = "select * from Prediction"
    mycursor.execute(select)
    rows = 0 
    for data in mycursor:
        print(data)
        rows +=1
    return rows , mycursor

# Where Command
def whereControls(id):
    rowsInWhere = 0
    mycursor =  mydb.cursor()
    userID = id
    query = f'SELECT * FROM Prediction WHERE ModelID ="{userID}"'
    mycursor.execute(query)

    for data in mycursor:
        rowsInWhere +=1
    return rowsInWhere , mycursor


