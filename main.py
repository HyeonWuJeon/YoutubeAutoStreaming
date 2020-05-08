import sys
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QUrl
# from PyQt5 import uic
from lib.AuthDialog import AuthDialog
import re
import pytube
import datetime
# from PyQt5.QtMultimedia import QSound
import sqlite3
import simplejson as json

conn = sqlite3.connect("H:/workspace/my_project/AutoYoutube/databases/sqlite1.db") #AutoCommit

from lib.YouViewerLayout import Ui_MainWindow
from PyQt5.QtWidgets import *
class Main(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
        #프로그램 초기화
        self.initAuthLock()

        #시그널 초기화
        self.initSignal()

        #로그인 관련 변수 선언
        self.user_id = None
        self.user_pw = None
        #재생 여부
        self.is_play = False
        # #Youtube 관련 작업
        self.youtb = None
        self.youtb_fsize = 0



    #기본 UI 비활성화
    def initAuthLock(self):
        self.previewButton.setEnabled(False)
        self.fileNavButton.setEnabled(False)
        self.streamCombobox.setEnabled(False)
        self.startButton.setEnabled(False)
        self.calendarWidget.setEnabled(False)
        self.urlTextEdit.setEnabled(False)
        self.pathTextEdit.setEnabled(False)
        self.showStatusMsg('인증안됨')



    #기본 UI 활성화
    def initAuthActive(self):
        self.previewButton.setEnabled(True)
        self.fileNavButton.setEnabled(True)
        self.streamCombobox.setEnabled(True)
        self.calendarWidget.setEnabled(True)
        self.urlTextEdit.setEnabled(True)
        self.pathTextEdit.setEnabled(True)
        self.showStatusMsg('인증 완료')

    def showStatusMsg(self,msg):
        self.statusbar.showMessage(msg)

    #시그널 초기화
    def initSignal(self):
        self.loginButton.clicked.connect(self.authCheck)
        self.previewButton.clicked.connect(self.load_url)
        self.exitButtion.clicked.connect(QtCore.QCoreApplication.instance().quit) #종료
        self.webView.loadProgress.connect(self.showProgressBrowserLoading)
        self.fileNavButton.clicked.connect(self.selectDownPath)
        self.startButton.clicked.connect(self.downloadYoutb)

    def authCheck(self):
        dlg = AuthDialog()
        dlg.exec_()
        self.user_id = dlg.user_id
        self.user_pw = dlg.user_pw
        c = conn.cursor()

        c.execute("SELECT * FROM users WHERE name ='%s'" % self.user_id)
        test = c.fetchone()
        print(test)

        print("id: %s password: %s" %(self.user_id,self.user_pw))
        if c.fetchone() != [] and test[2] == self.user_pw:
            self.initAuthActive() # 패스워드와 아이디 확인 후 버튼 활성화
            self.loginButton.setText("인증완료")
            self.loginButton.setEnabled(False)
            self.urlTextEdit.setFocus(True)
            self.append_log_msg("login Success")

        else:
            QMessageBox.about(self, "인증오류", "아이디 또는 비밀번호 인증 오류")


#URL 로딩 재생
    def load_url(self):
        url = self.urlTextEdit.text().strip()
        v = re.compile('^https://www.youtube.com/?') # ^ url 정규표현식
        if v.match(url) is not None: #정확히 매칭되었을경우
            self.append_log_msg('Play Click')
            self.webView.load(QUrl(url))
            self.showStatusMsg(url + "재생 중")
            self.is_play = True
            self.startButton.setEnabled(True)
            self.initialYouWork(url)

        else:
            QMessageBox.about(self,"URL 형식오류","Youtube 주소 형식이 아닙니다.")
            self.urlTextEdit.clear()
            self.urlTextEdit.setFocus(True)


#Stream 정렬
    def initialYouWork(self,url):
        video_list = pytube.YouTube(url)
        self.youtb = video_list.streams.all()
        self.streamCombobox.clear()
        for q in self.youtb:
            print('step1',q.itag,q.mime_type,q.abr)
            tmp_list, str_list = [], []
            tmp_list.append(str(q.mime_type or ''))
            tmp_list.append(str(q.itag or ''))
            tmp_list.append(str(q.abr or ''))
            str_list = [x for x in tmp_list if x != '']
            self.streamCombobox.addItem(','.join(str_list)) #,구분하여 요소들을 str로 만들어준다.


    ##DB에 로그인시도 기록 남기기
    def append_log_msg(self,act):
        now = datetime.datetime.now()
        nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')
        app_msg = self.user_id + ' : ' + act + ' - (' + nowDatetime + ')' #userid, 로그인성공 or 실패, 시간
        self.plainTextEdit.appendPlainText(app_msg) #로그창
        c = conn.cursor()

        c.execute("CREATE TABLE IF NOT EXISTS log(id INTEGER PRIMARY KEY AUTOINCREMENT, MSG text)")
        c.execute("INSERT INTO log('MSG') VALUES(?)", (app_msg,))

        conn.commit()


#로딩바 설정
    @pyqtSlot(int) #int 값 반환.
    def showProgressBrowserLoading(self, v):
        self.progressBar.setValue(v)


#저장파일 경로선택
    @pyqtSlot()
    def selectDownPath(self):
        fpath = QFileDialog.getExistingDirectory(self,'Select Directory')
        self.pathTextEdit.setText(fpath)

#링크 다운로드 /  스트리밍 선택
    @pyqtSlot()
    def downloadYoutb(self):
        down_dir = self.pathTextEdit.text().strip()
        if down_dir is None or down_dir == '' or not down_dir:
            QMessageBox.about(self,'경로 선택','다운로드 받을 경로를 선택하세요.')
            return None


        self.youtb[self.streamCombobox.currentIndex()].download(down_dir)
        self.append_log_msg('Download Click')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    you_viewer_main = Main()
    you_viewer_main.show()
    app.exec_()
