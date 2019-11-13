import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import scrolledtext

import math 
import mysql.connector 
import json


#===========================
# Geting the server settings
#===========================
def main():
    with open("serverSettings.json", "r") as file:
        serverSettings=json.load(file)
        return serverSettings
    
#===========================================
# mySQL connection to the Lab Buddy database
#===========================================
def connectToServer(serverSettingsUser,serverSettingsPassword,serverSettingsPortNumber,serverSettingsHost):
    try: 
        mydb=mysql.connector.connect(
            user=serverSettingsUser, 
            password =serverSettingsPassword,
            port=serverSettingsPortNumber, 
            host=serverSettingsHost, 
            database="")
     
        mycursor=mydb.cursor()
    
        # Creates all necessary databases and tables if they not exist yet
        mycursor.execute("CREATE DATABASE IF NOT EXISTS openlaboratory")
        mycursor.execute("USE openlaboratory")
        mycursor.execute("CREATE TABLE IF NOT EXISTS openlaboratory.lab_user (`user_id` INT NOT NULL AUTO_INCREMENT,`user_name` VARCHAR(20) NOT NULL,`user_pass` VARCHAR(20) NOT NULL, PRIMARY KEY (`user_id`), UNIQUE INDEX `user_name_UNIQUE` (`user_name` ASC));")
        mycursor.execute("CREATE TABLE IF NOT EXISTS openlaboratory.lab_item (`item_id` INT NOT NULL AUTO_INCREMENT,`item_name` VARCHAR(20) NOT NULL,`item_stock` VARCHAR(20) NOT NULL, PRIMARY KEY (`item_id`), UNIQUE INDEX `item_name_UNIQUE` (`item_name` ASC));")
        mycursor.execute("CREATE TABLE IF NOT EXISTS openlaboratory.lab_ana (`ana_id` INT NOT NULL AUTO_INCREMENT,`ana_name` VARCHAR(20) NOT NULL,`ana_descript` VARCHAR(20) NOT NULL, PRIMARY KEY (`ana_id`), UNIQUE INDEX `ana_name_UNIQUE` (`ana_name` ASC));")
        mycursor.execute("CREATE TABLE IF NOT EXISTS openlaboratory.lab_res (`res_id` INT NOT NULL AUTO_INCREMENT,`res_name` VARCHAR(20) NOT NULL,`res_descript` VARCHAR(20) NOT NULL, PRIMARY KEY (`res_id`), UNIQUE INDEX `res_name_UNIQUE` (`res_name` ASC));")
        
        return mydb
    except:
        pass  



#===============================
#Show/Hide function
#===============================

def showHide_1():
    subsubtoolbarFrame_1.grid()
    subsubtoolbarFrame_2.grid_forget()
    subsubtoolbarFrame_3.grid_forget()
    subsubtoolbarFrame_4.grid_forget()
    subsubtoolbarFrame_5.grid_forget()

def showHide_2():
    subsubtoolbarFrame_1.grid_forget()
    subsubtoolbarFrame_2.grid()
    subsubtoolbarFrame_3.grid_forget()
    subsubtoolbarFrame_4.grid_forget()
    subsubtoolbarFrame_5.grid_forget()

def showHide_3():
    subsubtoolbarFrame_1.grid_forget()
    subsubtoolbarFrame_2.grid_forget()
    subsubtoolbarFrame_3.grid()
    subsubtoolbarFrame_4.grid_forget()
    subsubtoolbarFrame_5.grid_forget()
    
def showHide_4():
    subsubtoolbarFrame_1.grid_forget()
    subsubtoolbarFrame_2.grid_forget()
    subsubtoolbarFrame_3.grid_forget()
    subsubtoolbarFrame_4.grid()
    subsubtoolbarFrame_5.grid_forget()
    
def showHide_5():
    subsubtoolbarFrame_1.grid_forget()
    subsubtoolbarFrame_2.grid_forget()
    subsubtoolbarFrame_3.grid_forget()
    subsubtoolbarFrame_4.grid_forget()
    subsubtoolbarFrame_5.grid()

#==============
#Class New User
#==============
class newUser:
    def __init__(self, username, password, password2):
        self.username=username
        self.password=password
        self.password2=password2
    
    # Validating Uniquenes of the username
    def validateUserName(self): 
        mydb=connectToServer(serverSettingsUser,serverSettingsPassword,serverSettingsPortNumber,serverSettingsHost)
        mycursor=mydb.cursor()
        checkForNameSQL="SELECT COUNT(*) FROM openlaboratory.lab_user WHERE user_name = %s;"
        mycursor.execute(checkForNameSQL,(self.username, ))
        checkForNameResult=mycursor.fetchall()
        result=int(checkForNameResult[0][0])
        if (result>=1):
            messagebox.showerror("User name error", "Please pick a new user name")
            userName=False
        else:
            userName=True
            return userName
        
    # Validating if the passwords are the same   
    def validateNewPassword(self): 
        if (self.password==self.password2):
            Password=True
            return Password
        else:
            Password=False
            messagebox.showerror("Password error", "Password is not the same")
            return Password

            
    # Creating a new user
    def createNewUser(self):
        mydb=connectToServer(serverSettingsUser,serverSettingsPassword,serverSettingsPortNumber,serverSettingsHost)
        mycursor=mydb.cursor()
        newUserSQL="INSERT INTO openlaboratory.lab_user (user_name, user_pass) VALUES (%s, %s);"
        newUser=(self.username, self.password)
        mycursor.execute(newUserSQL, newUser)
        mydb.commit()
        messagebox.showinfo("New user", "Neww User Created, Please Log-In Now")
        newUserNameEntered.set("")
        newPasswordNameEntered.set("")
        renewPasswordNameEntered.set("")
        
#==========================================================================
# Starting the registration process after clicking the rregistration button
#========================================================================== 
def startRegistration():
    # Geting the info for the regitration process
    try:
        regInfo1=newUserNameEntered.get()
        regInfo2=newPasswordNameEntered.get()
        regInfo3=renewPasswordNameEntered.get()
        newRegister=newUser(regInfo1, regInfo2, regInfo3)
        validateName=newRegister.validateUserName()
        validatePassword=newRegister.validateNewPassword()
        if (validateName==True) and (validatePassword==True):
            newRegister.createNewUser()
            
    except:
        pass
    
#========== 
#Class User
#==========
class User:
    def __init__(self, username, password):
        self.username=username
        self.password=password
        
    # Find username
    def findUserName(self): 
        mydb=connectToServer(serverSettingsUser,serverSettingsPassword,serverSettingsPortNumber,serverSettingsHost)
        mycursor=mydb.cursor()
        checkForNameSQL="SELECT * FROM openlaboratory.lab_user WHERE user_name = %s;"
        mycursor.execute(checkForNameSQL,(self.username, ))
        checkForNameResult=mycursor.fetchall()
        for result in checkForNameResult:
            if (result[1]==self.username):
                userName=True
                return userName
            else:
                userName=False
                messagebox.showerror("User name error", "Please check username")
                return userName
    
     # Validating if the password is correct   
    def findPassword(self): 
        mydb=connectToServer(serverSettingsUser,serverSettingsPassword,serverSettingsPortNumber,serverSettingsHost)
        mycursor=mydb.cursor()
        checkForNameSQL="SELECT * FROM openlaboratory.lab_user WHERE user_name = %s;"
        mycursor.execute(checkForNameSQL,(self.username, ))
        checkForNameResult=mycursor.fetchall()
        for result in checkForNameResult:
        
            if (result[2]==self.password):
                Password=True
                return Password
            else:
                Password=False
                messagebox.showerror("Password error", "Please check password")
                return Password

            
    # Log-In user
    def logInUser(self):
        mydb=connectToServer(serverSettingsUser,serverSettingsPassword,serverSettingsPortNumber,serverSettingsHost)
        mycursor=mydb.cursor()
        checkForNameSQL="SELECT * FROM openlaboratory.lab_user WHERE user_name = %s AND user_pass = %s;"
        mycursor.execute(checkForNameSQL,(self.username,self.password, ))
        checkForNameResult=mycursor.fetchall()
        for result in checkForNameResult:
            return result

#===========================================================
# Starting the logIn process after clicking the logIn button 
#===========================================================   
def startLogIn():
    # Geting the info for the regitration process
    try:
        logInfo1=logUserNameEntered.get()
        logInfo2=logPasswordNameEntered.get()
        newLog=User(logInfo1, logInfo2)
        logName=newLog.findUserName()
        logPassword=newLog.findPassword()
        if (logName==True) and (logPassword==True):
            newLog.logInUser()
            messagebox.showinfo("LogIn", "Loged In")
            logUserNameEntered.set("")
            logPasswordNameEntered.set("")
            LogID=newLog.logInUser()
            print(LogID[0])
            return LogID[0]
            
    except:
        pass

"""  
def savingServerSettings():
    # Geting the info for the server settings
    serverInfo1=str(dlg.lineEdit.text())
    serverInfo2=str(dlg.lineEdit_4.text())
    serverInfo3=str(dlg.lineEdit_5.text())
    serverInfo4=str(dlg.lineEdit_6.text())
    
    newServerSettings={"username":serverInfo1, "password":serverInfo2, "portNumber":serverInfo3, "host":serverInfo4}
    with open("serverSettings.json", "w") as file:
        json.dump(newServerSettings,file)
        
    messagebox.showinfo("New server settings", "Please restart the application to take effect")


# Code for the pagination of the tables

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
#==========================
#Geting the server settings
#==========================
if __name__ =="__main__":
    main()
    # Server settings
    serverSettings=main()
    serverSettingsUser=serverSettings["username"]
    serverSettingsPassword=serverSettings["password"]
    serverSettingsPortNumber=serverSettings["portNumber"]
    serverSettingsHost=serverSettings["host"]

#=====================
# Connecting to Server
#=====================  
connectToServer(serverSettingsUser,serverSettingsPassword,serverSettingsPortNumber,serverSettingsHost)
mydb=connectToServer(serverSettingsUser,serverSettingsPassword,serverSettingsPortNumber,serverSettingsHost)

#================
#Creates instance
#================
win=tk.Tk()

#====================
#Main window settings
#====================
win.title("Lab Buddy")
win.geometry("830x650")             
win.resizable(0,0)

#===================================
#Toolbar and subtoolbar window layer
#===================================
someFrame=ttk.LabelFrame(win, text="Lab Buddy")
someFrame.grid(column=0, row=0)
toolbarFrame=ttk.LabelFrame(someFrame, text="Toolbar")
toolbarFrame.grid(column=0, row=1)
subtoolbarFrame=ttk.LabelFrame(someFrame, text="Subtoolbar")
subtoolbarFrame.grid(column=0, row=2)

#=============
#Toolbar icons
#=============
toolButton_1=ttk.Button(toolbarFrame, text="Users", command=showHide_1)
toolButton_1.grid(column=1, row=1)
toolButton_2=ttk.Button(toolbarFrame, text="Methods", command=showHide_2)
toolButton_2.grid(column=2, row=1)
toolButton_3=ttk.Button(toolbarFrame, text="Results", command=showHide_3)
toolButton_3.grid(column=3, row=1)
toolButton_4=ttk.Button(toolbarFrame, text="Items", command=showHide_4)
toolButton_4.grid(column=4, row=1)
toolButton_5=ttk.Button(toolbarFrame, text="Settings", command=showHide_5)
toolButton_5.grid(column=5, row=1)

#==================================
#Frame to show/hide subtoolbar items
#===================================
subsubtoolbarFrame_1=ttk.LabelFrame(subtoolbarFrame, text="SubsubtoolbarFrame_1")
subsubtoolbarFrame_1.grid(column=1, row=0)
subsubtoolbarFrame_2=ttk.LabelFrame(subtoolbarFrame, text="SubsubtoolbarFrame_2")
subsubtoolbarFrame_2.grid(column=2, row=0)
subsubtoolbarFrame_3=ttk.LabelFrame(subtoolbarFrame, text="SubsubtoolbarFrame_3")
subsubtoolbarFrame_3.grid(column=3, row=0)
subsubtoolbarFrame_4=ttk.LabelFrame(subtoolbarFrame, text="SubsubtoolbarFrame_4")
subsubtoolbarFrame_4.grid(column=4, row=0)
subsubtoolbarFrame_5=ttk.LabelFrame(subtoolbarFrame, text="SubsubtoolbarFrame_5")
subsubtoolbarFrame_5.grid(column=5, row=0)

#==================================
#Subtoolbar items
#===================================

#Page Users
usersTab=ttk.Notebook(subsubtoolbarFrame_1)
usersFrame_1=ttk.Frame(usersTab)
usersTab.add(usersFrame_1, text="LogIn")
usersFrame_2=ttk.Frame(usersTab)
usersTab.add(usersFrame_2, text="SingIn")
usersTab.pack(expand=1, fill="both")
#tab1
logUserLabel=ttk.Label(usersFrame_1, text="User Name").grid(column=1,row=1, sticky=tk.W)
logPasswordLabel=ttk.Label(usersFrame_1, text="Password").grid(column=1,row=2, sticky=tk.W)
logUserNameEntered=tk.StringVar()
userNameTK=ttk.Entry(usersFrame_1, width=20, textvariable=logUserNameEntered).grid(column=1,row=1)
logPasswordNameEntered=tk.StringVar()
passwordNameTK=ttk.Entry(usersFrame_1, width=20, textvariable=logPasswordNameEntered).grid(column=1,row=2)
logUserButton=ttk.Button(usersFrame_1, text="Log-in", command=startLogIn).grid(column=1, row=3)
#tab2
newUserLabel=ttk.Label(usersFrame_2, text="User Name").grid(column=1,row=1, sticky=tk.W)
newPasswordLabel=ttk.Label(usersFrame_2, text="Password").grid(column=1,row=2, sticky=tk.W)
renewPasswordLabel=ttk.Label(usersFrame_2, text="Re-password").grid(column=1,row=3, sticky=tk.W)
newUserNameEntered=tk.StringVar()
newUserNameTK=ttk.Entry(usersFrame_2, width=20, textvariable=newUserNameEntered).grid(column=2,row=1)
newPasswordNameEntered=tk.StringVar()
newPasswordNameTK=ttk.Entry(usersFrame_2, width=20, textvariable=newPasswordNameEntered).grid(column=2,row=2)
renewPasswordNameEntered=tk.StringVar()
renewPasswordNameTK=ttk.Entry(usersFrame_2, width=20, textvariable=renewPasswordNameEntered).grid(column=2,row=3)
newUserButton=ttk.Button(usersFrame_2, text="Register", command=startRegistration).grid(column=1, row=4, columnspan=2)

#Page Methods
methodsTab=ttk.Notebook(subsubtoolbarFrame_2)
methodsFrame_1=ttk.Frame(methodsTab)
methodsTab.add(methodsFrame_1, text="Find Method")
methodsFrame_2=ttk.Frame(methodsTab)
methodsTab.add(methodsFrame_2, text="Edit Method")
methodsFrame_3=ttk.Frame(methodsTab)
methodsTab.add(methodsFrame_3, text="Add Method")
methodsTab.pack(expand=1, fill="both")

#tab1
methodsFrame_1_1=ttk.Frame(methodsFrame_1)
methodsFrame_1_1.pack(expand=1, fill="both")
methodsLabel_1=ttk.Label(methodsFrame_1_1, text="Name").grid(column=1,row=1)
methodsLabel_2=ttk.Label(methodsFrame_1_1, text="Category").grid(column=2,row=1)
methodsLabel_3=ttk.Label(methodsFrame_1_1, text="ISO").grid(column=3,row=1)
methodsLabel_4=ttk.Label(methodsFrame_1_1, text="Text").grid(column=4,row=1)
methodsNameEntered=tk.StringVar()
methodsNameComboBox=ttk.Combobox(methodsFrame_1_1, textvariable=methodsNameEntered).grid(column=1, row=2)
methodsCategoryEntered=tk.StringVar()
methodsCategoryComboBox=ttk.Combobox(methodsFrame_1_1, textvariable=methodsCategoryEntered).grid(column=2, row=2)
methodsISOEntered=tk.StringVar()
methodsISOEntry=ttk.Entry(methodsFrame_1_1, width=20, textvariable=methodsISOEntered).grid(column=3,row=2)
methodsTextEntered=tk.StringVar()
methodsTextEntry=ttk.Entry(methodsFrame_1_1, width=20, textvariable=methodsTextEntered).grid(column=4,row=2)
methodsFindButton=ttk.Button(methodsFrame_1_1, text="Find", command="").grid(column=7, row=2, sticky=tk.W)
methodsFrame_1_2=ttk.Frame(methodsFrame_1)
methodsFrame_1_2.pack(expand=1, fill="both")
methodsTextList_1=scrolledtext.ScrolledText(methodsFrame_1_2, width=100, height=100, wrap=tk.WORD)
methodsTextList_1.grid(column=0, columnspan=1)
methodsTextList_1.configure(state="disabled")

#tab2
methodsFrame_2_1=ttk.Frame(methodsFrame_2)
methodsFrame_2_1.pack(expand=1, fill="both")
methodsLabel_1=ttk.Label(methodsFrame_2_1, text="Name").grid(column=1,row=1)
methodsLabel_2=ttk.Label(methodsFrame_2_1, text="Category").grid(column=2,row=1)
methodsLabel_3=ttk.Label(methodsFrame_2_1, text="ISO").grid(column=3,row=1)
methodsLabel_4=ttk.Label(methodsFrame_2_1, text="Text").grid(column=4,row=1)
methodsNameEntered=tk.StringVar()
methodsNameComboBox=ttk.Combobox(methodsFrame_2_1, textvariable=methodsNameEntered).grid(column=1, row=2)
methodsCategoryEntered=tk.StringVar()
methodsCategoryComboBox=ttk.Combobox(methodsFrame_2_1, textvariable=methodsCategoryEntered).grid(column=2, row=2)
methodsISOEntered=tk.StringVar()
methodsISOEntry=ttk.Entry(methodsFrame_2_1, width=20, textvariable=methodsISOEntered).grid(column=3,row=2)
methodsTextEntered=tk.StringVar()
methodsTextEntry=ttk.Entry(methodsFrame_2_1, width=20, textvariable=methodsTextEntered).grid(column=4,row=2)
methodsEditButton=ttk.Button(methodsFrame_2_1, text="Edit", command="").grid(column=7, row=2, sticky=tk.W)
methodsFrame_2_2=ttk.Frame(methodsFrame_2)
methodsFrame_2_2.pack(expand=1, fill="both")
methodsTextList_1=scrolledtext.ScrolledText(methodsFrame_2_2, width=100, height=100, wrap=tk.WORD)
methodsTextList_1.grid(column=0, columnspan=1)

#tab3
methodsFrame_3_1=ttk.Frame(methodsFrame_3)
methodsFrame_3_1.pack(expand=1, fill="both")
methodsLabel_1=ttk.Label(methodsFrame_3_1, text="Name").grid(column=1,row=1)
methodsLabel_2=ttk.Label(methodsFrame_3_1, text="Category").grid(column=2,row=1)
methodsLabel_3=ttk.Label(methodsFrame_3_1, text="ISO").grid(column=3,row=1)
methodsLabel_4=ttk.Label(methodsFrame_3_1, text="Text").grid(column=4,row=1)
methodsNameEntered=tk.StringVar()
methodsNameComboBox=ttk.Combobox(methodsFrame_3_1, textvariable=methodsNameEntered).grid(column=1, row=2)
methodsCategoryEntered=tk.StringVar()
methodsCategoryComboBox=ttk.Combobox(methodsFrame_3_1, textvariable=methodsCategoryEntered).grid(column=2, row=2)
methodsISOEntered=tk.StringVar()
methodsISOEntry=ttk.Entry(methodsFrame_3_1, width=20, textvariable=methodsISOEntered).grid(column=3,row=2)
methodsTextEntered=tk.StringVar()
methodsTextEntry=ttk.Entry(methodsFrame_3_1, width=20, textvariable=methodsTextEntered).grid(column=4,row=2)
methodsAddButton=ttk.Button(methodsFrame_3_1, text="Add", command="").grid(column=7, row=2, sticky=tk.W)
methodsFrame_3_2=ttk.Frame(methodsFrame_3)
methodsFrame_3_2.pack(expand=1, fill="both")
methodsTextList_1=scrolledtext.ScrolledText(methodsFrame_3_2, width=100, height=100, wrap=tk.WORD)
methodsTextList_1.grid(column=0, columnspan=1)

#Page Results
resultsTab=ttk.Notebook(subsubtoolbarFrame_3)
resultsFrame_1=ttk.Frame(resultsTab)
resultsTab.add(resultsFrame_1, text="Find result")
resultsFrame_2=ttk.Frame(resultsTab)
resultsTab.add(resultsFrame_2, text="Edit result")
resultsFrame_3=ttk.Frame(resultsTab)
resultsTab.add(resultsFrame_3, text="Add result")
resultsTab.pack(expand=1, fill="both")

#tab1
resultsFrame_1_1=ttk.Frame(resultsFrame_1)
resultsFrame_1_1.pack(expand=1, fill="both")
resultsLabel_1=ttk.Label(resultsFrame_1_1, text="Name").grid(column=1,row=1)
resultsLabel_2=ttk.Label(resultsFrame_1_1, text="Category").grid(column=2,row=1)
resultsLabel_3=ttk.Label(resultsFrame_1_1, text="Patient").grid(column=3,row=1)
resultsLabel_4=ttk.Label(resultsFrame_1_1, text="Text").grid(column=4,row=1)
resultsNameEntered=tk.StringVar()
resultsNameComboBox=ttk.Combobox(resultsFrame_1_1, textvariable=resultsNameEntered).grid(column=1, row=2)
resultsCategoryEntered=tk.StringVar()
resultsCategoryComboBox=ttk.Combobox(resultsFrame_1_1, textvariable=resultsCategoryEntered).grid(column=2, row=2)
resultsPatientEntered=tk.StringVar()
resultsPatientEntry=ttk.Entry(resultsFrame_1_1, width=20, textvariable=resultsPatientEntered).grid(column=3,row=2)
resultsTextEntered=tk.StringVar()
resultsTextEntry=ttk.Entry(resultsFrame_1_1, width=20, textvariable=resultsTextEntered).grid(column=4,row=2)
resultsFindButton=ttk.Button(resultsFrame_1_1, text="Find", command="").grid(column=7, row=2, sticky=tk.W)
resultsFrame_1_2=ttk.Frame(resultsFrame_1)
resultsFrame_1_2.pack(expand=1, fill="both")
resultsTextList_1=scrolledtext.ScrolledText(resultsFrame_1_2, width=100, height=100, wrap=tk.WORD)
resultsTextList_1.grid(column=0, columnspan=1)
resultsTextList_1.configure(state="disabled")

#tab2
resultsFrame_2_1=ttk.Frame(resultsFrame_2)
resultsFrame_2_1.pack(expand=1, fill="both")
resultsLabel_1=ttk.Label(resultsFrame_2_1, text="Name").grid(column=1,row=1)
resultsLabel_2=ttk.Label(resultsFrame_2_1, text="Category").grid(column=2,row=1)
resultsLabel_3=ttk.Label(resultsFrame_2_1, text="Patient").grid(column=3,row=1)
resultsLabel_4=ttk.Label(resultsFrame_2_1, text="Text").grid(column=4,row=1)
resultsNameEntered=tk.StringVar()
resultsNameComboBox=ttk.Combobox(resultsFrame_2_1, textvariable=resultsNameEntered).grid(column=1, row=2)
resultsCategoryEntered=tk.StringVar()
resultsCategoryComboBox=ttk.Combobox(resultsFrame_2_1, textvariable=resultsCategoryEntered).grid(column=2, row=2)
resultsPatientEntered=tk.StringVar()
resultsPatientEntry=ttk.Entry(resultsFrame_2_1, width=20, textvariable=resultsPatientEntered).grid(column=3,row=2)
resultsTextEntered=tk.StringVar()
resultsTextEntry=ttk.Entry(resultsFrame_2_1, width=20, textvariable=resultsTextEntered).grid(column=4,row=2)
resultsEditButton=ttk.Button(resultsFrame_2_1, text="Edit", command="").grid(column=7, row=2, sticky=tk.W)
resultsFrame_2_2=ttk.Frame(resultsFrame_2)
resultsFrame_2_2.pack(expand=1, fill="both")
resultsTextList_1=scrolledtext.ScrolledText(resultsFrame_2_2, width=100, height=100, wrap=tk.WORD)
resultsTextList_1.grid(column=0, columnspan=1)

#tab3
resultsFrame_3_1=ttk.Frame(resultsFrame_3)
resultsFrame_3_1.pack(expand=1, fill="both")
resultsLabel_1=ttk.Label(resultsFrame_3_1, text="Name").grid(column=1,row=1)
resultsLabel_2=ttk.Label(resultsFrame_3_1, text="Category").grid(column=2,row=1)
resultsLabel_3=ttk.Label(resultsFrame_3_1, text="Patient").grid(column=3,row=1)
resultsLabel_4=ttk.Label(resultsFrame_3_1, text="Text").grid(column=4,row=1)
resultsNameEntered=tk.StringVar()
resultsNameComboBox=ttk.Combobox(resultsFrame_3_1, textvariable=resultsNameEntered).grid(column=1, row=2)
resultsCategoryEntered=tk.StringVar()
resultsCategoryComboBox=ttk.Combobox(resultsFrame_3_1, textvariable=resultsCategoryEntered).grid(column=2, row=2)
resultsPatientEntered=tk.StringVar()
resultsPatientEntry=ttk.Entry(resultsFrame_3_1, width=20, textvariable=resultsPatientEntered).grid(column=3,row=2)
resultsTextEntered=tk.StringVar()
resultsTextEntry=ttk.Entry(resultsFrame_3_1, width=20, textvariable=resultsTextEntered).grid(column=4,row=2)
resultsAddButton=ttk.Button(resultsFrame_3_1, text="Add", command="").grid(column=7, row=2, sticky=tk.W)
resultsFrame_3_2=ttk.Frame(resultsFrame_3)
resultsFrame_3_2.pack(expand=1, fill="both")
resultsTextList_1=scrolledtext.ScrolledText(resultsFrame_3_2, width=100, height=100, wrap=tk.WORD)
resultsTextList_1.grid(column=0, columnspan=1)

#Page Items
itemsTab=ttk.Notebook(subsubtoolbarFrame_4)
itemsFrame_1=ttk.Frame(itemsTab)
itemsTab.add(itemsFrame_1, text="Find Item")
itemsFrame_2=ttk.Frame(itemsTab)
itemsTab.add(itemsFrame_2, text="Edit Item")
itemsFrame_3=ttk.Frame(itemsTab)
itemsTab.add(itemsFrame_3, text="Add Item")
itemsTab.pack(expand=1, fill="both")

#tab1
itemsFrame_1_1=ttk.Frame(itemsFrame_1)
itemsFrame_1_1.pack(expand=1, fill="both")
itemsLabel_1=ttk.Label(itemsFrame_1_1, text="Name").grid(column=1,row=1)
itemsLabel_2=ttk.Label(itemsFrame_1_1, text="Category").grid(column=2,row=1)
itemsLabel_3=ttk.Label(itemsFrame_1_1, text="Location").grid(column=3,row=1)
itemsLabel_4=ttk.Label(itemsFrame_1_1, text="Text").grid(column=4,row=1)
itemsNameEntered=tk.StringVar()
itemsNameComboBox=ttk.Combobox(itemsFrame_1_1, textvariable=itemsNameEntered).grid(column=1, row=2)
itemsCategoryEntered=tk.StringVar()
itemsCategoryComboBox=ttk.Combobox(itemsFrame_1_1, textvariable=itemsCategoryEntered).grid(column=2, row=2)
itemsLocationEntered=tk.StringVar()
itemsLocationEntry=ttk.Entry(itemsFrame_1_1, width=20, textvariable=itemsLocationEntered).grid(column=3,row=2)
itemsTextEntered=tk.StringVar()
itemsTextEntry=ttk.Entry(itemsFrame_1_1, width=20, textvariable=itemsTextEntered).grid(column=4,row=2)
itemsFindButton=ttk.Button(itemsFrame_1_1, text="Find", command="").grid(column=7, row=2, sticky=tk.W)
itemsFrame_1_2=ttk.Frame(itemsFrame_1)
itemsFrame_1_2.pack(expand=1, fill="both")
itemsTextList_1=scrolledtext.ScrolledText(itemsFrame_1_2, width=100, height=100, wrap=tk.WORD)
itemsTextList_1.grid(column=0, columnspan=1)
itemsTextList_1.configure(state="disabled")

#tab2
itemsFrame_2_1=ttk.Frame(itemsFrame_2)
itemsFrame_2_1.pack(expand=1, fill="both")
itemsLabel_1=ttk.Label(itemsFrame_2_1, text="Name").grid(column=1,row=1)
itemsLabel_2=ttk.Label(itemsFrame_2_1, text="Category").grid(column=2,row=1)
itemsLabel_3=ttk.Label(itemsFrame_2_1, text="ISO").grid(column=3,row=1)
itemsLabel_4=ttk.Label(itemsFrame_2_1, text="Text").grid(column=4,row=1)
itemsNameEntered=tk.StringVar()
itemsNameComboBox=ttk.Combobox(itemsFrame_2_1, textvariable=itemsNameEntered).grid(column=1, row=2)
itemsCategoryEntered=tk.StringVar()
itemsCategoryComboBox=ttk.Combobox(itemsFrame_2_1, textvariable=itemsCategoryEntered).grid(column=2, row=2)
itemsISOEntered=tk.StringVar()
itemsISOEntry=ttk.Entry(itemsFrame_2_1, width=20, textvariable=itemsISOEntered).grid(column=3,row=2)
itemsTextEntered=tk.StringVar()
itemsTextEntry=ttk.Entry(itemsFrame_2_1, width=20, textvariable=itemsTextEntered).grid(column=4,row=2)
itemsEditButton=ttk.Button(itemsFrame_2_1, text="Edit", command="").grid(column=7, row=2, sticky=tk.W)
itemsFrame_2_2=ttk.Frame(itemsFrame_2)
itemsFrame_2_2.pack(expand=1, fill="both")
itemsTextList_1=scrolledtext.ScrolledText(itemsFrame_2_2, width=100, height=100, wrap=tk.WORD)
itemsTextList_1.grid(column=0, columnspan=1)

#tab3
itemsFrame_3_1=ttk.Frame(itemsFrame_3)
itemsFrame_3_1.pack(expand=1, fill="both")
itemsLabel_1=ttk.Label(itemsFrame_3_1, text="Name").grid(column=1,row=1)
itemsLabel_2=ttk.Label(itemsFrame_3_1, text="Category").grid(column=2,row=1)
itemsLabel_3=ttk.Label(itemsFrame_3_1, text="ISO").grid(column=3,row=1)
itemsLabel_4=ttk.Label(itemsFrame_3_1, text="Text").grid(column=4,row=1)
itemsNameEntered=tk.StringVar()
itemsNameComboBox=ttk.Combobox(itemsFrame_3_1, textvariable=itemsNameEntered).grid(column=1, row=2)
itemsCategoryEntered=tk.StringVar()
itemsCategoryComboBox=ttk.Combobox(itemsFrame_3_1, textvariable=itemsCategoryEntered).grid(column=2, row=2)
itemsISOEntered=tk.StringVar()
itemsISOEntry=ttk.Entry(itemsFrame_3_1, width=20, textvariable=itemsISOEntered).grid(column=3,row=2)
itemsTextEntered=tk.StringVar()
itemsTextEntry=ttk.Entry(itemsFrame_3_1, width=20, textvariable=itemsTextEntered).grid(column=4,row=2)
itemsAddButton=ttk.Button(itemsFrame_3_1, text="Add", command="").grid(column=7, row=2, sticky=tk.W)
itemsFrame_3_2=ttk.Frame(itemsFrame_3)
itemsFrame_3_2.pack(expand=1, fill="both")
itemsTextList_1=scrolledtext.ScrolledText(itemsFrame_3_2, width=100, height=100, wrap=tk.WORD)
itemsTextList_1.grid(column=0, columnspan=1)

#Page Settings
settingsTab=ttk.Notebook(subsubtoolbarFrame_5)
settingsFrame_1=ttk.Frame(settingsTab)
settingsTab.add(settingsFrame_1, text="Settings")
settingsFrame_2=ttk.Frame(settingsTab)
settingsTab.add(settingsFrame_2, text="About")
settingsTab.pack(expand=1, fill="both")

#tab1
settingsFrame_1_1=ttk.Frame(settingsFrame_1)
settingsFrame_1_1.pack(expand=1, fill="both")
settingsLabel_1=ttk.Label(settingsFrame_1_1, text="Server Settings").grid(column=2,row=1)
settingsLabel_2=ttk.Label(settingsFrame_1_1, text="User Name").grid(column=1,row=2, sticky=tk.W)
settingsLabel_3=ttk.Label(settingsFrame_1_1, text="Password").grid(column=1,row=3, sticky=tk.W)
settingsLabel_4=ttk.Label(settingsFrame_1_1, text="Porn Number").grid(column=1,row=4, sticky=tk.W)
settingsLabel_5=ttk.Label(settingsFrame_1_1, text="Host").grid(column=1,row=5, sticky=tk.W)
settingsLabel_6=ttk.Label(settingsFrame_1_1, text="Language").grid(column=3,row=1)
settingsUserNameEntered=tk.StringVar()
settingsUserNameEntry=ttk.Entry(settingsFrame_1_1, width=20, textvariable=settingsUserNameEntered).grid(column=2,row=2)
settingsPasswordEntered=tk.StringVar()
settingsPasswordEntry=ttk.Entry(settingsFrame_1_1, width=20, textvariable=settingsPasswordEntered).grid(column=2,row=3)
settingsPortNumberEntered=tk.StringVar()
settingsPortNumberEntry=ttk.Entry(settingsFrame_1_1, width=20, textvariable=settingsPortNumberEntered).grid(column=2,row=4)
settingsHostEntered=tk.StringVar()
settingsHostEntry=ttk.Entry(settingsFrame_1_1, width=20, textvariable=settingsHostEntered).grid(column=2,row=5)
settingsRadionEntered = tk.IntVar()
settingsRadion_1=tk.Radiobutton(settingsFrame_1_1, text="English", variable=settingsRadionEntered, value=1, command="")
settingsRadion_1.grid(column=3, row=2, sticky=tk.W, columnspan=3)   
settingsRadion_2=tk.Radiobutton(settingsFrame_1_1, text="Deutsch", variable=settingsRadionEntered, value=2, command="")
settingsRadion_2.grid(column=3, row=3, sticky=tk.W, columnspan=3)  
settingsRadion_3=tk.Radiobutton(settingsFrame_1_1, text="Srpski", variable=settingsRadionEntered, value=3, command="")
settingsRadion_3.grid(column=3, row=4, sticky=tk.W, columnspan=3)
settingsRadion_1.configure(state="disabled")
settingsRadion_2.configure(state="disabled")
settingsRadion_3.configure(state="disabled")
settingsSaveButton=ttk.Button(settingsFrame_1_1, text="Save", command="").grid(column=2, row=6, sticky=tk.W)

#tab2
settingsFrame_2_1=ttk.Frame(settingsFrame_2)
settingsFrame_2_1.pack(expand=1, fill="both")
settingsTextList_1=scrolledtext.ScrolledText(settingsFrame_2_1, width=100, height=100, wrap=tk.WORD)
settingsTextList_1.grid(column=0, columnspan=1)
settingsTextList_1.configure(state="disabled")

#=================================
#Show/Hide default settings for the frames
#=================================

subsubtoolbarFrame_1.grid()
subsubtoolbarFrame_2.grid_forget()
subsubtoolbarFrame_3.grid_forget()
subsubtoolbarFrame_4.grid_forget()
subsubtoolbarFrame_5.grid_forget()
#=========

#Start GUI
#=========
win.mainloop()