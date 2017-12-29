from collection.shops import search_shops
from collection.replys import search_replys
from common.db_connect import exec_query
from common.file_io import error_print
from common.file_io import set_last_index
import common.common
import datetime
import re



def compare(db_list):

    #shop_list = []
    reply_lists = []
    last_no = ""

    # DB 상호 목록별
    for result in db_list:

        try:
            # DB에서 읽어온 상점 정보
            no = result.get('no')
            name = result.get('name')
            db_addr = result.get('addr').strip().replace(' ', '')
            lat = result.get('lat')
            lon = result.get('lon')
            location_tuple = ()
            location_tuple = (no, lat, lon)
            last_no = no

            print('-- location_no => ' + str(no) + "  [" + common.common.current_time() + "]")

            # 이전에 검색한 DB상호명과 다르면 다음맵에서 다시 검색
            #shop_lists = search_shops(name)
            shop_list = ()
            shop_lists = search_shops(name, db_addr, location_tuple)

            # DB 상호명으로 다음(daum)맵에서 검색한 상호 목록 중
            # for shop_list in shop_lists:
            #
            #     # DB 주소의 특수문자 처리
            #     db_addr = change_specialChar(db_addr)
            #     # 다음맵 검색 데이터의 특수문자 처리
            #     shop_addr = change_specialChar(shop_list[3])
            #     #print("└ (" + shop_list[2] + ") " + shop_list[3])
            #
            #     # 다음(DAUM)맵에서 검색한 주소 데이터가 공백이 아니고
            #     if (shop_addr.strip() != ""):
            #         # DB 상점 주소와 일치(포함)하는 다음맵의 특정 상점정보 추출
            #         if ( (re.findall(shop_addr, db_addr)) or (re.findall(db_addr, shop_addr)) ):
            #             # 댓글 추출
            #             reply_list = {}
            #             reply_list = search_replys(shop_list[1], location_tuple)
            #             reply_lists.append(reply_list)
            #
            #             # DB poptok.post 테이블에 저장
            #             #input_results = exec_query("", "insert", reply_list)
            #
            #             # 파일에 마지막 인덱스번호 쓰기
            #             f = open('D:/Last_LocationNo.txt', 'w')
            #             f.write(str(no))
            #             f.close()
            #
            #             continue

            # -*-*-*-*-*-*-*-*-*-다음 검색 후 바로 비교/댓글 추출 start -*-*-*-*-*-*-*-*-*-*-*-

            # shop_lists = (DB location No, 위도, 경도, 작성자, 댓글내용, 작성일자, 해시태그)
            # DB poptok.post 테이블에 저장
            input_results = exec_query("", "insert", shop_lists)

            # 파일에 마지막 인덱스번호 쓰기
            set_last_index(location_tuple[0])

            # -*-*-*-*-*-*-*-*-*-다음 검색 후 바로 비교/댓글 추출 e n d -*-*-*-*-*-*-*-*-*-*-*-

        except Exception as e:
            error_print(e, "compare", last_no, "MF")
        finally:
            import datetime

    return reply_lists


def change_specialChar(str):

    # print("└ [1. " + str(re.findall(addr, shop_addr)) + "]")
    # print("└ [2. " + str(re.findall(shop_addr, addr)) + "]")
    # 정규표현식 . ^ $ * + ? { } [ ] \ | ( )
    # . => Dot(.) : 줄바꿈 문자인 \n를 제외한 모든 문자와 매치됨을 의미. []내에선 메타문자.
    #       예) a.b = "a + 모든문자 + b" => a와 b라는 문자 사이에 어떤 문자가 들어가도 모두 매치
    #       예) a[.]b = "a + Dot(.)문자 + b" =>
    # ^
    # $
    # * => 반복. * 바로 앞에 있는 특정 문자가 0.부.터. 무.한.대.로. 반복 가능.
    # + => 반복. + 는 최소 1.번. 이.상. 반복될 때 사용
    #      예) ca+t : c + a(1번 이상 반복) + t"
    # ?
    # { }
    # [ ] => 문자클래스. []내에 어떤 문자나 메타 문자와도 사용 가능. 단, 메타문자 ^제외(반대=NOT를 의미)
    #        []내 입력된 문자 중 한 개 문자와 매치. 예) [abc] a,b,c중 한개와 매치. "ant"=매치, "dog"=비매치
    #        []내 입력시 문자사이에 -는 From-To를 뜻함. 예) [0-9] 0부터 9까지. [a-zA-Z] 모든 알파벳 의미
    #    => 자주 사용하는 문자 클래스.
    #        [\d] = [0-9] : 숫자와 매치.
    #        [\D] = [^0-9] : 숫자 아닌 것과 매치
    #        [\s] = [ \t\n\r\f\v] : whitespace 문자와 매치. 맨 앞의 빈 칸은 공백문자(space)를 의미
    #        [\S] = [^ \t\n\r\f\v] : whitespace 문자가 아닌 것과 매치
    #        [\w] = [a-zA-Z0-9] : 문자+숫자(alphanumeric)와 매치
    #        [\W] = [^a-zA-Z0-9] : 문자+숫자(alphanumeric)가 아닌 문자와 매치
    # \
    # |
    # ( )
    str = str.replace('(', '<').replace(')', '>').replace('[', '<').replace(']', '>') \
            .replace('.', ',').replace('*', '&').replace('+', '＋')

    return str




if __name__ == '__main__':
    db_list = [{'name':'흑돈가 창원점','no':1,'addr':'경남 창원시 성산구 용지로 96 하이페르'}, \
               {'name':'본흑돈가','no':1,'addr':'충남 당진시 무수동1길 22 1층'}, \
               {'name':'흑돈가','no':1,'addr':'경남 사천시 사천읍 수양로 27'}, \
               {'name':'흑돈가','no':1,'addr':'제주특별자치도 제주시 한라대학로 11'}]

    compare(db_list)

    # print(sys.path)