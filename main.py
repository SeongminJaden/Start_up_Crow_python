#%%
import PyQt5.QtWidgets as qtw
import os
import sys
import time
import subprocess
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime

#%%
class nipa(object):
    def __init__(self):
        self.main_page = 'https://www.nipa.kr'
        self.page_source = None
        self.href_list = []
        self.date_list = []
        self.title_list = []

        self.title_index = []

        self.keyword = ['사업화', 'R&D', '엑셀러레이팅', '이노베이션', '데모데이', '공고']

    def main_page_in(self):
        req = requests.get("https://www.nipa.kr/home/2-2")
        self.page_source = BeautifulSoup(req.text, "html.parser")

    def get_title_date(self):
        date = self.page_source.select('#container > div.row.pdl15.pdr15 > div:nth-child(3) > div.bdWrap > table > tbody > tr > td:nth-child(5) > span')

        href = self.page_source.select('#container > div.row.pdl15.pdr15 > div:nth-child(3) > div.bdWrap > table > tbody > tr > td.tl > div > div:nth-child(1) > a')

        title = self.page_source.select('#container > div.row.pdl15.pdr15 > div:nth-child(3) > div.bdWrap > table > tbody > tr > td.tl > div > div:nth-child(1) > a')

        for i in title:
            temp_str = i.text
            temp_str = re.sub(r"\s", "", temp_str)
            self.title_list.append(temp_str)

        for i in href:
            self.href_list.append(i['href'])

        for i in date:
            self.date_list.append(i.text)

    def date_filter(self):
        now = datetime.now()
        date_list = [str(now.year), str(now.month), str(now.day)]

        for i in range(len(date_list)):
            if len(date_list[i]) == 1:
                date_list[i] = '0' + date_list[i]

        date_str = date_list[0] + '-' + date_list[1] + '-' + date_list[2]
        print(date_str)

        # 타겟 날짜 설정
        # date_str = '2023-07-06'

        if date_str in ''.join(self.date_list):
            print("오늘 공지된 지원사업이 있습니다. 크롤링해드릴게요!")
        else:
            print("오늘 공지된 지원사업은 없습니다.")

        for i in range(len(self.date_list)):
            if self.date_list[i] == date_str:
                self.title_index.append(i)
    def keyword_detect(self):
        f = open('./Output.txt', 'w', encoding='UTF-8')
        for i in self.title_index:
            req = requests.get(f"{self.main_page}{self.href_list[i]}")
            soup = BeautifulSoup(req.text, "html.parser")

            inner_text = soup.findAll('span')
            inner_str = ''
            for j in inner_text:
                inner_str += j.text.replace('\n', '')

            inner_str = re.sub(r"\s", "", inner_str)
            for j in self.keyword:
                if j in inner_str:
                    f.write(f"{self.title_list[i]} - {self.main_page}{self.href_list[i]}")
                    f.write('\n')
                    print(f"{self.title_list[i]} - {self.main_page}{self.href_list[i]}")
                    break
        f.close()

        f = open('./Output.txt', 'r', encoding='UTF-8')
        content = f.read()
        if not content:
            print("우리가 지원할 사업은 없습니다.")
            f.close()

    def start(self):
        self.main_page_in()
        self.get_title_date()
        self.date_filter()
        self.keyword_detect()


class WindowClass(qtw.QMainWindow):
    def __init__(self):
        super().__init__()

        # 윈도우 크기 설정
        window_width = 260
        window_height = 150

        screen = qtw.QDesktopWidget().screenGeometry()
        x = (screen.width() - window_width) // 2
        y = (screen.height() - window_height) // 2

        self.setGeometry(x, y, window_width, window_height)
        self.initbox_1()
        self.show()
        self.site = None
    def initbox_1(self):
        self.comboBox = qtw.QComboBox(self)
        self.comboBox.setFixedSize(200, 30)
        self.comboBox.addItem('선택')
        self.comboBox.addItem('전체크롤링')
        self.comboBox.addItem('정보통신산업진흥원')
        self.comboBox.addItem('정보통신기획평가원')
        self.comboBox.addItem('IP-R&D사업관리시스템')
        self.comboBox.addItem('중소기업기술정보진흥원')
        self.comboBox.addItem('기업마당')
        self.comboBox.addItem('startup park')
        self.comboBox.addItem('서울경제진흥원')
        self.comboBox.addItem('스타트업플러스')
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
            print('준비중')

        if text == '정보통신산업진흥원':
            print(text)
            print('https://www.nipa.kr')
            self.site = 'nipa'
        if text == '정보통신기획평가원':
            print(text)
            print('https://www.iitp.kr/kr/1/business/businessApiList.it')
            self.site = 'iitp'
        if text == 'K-startup':
            print(text)
            print('https://www.k-startup.go.kr/web/contents/bizpbanc-ongoing.do')
            self.site = 'kstartup'
        if text == 'IP-R&D사업관리시스템':
            print(text)
            print('https://biz.kista.re.kr/ippro/com/iprndMain/selectBusinessAnnounceList.do?bbsType=bs')
            self.site = 'ip'
        if text == '중소기업기술정보진흥원':
            print(text)
            print('https://smtech.go.kr/front/ifg/no/notice02_list.do')
            self.site = 'smtech'
        if text == '한국산업기술진흥원':
            print(text)
            print('https://www.kiat.or.kr/front/board/boardContentsListPage.do?board_id=90&MenuId=b159c9dac684471b87256f1e25404f5e')
            self.site = 'kiat'
        if text == '기업마당':
            print(text)
            print('https://www.bizinfo.go.kr/web/lay1/bbs/S1T122C128/AS/74/list.do')
            self.site = 'bizinfo'
        if text == 'startup park':
            print(text)
            print('https://www.startuppark.kr/user/business/list.do')
            self.site = 'startuppark'
        if text == '서울경제진흥원':
            print(text)
            print('https://seoul.rnbd.kr/client/c030100/c030100_00.jsp')
            self.site = 'sba'
        if text == '스타트업플러스':
            print(text)
            print('https://www.startup-plus.kr/cms_for_portal/process/program/list.do?show_no=906&check_no=96&c_relation=276&c_relation2=903')
            print('구현중')
            #self.site = 'nipa'
    def select_site(self):
        if self.site is None:
            print("선택해라 게이야")
        else:
            path = os.getcwd()
            path = path + f'\\{self.site}.py'
            subprocess.call(args=['python', path], shell=True)
            print("주현수가 준거 여기에 적용!")

#%%
if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()
