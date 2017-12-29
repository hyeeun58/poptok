from bs4 import BeautifulSoup
from selenium import webdriver
from common.file_io import error_print
from common.file_io import set_last_index
import time
import sys

import re
from collection.replys import search_replys



# 상점 코드별 댓글 추출
#def search_shops(shop_name):
def search_shops(shop_name, db_addr, location_tuple):

    # 주소 셋팅
    wd = webdriver.Chrome('D:/Python/webdriver/chromedriver.exe')
    query = '/?from=total&nil_suggest=btn&tab=place&q=' + shop_name
    wd.get('http://map.daum.net' + query)

    # 페이지 초기 로딩 = 검색결과
    time.sleep(1)
    html = wd.page_source
    bs = BeautifulSoup(html, 'html.parser')

    # 페이징 반복 횟수 추출
    total_cnt = bs.find('em', attrs={'id': 'info.search.place.cnt'}).text.replace(',', '')
    if (int(total_cnt) > 500):
        total_cnt = 500
    total_page = (int(total_cnt) // 15)
    if (int(total_cnt) % 15 > 0):
        total_page = total_page + 1
    page_cnt = 1
    result_list = []
    reply_lists = []
    return_list = []

    try:
        # 페이징 반복
        while ((page_cnt > 0) and (page_cnt <= total_page)):

            # 2페이지 이상이면
            if(page_cnt > 1):
                # 페이지 클릭
                if (page_cnt % 5 == 0):
                    wd.find_element_by_id('info.search.page.no{0}'.format(5)).click()
                elif (page_cnt % 5 != 1):
                    wd.find_element_by_id('info.search.page.no{0}'.format(page_cnt % 5)).click()
                elif (page_cnt != 1 and page_cnt % 5 == 1):
                    wd.find_element_by_id('info.search.page.next').click()

                # 페이지 재로딩
                if (page_cnt != 1):
                    time.sleep(1)
                    html = wd.page_source
                    bs = BeautifulSoup(html, 'html.parser')

            # 페이지별 목록 추출(최대 15개)
            content_all = bs.find('ul', attrs={'id': 'info.search.place.list'})
            contents = content_all.findAll('li', attrs={'class': 'PlaceItem'})
            # time.sleep(3)

            # 다음맵 검색 결과별
            for content in contents:
                content_names = content.find('a', attrs={'data-id': 'name'})  # 상호명
                content_newaddrs = content.find('p', attrs={'data-id': 'newaddr'})  # 도로명주소
                content_oldaddrs = content.find('span', attrs={'data-id': 'address'})  # 지번 주소
                content_reply_cnt = content.find('a', attrs={'data-id': 'numberofscore'})  # 댓글(평가) 수
                content_mores = content.find('a', attrs={'data-id': 'moreview'})  # 상세보기 링크

                name = content_names.text
                addr_new = content_newaddrs.text
                addr_old = content_oldaddrs.text
                reply_cnt = content_reply_cnt.text
                more_href = content_mores.get("href").split("/")

                # [0]:상호명, [1]:cid, [2]:댓글건수, [3]:도로명주소
                shop_list = ()
                shop_list = (name, more_href[3], reply_cnt, addr_new.strip().replace(' ', ''))

                if(more_href[2] != 'place.map.daum.net'):
                    #print("****** No Shop ******")
                    continue
                elif(reply_cnt != "0건"):
                    result_list.append(dict)
                    # -*-*-*-*-*-*-*-*-*-다음 검색 후 바로 비교/댓글 추출 start -*-*-*-*-*-*-*-*-*-*-*-
                    db_addr = change_specialChar(db_addr)
                    shop_addr = change_specialChar(shop_list[3])

                    if (shop_addr.strip() != ""):
                        if ( (re.findall(shop_addr, db_addr)) or (re.findall(db_addr, shop_addr)) ):
                            print("****** Find Shop ******")
                            reply_list = {}
                            reply_list = search_replys(shop_list[1], location_tuple)
                            return_list = reply_list
                            #print(return_list)
                            #reply_lists.append(reply_list)

                            # DB poptok.post 테이블에 저장
                            #input_results = exec_query("", "insert", reply_list)

                            # 파일에 마지막 인덱스번호 쓰기
                            #set_last_index(location_tuple[0])


                            break

                    # -*-*-*-*-*-*-*-*-*-다음 검색 후 바로 비교/댓글 추출 e n d -*-*-*-*-*-*-*-*-*-*-*-

            # 카운팅 증가
            page_cnt = page_cnt + 1

    except Exception as e:
        # print(e)
        # print('ERROR =>> ', sys.exc_info())
        error_print(e, "shops", location_tuple[0], "MF")

    finally:
        time.sleep(1)
        wd.quit()

        #return result_list
        return return_list



def change_specialChar(str):

    str = str.replace('(', '<').replace(')', '>').replace('[', '<').replace(']', '>') \
            .replace('.', ',').replace('*', '&').replace('+', '＋')

    return str



if __name__ == '__main__':

    shop_word = '흑돈가'
    # shop_word = '담소사골순대'
    search_shops(shop_word)

    # print(sys.path)