from PyQt5 import QtWidgets, uic

import math 
import mysql.connector 

try: 
    mydb=mysql.connector.connect(
        user="admin", 
        password ="admin", 
        host="localhost", 
        database="")
except:
    mydb=None 
mycursor=mydb.cursor()

if(mydb!=None):
	print("MySQL Connection Successful")
else:
	print("MySQL Connection Unsuccessful")

app=QtWidgets.QApplication([])
dig=uic.loadUi("LabBuddy.ui")
dig.show()
app.exec()