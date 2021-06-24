from rest_framework.common.services import Reader, Printer, Scraper
from rest_framework.common.entity import FileDTO
import numpy as np
import pandas as pd
import folium
from selenium import webdriver
from glob import glob
import re

'''
문제정의
셀프 주유소는 정말 저렴할까?
4-1 Selenium 사용하기
4-2 서울시 구별 주유소 가격 정보 얻기
4-5 구별 주유 가격에 대한 데이터의 정리
4-6 서울시 주유 가격 상하위 10개 주유소 지도에 표기하기
'''

'''
<class 'pandas.core.frame.DataFrame'>
Int64Index: 537 entries, 0 to 45
Data columns (total 10 columns):
 #   Column  Non-Null Count  Dtype 
---  ------  --------------  ----- 
 0   지역      537 non-null    object
 1   상호      537 non-null    object
 2   주소      537 non-null    object
 3   상표      537 non-null    object
 4   전화번호    537 non-null    object
 5   셀프여부    537 non-null    object
 6   고급휘발유   537 non-null    object
 7   휘발유     537 non-null    object
 8   경유      537 non-null    object
 9   실내등유    537 non-null    object
dtypes: object(10)
memory usage: 46.1+ KB
'''

class Service():

    def __init__(self):
        self.file = FileDTO()
        self.reader = Reader()
        self.printer = Printer()
        self.scraper = Scraper()


    def get_url(self):
        file = self.file
        reader = self.reader
        printer = self.printer
        scraper = self.scraper
        file.url = 'https://www.opinet.co.kr/searRgSelect.do'
        driver = scraper.driver()
        print(driver.get(file.url))

        gu_list_raw = driver.find_element_by_xpath("""//*[@id="SIGUNGU_NMO"]""")
        gu_list = gu_list_raw.find_dlements_by_tag_name("option")
        gu_names =[option.get_attribute("value") for option in gu_list]
        gu_names.remove('')
        print(gu_names)

    def gas_station_price_info(self):
        file = self.file
        reader = self.reader
        #print(glob('./data/지역_위치별*xls'))
        station_files = glob('./data/지역_위치별*xls')
        tmp_raw = []
        for i in station_files:
            t = pd.read_excel(i, header=2)
            tmp_raw.append(t)
        station_raw = pd.concat(tmp_raw)  # 파일 전체 합치기
        station_raw.info()
        '''
        print("*"*100)
        print(station_raw.head(2))
        print(station_raw.tail(2))
        '''

        stations = pd.DataFrame({'Oil_store':station_raw['상호'],
                                 '주소':station_raw['주소'],
                                 '가격':station_raw['휘발유'],
                                 '셀프':station_raw['셀프여부'],
                                 '상표':station_raw['상표']})
        #print(stations.head())
        stations['구'] = [i.split()[1] for i in stations['주소']]
        stations['구'].unique()  # unique 중복 값 제거 하나의 데이터만 출력
        # print(stations[stations['구']=='서울특별시'])
        #          Oil_store                           주소    가격 셀프     상표      구
        # 12  SK네트웍스(주)효진주유소  1 서울특별시 성동구 동일로 129 (성수동2가)  1654  N  SK에너지  서울특별시

        stations[stations['구'] == '서울특별시'] = '성동구'
        stations['구'].unique()
        #print(stations[stations['구'] == '특별시'])
        #Oil_store                        주소    가격 셀프     상표    구
        #  10     서현주유소  서울 특별시 도봉구 방학로 142 (방학동)  1524  Y  S-OIL  특별시

        stations[stations['구'] == '서울특별시'] = '도봉구'
        stations['구'].unique()
        # print(stations[stations['가격'] == '-'])
        '''
                Oil_store                          주소 가격 셀프     상표     구
        18  명진석유(주)동서울주유소  서울특별시 강동구  천호대로 1456 (상일동)  -  Y  GS칼텍스   강동구
        33          하나주유소   서울특별시 영등포구  도림로 236 (신길동)  -  N  S-OIL  영등포구
        12   (주)에이앤이청담주유소    서울특별시 강북구 도봉로 155  (미아동)  -  Y  SK에너지   강북구
        13          송정주유소    서울특별시 강북구 인수봉로 185 (수유동)  -  N   자가상표   강북구

        '''

        '''
        stations = stations[stations['가격'] != '-']

        p = re.compile('^[0-9]+$')
        for i in stations:
            temp_stations.append(stations[stations['가격'] != p.match(stations['가격'][1])])
        stations = stations[stations['가격'] != p.match()]
        stations['가격'] = [ float(i) for i in stations['가격']]
        stations.reset_index(inplace=True)
        del stations['index']
        #printer.dframe(stations)
        '''



if __name__ == '__main__':
    s = Service()
    #s.get_url()
    s.gas_station_price_info()
