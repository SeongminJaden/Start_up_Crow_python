#%%
import PyQt5.QtWidgets as qtw
import os
import sys
import subprocess

import bizinfo, iitp, ip, kiat, kstartup, nipa, sba, smtech, startuppark

#%%
class WindowClass(qtw.QMainWindow):
    def __init__(self):
        super().__init__()

        # 윈도우 크기 설정
        window_width = 260
        window_height = 150

        screen = qtw.QDesktopWidget().screenGeometry()
        x = (screen.width() - window_width) // 2
        y = (screen.height() - window_height) // 2

        self.module_dict = {}

        self.setGeometry(x, y, window_width, window_height)
        self.initbox_1()
        self.show()
        self.site = None

    def addbox(self, name, module = None):
        self.comboBox.addItem(name)

        if module is not None:
            self.module_dict[name] = module

    def initbox_1(self):
        self.comboBox = qtw.QComboBox(self)
        self.comboBox.setFixedSize(200, 30)
        self.addbox('선택')
        self.addbox('전체크롤링')
        self.addbox('정보통신산업진흥원', nipa.nipa())
        self.addbox('정보통신기획평가원', iitp.evaluator())
        # self.addbox('IP-R&D사업관리시스템', ip.IP())
        self.addbox('중소기업기술정보진흥원', smtech.SMTECH())
        self.addbox('기업마당', bizinfo.madang())
        self.addbox('startup park', startuppark.startup_park())
        self.addbox('서울경제진흥원', sba.Seoul())
        self.addbox('스타트업플러스', None)
        self.comboBox.activated[str].connect(self.selectedComboItem)
        self.comboBox.move(30, 30)
        self.button = qtw.QPushButton("크롤링!", self)
        self.button.setFixedSize(200, 30)
        self.button.move(30, 90)
        self.button.clicked.connect(self.select_site)

    def selectedComboItem(self, text):
        if text == '전체크롤링':
            print(text)
            print('https://www.nipa.kr')
            print('https://www.iitp.kr/kr/1/business/businessApiList.it')
            print('https://www.k-startup.go.kr/web/contents/bizpbanc-ongoing.do')
            print('https://biz.kista.re.kr/ippro/com/iprndMain/selectBusinessAnnounceList.do?bbsType=bs')
            print('https://smtech.go.kr/front/ifg/no/notice02_list.do')
            print('https://www.kiat.or.kr/front/board/boardContentsListPage.do?board_id=90&MenuId=b159c9dac684471b87256f1e25404f5e')
            print('https://www.bizinfo.go.kr/web/lay1/bbs/S1T122C128/AS/74/list.do')
            print('https://www.startuppark.kr/user/business/list.do')
            print('https://seoul.rnbd.kr/client/c030100/c030100_00.jsp')
            print('https://www.startup-plus.kr/cms_for_portal/process/program/list.do?show_no=906&check_no=96&c_relation=276&c_relation2=903')
            self.site = 'all'

        if text == '정보통신산업진흥원':
            print(text)
            print('https://www.nipa.kr')
            self.site = text
        if text == '정보통신기획평가원':
            print(text)
            print('https://www.iitp.kr/kr/1/business/businessApiList.it')
            self.site = text
        if text == 'K-startup':
            print(text)
            print('https://www.k-startup.go.kr/web/contents/bizpbanc-ongoing.do')
            self.site = text
        if text == 'IP-R&D사업관리시스템':
            print(text)
            print('https://biz.kista.re.kr/ippro/com/iprndMain/selectBusinessAnnounceList.do?bbsType=bs')
            self.site = text
        if text == '중소기업기술정보진흥원':
            print(text)
            print('https://smtech.go.kr/front/ifg/no/notice02_list.do')
            self.site = text
        if text == '한국산업기술진흥원':
            print(text)
            print('https://www.kiat.or.kr/front/board/boardContentsListPage.do?board_id=90&MenuId=b159c9dac684471b87256f1e25404f5e')
            self.site = text
        if text == '기업마당':
            print(text)
            print('https://www.bizinfo.go.kr/web/lay1/bbs/S1T122C128/AS/74/list.do')
            self.site = text
        if text == 'startup park':
            print(text)
            print('https://www.startuppark.kr/user/business/list.do')
            self.site = text
        if text == '서울경제진흥원':
            print(text)
            print('https://seoul.rnbd.kr/client/c030100/c030100_00.jsp')
            self.site = text
        if text == '스타트업플러스':
            print(text)
            print('https://www.startup-plus.kr/cms_for_portal/process/program/list.do?show_no=906&check_no=96&c_relation=276&c_relation2=903')
            print('구현중')
            #self.site = text

    def select_site(self):
        if self.site is None:
            print("선택해라 게이야")
        else:
            if self.site == 'all':
                f = open('./Output.txt', 'w', encoding='UTF-8')
                f.close()
                for eval in self.module_dict.values():
                    eval.start(refresh = False)
                print('크롤링 완료')
            else:
                eval = self.module_dict[self.site]
                eval.start()
                print('크롤링 완료')

#%%
if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()
