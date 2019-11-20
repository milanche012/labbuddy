import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import scrolledtext
from tkinter import Scrollbar

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
        mycursor.execute("CREATE TABLE IF NOT EXISTS openlaboratory.lab_res_chem (`res_chem_id` INT NOT NULL AUTO_INCREMENT,`res_chem_f_name` VARCHAR(20) NOT NULL,`res_chem_l_name` VARCHAR(20) NOT NULL,`res_chem_address` VARCHAR(20) NOT NULL,`res_chem_date` VARCHAR(20) NOT NULL,`res_chem_type` VARCHAR(20) NOT NULL,`res_chem_serial` VARCHAR(20) NOT NULL,`res_chem_odor` VARCHAR(20) NOT NULL,`res_chem_taste` VARCHAR(20) NOT NULL,`res_chem_turb` VARCHAR(20) NOT NULL,`res_chem_color` VARCHAR(20) NOT NULL,`res_chem_ph` VARCHAR(20) NOT NULL,`res_chem_no3` VARCHAR(20) NOT NULL,`res_chem_no2` VARCHAR(20) NOT NULL,`res_chem_nh3` VARCHAR(20) NOT NULL,`res_chem_cl` VARCHAR(20) NOT NULL,`res_chem_fe` VARCHAR(20) NOT NULL,`res_chem_mn` VARCHAR(20) NOT NULL,`res_chem_kmno4` VARCHAR(20) NOT NULL,`res_chem_elec` VARCHAR(20) NOT NULL,`res_chem_descript` VARCHAR(20) NOT NULL, PRIMARY KEY (`res_chem_id`), UNIQUE INDEX `res_chem_serial_UNIQUE` (`res_chem_serial` ASC));")
        mycursor.execute("CREATE TABLE IF NOT EXISTS openlaboratory.lab_res_micro (`res_micro_id` INT NOT NULL AUTO_INCREMENT,`res_micro_f_name` VARCHAR(20) NOT NULL,`res_micro_l_name` VARCHAR(20) NOT NULL,`res_micro_addres` VARCHAR(20) NOT NULL,`res_micro_date` VARCHAR(20) NOT NULL,`res_micro_type` VARCHAR(20) NOT NULL,`res_micro_serial` VARCHAR(20) NOT NULL,`res_micro_meso` VARCHAR(20) NOT NULL,`res_micro_coli` VARCHAR(20) NOT NULL,`res_micro_f_colli` VARCHAR(20) NOT NULL,`res_micro_f_strept` VARCHAR(20) NOT NULL,`res_micro_prot` VARCHAR(20) NOT NULL,`res_micro_pseudo` VARCHAR(20) NOT NULL,`res_micro_clos` VARCHAR(20) NOT NULL,`res_micro_descript` VARCHAR(20) NOT NULL, PRIMARY KEY (`res_micro_id`), UNIQUE INDEX `res_micro_serial_UNIQUE` (`res_micro_serial` ASC));")

        
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

def showHide_2():
    subsubtoolbarFrame_1.grid_forget()
    subsubtoolbarFrame_2.grid()
    subsubtoolbarFrame_3.grid_forget()

def showHide_3():
    subsubtoolbarFrame_1.grid_forget()
    subsubtoolbarFrame_2.grid_forget()
    subsubtoolbarFrame_3.grid()  
    
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
            toolButton_2.grid(column=2, row=1)
            toolButton_3.grid(column=3, row=1)
            return LogID[0]
            
    except:
        pass
#==========================
#Class New Chemistry Result
#==========================
class newChemRes:
    def __init__(self, f_name, l_name, address, date, res_type, serial, odor, taste, turbidity, color, ph, no3, no2, nh3, cl, fe, mn, kmno4, el_conduction, description):
        self.f_name=f_name
        self.l_name=l_name
        self.address=address
        self.date=date
        self.res_type=res_type
        self.serial=serial
        self.odor=odor
        self.taste=taste
        self.turbidity=turbidity
        self.color=color
        self.ph=ph
        self.no3=no3
        self.no2=no2
        self.nh3=nh3
        self.cl=cl
        self.fe=fe
        self.mn=mn
        self.kmno4=kmno4
        self.el_conduction=el_conduction
        self.description=description
    
    # Validating the existance of the serial number
    def validateSerial(self): 
        mydb=connectToServer(serverSettingsUser,serverSettingsPassword,serverSettingsPortNumber,serverSettingsHost)
        mycursor=mydb.cursor()
        checkResSerialSQL="SELECT COUNT(*) FROM openlaboratory.lab_res_chem WHERE res_chem_serial = %s;"
        mycursor.execute(checkResSerialSQL,(self.serial, ))
        checkResSerialResult=mycursor.fetchall()
        result=int(checkResSerialResult[0][0])
        if (result>=1):
            messagebox.showerror("Serial error", "Typed serial number is in use. Please check the serial number again.")
            resSerial=False
        else:
            resSerial=True
            return resSerial
        
    # Validating if the form is corect   
    def validateForm(self): 
        if self.f_name and self.l_name and  self.address and  self.date and  self.res_type and  self.serial and  self.odor and  self.taste and  self.turbidity and  self.color and  self.ph and  self.no3 and  self.no2 and  self.nh3 and  self.cl and  self.fe and  self.mn and  self.kmno4 and  self.el_conduction and  self.description:
            
            form=True
            return form
        else:
            form=False
            messagebox.showerror("Form error", "Please check the form")
            return form
            
    # Creating a new chemistry result
    def createNewChemRes(self):
        mydb=connectToServer(serverSettingsUser,serverSettingsPassword,serverSettingsPortNumber,serverSettingsHost)
        mycursor=mydb.cursor()
        newChemResSQL="INSERT INTO openlaboratory.lab_res_chem (res_chem_f_name, res_chem_l_name,res_chem_address, res_chem_date, res_chem_type, res_chem_serial, res_chem_odor, res_chem_taste, res_chem_turb, res_chem_color, res_chem_ph, res_chem_no3, res_chem_no2, res_chem_nh3, res_chem_cl, res_chem_fe, res_chem_mn, res_chem_kmno4, res_chem_elec, res_chem_descript ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        newChemRes=(self.f_name, self.l_name, self.address, self.date, self.res_type, self.serial, self.odor, self.taste, self.turbidity, self.color, self.ph, self.no3, self.no2, self.nh3, self.cl, self.fe, self.mn, self.kmno4, self.el_conduction, self.description)
        mycursor.execute(newChemResSQL, newChemRes)
        mydb.commit()
        messagebox.showinfo("New Chemistry Result", "New Chemistry Result Entered")

        
#==========================================================================
# Starting to enter a new chemistry result after clicking the Add button
#========================================================================== 
def startNewChemResult():
    # Geting the info for the new chemistry result process
    try:
        chemResultInfo1=resultsAddFirstNameEntered.get()
        chemResultInfo2=resultsAddLastNameEntered.get()
        chemResultInfo3=resultsAddAddressEntered.get()
        chemResultInfo4=resultsAddDateEntered.get()
        chemResultInfo5=resultsAddTypeEntered.get()
        chemResultInfo6=resultsAddIdEntered.get()
        chemResultInfo7=resultsAddOdorEntered.get()
        chemResultInfo8=resultsAddTasteEntered.get()
        chemResultInfo9=resultsAddTurbidityEntered.get()
        chemResultInfo10=resultsAddColorEntered.get()
        chemResultInfo11=resultsAddPhEntered.get()
        chemResultInfo12=resultsAddNO3Entered.get()
        chemResultInfo13=resultsAddNO2Entered.get()
        chemResultInfo14=resultsAddNH3Entered.get()
        chemResultInfo15=resultsAddClEntered.get()
        chemResultInfo16=resultsAddFeEntered.get()
        chemResultInfo17=resultsAddMnEntered.get()
        chemResultInfo18=resultsAddKMnO4Entered.get()
        chemResultInfo19=resultsAddElConductivityEntered.get()
        chemResultInfo20=resultsTextList_2.get('1.0', tk.END)
        startingNewChemResult=newChemRes(chemResultInfo1, chemResultInfo2, chemResultInfo3, chemResultInfo4, chemResultInfo5, chemResultInfo6, chemResultInfo7, chemResultInfo8, chemResultInfo9, chemResultInfo10, chemResultInfo11, chemResultInfo12, chemResultInfo13, chemResultInfo14, chemResultInfo15, chemResultInfo16, chemResultInfo17, chemResultInfo18, chemResultInfo19, chemResultInfo20)
        validateSerial=startingNewChemResult.validateSerial()
        validateForm=startingNewChemResult.validateForm()
        if (validateSerial==True) and (validateForm==True):
            startingNewChemResult.createNewChemRes()
            
    except:
        pass
#===============================
#Searching for Chemistry Results
#===============================
def findChemResult(): 
    
    findChemResultInfo1=resultsEditIdEntered.get()
    mydb=connectToServer(serverSettingsUser,serverSettingsPassword,serverSettingsPortNumber,serverSettingsHost)
    mycursor=mydb.cursor()
    findChemResSQL="SELECT COUNT(*) FROM openlaboratory.lab_res_chem WHERE res_chem_serial = %s;"
    mycursor.execute(findChemResSQL,(findChemResultInfo1, ))
    findChemResResult=mycursor.fetchall()
    result=int(findChemResResult[0][0])
    if (result!=1):
        messagebox.showerror("Serial error", "No serial number in use. Please check the serial number again.")
        resSerial=False
        return resSerial
    else:
        resSerial=True
        getChemResSQL="SELECT * FROM openlaboratory.lab_res_chem WHERE res_chem_serial = %s;"
        mycursor.execute(getChemResSQL,(findChemResultInfo1, ))
        getChemResResult=mycursor.fetchall()
        resultsEditFirstNameEntered.set(getChemResResult[0][1])
        resultsEditLastNameEntered.set(getChemResResult[0][2])
        resultsEditAddressEntered.set(getChemResResult[0][3])
        resultsEditDateEntered.set(getChemResResult[0][4])
        resultsEditTypeEntered.set(getChemResResult[0][5])
        resultsEditIdEntered.set(getChemResResult[0][6])
        resultsEditOdorEntered.set(getChemResResult[0][7])
        resultsEditTasteEntered.set(getChemResResult[0][8])
        resultsEditTurbidityEntered.set(getChemResResult[0][9])
        resultsEditColorEntered.set(getChemResResult[0][10])
        resultsEditPhEntered.set(getChemResResult[0][11])
        resultsEditNO3Entered.set(getChemResResult[0][12])
        resultsEditNO2Entered.set(getChemResResult[0][13])
        resultsEditNH3Entered.set(getChemResResult[0][14])
        resultsEditClEntered.set(getChemResResult[0][15])
        resultsEditFeEntered.set(getChemResResult[0][16])
        resultsEditMnEntered.set(getChemResResult[0][17])
        resultsEditKMnO4Entered.set(getChemResResult[0][18])
        resultsEditElConductivityEntered.set(getChemResResult[0][19])
        resultsTextList_4.delete(1.0, tk.END)
        resultsTextList_4.insert(1.0, getChemResResult[0][20])
        return resSerial

#===============================
#Editing Chemistry Results
#===============================
def editChemResult(): 
    
    editChemResultInfo1=resultsEditIdEntered.get()
    mydb=connectToServer(serverSettingsUser,serverSettingsPassword,serverSettingsPortNumber,serverSettingsHost)
    mycursor=mydb.cursor()
    editChemResSQL="SELECT COUNT(*) FROM openlaboratory.lab_res_chem WHERE res_chem_serial = %s;"
    mycursor.execute(editChemResSQL,(editChemResultInfo1, ))
    editChemResResult=mycursor.fetchall()
    result=int(editChemResResult[0][0])
    if (result!=1):
        messagebox.showerror("Serial error", "No serial number in use. Please check the serial number again.")
        resSerial=False
        return resSerial
    else:
        editChemResultInfo1=resultsEditFirstNameEntered.get()
        editChemResultInfo2=resultsEditLastNameEntered.get()
        editChemResultInfo3=resultsEditAddressEntered.get()
        editChemResultInfo4=resultsEditDateEntered.get()
        editChemResultInfo5=resultsEditTypeEntered.get()
        editChemResultInfo6=resultsEditIdEntered.get()
        editChemResultInfo7=resultsEditOdorEntered.get()
        editChemResultInfo8=resultsEditTasteEntered.get()
        editChemResultInfo9=resultsEditTurbidityEntered.get()
        editChemResultInfo10=resultsEditColorEntered.get()
        editChemResultInfo11=resultsEditPhEntered.get()
        editChemResultInfo12=resultsEditNO3Entered.get()
        editChemResultInfo13=resultsEditNO2Entered.get()
        editChemResultInfo14=resultsEditNH3Entered.get()
        editChemResultInfo15=resultsEditClEntered.get()
        editChemResultInfo16=resultsEditFeEntered.get()
        editChemResultInfo17=resultsEditMnEntered.get()
        editChemResultInfo18=resultsEditKMnO4Entered.get()
        editChemResultInfo19=resultsEditElConductivityEntered.get()
        editChemResultInfo20=resultsTextList_4.get('1.0', tk.END)
        resSerial=True
        getChemResSQL="UPDATE openlaboratory.lab_res_chem SET res_chem_f_name=%s, res_chem_l_name=%s, res_chem_address=%s, res_chem_date=%s, res_chem_type=%s, res_chem_serial=%s, res_chem_odor=%s, res_chem_taste=%s, res_chem_turb=%s, res_chem_color=%s, res_chem_ph=%s, res_chem_no3=%s, res_chem_no2=%s, res_chem_nh3=%s, res_chem_cl=%s, res_chem_fe=%s, res_chem_mn=%s, res_chem_kmno4=%s, res_chem_elec=%s, res_chem_descript=%s WHERE res_chem_serial = %s;"
        mycursor.execute(getChemResSQL,(editChemResultInfo1,editChemResultInfo2,editChemResultInfo3,editChemResultInfo4,editChemResultInfo5,editChemResultInfo6,editChemResultInfo7,editChemResultInfo8,editChemResultInfo9,editChemResultInfo10,editChemResultInfo11,editChemResultInfo12,editChemResultInfo13,editChemResultInfo14,editChemResultInfo15,editChemResultInfo16,editChemResultInfo17,editChemResultInfo18,editChemResultInfo19,editChemResultInfo20,editChemResultInfo6 ))
        mydb.commit()
        messagebox.showinfo("Edit Chemistry Result", "Chemistry Result Edited")

     
        return resSerial
    
#==========================
#Class New Microbiology Result
#==========================
class newMicroRes:
    def __init__(self, f_name, l_name, address, date, res_type, serial, meso, coli, f_coli, f_strept, prot, pseudo, clos, description):
        self.f_name=f_name
        self.l_name=l_name
        self.address=address
        self.date=date
        self.res_type=res_type
        self.serial=serial
        self.meso=meso
        self.coli=coli
        self.f_coli=f_coli
        self.f_strept=f_strept
        self.prot=prot
        self.pseudo=pseudo
        self.clos=clos
        self.description=description
    
    # Validating the existance of the serial number
    def validateSerial(self): 
        mydb=connectToServer(serverSettingsUser,serverSettingsPassword,serverSettingsPortNumber,serverSettingsHost)
        mycursor=mydb.cursor()
        checkResSerialSQL="SELECT COUNT(*) FROM openlaboratory.lab_res_micro WHERE res_micro_serial = %s;"
        mycursor.execute(checkResSerialSQL,(self.serial, ))
        checkResSerialResult=mycursor.fetchall()
        result=int(checkResSerialResult[0][0])
        if (result>=1):
            messagebox.showerror("Serial error", "Typed serial number is in use. Please check the serial number again.")
            resSerial=False
        else:
            resSerial=True
            return resSerial
        
    # Validating if the form is corect   
    def validateForm(self): 
        if self.f_name and self.l_name and  self.address and  self.date and  self.res_type and  self.serial and  self.meso and  self.coli and  self.f_coli and  self.f_strept and  self.prot and  self.pseudo and  self.clos and  self.description:
            
            form=True
            return form
        else:
            form=False
            messagebox.showerror("Form error", "Please check the form")
            return form
            
    # Creating a new Micorbiology result
    def createNewMicroRes(self):
        mydb=connectToServer(serverSettingsUser,serverSettingsPassword,serverSettingsPortNumber,serverSettingsHost)
        mycursor=mydb.cursor()
        newMicroResSQL="INSERT INTO openlaboratory.lab_res_micro (res_micro_f_name, res_micro_l_name, res_micro_address, res_micro_date, res_micro_type, res_micro_serial, res_micro_meso, res_micro_coli, res_micro_f_coli, res_micro_f_strept, res_micro_prot, res_micro_pseudo, res_micro_clos, res_micro_descript ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        newMicroRes=(self.f_name, self.l_name, self.address, self.date, self.res_type, self.serial, self.meso, self.coli, self.f_coli, self.f_strept, self.prot, self.pseudo, self.clos, self.description)
        mycursor.execute(newMicroResSQL, newMicroRes)
        mydb.commit()
        messagebox.showinfo("New Micorbiology Result", "New Micorbiology Result Entered")

        
#==========================================================================
# Starting to enter a new Microbiology result after clicking the Add button
#========================================================================== 
def startNewMicroResult():
    # Geting the info for the new microbiology result process
    try:
        microResultInfo1=resultsAddMicroFirstNameEntered.get()
        microResultInfo2=resultsAddMicroLastNameEntered.get()
        microResultInfo3=resultsAddMicroAddressEntered.get()
        microResultInfo4=resultsAddMicroDateEntered.get()
        microResultInfo5=resultsAddMicroTypeEntered.get()
        microResultInfo6=resultsAddMicroIdEntered.get()
        microResultInfo7=resultsAddMicroAerobicMesophilicEntered.get()
        microResultInfo8=resultsAddMicroColiformEntered.get()
        microResultInfo9=resultsAddMicroFaecalColiformEntered.get()
        microResultInfo10=resultsAddMicroStreptococciEntered.get()
        microResultInfo11=resultsAddMicroProteusEntered.get()
        microResultInfo12=resultsAddMicroPseudomonasEntered.get()
        microResultInfo13=resultsAddMicroClostridiaEntered.get()
        microResultInfo14=resultsTextList_3.get('1.0', tk.END)
        startingNewMicroResult=newMicroRes(microResultInfo1, microResultInfo2, microResultInfo3, microResultInfo4, microResultInfo5, microResultInfo6, microResultInfo7, microResultInfo8, microResultInfo9, microResultInfo10, microResultInfo11, microResultInfo12, microResultInfo13, microResultInfo14)
        validateSerial=startingNewMicroResult.validateSerial()
        validateForm=startingNewMicroResult.validateForm()
        if (validateSerial==True) and (validateForm==True):
            startingNewMicroResult.createNewMicroRes()
            
    except:
        pass
#===============================
#Searching for Microbiology Results
#===============================
def findMicroResult(): 
    
    findMicroResultInfo1=resultsEditMicroIdEntered.get()
    mydb=connectToServer(serverSettingsUser,serverSettingsPassword,serverSettingsPortNumber,serverSettingsHost)
    mycursor=mydb.cursor()
    findMicroResSQL="SELECT COUNT(*) FROM openlaboratory.lab_res_micro WHERE res_micro_serial = %s;"
    mycursor.execute(findMicroResSQL,(findMicroResultInfo1, ))
    findMicroResResult=mycursor.fetchall()
    result=int(findMicroResResult[0][0])
    if (result!=1):
        messagebox.showerror("Serial error", "No serial number in use. Please check the serial number again.")
        resSerial=False
        return resSerial
    else:
        resSerial=True
        getMicroResSQL="SELECT * FROM openlaboratory.lab_res_micro WHERE res_micro_serial = %s;"
        mycursor.execute(getMicroResSQL,(findMicroResultInfo1, ))
        getMicroResResult=mycursor.fetchall()
        resultsEditMicroFirstNameEntered.set(getMicroResResult[0][1])
        resultsEditMicroLastNameEntered.set(getMicroResResult[0][2])
        resultsEditMicroAddressEntered.set(getMicroResResult[0][3])
        resultsEditMicroDateEntered.set(getMicroResResult[0][4])
        resultsEditMicroTypeEntered.set(getMicroResResult[0][5])
        resultsEditMicroIdEntered.set(getMicroResResult[0][6])
        resultsEditMicroAerobicMesophilicEntered.set(getMicroResResult[0][7])
        resultsEditMicroColiformEntered.set(getMicroResResult[0][8])
        resultsEditMicroFaecalColiformEntered.set(getMicroResResult[0][9])
        resultsEditMicroStreptococciEntered.set(getMicroResResult[0][10])
        resultsEditMicroProteusEntered.set(getMicroResResult[0][11])
        resultsEditMicroPseudomonasEntered.set(getMicroResResult[0][12])
        resultsEditMicroClostridiaEntered.set(getMicroResResult[0][13])
        resultsTextList_5.delete(1.0, tk.END)
        resultsTextList_5.insert(1.0, getMicroResResult[0][14])
        return resSerial

#===============================
#Editing Microbiology Results
#===============================
def editMicroResult(): 
    
    editMicroResultInfo1=resultsEditIdEntered.get()
    mydb=connectToServer(serverSettingsUser,serverSettingsPassword,serverSettingsPortNumber,serverSettingsHost)
    mycursor=mydb.cursor()
    editMicroResSQL="SELECT COUNT(*) FROM openlaboratory.lab_res_micro WHERE res_micro_serial = %s;"
    mycursor.execute(editMicroResSQL,(editMicroResultInfo1, ))
    editMicroResResult=mycursor.fetchall()
    result=int(editMicroResResult[0][0])
    if (result!=1):
        messagebox.showerror("Serial error", "No serial number in use. Please check the serial number again.")
        resSerial=False
        return resSerial
    else:
        editMicroResultInfo1=resultsEditMicroFirstNameEntered.get()
        editMicroResultInfo2=resultsEditMicroLastNameEntered.get()
        editMicroResultInfo3=resultsEditMicroAddressEntered.get()
        editMicroResultInfo4=resultsEditMicroDateEntered.get()
        editMicroResultInfo5=resultsEditMicroTypeEntered.get()
        editMicroResultInfo6=resultsEditMicroIdEntered.get()
        editMicroResultInfo7=resultsEditMicroAerobicMesophilicEntered.get()
        editMicroResultInfo8=resultsEditMicroColiformEntered.get()
        editMicroResultInfo9=resultsEditMicroFaecalColiformEntered.get()
        editMicroResultInfo10=resultsEditMicroStreptococciEntered.get()
        editMicroResultInfo11=resultsEditMicroProteusEntered.get()
        editMicroResultInfo12=resultsEditMicroPseudomonasEntered.get()
        editMicroResultInfo13=resultsEditMicroClostridiaEntered.get()
        editMicroResultInfo14=resultsTextList_5.get('1.0', tk.END)
        resSerial=True
        getMicroResSQL="UPDATE openlaboratory.lab_res_micro SET res_micro_f_name=%s, res_micro_l_name=%s, res_micro_address=%s, res_micro_date=%s, res_micro_type=%s, res_micro_serial=%s, res_micro_meso=%s, res_micro_coli=%s, res_micro_f_coli=%s, res_micro_f_strept=%s, res_micro_prot=%s, res_micro_pseudo=%s, res_micro_clos=%s, res_micro_descript=%s WHERE res_micro_serial = %s;"
        mycursor.execute(getMicroResSQL,(editMicroResultInfo1,editMicroResultInfo2,editMicroResultInfo3,editMicroResultInfo4,editMicroResultInfo5,editMicroResultInfo6,editMicroResultInfo7,editMicroResultInfo8,editMicroResultInfo9,editMicroResultInfo10,editMicroResultInfo11,editMicroResultInfo12,editMicroResultInfo13,editMicroResultInfo14,editMicroResultInfo6 ))
        mydb.commit()
        messagebox.showinfo("Edit Chemistry Result", "Chemistry Result Edited")

     
        return resSerial    
#===============================
#Searching for All Results
#===============================
def findAllResult(): 
   
    findAllResultInfo1=resultsFindAllFirstNameEntered.get()
    findAllResultInfo2=resultsFindAllLastNameEntered.get()
    findAllResultInfo3=resultsFindAllCategoryEntered.get()
    if findAllResultInfo3=="Chemistry":
        resultsTree_1["columns"]=("1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20")
        resultsTree_1.column("#0", width=50, minwidth=25)
        resultsTree_1.column("1", width=50, minwidth=25)
        resultsTree_1.column("2", width=50, minwidth=25)
        resultsTree_1.column("3", width=50, minwidth=25)
        resultsTree_1.column("4", width=50, minwidth=25)
        resultsTree_1.column("5", width=50, minwidth=25)
        resultsTree_1.column("6", width=50, minwidth=25)
        resultsTree_1.column("7", width=50, minwidth=25)
        resultsTree_1.column("8", width=50, minwidth=25)
        resultsTree_1.column("9", width=50, minwidth=25)
        resultsTree_1.column("10", width=50, minwidth=25)
        resultsTree_1.column("11", width=50, minwidth=25)
        resultsTree_1.column("12", width=50, minwidth=25)
        resultsTree_1.column("13", width=50, minwidth=25)
        resultsTree_1.column("14", width=50, minwidth=25)
        resultsTree_1.column("15", width=50, minwidth=25)
        resultsTree_1.column("16", width=50, minwidth=25)
        resultsTree_1.column("17", width=50, minwidth=25)
        resultsTree_1.column("18", width=50, minwidth=25)
        resultsTree_1.column("19", width=50, minwidth=25)
        resultsTree_1.column("20", width=50, minwidth=25)
        resultsTree_1.heading("#0",text="ID",anchor=tk.W)
        resultsTree_1.heading("1",text="First Name",anchor=tk.W)
        resultsTree_1.heading("2",text="Last Name",anchor=tk.W)
        resultsTree_1.heading("3",text="Address",anchor=tk.W)
        resultsTree_1.heading("4",text="Date",anchor=tk.W)
        resultsTree_1.heading("5",text="Type",anchor=tk.W)
        resultsTree_1.heading("6",text="Serial No",anchor=tk.W)
        resultsTree_1.heading("7",text="Odor",anchor=tk.W)
        resultsTree_1.heading("8",text="Taste",anchor=tk.W)
        resultsTree_1.heading("9",text="Turbidity",anchor=tk.W)
        resultsTree_1.heading("10",text="Color",anchor=tk.W)
        resultsTree_1.heading("11",text="Ph Value",anchor=tk.W)
        resultsTree_1.heading("12",text="NO3",anchor=tk.W)
        resultsTree_1.heading("13",text="NO2",anchor=tk.W)
        resultsTree_1.heading("14",text="NH3",anchor=tk.W)
        resultsTree_1.heading("15",text="Cl",anchor=tk.W)
        resultsTree_1.heading("16",text="Fe",anchor=tk.W)
        resultsTree_1.heading("17",text="Mn",anchor=tk.W)
        resultsTree_1.heading("18",text="KMnO4",anchor=tk.W)
        resultsTree_1.heading("19",text="El. Conduction",anchor=tk.W)
        resultsTree_1.heading("20",text="Additional Information",anchor=tk.W)
        findAllResSQL="SELECT * FROM openlaboratory.lab_res_chem WHERE res_chem_f_name = %s AND res_chem_l_name = %s;"
        mydb=connectToServer(serverSettingsUser,serverSettingsPassword,serverSettingsPortNumber,serverSettingsHost)
        mycursor=mydb.cursor()
        mycursor.execute(findAllResSQL,(findAllResultInfo1,findAllResultInfo2, ))
        findAllResResult=mycursor.fetchall() 
        i=0
        for listResult in findAllResResult:
            resultsTree_1.insert("", i, text=listResult[0], values=(listResult[1],listResult[2],listResult[3],listResult[4],listResult[5],listResult[6],listResult[7],listResult[8],listResult[9],listResult[10],listResult[11],listResult[12],listResult[13],listResult[14],listResult[15],listResult[16],listResult[17],listResult[18],listResult[19],listResult[20]))
            i=i+1  
    elif findAllResultInfo3=="Microbiology":
        resultsTree_1["columns"]=("1","2","3","4","5","6","7","8","9","10","11","12","13")
        resultsTree_1.column("#0", width=50, minwidth=25)
        resultsTree_1.column("1", width=50, minwidth=25)
        resultsTree_1.column("2", width=50, minwidth=25)
        resultsTree_1.column("3", width=50, minwidth=25)
        resultsTree_1.column("4", width=50, minwidth=25)
        resultsTree_1.column("5", width=50, minwidth=25)
        resultsTree_1.column("6", width=50, minwidth=25)
        resultsTree_1.column("7", width=50, minwidth=25)
        resultsTree_1.column("8", width=50, minwidth=25)
        resultsTree_1.column("9", width=50, minwidth=25)
        resultsTree_1.column("10", width=50, minwidth=25)
        resultsTree_1.column("11", width=50, minwidth=25)
        resultsTree_1.column("12", width=50, minwidth=25)
        resultsTree_1.column("13", width=50, minwidth=25)
        resultsTree_1.heading("#0",text="ID",anchor=tk.W)
        resultsTree_1.heading("1",text="First Name",anchor=tk.W)
        resultsTree_1.heading("2",text="Last Name",anchor=tk.W)
        resultsTree_1.heading("3",text="Address",anchor=tk.W)
        resultsTree_1.heading("4",text="Date",anchor=tk.W)
        resultsTree_1.heading("5",text="Type",anchor=tk.W)
        resultsTree_1.heading("6",text="Serial No",anchor=tk.W)
        resultsTree_1.heading("7",text="Aerobic Mesophilic Bacteria/1ml",anchor=tk.W)
        resultsTree_1.heading("8",text="Coliform Bacteria/100ml",anchor=tk.W)
        resultsTree_1.heading("9",text="Faecal Streptococci/100ml",anchor=tk.W)
        resultsTree_1.heading("10",text="Proteus Species/100ml",anchor=tk.W)
        resultsTree_1.heading("11",text="Pseudomonas Aeruginosa/100ml",anchor=tk.W)
        resultsTree_1.heading("12",text="Sulfide-reducing Clostridia/100ml",anchor=tk.W)
        resultsTree_1.heading("13",text="Additional Information",anchor=tk.W)

        findAllResSQL="SELECT * FROM openlaboratory.lab_res_micro WHERE res_micro_f_name = %s AND res_micro_l_name = %s;"
        mydb=connectToServer(serverSettingsUser,serverSettingsPassword,serverSettingsPortNumber,serverSettingsHost)
        mycursor=mydb.cursor()
        mycursor.execute(findAllResSQL,(findAllResultInfo1,findAllResultInfo2, ))
        findAllResResult=mycursor.fetchall() 
        i=0
        for listResult in findAllResResult:
            resultsTree_1.insert("", i, text=listResult[0], values=(listResult[1],listResult[2],listResult[3],listResult[4],listResult[5],listResult[6],listResult[7],listResult[8],listResult[9],listResult[10],listResult[11],listResult[12],listResult[13]))
            i=i+1

 
def savingServerSettings():
    # Geting the info for the server settings
    serverInfo1=settingsUserNameEntered.get()
    serverInfo2=settingsPasswordEntered.get()
    serverInfo3=settingsPortNumberEntered.get()
    serverInfo4=settingsHostEntered.get()
    
    newServerSettings={"username":serverInfo1, "password":serverInfo2, "portNumber":serverInfo3, "host":serverInfo4}
    with open("serverSettings.json", "w") as file:
        json.dump(newServerSettings,file)
        
    messagebox.showinfo("New server settings", "Please restart the application to take effect")

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
someFrame.grid(column=0, row=0, sticky=tk.W)
toolbarFrame=ttk.LabelFrame(someFrame, text="Toolbar")
toolbarFrame.grid(column=0, row=1, sticky=tk.W)
subtoolbarFrame=ttk.LabelFrame(someFrame, text="Subtoolbar")
subtoolbarFrame.grid(column=0, row=2, sticky=tk.W)

#=============
#Toolbar icons
#=============
toolButton_1=ttk.Button(toolbarFrame, text="Users", command=showHide_1, width=25)
toolButton_1.grid(column=1, row=1)
toolButton_2=ttk.Button(toolbarFrame, text="Results", command=showHide_2, width=25)
toolButton_2.grid(column=2, row=1)
toolButton_3=ttk.Button(toolbarFrame, text="Settings", command=showHide_3, width=25)
toolButton_3.grid(column=3, row=1)


#==================================
#Frame to show/hide subtoolbar items
#===================================
subsubtoolbarFrame_1=ttk.LabelFrame(subtoolbarFrame, text="SubsubtoolbarFrame_1")
subsubtoolbarFrame_1.grid(column=1, row=0)
subsubtoolbarFrame_2=ttk.LabelFrame(subtoolbarFrame, text="SubsubtoolbarFrame_2")
subsubtoolbarFrame_2.grid(column=2, row=0)
subsubtoolbarFrame_3=ttk.LabelFrame(subtoolbarFrame, text="SubsubtoolbarFrame_3")
subsubtoolbarFrame_3.grid(column=3, row=0)

#==================================
#Subtoolbar items
#===================================

#Page Users
usersTab=ttk.Notebook(subsubtoolbarFrame_1,width=820, height=525)
usersFrame_1=ttk.Frame(usersTab)
usersTab.add(usersFrame_1, text="LogIn")
usersFrame_2=ttk.Frame(usersTab)
usersTab.add(usersFrame_2, text="SingIn")
usersTab.pack(expand=1, fill="both")
#tab1
usersFrame_1_1=ttk.Frame(usersFrame_1)
usersFrame_1_1.pack(fill="none", expand=True)
logUserLabel=ttk.Label(usersFrame_1_1, text="User Name:").grid(column=1,row=1, sticky=tk.W)
logPasswordLabel=ttk.Label(usersFrame_1_1, text="Password:").grid(column=1,row=2, sticky=tk.W)
logUserNameEntered=tk.StringVar()
userNameTK=ttk.Entry(usersFrame_1_1, width=20, textvariable=logUserNameEntered).grid(column=2,row=1)
logPasswordNameEntered=tk.StringVar()
passwordNameTK=ttk.Entry(usersFrame_1_1, width=20, textvariable=logPasswordNameEntered).grid(column=2,row=2)
logUserButton=ttk.Button(usersFrame_1_1, text="Log-in", command=startLogIn).grid(column=2, row=3)
#tab2
usersFrame_2_1=ttk.Frame(usersFrame_2)
usersFrame_2_1.pack(fill="none", expand=True)
newUserLabel=ttk.Label(usersFrame_2_1, text="User Name:").grid(column=1,row=1, sticky=tk.W)
newPasswordLabel=ttk.Label(usersFrame_2_1, text="Password:").grid(column=1,row=2, sticky=tk.W)
renewPasswordLabel=ttk.Label(usersFrame_2_1, text="Re-password:").grid(column=1,row=3, sticky=tk.W)
newUserNameEntered=tk.StringVar()
newUserNameTK=ttk.Entry(usersFrame_2_1, width=20, textvariable=newUserNameEntered).grid(column=2,row=1)
newPasswordNameEntered=tk.StringVar()
newPasswordNameTK=ttk.Entry(usersFrame_2_1, width=20, textvariable=newPasswordNameEntered).grid(column=2,row=2)
renewPasswordNameEntered=tk.StringVar()
renewPasswordNameTK=ttk.Entry(usersFrame_2_1, width=20, textvariable=renewPasswordNameEntered).grid(column=2,row=3)
newUserButton=ttk.Button(usersFrame_2_1, text="Register", command=startRegistration).grid(column=2, row=4)

#Page Results
resultsTab=ttk.Notebook(subsubtoolbarFrame_2,width=820, height=525)
resultsFrame_1=ttk.Frame(resultsTab)
resultsTab.add(resultsFrame_1, text="Find results")
resultsFrame_2=ttk.Frame(resultsTab)
resultsTab.add(resultsFrame_2, text="Add Chemistry results")
resultsFrame_3=ttk.Frame(resultsTab)
resultsTab.add(resultsFrame_3, text="Add Microbiology results")
resultsFrame_4=ttk.Frame(resultsTab)
resultsTab.add(resultsFrame_4, text="Edit Chemistry results")
resultsFrame_5=ttk.Frame(resultsTab)
resultsTab.add(resultsFrame_5, text="Edit Microbiology results")
resultsTab.pack(expand=1, fill="both")

#tab1
resultsFrame_1_1=ttk.Frame(resultsFrame_1)
resultsFrame_1_1.pack(expand=0, fill="both")
resultsLabel_1=ttk.Label(resultsFrame_1_1, text="First Name:").grid(column=1,row=1,sticky=tk.W)
resultsLabel_2=ttk.Label(resultsFrame_1_1, text="Last Name:").grid(column=2,row=1,sticky=tk.W)
resultsLabel_4=ttk.Label(resultsFrame_1_1, text="Category:").grid(column=3,row=1,sticky=tk.W)
resultsFindAllFirstNameEntered=tk.StringVar()
resultsFindAllFirstNameEntry=ttk.Entry(resultsFrame_1_1, width=15, textvariable=resultsFindAllFirstNameEntered).grid(column=1,row=2)
resultsFindAllLastNameEntered=tk.StringVar()
resultsFindAllLastNameEntry=ttk.Entry(resultsFrame_1_1, width=15, textvariable=resultsFindAllLastNameEntered).grid(column=2,row=2)
resultsFindAllCategoryEntered=tk.StringVar()
resultsFindAllCategoryComboBox=ttk.Combobox(resultsFrame_1_1, state="readonly", values=("Chemistry","Microbiology"), width=15, textvariable=resultsFindAllCategoryEntered).grid(column=3, row=2)
resultsFindButton=ttk.Button(resultsFrame_1_1, width=15, text="Find", command=findAllResult).grid(column=4, row=2)
resultsFrame_1_2=ttk.Frame(resultsFrame_1)
resultsFrame_1_2.pack(expand=1, fill="both")
scrollbar_1=tk.Scrollbar(resultsFrame_1_2)
scrollbar_1.pack(side=tk.RIGHT,fill=tk.Y)
scrollbar_2=tk.Scrollbar(resultsFrame_1_2, orient='horizontal')
scrollbar_2.pack(side=tk.BOTTOM,fill=tk.X)
resultsTree_1=ttk.Treeview(resultsFrame_1_2)
resultsTree_1.pack(side=tk.TOP,fill=tk.BOTH, expand=1)
resultsTree_1.config(yscrollcommand=scrollbar_1.set)
scrollbar_1.config(command=resultsTree_1.yview)
resultsTree_1.config(xscrollcommand=scrollbar_2.set)
scrollbar_2.config(command=resultsTree_1.xview)


#tab2
resultsFrame_2_1=ttk.Frame(resultsFrame_2)
resultsFrame_2_1.pack(expand=0, fill="both")
resultsLabel_1=ttk.Label(resultsFrame_2_1, width=20, text="First Name:").grid(column=1,row=1,sticky=tk.W)
resultsLabel_2=ttk.Label(resultsFrame_2_1, width=20, text="Last Name:").grid(column=2,row=1,sticky=tk.W)
resultsLabel_3=ttk.Label(resultsFrame_2_1, width=20, text="Address:").grid(column=3,row=1,sticky=tk.W)
resultsLabel_6=ttk.Label(resultsFrame_2_1, width=20, text="Date:").grid(column=4,row=1,sticky=tk.W)
resultsLabel_5=ttk.Label(resultsFrame_2_1, width=20, text="Type:").grid(column=5,row=1,sticky=tk.W)
resultsLabel_6=ttk.Label(resultsFrame_2_1, width=20, text="Serial No:").grid(column=6,row=1,sticky=tk.W)
resultsAddFirstNameEntered=tk.StringVar()
resultsAddFirstNameEntry=ttk.Entry(resultsFrame_2_1, width=15, textvariable=resultsAddFirstNameEntered).grid(column=1,row=2,sticky=tk.W)
resultsAddLastNameEntered=tk.StringVar()
resultsAddLastNameEntry=ttk.Entry(resultsFrame_2_1, width=15, textvariable=resultsAddLastNameEntered).grid(column=2,row=2,sticky=tk.W)
resultsAddAddressEntered=tk.StringVar()
resultsAddAddressEntry=ttk.Entry(resultsFrame_2_1, width=15, textvariable=resultsAddAddressEntered).grid(column=3,row=2,sticky=tk.W)
resultsAddDateEntered=tk.StringVar()
resultsAddDateEntry=ttk.Entry(resultsFrame_2_1, width=15, textvariable=resultsAddDateEntered).grid(column=4,row=2,sticky=tk.W)
resultsAddTypeEntered=tk.StringVar()
resultsAddTypeComboBox=ttk.Combobox(resultsFrame_2_1, width=12, textvariable=resultsAddTypeEntered).grid(column=5, row=2,sticky=tk.W)
resultsAddIdEntered=tk.StringVar()
resultsAddIdEntry=ttk.Entry(resultsFrame_2_1, width=15, textvariable=resultsAddIdEntered).grid(column=6,row=2,sticky=tk.W)
resultsFrame_2_2=ttk.Frame(resultsFrame_2)
resultsFrame_2_2.pack(expand=1, fill="both")
resultsLabel_7=ttk.Label(resultsFrame_2_2, text="Odor:").grid(column=1,row=1,sticky=tk.W)
resultsLabel_8=ttk.Label(resultsFrame_2_2, text="Taste:").grid(column=2,row=1,sticky=tk.W)
resultsLabel_9=ttk.Label(resultsFrame_2_2, text="Turbidity:").grid(column=3,row=1,sticky=tk.W)
resultsLabel_10=ttk.Label(resultsFrame_2_2, text="Color:").grid(column=4,row=1,sticky=tk.W)
resultsLabel_11=ttk.Label(resultsFrame_2_2, text="Ph value:").grid(column=5,row=1,sticky=tk.W)
resultsLabel_12=ttk.Label(resultsFrame_2_2, text="Nitrates (NO3):").grid(column=6,row=1,sticky=tk.W)
resultsLabel_13=ttk.Label(resultsFrame_2_2, text="Nitrites (NO2):").grid(column=1,row=3,sticky=tk.W)
resultsLabel_14=ttk.Label(resultsFrame_2_2, text="Ammonia (NH3):").grid(column=2,row=3,sticky=tk.W)
resultsLabel_15=ttk.Label(resultsFrame_2_2, text="Chlorides (Cl):").grid(column=3,row=3,sticky=tk.W)
resultsLabel_16=ttk.Label(resultsFrame_2_2, text="Iron (Fe):").grid(column=4,row=3,sticky=tk.W)
resultsLabel_17=ttk.Label(resultsFrame_2_2, text="Manganese (Mn):").grid(column=5,row=3,sticky=tk.W)
resultsLabel_18=ttk.Label(resultsFrame_2_2, text="KMnO4 Consumption:").grid(column=6,row=3,sticky=tk.W)
resultsLabel_19=ttk.Label(resultsFrame_2_2, text="Electrical Coduction:").grid(column=6,row=5,sticky=tk.W)
resultsLabel_20=ttk.Label(resultsFrame_2_2, text="Additional Information:").grid(column=1,row=7,sticky=tk.W, columnspan=2)
resultsAddOdorEntered=tk.StringVar()
resultsAddOdorEntry=ttk.Entry(resultsFrame_2_2, width=15, textvariable=resultsAddOdorEntered).grid(column=1,row=2,sticky=tk.W)
resultsAddTasteEntered=tk.StringVar()
resultsAddTasteEntry=ttk.Entry(resultsFrame_2_2, width=15, textvariable=resultsAddTasteEntered).grid(column=2,row=2,sticky=tk.W)
resultsAddTurbidityEntered=tk.StringVar()
resultsAddTurbidityEntry=ttk.Entry(resultsFrame_2_2, width=15, textvariable=resultsAddTurbidityEntered).grid(column=3,row=2,sticky=tk.W)
resultsAddColorEntered=tk.StringVar()
resultsAddColorEntry=ttk.Entry(resultsFrame_2_2, width=15, textvariable=resultsAddColorEntered).grid(column=4,row=2,sticky=tk.W)
resultsAddPhEntered=tk.StringVar()
resultsAddPhEntry=ttk.Entry(resultsFrame_2_2, width=15, textvariable=resultsAddPhEntered).grid(column=5,row=2,sticky=tk.W)
resultsAddNO3Entered=tk.StringVar()
resultsAddNO3Entry=ttk.Entry(resultsFrame_2_2, width=15, textvariable=resultsAddNO3Entered).grid(column=6,row=2,sticky=tk.W)
resultsAddNO2Entered=tk.StringVar()
resultsAddNO2Entry=ttk.Entry(resultsFrame_2_2, width=15, textvariable=resultsAddNO2Entered).grid(column=1,row=4,sticky=tk.W)
resultsAddNH3Entered=tk.StringVar()
resultsAddNH3Entry=ttk.Entry(resultsFrame_2_2, width=15, textvariable=resultsAddNH3Entered).grid(column=2,row=4,sticky=tk.W)
resultsAddClEntered=tk.StringVar()
resultsAddClEntry=ttk.Entry(resultsFrame_2_2, width=15, textvariable=resultsAddClEntered).grid(column=3,row=4,sticky=tk.W)
resultsAddFeEntered=tk.StringVar()
resultsAddFeEntry=ttk.Entry(resultsFrame_2_2, width=15, textvariable=resultsAddFeEntered).grid(column=4,row=4,sticky=tk.W)
resultsAddMnEntered=tk.StringVar()
resultsAddMnEntry=ttk.Entry(resultsFrame_2_2, width=15, textvariable=resultsAddMnEntered).grid(column=5,row=4,sticky=tk.W)
resultsAddKMnO4Entered=tk.StringVar()
resultsAddKMnO4Entry=ttk.Entry(resultsFrame_2_2, width=15, textvariable=resultsAddKMnO4Entered).grid(column=6,row=4,sticky=tk.W)
resultsAddElConductivityEntered=tk.StringVar()
resultsAddElConductivityEntry=ttk.Entry(resultsFrame_2_2, width=15, textvariable=resultsAddElConductivityEntered).grid(column=6,row=6,sticky=tk.W)
resultsTextList_2=scrolledtext.ScrolledText(resultsFrame_2_2, width=100, height=19,wrap=tk.WORD)
resultsTextList_2.grid(column=1, row=8, columnspan=8)
resultsAddFindButton=ttk.Button(resultsFrame_2_2, width=15, text="Add", command=startNewChemResult).grid(column=6, row=10)

#tab3
resultsFrame_3_1=ttk.Frame(resultsFrame_3)
resultsFrame_3_1.pack(expand=0, fill="both")
resultsLabel_1=ttk.Label(resultsFrame_3_1, width=20, text="First Name:").grid(column=1,row=1,sticky=tk.W)
resultsLabel_2=ttk.Label(resultsFrame_3_1, width=20, text="Last Name:").grid(column=2,row=1,sticky=tk.W)
resultsLabel_3=ttk.Label(resultsFrame_3_1, width=20, text="Address:").grid(column=3,row=1,sticky=tk.W)
resultsLabel_6=ttk.Label(resultsFrame_3_1, width=20, text="Date").grid(column=4,row=1,sticky=tk.W)
resultsLabel_5=ttk.Label(resultsFrame_3_1, width=20, text="Type:").grid(column=5,row=1,sticky=tk.W)
resultsLabel_6=ttk.Label(resultsFrame_3_1, width=20, text="Serial No:").grid(column=6,row=1,sticky=tk.W)
resultsAddMicroFirstNameEntered=tk.StringVar()
resultsAddMicroFirstNameEntry=ttk.Entry(resultsFrame_3_1, width=15, textvariable=resultsAddMicroFirstNameEntered).grid(column=1,row=2,sticky=tk.W)
resultsAddMicroLastNameEntered=tk.StringVar()
resultsAddMicroLastNameEntry=ttk.Entry(resultsFrame_3_1, width=15, textvariable=resultsAddMicroLastNameEntered).grid(column=2,row=2,sticky=tk.W)
resultsAddMicroAddressEntered=tk.StringVar()
resultsAddMicroAddressEntry=ttk.Entry(resultsFrame_3_1, width=15, textvariable=resultsAddMicroAddressEntered).grid(column=3,row=2,sticky=tk.W)
resultsAddMicroDateEntered=tk.StringVar()
resultsAddMicroDateEntry=ttk.Entry(resultsFrame_3_1, width=15, textvariable=resultsAddMicroDateEntered).grid(column=4,row=2,sticky=tk.W)
resultsAddMicroTypeEntered=tk.StringVar()
resultsAddMicroTypeComboBox=ttk.Combobox(resultsFrame_3_1, width=12, textvariable=resultsAddMicroTypeEntered).grid(column=5, row=2,sticky=tk.W)
resultsAddMicroIdEntered=tk.StringVar()
resultsAddMicroIdEntry=ttk.Entry(resultsFrame_3_1, width=15, textvariable=resultsAddMicroIdEntered).grid(column=6,row=2,sticky=tk.W)
resultsFrame_3_2=ttk.Frame(resultsFrame_3)
resultsFrame_3_2.pack(expand=1, fill="both")
resultsLabel_7=ttk.Label(resultsFrame_3_2, text="Aero. Meso. Bact.:").grid(column=1,row=3,sticky=tk.W)
resultsLabel_8=ttk.Label(resultsFrame_3_2, text="Coliform Bact.:").grid(column=2,row=3,sticky=tk.W)
resultsLabel_9=ttk.Label(resultsFrame_3_2, text="F. Coliform Bact.:").grid(column=3,row=3,sticky=tk.W)
resultsLabel_10=ttk.Label(resultsFrame_3_2, text="F. Streptococci:").grid(column=4,row=3,sticky=tk.W)
resultsLabel_11=ttk.Label(resultsFrame_3_2, text="Proteus Spp.:").grid(column=5,row=3,sticky=tk.W)
resultsLabel_12=ttk.Label(resultsFrame_3_2, text="Pseudo. Aeruginosa:").grid(column=6,row=3,sticky=tk.W)
resultsLabel_13=ttk.Label(resultsFrame_3_2, text="Sulfide Clostridia:").grid(column=6,row=5,sticky=tk.W)
resultsLabel_20=ttk.Label(resultsFrame_3_2, text="Additional Information:").grid(column=1,row=7,sticky=tk.W, columnspan=2)
resultsAddMicroAerobicMesophilicEntered=tk.StringVar()
resultsAddMicroAerobicMesophilicEntry=ttk.Entry(resultsFrame_3_2, width=15, textvariable=resultsAddMicroAerobicMesophilicEntered).grid(column=1,row=4,sticky=tk.W)
resultsAddMicroColiformEntered=tk.StringVar()
resultsAddMicroColiformEntry=ttk.Entry(resultsFrame_3_2, width=15, textvariable=resultsAddMicroColiformEntered).grid(column=2,row=4,sticky=tk.W)
resultsAddMicroFaecalColiformEntered=tk.StringVar()
resultsAddMicroFaecalColiformEntry=ttk.Entry(resultsFrame_3_2, width=15, textvariable=resultsAddMicroFaecalColiformEntered).grid(column=3,row=4,sticky=tk.W)
resultsAddMicroStreptococciEntered=tk.StringVar()
resultsAddMicroStreptococciEntry=ttk.Entry(resultsFrame_3_2, width=15, textvariable=resultsAddMicroStreptococciEntered).grid(column=4,row=4,sticky=tk.W)
resultsAddMicroProteusEntered=tk.StringVar()
resultsAddMicroProteusEntry=ttk.Entry(resultsFrame_3_2, width=15, textvariable=resultsAddMicroProteusEntered).grid(column=5,row=4,sticky=tk.W)
resultsAddMicroPseudomonasEntered=tk.StringVar()
resultsAddMicroPseudomonasEntry=ttk.Entry(resultsFrame_3_2, width=15, textvariable=resultsAddMicroPseudomonasEntered).grid(column=6,row=4,sticky=tk.W)
resultsAddMicroClostridiaEntered=tk.StringVar()
resultsAddMicroClostridiaEntry=ttk.Entry(resultsFrame_3_2, width=15, textvariable=resultsAddMicroClostridiaEntered).grid(column=6,row=6,sticky=tk.W)
resultsTextList_3=scrolledtext.ScrolledText(resultsFrame_3_2, width=100, height=22, wrap=tk.WORD)
resultsTextList_3.grid(column=1, row=8, columnspan=6)
resultsFindButton=ttk.Button(resultsFrame_3_2, width=15, text="Add", command=startNewMicroResult).grid(column=4, row=9)

#tab4
resultsFrame_4_1=ttk.Frame(resultsFrame_4)
resultsFrame_4_1.pack(expand=0, fill="both")
resultsLabel_1=ttk.Label(resultsFrame_4_1, width=20, text="First Name:").grid(column=1,row=1,sticky=tk.W)
resultsLabel_2=ttk.Label(resultsFrame_4_1, width=20, text="Last Name:").grid(column=2,row=1,sticky=tk.W)
resultsLabel_3=ttk.Label(resultsFrame_4_1, width=20, text="Address:").grid(column=3,row=1,sticky=tk.W)
resultsLabel_6=ttk.Label(resultsFrame_4_1, width=20, text="Date:").grid(column=4,row=1,sticky=tk.W)
resultsLabel_5=ttk.Label(resultsFrame_4_1, width=20, text="Type:").grid(column=5,row=1,sticky=tk.W)
resultsLabel_6=ttk.Label(resultsFrame_4_1, width=20, text="Serial No:").grid(column=6,row=1,sticky=tk.W)
resultsEditFirstNameEntered=tk.StringVar()
resultsEditFirstNameEntry=ttk.Entry(resultsFrame_4_1, width=15, textvariable=resultsEditFirstNameEntered).grid(column=1,row=2,sticky=tk.W)
resultsEditLastNameEntered=tk.StringVar()
resultsEditLastNameEntry=ttk.Entry(resultsFrame_4_1, width=15, textvariable=resultsEditLastNameEntered).grid(column=2,row=2,sticky=tk.W)
resultsEditAddressEntered=tk.StringVar()
resultsEditAddressEntry=ttk.Entry(resultsFrame_4_1, width=15, textvariable=resultsEditAddressEntered).grid(column=3,row=2,sticky=tk.W)
resultsEditDateEntered=tk.StringVar()
resultsEditDateEntry=ttk.Entry(resultsFrame_4_1, width=15, textvariable=resultsEditDateEntered).grid(column=4,row=2,sticky=tk.W)
resultsEditTypeEntered=tk.StringVar()
resultsEditTypeComboBox=ttk.Combobox(resultsFrame_4_1, width=12, textvariable=resultsEditTypeEntered).grid(column=5, row=2,sticky=tk.W)
resultsEditIdEntered=tk.StringVar()
resultsEditIdEntry=ttk.Entry(resultsFrame_4_1, width=15, textvariable=resultsEditIdEntered).grid(column=6,row=2,sticky=tk.W)
resultsFrame_4_2=ttk.Frame(resultsFrame_4)
resultsFrame_4_2.pack(expand=1, fill="both")
resultsLabel_7=ttk.Label(resultsFrame_4_2, text="Odor:").grid(column=1,row=1,sticky=tk.W)
resultsLabel_8=ttk.Label(resultsFrame_4_2, text="Taste:").grid(column=2,row=1,sticky=tk.W)
resultsLabel_9=ttk.Label(resultsFrame_4_2, text="Turbidity:").grid(column=3,row=1,sticky=tk.W)
resultsLabel_10=ttk.Label(resultsFrame_4_2, text="Color:").grid(column=4,row=1,sticky=tk.W)
resultsLabel_11=ttk.Label(resultsFrame_4_2, text="Ph value:").grid(column=5,row=1,sticky=tk.W)
resultsLabel_12=ttk.Label(resultsFrame_4_2, text="Nitrates (NO3):").grid(column=6,row=1,sticky=tk.W)
resultsLabel_13=ttk.Label(resultsFrame_4_2, text="Nitrites (NO2):").grid(column=1,row=3,sticky=tk.W)
resultsLabel_14=ttk.Label(resultsFrame_4_2, text="Ammonia (NH3):").grid(column=2,row=3,sticky=tk.W)
resultsLabel_15=ttk.Label(resultsFrame_4_2, text="Chlorides (Cl):").grid(column=3,row=3,sticky=tk.W)
resultsLabel_16=ttk.Label(resultsFrame_4_2, text="Iron (Fe):").grid(column=4,row=3,sticky=tk.W)
resultsLabel_17=ttk.Label(resultsFrame_4_2, text="Manganese (Mn):").grid(column=5,row=3,sticky=tk.W)
resultsLabel_18=ttk.Label(resultsFrame_4_2, text="KMnO4 Consumption:").grid(column=6,row=3,sticky=tk.W)
resultsLabel_19=ttk.Label(resultsFrame_4_2, text="Electrical Coduction:").grid(column=6,row=5,sticky=tk.W)
resultsLabel_20=ttk.Label(resultsFrame_4_2, text="Additional Information:").grid(column=1,row=7,sticky=tk.W, columnspan=2)
resultsEditOdorEntered=tk.StringVar()
resultsEditOdorEntry=ttk.Entry(resultsFrame_4_2, width=15, textvariable=resultsEditOdorEntered).grid(column=1,row=2,sticky=tk.W)
resultsEditTasteEntered=tk.StringVar()
resultsEditTasteEntry=ttk.Entry(resultsFrame_4_2, width=15, textvariable=resultsEditTasteEntered).grid(column=2,row=2,sticky=tk.W)
resultsEditTurbidityEntered=tk.StringVar()
resultsEditTurbidityEntry=ttk.Entry(resultsFrame_4_2, width=15, textvariable=resultsEditTurbidityEntered).grid(column=3,row=2,sticky=tk.W)
resultsEditColorEntered=tk.StringVar()
resultsEditColorEntry=ttk.Entry(resultsFrame_4_2, width=15, textvariable=resultsEditColorEntered).grid(column=4,row=2,sticky=tk.W)
resultsEditPhEntered=tk.StringVar()
resultsEditPhEntry=ttk.Entry(resultsFrame_4_2, width=15, textvariable=resultsEditPhEntered).grid(column=5,row=2,sticky=tk.W)
resultsEditNO3Entered=tk.StringVar()
resultsEditNO3Entry=ttk.Entry(resultsFrame_4_2, width=15, textvariable=resultsEditNO3Entered).grid(column=6,row=2,sticky=tk.W)
resultsEditNO2Entered=tk.StringVar()
resultsEditNO2Entry=ttk.Entry(resultsFrame_4_2, width=15, textvariable=resultsEditNO2Entered).grid(column=1,row=4,sticky=tk.W)
resultsEditNH3Entered=tk.StringVar()
resultsEditNH3Entry=ttk.Entry(resultsFrame_4_2, width=15, textvariable=resultsEditNH3Entered).grid(column=2,row=4,sticky=tk.W)
resultsEditClEntered=tk.StringVar()
resultsEditClEntry=ttk.Entry(resultsFrame_4_2, width=15, textvariable=resultsEditClEntered).grid(column=3,row=4,sticky=tk.W)
resultsEditFeEntered=tk.StringVar()
resultsEditFeEntry=ttk.Entry(resultsFrame_4_2, width=15, textvariable=resultsEditFeEntered).grid(column=4,row=4,sticky=tk.W)
resultsEditMnEntered=tk.StringVar()
resultsEditMnEntry=ttk.Entry(resultsFrame_4_2, width=15, textvariable=resultsEditMnEntered).grid(column=5,row=4,sticky=tk.W)
resultsEditKMnO4Entered=tk.StringVar()
resultsEditKMnO4Entry=ttk.Entry(resultsFrame_4_2, width=15, textvariable=resultsEditKMnO4Entered).grid(column=6,row=4,sticky=tk.W)
resultsEditElConductivityEntered=tk.StringVar()
resultsEditElConductivityEntry=ttk.Entry(resultsFrame_4_2, width=15, textvariable=resultsEditElConductivityEntered).grid(column=6,row=6,sticky=tk.W)
resultsTextList_4=scrolledtext.ScrolledText(resultsFrame_4_2, width=100, height=19,wrap=tk.WORD)
resultsTextList_4.grid(column=1, row=8, columnspan=8)
resultsFindButton=ttk.Button(resultsFrame_4_2, width=15, text="Find", command=findChemResult).grid(column=5, row=10)
resultsFindButton=ttk.Button(resultsFrame_4_2, width=15, text="Edit", command=editChemResult).grid(column=6, row=10)
#tab5
resultsFrame_5_1=ttk.Frame(resultsFrame_5)
resultsFrame_5_1.pack(expand=0, fill="both")
resultsLabel_1=ttk.Label(resultsFrame_5_1, width=20, text="First Name:").grid(column=1,row=1,)
resultsLabel_2=ttk.Label(resultsFrame_5_1, width=20, text="Last Name:").grid(column=2,row=1)
resultsLabel_3=ttk.Label(resultsFrame_5_1, width=20, text="Address:").grid(column=3,row=1)
resultsLabel_6=ttk.Label(resultsFrame_5_1, width=20, text="Date:").grid(column=4,row=1)
resultsLabel_5=ttk.Label(resultsFrame_5_1, width=20, text="Type:").grid(column=5,row=1)
resultsLabel_6=ttk.Label(resultsFrame_5_1, width=20, text="Serial No:").grid(column=6,row=1)
resultsEditMicroFirstNameEntered=tk.StringVar()
resultsEditMicroFirstNameEntry=ttk.Entry(resultsFrame_5_1, width=15, textvariable=resultsEditMicroFirstNameEntered).grid(column=1,row=2,sticky=tk.W)
resultsEditMicroLastNameEntered=tk.StringVar()
resultsEditMicroLastNameEntry=ttk.Entry(resultsFrame_5_1, width=15, textvariable=resultsEditMicroLastNameEntered).grid(column=2,row=2,sticky=tk.W)
resultsEditMicroAddressEntered=tk.StringVar()
resultsEditMicroAddressEntry=ttk.Entry(resultsFrame_5_1, width=15, textvariable=resultsEditMicroAddressEntered).grid(column=3,row=2,sticky=tk.W)
resultsEditMicroDateEntered=tk.StringVar()
resultsEditMicroDateEntry=ttk.Entry(resultsFrame_5_1, width=15, textvariable=resultsEditMicroDateEntered).grid(column=4,row=2,sticky=tk.W)
resultsEditMicroTypeEntered=tk.StringVar()
resultsEditMicroTypeComboBox=ttk.Combobox(resultsFrame_5_1, width=12, textvariable=resultsEditMicroTypeEntered).grid(column=5, row=2,sticky=tk.W)
resultsEditMicroIdEntered=tk.StringVar()
resultsEditMicroIdEntry=ttk.Entry(resultsFrame_5_1, width=15, textvariable=resultsEditMicroIdEntered).grid(column=6,row=2,sticky=tk.W)
resultsFrame_5_2=ttk.Frame(resultsFrame_5)
resultsFrame_5_2.pack(expand=1, fill="both")
resultsLabel_7=ttk.Label(resultsFrame_5_2, text="Aero. Meso. Bact.:").grid(column=1,row=3,sticky=tk.W)
resultsLabel_8=ttk.Label(resultsFrame_5_2, text="Coliform Bact.:").grid(column=2,row=3,sticky=tk.W)
resultsLabel_9=ttk.Label(resultsFrame_5_2, text="F. Coliform Bact.:").grid(column=3,row=3,sticky=tk.W)
resultsLabel_10=ttk.Label(resultsFrame_5_2, text="F. Streptococci:").grid(column=4,row=3,sticky=tk.W)
resultsLabel_11=ttk.Label(resultsFrame_5_2, text="Proteus Spp.:").grid(column=5,row=3,sticky=tk.W)
resultsLabel_12=ttk.Label(resultsFrame_5_2, text="Pseudo. Aeruginosa:").grid(column=6,row=3,sticky=tk.W)
resultsLabel_13=ttk.Label(resultsFrame_5_2, text="Sulfide Clostridia:").grid(column=6,row=5,sticky=tk.W)
resultsLabel_20=ttk.Label(resultsFrame_5_2, text="Additional Information_").grid(column=1,row=7,sticky=tk.W, columnspan=2)
resultsEditMicroAerobicMesophilicEntered=tk.StringVar()
resultsEditMicroAerobicMesophilicEntry=ttk.Entry(resultsFrame_5_2, width=15, textvariable=resultsEditMicroAerobicMesophilicEntered).grid(column=1,row=4,sticky=tk.W)
resultsEditMicroColiformEntered=tk.StringVar()
resultsEditMicroColiformEntry=ttk.Entry(resultsFrame_5_2, width=15, textvariable=resultsEditMicroColiformEntered).grid(column=2,row=4,sticky=tk.W)
resultsEditMicroFaecalColiformEntered=tk.StringVar()
resultsEditMicroFaecalColiformEntry=ttk.Entry(resultsFrame_5_2, width=15, textvariable=resultsEditMicroFaecalColiformEntered).grid(column=3,row=4,sticky=tk.W)
resultsEditMicroStreptococciEntered=tk.StringVar()
resultsEditMicroStreptococciEntry=ttk.Entry(resultsFrame_5_2, width=15, textvariable=resultsEditMicroStreptococciEntered).grid(column=4,row=4,sticky=tk.W)
resultsEditMicroProteusEntered=tk.StringVar()
resultsEditMicroProteusEntry=ttk.Entry(resultsFrame_5_2, width=15, textvariable=resultsEditMicroProteusEntered).grid(column=5,row=4,sticky=tk.W)
resultsEditMicroPseudomonasEntered=tk.StringVar()
resultsEditMicroPseudomonasEntry=ttk.Entry(resultsFrame_5_2, width=15, textvariable=resultsEditMicroPseudomonasEntered).grid(column=6,row=4,sticky=tk.W)
resultsEditMicroClostridiaEntered=tk.StringVar()
resultsEditMicroClostridiaEntry=ttk.Entry(resultsFrame_5_2, width=15, textvariable=resultsEditMicroClostridiaEntered).grid(column=6,row=6,sticky=tk.W)
resultsTextList_5=scrolledtext.ScrolledText(resultsFrame_5_2, width=100, height=22, wrap=tk.WORD)
resultsTextList_5.grid(column=1, row=8, columnspan=6)
resultsFindButton=ttk.Button(resultsFrame_5_2, width=15, text="Find", command=findMicroResult).grid(column=5, row=9,sticky=tk.W)
resultsFindButton=ttk.Button(resultsFrame_5_2, width=15, text="Edit", command=editMicroResult).grid(column=6, row=9,sticky=tk.W)
#Page Settings
settingsTab=ttk.Notebook(subsubtoolbarFrame_3)
settingsFrame_1=ttk.Frame(settingsTab)
settingsTab.add(settingsFrame_1, text="Settings")
settingsFrame_2=ttk.Frame(settingsTab)
settingsTab.add(settingsFrame_2, text="About")
settingsTab.pack(expand=1, fill="both")

#tab1

settingsFrame_1_1=ttk.Frame(settingsFrame_1)
settingsFrame_1_1.pack(expand=1, fill="both")
settingsLabel_1=ttk.Label(settingsFrame_1_1, width=20, text="User Name:").grid(column=1,row=1, sticky=tk.W)
settingsLabel_2=ttk.Label(settingsFrame_1_1, width=20, text="Password:").grid(column=2,row=1, sticky=tk.W)
settingsLabel_3=ttk.Label(settingsFrame_1_1, width=20, text="Porn Number:").grid(column=3,row=1, sticky=tk.W)
settingsLabel_4=ttk.Label(settingsFrame_1_1, width=20, text="Host:").grid(column=4,row=1, sticky=tk.W)
settingsLabel_5=ttk.Label(settingsFrame_1_1, width=20, text="Language:").grid(column=1,row=3, sticky=tk.W)
settingsUserNameEntered=tk.StringVar()
settingsUserNameEntry=ttk.Entry(settingsFrame_1_1, width=20, textvariable=settingsUserNameEntered).grid(column=1,row=2)
settingsPasswordEntered=tk.StringVar()
settingsPasswordEntry=ttk.Entry(settingsFrame_1_1, width=20, textvariable=settingsPasswordEntered).grid(column=2,row=2)
settingsPortNumberEntered=tk.StringVar()
settingsPortNumberEntry=ttk.Entry(settingsFrame_1_1, width=20, textvariable=settingsPortNumberEntered).grid(column=3,row=2)
settingsHostEntered=tk.StringVar()
settingsHostEntry=ttk.Entry(settingsFrame_1_1, width=20, textvariable=settingsHostEntered).grid(column=4,row=2)
settingsRadionEntered = tk.IntVar()
settingsRadion_1=tk.Radiobutton(settingsFrame_1_1, text="English", variable=settingsRadionEntered, value=1, command="")
settingsRadion_1.grid(column=1, row=4, sticky=tk.W, columnspan=3)   
settingsRadion_2=tk.Radiobutton(settingsFrame_1_1, text="Deutsch", variable=settingsRadionEntered, value=2, command="")
settingsRadion_2.grid(column=2, row=4, sticky=tk.W, columnspan=3)  
settingsRadion_3=tk.Radiobutton(settingsFrame_1_1, text="Srpski", variable=settingsRadionEntered, value=3, command="")
settingsRadion_3.grid(column=3, row=4, sticky=tk.W, columnspan=3)
settingsRadion_1.configure(state="disabled")
settingsRadion_2.configure(state="disabled")
settingsRadion_3.configure(state="disabled")
settingsSaveButton=ttk.Button(settingsFrame_1_1, text="Save Settings", command=savingServerSettings).grid(column=4, row=5, sticky=tk.W)
settingsUserNameEntered.set(serverSettingsUser)
settingsPasswordEntered.set(serverSettingsPassword)
settingsPortNumberEntered.set(serverSettingsPortNumber)
settingsHostEntered.set(serverSettingsHost)

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
toolButton_2.grid_forget()
toolButton_3.grid_forget()

#=========
#Start GUI
#=========
win.mainloop()