from bs4 import BeautifulSoup
from selenium import webdriver
from konlpy.tag import Kkma
import time



# 상점 코드별 댓글 추출
def search_replys(shop_code, location_tuple):

    # 주소 셋팅
    url = 'https://place.map.daum.net/m/' + shop_code + '#comment'
    wd = webdriver.Chrome('D:/Python/webdriver/chromedriver.exe')
    wd.get(url)

    # 페이지 로딩
    bs_1 = loading_page(wd)

    # 댓글 전체수로 노출 페이지('더보기'버튼) 수 추출
    total_cnt = bs_1.find('span', attrs={'class': 'txt_person color_b'}).text
    repeat_cnt = int(total_cnt) // 10
    if(int(total_cnt) % 10 == 0):
        repeat_cnt = repeat_cnt - 1
    cnt = 1
    time.sleep(1)

    # [카카오맵 열기] 버튼 닫기
    btn_close = wd.find_elements_by_class_name('btn_close')
    btn_close[1].click()


    # 전체 댓글 출력
    while cnt <= repeat_cnt:
        # 한 페이지(10개) 미만 시 더보기 버튼 없음
        if (repeat_cnt > 1):
            # xpath로 객체 추출
            elements = wd.find_element_by_xpath('//*[@id="mArticle"]/div[9]/div/div[2]/a')
            # 스크롤 다운
            wd.execute_script('window.scrollTo(0, 100000)')
            # 더보기 버튼 클릭
            elements.click()

            # 페이지 재로딩
            bs_2 = loading_page(wd)

        cnt = cnt + 1

    #페이지 재로딩
    bs_3 = loading_page(wd)

    # 더보기 한 페이지당 댓글 목록(10개씩) 추출
    lists = bs_3.find('ul', attrs={'class': 'list_grade'})
    contents = lists.findAll('li')

    # 댓글 결과물
    output_tuple = output_replys(contents, shop_code, location_tuple)

    wd.quit()

    #return contents
    return output_tuple



# 페이지 로딩
def loading_page(wd):
    time.sleep(2)
    html = wd.page_source
    bs = BeautifulSoup(html, 'html.parser')
    time.sleep(1)

    return bs



# 댓글 결과물(프린트/리스트)
def output_replys(contents, shop_code, loc):

    output_list = []
    replys = ()
    for content in contents:
        # 작성자 닉네임, 작성일자, 댓글 내용
        writer = content.find('span', attrs={'class': 'name_user loss_word'}).text
        wdate = content.find('span', attrs={'class': 'time_write'}).text
        reply = content.find('p', attrs={'class': 'txt_comment'}).text
        #time.sleep(1)

        replys = ()
        # DB location No, 위도, 경도, 작성자, 댓글내용, 작성일자, 해시태그
        replys = (loc[0], writer, reply, wdate, make_tags(reply), loc[1], loc[2], 0)
        output_list.append(replys)

    return output_list



# 해시태그 추출
def make_tags(words):

    result_tag = ""
    kkma = Kkma()
    nouns = kkma.nouns(words)

    for index, n in enumerate(nouns):
        if(index > 0):
            result_tag += ", "
        result_tag += ("#" + n)

    return result_tag




# 메인
if __name__=='__main__':
    shop_code = '1754846295'
    search_replys(shop_code)