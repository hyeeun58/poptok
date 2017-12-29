from common.db_connect import exec_query
from collection.shops import search_shops
from collection.compare import compare
from common.file_io import error_print
from common.file_io import get_last_index
import common.common



# DB 상점 정보 조회 ---------------------------

# SQL문
query_select = " SELECT businessName as name, locationNo as no, " +\
                " case when substring_index(newAddress,' ',1) in " +\
                " ('서울특별시','대전광역시','대구광역시','부산광역시','광주광역시'," +\
                " '인천광역시','울산광역시','강원도','경기도') " +\
                " then concat(substring(newAddress,1,2), " +\
                " substring(newAddress,(length(substring_index(newAddress,' ',1))/3)+1)) " +\
                " when substring_index(newAddress,' ',1) in " +\
                " ('충청북도','충정남도','경상북도','경상남도','전라북도','전라남도') " +\
                " then concat(substring(newAddress,1,1), substring(newAddress,3,1), " +\
                " substring(newAddress,(length(substring_index(newAddress,' ',1))/3)+1)) " +\
                " else newAddress end as addr " +\
                " , latitude as lat, longitude as lon" +\
                " FROM  poptok.locationInfo " +\
                " WHERE locationNo >= %s " +\
                " AND	newAddress LIKE '서울%%' " +\
                " LIMIT 100 "


#query_count = " SELECT count(*) as cnt FROM poptok.locationInfo "
print("################## START ########################")
print(common.common.current_time())

total_cnt = 337358
cnt = 1

try:
    # 파일에서 마지막 인덱스번호 읽어오기
    if(get_last_index() != ''):
        cnt = int(get_last_index()) + 1

    # 수행
    while cnt <= total_cnt:
        param = str(cnt)
        select_results = exec_query(query_select, "select", param)

        # location 상호명- 다음맵에 검색 상호 댓글 비교/추출/저장
        insert_datas = compare(select_results)

        # 카운트 증가
        cnt = int(get_last_index()) + 1

finally:
    print("################## END ########################")
    print(common.common.current_time())






