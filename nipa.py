import os
import sys
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime

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
        f = open('./Output.txt', 'a', encoding='UTF-8')
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

    def txt_refresh(self):
        f = open('./Output.txt', 'w', encoding='UTF-8')
        f.close()

    def start(self, refresh = True):
        if refresh:
            self.txt_refresh()

        self.main_page_in()
        self.get_title_date()
        self.date_filter()
        self.keyword_detect()


if __name__ == '__main__':
    nipa = nipa()
    nipa.start()


