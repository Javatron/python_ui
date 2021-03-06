import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QMessageBox
from PyQt5.QtGui import QMouseEvent, QCursor, QFont, QIcon


class MsgBox(QtWidgets.QDialog):
    def __init__(self, prompt="Provide Password:", title="title"):
        """
        param::prompt describes what u want 
        param:: title
        """
        super().__init__()
        self.title = title
        self.left = 50
        self.top = 50
        self.width = 250
        self.height = 140
        self.prompt = prompt
        self.password = ""
        self.state = False
        self.fontHiddenMode = True
        self.__initUI()


    def __initUI(self):

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.font = QFont('Droid Sans', 14, QFont.Bold)
        self.label = QLabel(self.prompt, self)
        self.label.setFont(self.font)

        self.label.adjustSize()

        self.inputLine = QLineEdit(self)
        self.inputLine.setEchoMode(QLineEdit.Password)
        self.inputLine.setText = ""
        self.inputLine.setClearButtonEnabled(True)
        self.inputLine.selectAll()
        self.inputLine.setFocus()
        self.inputLine.setFixedSize(235,25)
        self.inputLine.setSizePolicy(QtWidgets.QSizePolicy.Fixed,QtWidgets.QSizePolicy.Fixed)

        self.okButton = QPushButton("Ok",self)
        self.okButton.clicked.connect(self.__okClick)

        self.cancelButton = QPushButton("Cancel",self)
        self.cancelButton.clicked.connect(self.__cancelClick)

        self.showButton = QPushButton("Show",self)
        self.showButton.clicked.connect(self.__showClick)


        self.bar  = QHBoxLayout()
        self.bar.addWidget(MyBar(self,title=self.title))

        self.labelBox = QHBoxLayout()
        self.labelBox.setAlignment(QtCore.Qt.AlignCenter)
        self.labelBox.addWidget(self.label)

        self.inputLineBox = QHBoxLayout()
        self.labelBox.setAlignment(QtCore.Qt.AlignCenter)
        self.inputLineBox.addWidget(self.inputLine)



        self.buttonsBox = QHBoxLayout()
        self.buttonsBox.addWidget(self.okButton)
        self.buttonsBox.addStretch(1)
        self.buttonsBox.addWidget(self.showButton)
        self.buttonsBox.addStretch(2)
        self.buttonsBox.addWidget(self.cancelButton)



        self.vbox = QVBoxLayout(self)
        self.vbox.addLayout(self.bar)
        self.vbox.addStretch(1)
        self.vbox.addLayout(self.labelBox)
        self.vbox.addStretch(2)
        self.vbox.addLayout(self.inputLineBox)
        self.vbox.addStretch(3)
        self.vbox.addLayout(self.buttonsBox)
        
        self.setLayout(self.vbox)

        self.__center()
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
        self.show()

    def __okClick(self):
        if self.inputLine.text() != "":
            self.password = self.inputLine.text()
            self.state = True
            self.accept()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText('Error\nThe password can not be left blank.')
            msg.setWindowTitle("Error")
            
            msg.setSizePolicy(QtWidgets.QSizePolicy.Fixed,QtWidgets.QSizePolicy.Fixed)
            msg.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
            msg.exec_()

    def __cancelClick(self):
            self.state = False
            self.reject()

    def __showClick(self):
        
        if self.inputLine.text() != "":
            self.showButton.setEnabled(False)
            if not self.fontHiddenMode:
                    self.inputLine.setEchoMode(QLineEdit.Password)
                    self.fontHiddenMode = not self.fontHiddenMode
            else:
                    self.inputLine.setEchoMode(QLineEdit.Normal)
                    self.fontHiddenMode = not self.fontHiddenMode
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText('First, fill in the password.')
            msg.setWindowTitle("Information")
            
            msg.setSizePolicy(QtWidgets.QSizePolicy.Fixed,QtWidgets.QSizePolicy.Fixed)
            msg.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
            msg.exec_()

    def mousePressEvent(self, QMouseEvent):
        self.inputLine.setEchoMode(QLineEdit.Password)

    @staticmethod
    def show_dialog(prompt="Provide Password:", title="Title"):
        app = QtWidgets.QApplication(sys.argv)
        msgbox = MsgBox(prompt,title)
        app.exec_()
        return (msgbox.password, msgbox.state)
        
    def __center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())



class MyBar(QtWidgets.QWidget):

    def __init__(self, parent, title='title'):
        super(MyBar, self).__init__()
        self.parent = parent
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.title = QLabel(title)

        btn_size = 20

        self.btn_close = QPushButton("x")
        self.btn_close.clicked.connect(self.btn_close_clicked)
        self.btn_close.setFixedSize(btn_size,btn_size)
        self.btn_close.setStyleSheet("background-color: red;")

        self.btn_min = QPushButton("-")
        self.btn_min.clicked.connect(self.btn_min_clicked)
        self.btn_min.setFixedSize(btn_size, btn_size)
        self.btn_min.setStyleSheet("background-color: gray;")

        self.title.setFixedHeight(20)
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.btn_min)
        self.layout.addWidget(self.btn_close)

        self.title.setStyleSheet("""
            color: black;
            font: 'Times New Roman' 12px;
            border-style: outset;
            border-width: 1px;
            border-color: black;
        """)
        self.title.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.setLayout(self.layout)

        self.start = QtCore.QPoint(0, 0)
        self.pressing = False

    def btn_close_clicked(self):
        self.parent.reject()
    def btn_min_clicked(self):
        self.parent.showMinimized()
    
if __name__ == '__main__':
    
    password, state = MsgBox.show_dialog()
    print(password, state)
    if password == "admin":
        print('laslgosdlgoasd')
