import datetime
from time import sleep, time
import time

import random
import requests
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from lib import common_test
Common = common_test.Common

chrome_options = Options()
chrome_options.add_argument('start-maximized')
chrome_options.add_argument('enable-automation')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--window-size=1280x1696')
chrome_options.add_argument('--user-data-dir=/tmp/user-data')
chrome_options.add_argument('--enable-logging')
chrome_options.add_argument('--log-path=/home/log_chromedriver/chromedriver.log')
chrome_options.add_argument('--log-level=0')
chrome_options.add_argument('--v=99')
chrome_options.add_argument('--single-process')
chrome_options.add_argument('--data-path=/tmp/data-path')
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--homedir=/tmp')
chrome_options.add_argument('--disk-cache-dir=/tmp/cache-dir')
chrome_options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')


# proxy 리스트 - 무료
def get_proxy_api():
    url = "https://proxylist.geonode.com/api/proxy-list?limit=150&page=1&sort_by=lastChecked&sort_type=desc&filterLastChecked=50&protocols=https%2Chttps%2Csocks4%2Csocks5"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        ip_addresses = [item["ip"] for item in data["data"]]
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        ip_addresses = []
    
    return ip_addresses

    
# 오늘 날짜
todayhh = datetime.datetime.now().strftime("%Y%m%d%H")
# 검색할 키워드 목록
d = Common.list_keyword()
agent = [0, 1]


for i in range(len(d)):

    if i == 3:
        break
    # 모바일
    #_filename_html = "/home/search_keyword_ver3/testhtml/" + todayhh + "_" + str(d[i][0]) + "_m.html"
    #crawl_url = 'https://m.search.naver.com/search.naver?sm=mtp_hty.top&where=m&query=' + str(d[i][0])
    
    # PC
    _filename_html = "/home/search_keyword_ver3/testhtml/" + todayhh + "_" + str(d[i][0]) + ".html"
    crawl_url = 'https://search.naver.com/search.naver?ie=UTF-8&sm=whl_hty&query=' + str(d[i][0])

    print(crawl_url)
    
    try:
        # proxy 서버 ip
        proxy_server_list = get_proxy_api()
        proxy_server = None  # 초기화
        print("Proxy List count:", len(proxy_server_list))
        
        proxy_server = random.choice(proxy_server_list)
        print("proxy : " + proxy_server)
        
        webdriver.DesiredCapabilities.CHROME['proxy'] = {
            "httpProxy": proxy_server,
            "ftpProxy": proxy_server,
            "sslProxy": proxy_server,
            "proxyType": "MANUAL"
        }

        # Chrome WebDriver 이용해 chrome 실행
        driver = webdriver.Chrome('/home/chromedriver', options=chrome_options)
        driver.get(crawl_url)

        #get url 페이지 로딩 대기
        driver.implicitly_wait(5)

        #웹드라이버 페이지 소스 html에 저장
        html = driver.page_source

        # 창 최대화
        #driver.maximize_window()
        # 스크린샷 찍기
        #driver.save_screenshot("/home/search_keyword_ver3/capture.png")
        #print("save")

        #페이지 소스 파일 저장
        Common.file_create(_filename_html, html, 0)
        print(_filename_html + " created.")

        file_create_time_li = Common.file_create_time(_filename_html, 1)
        driver.quit()
    except Exception as e:
        print(e)
    

    time.sleep(random.randrange(5, 10))
