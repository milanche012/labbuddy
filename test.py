from PyQt5 import QtWidgets, uic

app=QtWidgets.QApplication([])
dig=uic.loadUi("LabBuddy.ui")
dig.show()
app.exec()