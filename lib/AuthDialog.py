
#로그인파일

import sys
from PyQt5.QtWidgets import *

class AuthDialog(QDialog): #Qdialog 상속 확인/취소
    def __init__(self):
        super().__init__()
        self.setupUI()

        self.__user_id = None
        self.__user_pw = None

    @property
    def user_id(self):
        return self.__user_id

    @property
    def user_pw(self):
        return self.__user_pw

    def setupUI(self):
        self.setGeometry(200,500,300,100) #로그인창위치
        self.setWindowTitle("Sign In")
        self.setFixedSize(400,100)

        label1 = QLabel("ID:")
        label2 = QLabel("Password:")

##글작성
        self.lineEdit1 = QLineEdit()
        self.lineEdit2 = QLineEdit()
        self.lineEdit2.setEchoMode(QLineEdit().Password) #패스워드 암호화

##버튼 생성
        self.pushButton = QPushButton("로그인")
        self.pushButton.clicked.connect(self.submitLogin)

##파이큐티 자동배치 : 크기조절 , 위치
        layout = QGridLayout()
        layout.addWidget(label1,0,0) #배치할 라벨명/행/렬
        layout.addWidget(self.lineEdit1,0,1)
        layout.addWidget(self.pushButton,0,2)
        layout.addWidget(label2,1,0)
        layout.addWidget(self.lineEdit2,1,1)

        self.setLayout(layout)

    def submitLogin(self):
        self.__user_id = self.lineEdit1.text()
        self.__user_pw = self.lineEdit2.text()
        print(self.__user_id,self.__user_pw)

        if self.__user_id is None or self.__user_id == '' or not self.__user_id:
            QMessageBox.about(self,"인증오류","ID를 입력하세요.")
            self.lineEdit1.setFocus(True)
            return None

        if self.__user_pw is None or self.__user_pw == '' or not self.__user_pw:
            QMessageBox.about(self,"인증오류","PW를 입력하세요.")
            self.lineEdit2.setFocus(True)
            return None


        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    loginDialog = AuthDialog()
    loginDialog.show()
    app.exec_()
