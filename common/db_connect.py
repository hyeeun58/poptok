from common.file_io import error_print
import pymysql
import common.config



def exec_query(sql_query, mode, values):
    result = []
    err_msg = ''

    # MySQL 또는 MariaSQL에 연결
    conn = pymysql.connect(host=common.config.host, port=common.config.port,\
                           user=common.config.user, password=common.config.password,\
                           database=common.config.database, charset=common.config.charset)

    try:
        # 커서 생성
        # cursor는 python에서의 query를 db와 연결해주는 연동해주는 역할을 하는 듯
        # pymysql.cursors.DictCursor: 결과를 dictionary 형태로 보여줌
        # sql을 실행하고 select 구문 결과를 접근할 수 있는 커서 생성
        curs = conn.cursor(pymysql.cursors.DictCursor)

        # 쿼리 수행
        # cursor의 execute를 통해, db에서 query 수행
        if(mode == "insert"):

            for value in values:
                # for v in value:
                #     # DB insert 프로시저 호출
                #     # DB location No, 작성자, 댓글내용, 작성일자, 해시태그, 위도, 경도
                #     rslt = curs.callproc("P_PostDataInsertForDaum", v)
                #     result.append(rslt)
                # -*-*-*-*-*-*-*-*-*-다음맵 검색 후 바로 비교/댓글 추출 start -*-*-*-*-*-*-*-*-*-*-*-
                rslt = curs.callproc("P_PostDataInsertForDaum", value)
                print(rslt)
                #result.append(rslt)
                # -*-*-*-*-*-*-*-*-*-다음맵 검색 후 바로 비교/댓글 추출 end -*-*-*-*-*-*-*-*-*-*-*-

        else:
            curs.execute(sql_query, values)

            # 수행 결과 담아오기
            # select 결과에 접근할 수 있는 iterator 생성
            data = curs.fetchall()

            cnt = 0
            for d in data:
                result.append(d)
                cnt = cnt + 1

        return result

    except Exception as e:
        error_print(e, "db_connect", "", "MF")

    finally:
        # db 연결 끊음
        conn.close()




# 메인
if __name__=='__main__':
    
    # # SQL문
    # query = " SELECT businessName, newAddress, locationNo " + \
    #         " FROM  locationInfo " + \
    #         " WHERE businessName like '%흑돈가%' " + \
    #         " ORDER BY  businessName"
    #
    # # 수행
    # results = exec_query(query)
    #
    # # 결과 출력
    # for result in results:
    #     no = result.get('locationNo')
    #     name = result.get('businessName')
    #     addr = result.get('newAddress')
    #     print("[" + no + "] " + name + " = " + addr)


    # 프로시져 호출/응답 테스트
    conn = pymysql.connect(host=common.config.host, port=common.config.port,\
                           user=common.config.user, password=common.config.password,\
                           database=common.config.database, charset=common.config.charset)
    curs = conn.cursor(pymysql.cursors.DictCursor)
    v = (32, '홍길남', '10년째 잘먹고 있습니다람쥐', '2017.12.20.', \
         '#10, #10년, #년', '126.92765540000000000', '37.49922947000000000', 0)
    rslt = curs.callproc("P_PostDataInsertForDaum", v)
    print(v)