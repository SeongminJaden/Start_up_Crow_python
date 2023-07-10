from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from chromedriver_autoinstaller import get_chrome_version, install
import re
import os
from time import sleep
from datetime import datetime

class KIAT(object):
    def __init__(self):
        self.driver = None
        self.title_index = []

        self.page_script = []
        self.title_text = []

        self.keyword_list = ['지원분야', '네트워크', '사업화', 'R&D', '엑셀러레이팅', '이노베이션', '데모데이', 'IR']

    def driver_return(self):
        options = webdriver.ChromeOptions()
        options.add_argument("headless")

        chrome_ver = get_chrome_version().split('.')[0]  # 크롬드라이버 버전 확인

        while True:
            if os.path.exists(f'./{chrome_ver}'):  # 크롬드라이버 확인
                driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe', options=options)
                break
            else:
                install(True)
                driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe', options=options)
                break

        driver.implicitly_wait(15)
        driver.set_window_rect(0, 0, 1200, 1080)
        return driver

    def title_status_get(self):
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        status = soup.select('#contentsList > div.list_table_area.only_web_list > table > tbody > tr > td.last.td_app_state > span')

        for i in range(len(status)):
            if status[i].text == '접수중':
                self.title_index.append(i)

    def title_text_get_filter(self):
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        for i in self.title_index:
            titles = soup.select(f'#contentsList > div.list_table_area.only_web_list > table > tbody > tr:nth-child({i+1}) > td.alignl.td_title > a')

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
        f = open('./Output.txt', 'w', encoding='UTF-8')
        f.close()

    def txt_write(self, string):
        f = open('./Output.txt', 'a', encoding='UTF-8')
        f.write(string)
        f.write('\n')
        f.close()

    def main_page_in(self):
        self.driver.get('https://www.kiat.or.kr/front/board/boardContentsListPage.do?board_id=90&MenuId=b159c9dac684471b87256f1e25404f5e')
        sleep(2)

    def start(self):
        self.txt_refresh()
        self.driver = self.driver_return()
        self.main_page_in()
        self.title_status_get()
        self.title_text_get_filter()
        self.driver.close()


if __name__ == "__main__":
    KIAT = KIAT()
    KIAT.start()