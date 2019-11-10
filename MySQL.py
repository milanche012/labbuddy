# mySQL connection to the python database
# pylint: disable=F0401
# pylint: disable=E0611

import mysql.connector

try:
    mydb=mysql.connector.connect(user = "admin", 
                            password = "admin",
                            host = "localhost",
                            database = "python")
except:
    mydb=None
if(mydb!=None):
    print("MySQL Connection Successful")
else:
    print("MySQL Connection Unsuccessful")
