import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime

class evaluator(object):
    def __init__(self):
        self.title_href = []
        self.date_list = []

        self.title_text = []

        self.index_list = []

        self.today_date = None

        self.keyword = ['사업화', 'R&D', '엑셀러레이팅', '이노베이션', '데모데이', '공고']

    def page_source_get(self):
        req = requests.get('https://www.iitp.kr/kr/1/business/businessApiList.it')

        page_source = BeautifulSoup(req.text, "html.parser")

        title_href = page_source.select('#conArea > div.table-responsive > table > tbody > tr > td.no-space.comment-group0 > a')

        title_date = page_source.select('#conArea > div.table-responsive > table > tbody > tr > td:nth-child(3)')

        for i in title_href:
            self.title_href.append(i['href'])
            self.title_text.append(i.text.replace(' ', ''))

        for i in title_date:
            temp = i.text
            index = temp.find('~')
            temp = temp[index+1:].split('.')
            date_str = ''

            for j in temp:
                date_str += j

            self.date_list.append(int(date_str))

    def date_compare(self):
        now = datetime.now()
        date_list = [str(now.year), str(now.month), str(now.day)]

        for i in range(len(date_list)):
            if len(date_list[i]) == 1:
                date_list[i] = '0' + date_list[i]

        self.today_date = int(date_list[0] + date_list[1] + date_list[2])

        for i in range(len(self.date_list)):
            if self.date_list[i] > self.today_date:
                self.index_list.append(i)

    def title_keyword_detect(self):
        for i in self.index_list:
            for j in self.keyword:
                if j in self.title_text[i]:
                    self.txt_write(self.title_text[i] + ' - ' + self.title_href[i])

    def txt_refresh(self):
        f = open('./Output.txt', 'w', encoding='UTF-8')
        f.close()

    def txt_write(self, txt_string):
        f = open('./Output.txt', 'a', encoding='UTF-8')
        f.write(txt_string)
        f.write('\n')
        f.close()

    def start(self):
        self.txt_refresh()
        self.page_source_get()
        self.date_compare()
        self.title_keyword_detect()


if __name__ == "__main__":
    evaluator = evaluator()
    evaluator.start()