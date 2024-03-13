import selenium
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
#from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.common.exceptions import NoSuchElementException

# # 웹브라우저를 띄우지 않고 진행하기 위한 설정
options = ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver_path = 'chromedriver.exe'

# 데이터 수집하는 범위를 축소하기 위해 page_num = 10으로 설정
def get_movie_reviews(url, page_num = 10):
    wd = webdriver.Chrome('chromedriver',options=options)
    wd.get(url)

    writer_list = []
    review_list = []
    date_list = []

    for page_no in range(1,page_num+1):
        try:
            page_ul = wd.find_element(By.CLASS_NAME,'pageing_point')
            page_num = page_ul.find_element(By.LINK_TEXT,str(page_no))
            # 링크를 .click()을 통해 이동
            page_num.click() # click() : 요소를 클릭하는것
            time.sleep(1)

            # 작성자 가져오기
            # element는 첫번째 요소만 return, elements는 여러개 리스트로 return
            writers = wd.find_elements(By.CLASS_NAME,'write-name')
            writer_list += [writers.text for writer in writers]

            # 리뷰 가져오기
            reviews = wd.find_element(By.CLASS_NAME,'box-comment')
            review_list += [reviews.text for review in reviews]

            # 날짜 가져오기
            dates = wd.find_element(By.CLASS_NAME,'day')
            date_list += [dates.text for date in dates]

            if page_no % 10 == 0:
                next_button = page_ul.find_element(By.CLASS_NAME,'btn-paging next')
                next_button.click()
                time.sleep(1)

        # 마지막 페이지까지 갔을 경우 예외처리
        except NoSuchElementException:
            break
    
    # 결과 csv파일로 저장하기
    df = pd.DataFrame({'작성자': writer_list, 
                       '리뷰내용' : review_list,
                       '날짜': date_list})
    
    review_info = df.to_csv("review_info.csv")

    print(review_info)

    return review_info

url = 'http://www.cgv.co.kr/movies/detail-view/?midx=88012'
get_movie_reviews(url, 12)
get_movie_reviews