# mySQL connection to the python database
# pylint: disable=F0401
# pylint: disable=E0611
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

# Creates all necessary databases and tables if they not exist yet

mycursor.execute("CREATE DATABASE IF NOT EXISTS openlaboratory")
mycursor.execute("USE openlaboratory")
mycursor.execute("CREATE TABLE IF NOT EXISTS `openlaboratory`.`lab_user` (`user_id` INT NOT NULL AUTO_INCREMENT,`user_name` VARCHAR(20) NOT NULL,`user_pass` VARCHAR(20) NOT NULL, PRIMARY KEY (`user_id`), UNIQUE INDEX `user_name_UNIQUE` (`user_name` ASC));")
mycursor.execute("CREATE TABLE IF NOT EXISTS `openlaboratory`.`lab_item` (`item_id` INT NOT NULL AUTO_INCREMENT,`item_name` VARCHAR(20) NOT NULL,`item_stock` VARCHAR(20) NOT NULL, PRIMARY KEY (`item_id`), UNIQUE INDEX `item_name_UNIQUE` (`item_name` ASC));")
mycursor.execute("CREATE TABLE IF NOT EXISTS `openlaboratory`.`lab_ana` (`ana_id` INT NOT NULL AUTO_INCREMENT,`ana_name` VARCHAR(20) NOT NULL,`ana_descript` VARCHAR(20) NOT NULL, PRIMARY KEY (`ana_id`), UNIQUE INDEX `ana_name_UNIQUE` (`ana_name` ASC));")
mycursor.execute("CREATE TABLE IF NOT EXISTS `openlaboratory`.`lab_res` (`res_id` INT NOT NULL AUTO_INCREMENT,`res_name` VARCHAR(20) NOT NULL,`res_descript` VARCHAR(20) NOT NULL, PRIMARY KEY (`res_id`), UNIQUE INDEX `res_name_UNIQUE` (`res_name` ASC));")

# mySQL code samples

newUserSQL="INSERT INTO lab_user (user_name, user_pass) VALUES (%s, %s);"
newUser=("Milan", "stokic")
#mycursor.execute(newUserSQL, newUser)
selectUserSQL="SELECT * FROM openlaboratory.lab_user;"
mycursor.execute(selectUserSQL)
myUserResult=mycursor.fetchall() #try to use .fetchone
for row in myUserResult:
    print(row)

newItemSQL="INSERT INTO lab_item (item_name, item_stock) VALUES (%s, %s);"
newItems=[("Solja3", "3"),
          ("Solja4", "3"),
          ("Solja5", "3"),
          ("Solja6", "3"),
          ("Solja7", "3"),
          ("Solja8", "3")]
#mycursor.executemany(newItemSQL, newItems)

# Code for the pagination of the tables
"""
resultsPerPage=5
mycursor.execute("SELECT COUNT(*) FROM openlaboratory.lab_item WHERE item_name LIKE \"Solja%\";")
results=mycursor.fetchone()
numberOfRows=results[0]
numberOfPages=math.ceil(numberOfRows/resultsPerPage)
currentPageNumb=2
pageFirstRes=(currentPageNumb-1)*resultsPerPage
pageFirstRes=int(pageFirstRes)
print(pageFirstRes)
pagination=(pageFirstRes, resultsPerPage)
paginationSQL="SELECT * FROM openlaboratory.lab_item LIMIT %s, %s;"
mycursor.execute(paginationSQL, pagination)
myPaginationResult=mycursor.fetchall() 
for row in myPaginationResult:
    print(row)
"""
selectItemSQL="SELECT * FROM openlaboratory.lab_item;"
mycursor.execute(selectItemSQL)
myItemResult=mycursor.fetchall() 
for row in myItemResult:
    print(row)
myItemUpdateSQL="UPDATE openlaboratory.lab_item SET item_stock = %s WHERE item_name = %s;"
mycursor.execute(myItemUpdateSQL, (15, "Solja5"))

myItemSpecSQL="SELECT * FROM openlaboratory.lab_item WHERE item_name = %s;"
mycursor.execute(myItemSpecSQL,("Solja5", )) #use mySQL formula with place-holders and tupels to battle SQL injection
myItemSpecResult=mycursor.fetchall() 
for row in myItemSpecResult:
    print(row)

newAnaSQL="INSERT INTO lab_ana (ana_name, ana_descript) VALUES (%s, %s);"
newAna=("Colli", "Colli bacterija")
#mycursor.execute(newAnaSQL, newAna)
selectAnarSQL="SELECT * FROM openlaboratory.lab_ana;"
mycursor.execute(selectAnarSQL)
myAnaResult=mycursor.fetchall()
for row in myAnaResult:
    print(row)

newResSQL="INSERT INTO lab_res (res_name, res_descript) VALUES (%s, %s);"
newRes=("Colli", "negativ")
#mycursor.execute(newResSQL, newRes)
selectResSQL="SELECT * FROM openlaboratory.lab_res;"
mycursor.execute(selectResSQL)
myResResult=mycursor.fetchall()
for row in myResResult:
    print(row)

mydb.commit()
