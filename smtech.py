import requests
from bs4 import BeautifulSoup
import re


class SMTECH(object):
    def __init__(self):
        self.title_index = []

        self.title_list = []

        self.title_url = []

        self.page_source = None

        self.keyword = ['사업화', 'R&D', '엑셀러레이팅', '이노베이션', '데모데이']

    def title_get(self):
        for i in self.title_index:
            title = self.page_source.select(f'#subcontent > div.right.fl > div.l15 > table > tbody > tr:nth-child({i + 1}) > td:nth-child(3) > a')

            for j in title:
                self.title_list.append(j.text)

    def img_type_get(self):
        req = requests.get('https://smtech.go.kr/front/ifg/no/notice02_list.do')
        self.page_source = BeautifulSoup(req.text, "html.parser")

        img = self.page_source.select('#subcontent > div.right.fl > div.l15 > table > tbody > tr > td.ac.ll > img')

        for i in range(len(img)):
            if img[i]['alt'] == '접수중':
                self.title_index.append(i)

    def href_get(self):
        hrefs = self.page_source.select('#subcontent > div.right.fl > div.l15 > table > tbody > tr > td:nth-child(3) > a')

        for i in self.title_index:
            href = hrefs[i]['href']
            index = href.find('?')
            href = href[index:]

            self.title_url.append('https://smtech.go.kr/front/ifg/no/notice02_detail.do' + href)

    def title_page_in(self):
        for i in range(len(self.title_url)):
            req = requests.get(self.title_url[i])
            self.page_source = BeautifulSoup(req.text, "html.parser")

            inner = self.page_source.select('#subcontent > div.right.fl > div.l15 > table > tbody > tr:nth-child(8) > td > div')

            inner_str = ''

            for j in inner:
                t_str = re.sub(r"\s", "", j.text)
                inner_str += t_str

            for j in self.keyword:
                if j in inner_str:
                    self.txt_write(self.title_list[self.title_index[i]] + ' - ' + self.title_url[i])
                    break

    def txt_write(self, string):
        f = open('./Output.txt', 'a', encoding='UTF-8')
        f.write(string)
        f.write('\n')
        f.close()

    def txt_refresh(self):
        f = open('./Output.txt', 'w', encoding='UTF-8')
        f.close()

    def start(self, refresh = True):
        if refresh:
            self.txt_refresh()

        self.img_type_get()
        self.title_get()
        self.href_get()
        self.title_page_in()


if __name__ == "__main__":
    SMTECH = SMTECH()
    SMTECH.start()