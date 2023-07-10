import re
import requests
from bs4 import BeautifulSoup

class Seoul(object):
    def __init__(self):
        self.href_list = []
        self.title_list = []

        self.keyword_list = ['지원분야', '네트워크', '사업화', 'R&D', '엑셀러레이팅', '이노베이션', '데모데이', 'IR']

    def main_page_in(self):
        req = requests.get("https://seoul.rnbd.kr/client/c030100/c030100_00.jsp")
        page_source = BeautifulSoup(req.text, "html.parser")

        a = page_source.select('#contents > div.cnt_con.board.business_notice > div.board_list.basic > table > tbody > tr > td:nth-child(4) > span')

        hrefs = page_source.select('#contents > div.cnt_con.board.business_notice > div.board_list.basic > table > tbody > tr > td.t1 > a')

        for i in range(len(a)):
            if a[i].text == '모집중':
                self.href_list.append(hrefs[i]['href'])
                self.title_list.append(hrefs[i].text)

        for i in range(len(self.href_list)):
            index = self.href_list[i].find("_")
            temp_href = self.href_list[i][:index]

            req = requests.get(f"https://seoul.rnbd.kr/client/{temp_href}/{self.href_list[i]}")

            page_source = BeautifulSoup(req.text, "html.parser")

            page_source.select('#contents > div.cnt_con.board.business_notice > div > form > table > tbody > tr:nth-child(3) > td')

            temp_str = ''

            for j in page_source:
                t_str = j.text
                t_str = re.sub(r"\s", "", t_str)

                temp_str += t_str

            for j in self.keyword_list:
                if j in temp_str:
                    self.txt_write(self.title_list[i] + ' - ' + f"https://seoul.rnbd.kr/client/{temp_href}/{self.href_list[i]}")
                    break

    def txt_write(self, string):
        f = open('./Output.txt', 'a', encoding='UTF-8')
        f.write(string)
        f.write('\n')
        f.close()

    def txt_refresh(self):
        f = open('./Output.txt', 'w', encoding='UTF-8')
        f.close()

    def start(self):
        self.txt_refresh()
        self.main_page_in()


if __name__ == '__main__':
    Seoul = Seoul()
    Seoul.start()