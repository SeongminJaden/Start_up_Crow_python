import os
import re
import asyncio
import requests
from time import sleep
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from chromedriver_autoinstaller import get_chrome_version, install
from selenium.webdriver.chrome.service import Service
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
#nipa
class nipa(object):
    def __init__(self):
        self.main_page = 'https://www.nipa.kr'
        self.page_source = None
        self.href_list = []
        self.date_list = []
        self.title_list = []

        self.title_index = []

        self.keyword = ['사업화', 'R&D', '엑셀러레이팅', '이노베이션', '데모데이', '공고', '농식품', '농업', '환경', '빅데이터', 'IR', '투자']

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

        # 타겟 날짜 설정
        #date_str = '2023-07-07'

        for i in range(len(self.date_list)):
            if self.date_list[i] == date_str:
                self.title_index.append(i)

    def keyword_detect(self):
        f = open('./Output/nipa_Output.txt', 'w', encoding='UTF-8')
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
                    print(f"{self.main_page}{self.href_list[i]}")
                    break
        f.close()

    def start(self):
        self.main_page_in()
        self.get_title_date()
        self.date_filter()
        self.keyword_detect()

#기업마당
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

        print('내용 : ', inner_str)

        loop_bool = False

        for i in self.keyword_list:
            if i in inner_str:
                loop_bool = True
                break

        if loop_bool:
            f = open('./Output/bizinfo_Output.txt', 'a', encoding='UTF-8')
            f.write(title + ' - ' + f'https://www.bizinfo.go.kr/web/lay1/bbs/S1T122C128/AS/74/view.do?pblancId=PBLN_{page_number}')
            f.write('\n')
            f.close()

    def inner_text_detect(self):
        if len(self.page_href) == 0:
            return True

        for i in self.page_href:
            self.page_in(i)

    def txt_refresh(self):
        f = open('./Output/bizinfo_Output.txt', 'w', encoding='UTF-8')
        f.close()

    def start(self):
        self.txt_refresh()
        for i in range(1, self.page_number + 1):
            self.today_date_set()
            self.page_source_get(i)
            self.inner_text_detect()

#iitp
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
        f = open('./Output/iitp_Output.txt', 'w', encoding='UTF-8')
        f.close()

    def txt_write(self, txt_string):
        f = open('./Output/iitp_Output.txt', 'a', encoding='UTF-8')
        f.write(txt_string)
        f.write('\n')
        f.close()

    def start(self):
        self.txt_refresh()
        self.page_source_get()
        self.date_compare()
        self.title_keyword_detect()
#ip
class IP(object):
    def __init__(self):
        self.driver = None

        self.page_list = []
        self.title_list = []

        self.page_index = []
        self.page_script = []

        self.keyword_list = ['지원분야', '네트워크', '사업화', 'R&D', '엑셀러레이팅', '이노베이션', '데모데이', 'IR']
        self.chrome_ver = get_chrome_version().split('.')[0]  # 크롬드라이버 버전 확인
        self.chrome_driver_path = f'./{self.chrome_ver}/chromedriver.exe'
        self.service = Service(self.chrome_driver_path)
    def driver_return(self):
        options = webdriver.ChromeOptions()
        options.add_argument("headless")

        chrome_ver = get_chrome_version().split('.')[0]  # 크롬드라이버 버전 확인

        while True:
            if os.path.exists(f'./{chrome_ver}'):  # 크롬드라이버 확인
                driver = webdriver.Chrome(service=self.service, options=options)
                break
            else:
                install(True)
                driver = webdriver.Chrome(service=self.service, options=options)
                break

        driver.implicitly_wait(15)
        driver.set_window_rect(0, 0, 1200, 1080)
        return driver

    def main_page_in(self):
        self.driver.get("https://biz.kista.re.kr/ippro/com/iprndMain/selectBusinessAnnounceList.do?bbsType=bs")

        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        data = soup.select('body > div.main_contents > div.sub_contents > form > table > tbody > tr > td.left > a')

        img = soup.select('body > div.main_contents > div.sub_contents > form > table > tbody > tr > td.left > a > img')

        for i in img:
            self.page_list.append(i['src'])

        for i in data:
            t_str = inner_str = re.sub(r"\s", "", i.text)
            self.page_script.append(i['href'])
            self.title_list.append(t_str)

        for i in range(len(self.page_list)):
            if self.page_list[i] == '/ippro/images/btn_now.png':
                self.page_index.append(i)

        for i in self.page_index:
            for j in self.keyword_list:
                if j in self.title_list[i]:
                    self.page_in(i)
                    self.txt_write(self.title_list[i] + ' - ' + self.driver.current_url)
                    self.driver.back()
                    break

    def txt_write(self, string):
        f = open('./Output/IP_Output.txt', 'a', encoding='UTF-8')
        f.write(string)
        f.write('\n')
        f.close()

    def txt_refresh(self):
        f = open('./Output/IP_Output.txt', 'w', encoding='UTF-8')
        f.close()

    def page_in(self, index):
        self.driver.execute_script(self.page_script[index])

    def start(self):
        self.txt_refresh()
        self.driver = self.driver_return()
        self.main_page_in()
        self.driver.close()

#KIAT
class KIAT(object):
    def __init__(self):
        self.driver = None
        self.title_index = []

        self.page_script = []
        self.title_text = []

        self.keyword_list = ['지원분야', '네트워크', '사업화', 'R&D', '엑셀러레이팅', '이노베이션', '데모데이', 'IR']
        self.chrome_ver = get_chrome_version().split('.')[0]  # 크롬드라이버 버전 확인
        self.chrome_driver_path = f'./{self.chrome_ver}/chromedriver.exe'
        self.service = Service(self.chrome_driver_path)

    def driver_return(self):
        options = webdriver.ChromeOptions()
        options.add_argument("headless")

        chrome_ver = get_chrome_version().split('.')[0]  # 크롬드라이버 버전 확인

        while True:
            if os.path.exists(f'./{chrome_ver}'):  # 크롬드라이버 확인
                driver = webdriver.Chrome(service=self.service, options=options)
                break
            else:
                install(True)
                driver = webdriver.Chrome(service=self.service, options=options)
                break

        driver.implicitly_wait(15)
        driver.set_window_rect(0, 0, 1200, 1080)
        return driver

    def title_status_get(self):
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        status = soup.select(
            '#contentsList > div.list_table_area.only_web_list > table > tbody > tr > td.last.td_app_state > span')

        for i in range(len(status)):
            if status[i].text == '접수중':
                self.title_index.append(i)

    def title_text_get_filter(self):
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        for i in self.title_index:
            titles = soup.select(
                f'#contentsList > div.list_table_area.only_web_list > table > tbody > tr:nth-child({i + 1}) > td.alignl.td_title > a')

            for j in titles:
                self.title_text.append(j.text.replace(' ', ''))
                self.page_script.append(j['href'])

        for i in range(len(self.title_text)):
            for j in self.keyword_list:
                if j in self.title_text[i]:
                    self.driver.execute_script(self.page_script[i])
                    self.txt_write(self.title_text[i] + ' - ' + self.driver.current_url)
                    self.driver.back()
                    break

    def txt_refresh(self):
        f = open('./Output/Kiat_Output.txt', 'w', encoding='UTF-8')
        f.close()

    def txt_write(self, string):
        f = open('./Output/Kiat_Output.txt', 'a', encoding='UTF-8')
        f.write(string)
        f.write('\n')
        f.close()

    def main_page_in(self):
        self.driver.get(
            'https://www.kiat.or.kr/front/board/boardContentsListPage.do?board_id=90&MenuId=b159c9dac684471b87256f1e25404f5e')
        sleep(2)

    def start(self):
        self.txt_refresh()
        self.driver = self.driver_return()
        self.main_page_in()
        self.title_status_get()
        self.title_text_get_filter()
        self.driver.close()

#kstartup
class selenium(object):
    def __init__(self):
        self.driver = None
        self.date_list = []
        self.page_num = []

        self.page_index = []

        self.today_date = None

        self.keyword_list = ['지원분야', '네트워크', '사업화', 'R&D', '엑셀러레이팅', '이노베이션', '데모데이', 'IR']

    def driver_return(self):
        chrome_ver = get_chrome_version().split('.')[0]  # 크롬드라이버 버전 확인

        while True:
            if os.path.exists(f'./{chrome_ver}'):  # 크롬드라이버 확인
                driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe')
                break
            else:
                install(True)
                driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe')
                break

        driver.implicitly_wait(15)
        driver.set_window_rect(0, 0, 1200, 1080)
        return driver

    def data_crawling(self, path):
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        data = soup.select(path)

        return data

    def date_compare(self):
        now = datetime.now()
        date_list = [str(now.year), str(now.month), str(now.day)]

        for i in range(len(date_list)):
            if len(date_list[i]) == 1:
                date_list[i] = '0' + date_list[i]

        self.today_date = date_list[0] + '-' + date_list[1] + '-' + date_list[2]

        # 타겟 날짜 설정
        #self.today_date = '2023-07-06'

        for i in range(len(self.date_list)):
            if self.date_list[i] == self.today_date:
                self.page_index.append(i)

    def main_page_in(self):
        self.driver.get("https://www.k-startup.go.kr/web/contents/bizpbanc-ongoing.do")

        self.driver.execute_script("ItgJs.mainPopClose('cmn_pop_pbancList_010');")

    def date_get(self):
        date_list_get = self.data_crawling('#bizPbancList > ul > li > div > div.right > div.bottom > span:nth-child(3)')
        for i in date_list_get:
            temp_str = i.text
            temp_str = re.sub(r"\s", "", temp_str).replace('등록일자', '')

            self.date_list.append(temp_str)

    def href_get(self):
        middle_element = self.driver.find_elements(By.CLASS_NAME, 'middle')
        for i in middle_element:
            a_tag = i.find_element(By.TAG_NAME, 'a')

            a_tag_str = a_tag.get_attribute('href')

            index_1 = a_tag_str.find('(')
            index_2 = a_tag_str.find(')')

            page_num = a_tag_str[index_1+1:index_2]

            self.page_num.append(page_num)

    def url_in_index(self, site_number):
        temp_str = ''

        self.driver.get(f"https://www.k-startup.go.kr/web/contents/bizpbanc-ongoing.do?schM=view&pbancSn={site_number}&page=1&schStr=regist&pbancEndYn=N")

        temp_support_areas = self.data_crawling('#contentViewHtml > div > div > div > div.information_box-wrap > div.bg_box > ul:nth-child(1) > li:nth-child(1) > div > p.txt')

        for i in temp_support_areas:
            temp_str = i.text
            temp_str = re.sub(r"\s", "", temp_str)

        return temp_str

    def keyword_detect(self, keyword):
        if keyword in self.keyword_list:
            return True
        else:
            return False

    def page_title_get(self):
        temp_str = ''
        title = self.data_crawling('#scrTitle')
        for i in title:
            temp_str = i.text
            temp_str = re.sub(r"\s", "", temp_str)

        return temp_str

    def txt_write(self, string):
        f = open('./Output/K_start_up_Output.txt', 'a', encoding='UTF-8')
        f.write(string)
        f.write('\n')
        f.close()

    def data_detect_n_write_txt(self):
        for i in self.page_index:
            support_areas = self.url_in_index(self.page_num[i])
            if self.keyword_detect(support_areas):
                title = self.page_title_get()
                self.txt_write(title + ' - ' + self.driver.current_url)

    def txt_refresh(self):
        f = open('./Output/K_start_up_Output.txt', 'w', encoding='UTF-8')

    def start(self):
        self.txt_refresh()
        self.driver = self.driver_return()
        self.main_page_in()
        self.date_get()
        self.date_compare()
        self.href_get()
        self.data_detect_n_write_txt()
        self.driver.close()

#SBA
class Seoul(object):
    def __init__(self):
        self.href_list = []
        self.title_list = []

        self.keyword_list = ['지원분야', '네트워크', '사업화', 'R&D', '엑셀러레이팅', '이노베이션', '데모데이', 'IR']

    def main_page_in(self):
        req = requests.get("https://seoul.rnbd.kr/client/c030100/c030100_00.jsp")
        page_source = BeautifulSoup(req.text, "html.parser")

        a = page_source.select(
            '#contents > div.cnt_con.board.business_notice > div.board_list.basic > table > tbody > tr > td:nth-child(4) > span')

        hrefs = page_source.select(
            '#contents > div.cnt_con.board.business_notice > div.board_list.basic > table > tbody > tr > td.t1 > a')

        for i in range(len(a)):
            if a[i].text == '모집중':
                self.href_list.append(hrefs[i]['href'])
                self.title_list.append(hrefs[i].text)

        for i in range(len(self.href_list)):
            index = self.href_list[i].find("_")
            temp_href = self.href_list[i][:index]

            req = requests.get(f"https://seoul.rnbd.kr/client/{temp_href}/{self.href_list[i]}")

            page_source = BeautifulSoup(req.text, "html.parser")

            page_source.select(
                '#contents > div.cnt_con.board.business_notice > div > form > table > tbody > tr:nth-child(3) > td')

            temp_str = ''

            for j in page_source:
                t_str = j.text
                t_str = re.sub(r"\s", "", t_str)

                temp_str += t_str

            for j in self.keyword_list:
                if j in temp_str:
                    self.txt_write(self.title_list[
                                       i] + ' - ' + f"https://seoul.rnbd.kr/client/{temp_href}/{self.href_list[i]}")
                    break

    def txt_write(self, string):
        f = open('./Output/SBA_Output.txt', 'a', encoding='UTF-8')
        f.write(string)
        f.write('\n')
        f.close()

    def txt_refresh(self):
        f = open('./Output/SBA_Output.txt', 'w', encoding='UTF-8')
        f.close()

    def start(self):
        self.txt_refresh()
        self.main_page_in()

#SMTACH
class SMTECH(object):
    def __init__(self):
        self.title_index = []

        self.title_list = []

        self.title_url = []

        self.page_source = None

        self.keyword = ['사업화', 'R&D', '엑셀러레이팅', '이노베이션', '데모데이']

    def title_get(self):
        for i in range(16):
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

    def start(self):
        self.txt_refresh()
        self.img_type_get()
        self.title_get()
        self.href_get()
        self.title_page_in()


class SlackAPI:
    """
    슬랙 API 핸들러
    """

    def __init__(self, token):
        # 슬랙 클라이언트 인스턴스 생성
        self.client = WebClient(token)
        self.file_name = [['SMTECH 지원사업 입니다.', './Output/SMTECH_Output.txt'],
                     ['서울경제진흥원 지원사업 입니다.', './Output/SBA_Output.txt'],
                     ['K-startup 지원사업 입니다.', './Output/K_start_up_Output.txt'],
                     ['Kiat 지원사업 입니다.', './Output/Kiat_Output.txt'],
                     ['IP R&D포털 지원사업 입니다.', './Output/IP_Output.txt'],
                     ['Iitp 지원사업 입니다.', './Output/iitp_Output.txt'],
                     ['기업마당 지원사업 입니다.', './Output/bizinfo_Output.txt'],
                     ['Nipa 지워사업 입니다.', './Output/nipa_Output.txt']]

    def get_channel_id(self, channel_name):
        """
        슬랙 채널ID 조회
        """
        # conversations_list() 메서드 호출
        result = self.client.conversations_list()
        # 채널 정보 딕셔너리 리스트
        channels = result.data['channels']
        # 채널 명이 'test'인 채널 딕셔너리 쿼리
        channel = list(filter(lambda c: c["name"] == channel_name, channels))[0]
        # 채널ID 파싱
        channel_id = channel["id"]
        return channel_id

    def get_message_ts(self, channel_id, query):
        """
        슬랙 채널 내 메세지 조회
        """
        # conversations_history() 메서드 호출
        result = self.client.conversations_history(channel=channel_id)
        # 채널 내 메세지 정보 딕셔너리 리스트
        messages = result.data['messages']
        # 채널 내 메세지가 query와 일치하는 메세지 딕셔너리 쿼리
        message = list(filter(lambda m: m["text"] == query, messages))[0]
        # 해당 메세지ts 파싱
        message_ts = message["ts"]
        return message_ts

    def post_thread_message(self, channel_id, message_ts, text):
        """
        슬랙 채널 내 메세지의 Thread에 댓글 달기
        """
        # chat_postMessage() 메서드 호출
        result = self.client.chat_postMessage(
            channel=channel_id,
            text=text,
            thread_ts=message_ts
        )
        return result

    def post_message(self, channel_id, text):
        """
        슬랙 채널에 메세지 보내기
        """
        # chat_postMessage() 메서드 호출
        result = self.client.chat_postMessage(
            channel=channel_id,
            text=text
        )
        return result

    def file_read_to_slack(self):
        channel_name = "테스트"
        query = f"오늘({datetime.today().year}년{datetime.today().month}월{datetime.today().day}일)의 정부지원사업들을 알려줄게요!"
        datetime.today().year  # 현재 연도 가져오기

        datetime.today().month  # 현재 월 가져오기

        datetime.today().day  # 현재 일 가져오기

        datetime.today().hour  # 현재 시간 가져오기
        # 채널ID 파싱
        slack.post_message(channel_name, query)
        channel_id = slack.get_channel_id(channel_name)
        # 메세지ts 파싱
        message_ts = slack.get_message_ts(channel_id, query)
        for i in self.file_name:
            filename = i[1]
            with open(filename, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                print(i[0])
                if not lines:
                    print('해당 기관은 없네요.')
                else:
                    for line in lines:
                        line = line.strip()
                        slack.post_thread_message(channel_id, message_ts, line)


if __name__ == "__main__":
    SMTECH = SMTECH()
    madang = madang()
    evaluator = evaluator()
    IP = IP()
    nipa = nipa()
    KIAT = KIAT()
    selenium = selenium()
    Seoul = Seoul()

    SMTECH.start()
    Seoul.start()
    selenium.start()
    KIAT.start()
    IP.start()
    evaluator.start()
    nipa.start()
    madang.start()

    sleep(1)
    print('크롤링 끝!')
    token = "xoxb-5612875251568-5586282896005-3eZ7ZzvFdqiiNFlqfyFv3hQQ"
    slack = SlackAPI(token)
    slack.file_read_to_slack()
