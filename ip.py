import os
import re
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


class IP(object):
    def __init__(self):
        self.driver = None

        self.page_list = []
        self.title_list = []

        self.page_index = []
        self.page_script = []

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
        f = open('./Output.txt', 'a', encoding='UTF-8')
        f.write(string)
        f.write('\n')
        f.close()

    def txt_refresh(self):
        f = open('./Output.txt', 'w', encoding='UTF-8')
        f.close()

    def page_in(self, index):
        self.driver.execute_script(self.page_script[index])

    def start(self, refresh = True):
        if refresh:
            self.txt_refresh()

        self.driver = self.driver_return()
        self.main_page_in()
        self.driver.close()


if __name__ == "__main__":
    IP = IP()
    IP.start()