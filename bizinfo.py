from bs4 import BeautifulSoup
import requests
from datetime import datetime
import re

class madang(object):
    def __init__(self):
        self.page_source = None
        self.page_href = []

        self.today_date = None
        self.date_list = []

        self.page_number = 10

        self.title_keyword = ['지원분야', '네트워크', '사업화', 'R&D', '엑셀러레이팅', '이노베이션', '데모데이', 'IR']
        self.keyword_list = ['지원분야', '네트워크', '사업화', 'R&D', '엑셀러레이팅', '이노베이션', '데모데이', 'IR']

    def page_source_get(self, index):
        self.date_list.clear()
        self.page_href.clear()

        req = requests.get(f"https://www.bizinfo.go.kr/web/lay1/bbs/S1T122C128/AS/74/list.do?rows=15&cpage={index}")
        self.page_source = BeautifulSoup(req.text, "html.parser")

        a = self.page_source.select('#articleSearchForm > div.support_project > div.table_Type_1 > table > tbody > tr > td:nth-child(7)')

        for i in a:
            self.date_list.append(i.text)

        page_num = self.page_source.select('#articleSearchForm > div.support_project > div.table_Type_1 > table > tbody > tr > td.txt_l > a')

        for i in range(len(page_num)):
            if not self.date_list[i] == self.today_date:
                continue

            index = page_num[i]['href'].find('_')
            self.page_href.append(page_num[i]['href'][index+1:])

    def today_date_set(self):
        now = datetime.now()
        date_list = [str(now.year), str(now.month), str(now.day)]

        for i in range(len(date_list)):
            if len(date_list[i]) == 1:
                date_list[i] = '0' + date_list[i]

        self.today_date = date_list[0] + '-' + date_list[1] + '-' + date_list[2]

        #self.today_date = '2023-07-06'

    def page_in(self, page_number):
        req = requests.get(f'https://www.bizinfo.go.kr/web/lay1/bbs/S1T122C128/AS/74/view.do?pblancId=PBLN_{page_number}')

        self.page_source = BeautifulSoup(req.text, "html.parser")

        title = self.page_source.select('#container > div.sub_cont > div.sub_cont.support_project > div.support_project_detail > div.title_area > div:nth-child(1) > h2')

        for i in title:
            title = i.text

        #print('제목 : ', title)

        loop_bool = False

        for i in self.title_keyword:
            if i in title:
                loop_bool = True
                break

        if not loop_bool:
            return True

        inner = self.page_source.select('#container > div.sub_cont > div.sub_cont.support_project > div.support_project_detail > div.view_cont > ul > li:nth-child(4) > div')

        inner_str = ''

        for i in inner:
            t_str = i.text
            t_str = re.sub(r"\s", "", t_str)
            inner_str += t_str

        #print('내용 : ', inner_str)

        loop_bool = False

        for i in self.keyword_list:
            if i in inner_str:
                loop_bool = True
                break

        if loop_bool:
            f = open('./Output.txt', 'a', encoding='UTF-8')
            f.write(title + ' - ' + f'https://www.bizinfo.go.kr/web/lay1/bbs/S1T122C128/AS/74/view.do?pblancId=PBLN_{page_number}')
            f.write('\n')
            f.close()

    def inner_text_detect(self):
        if len(self.page_href) == 0:
            return True

        for i in self.page_href:
            self.page_in(i)

    def txt_refresh(self):
        f = open('./Output.txt', 'w', encoding='UTF-8')
        f.close()

    def start(self, refresh = True):
        if refresh:
            self.txt_refresh()

        for i in range(1, self.page_number + 1):
            self.today_date_set()
            self.page_source_get(i)
            self.inner_text_detect()


if __name__ == '__main__':
    madang = madang()
    madang.start()