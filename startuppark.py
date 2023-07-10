import requests
from bs4 import BeautifulSoup

class startup_park(object):
    def __init__(self):
        self.page_source = None

        self.title_index = []
        self.href_list = []

        self.max_page = 10

        self.title_keyword = ['지원분야', '네트워크', '사업화', 'R&D', '엑셀러레이팅', '이노베이션', '데모데이', 'IR', '공고']

    def page_source_get(self, index):
        self.href_list.clear()
        self.title_index.clear()

        req = requests.get(f'https://www.startuppark.kr/user/business/list.do?page={index}&tabGubn=0&srchValue=')
        self.page_source = BeautifulSoup(req.text, "html.parser")

        a = self.page_source.select('div.box_list1 > div > a > ul > li:nth-child(3) > dl > dd')

        for i in range(len(a)):
            if a[i].text == '신청중':
                self.title_index.append(i)

        hrefs = self.page_source.select('div.box_list1 > div > a')

        temp_hrefs = []

        for i in hrefs:
            if "write" in i['href']:
                pass
            else:
                temp_hrefs.append(i)

        hrefs = temp_hrefs

        for i in range(len(hrefs)):
            for j in self.title_index:
                if i == j:
                    self.href_list.append(hrefs[i]['href'])
                    break

    def inner_page_in(self, page_string):
        req = requests.get(f'https://www.startuppark.kr/user/business/{page_string}')
        self.page_source = BeautifulSoup(req.text, "html.parser")

        inner_title = self.page_source.select('#formWrite > div.detail1 > h4')

        title = ''

        for i in inner_title:
            title = i.text

        for i in self.title_keyword:
            if i in title:
                self.txt_write(title + ' - ' + f'https://www.startuppark.kr/user/business/{page_string}')

    def txt_write(self, str):
        f = open('./Output.txt', 'a', encoding='UTF-8')
        f.write(str)
        f.write('\n')
        f.close()

    def txt_refresh(self):
        f = open('./Output.txt', 'w', encoding='UTF-8')
        f.close()

    def start(self):
        self.txt_refresh()
        for i in range(1, self.max_page + 1):
            self.page_source_get(i)
            for j in self.href_list:
                self.inner_page_in(j)


if __name__ == '__main__':
    startup_park = startup_park()
    startup_park.start()