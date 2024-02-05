from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from chromedriver_autoinstaller import get_chrome_version, install
import os
from time import sleep
import re
from datetime import datetime


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
        f = open('./Output.txt', 'a', encoding='UTF-8')
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
        f = open('./Output.txt', 'w', encoding='UTF-8')

    def start(self, refresh = True):
        if refresh:
            self.txt_refresh()

        self.driver = self.driver_return()
        self.main_page_in()
        self.date_get()
        self.date_compare()
        self.href_get()
        self.data_detect_n_write_txt()
        self.driver.close()


if __name__ == "__main__":
    selenium = selenium()
    selenium.start()