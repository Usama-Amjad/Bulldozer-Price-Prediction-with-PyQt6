import csv
# Writing data into csv
def writingData(modID,year,meter,result):
    with open("./static_data/files/data.csv" , "a") as data:
            data.write(f"{modID},{year},{meter},{result}\n")
            data.close()

def delete_row(self):
        # Delete the selected row from the table widget and the data
        selected_row = self.table_widget.currentRow()
        if selected_row >= 0:
            self.table_widget.removeRow(selected_row)
            self.data.drop(selected_row, inplace=True)
            self.data.reset_index(drop=True, inplace=True)

def search(modelID):
    csv_file = csv.reader(open('./static_data/files/data.csv', "r"), delimiter=",")
    for row in csv_file:
        if modelID==row[0]:
            print(row)

def viewAll():
    csv_file = csv.reader(open('./static_data/files/data.csv', "r"), delimiter=",")
    for row in csv_file:
        print(row)
    
                  