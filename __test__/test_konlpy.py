from konlpy.tag import Kkma
import re

kkma = Kkma()



# 해시태그 만들기
def make_tags(words):

    nouns = kkma.nouns(words)
    print(nouns)

    result_tag = ""
    cnt = 0
    for index, n in enumerate(nouns):
        if(index > 0):
            result_tag += ", "
        result_tag += ("#" + n)

    print(result_tag)

    return result_tag


# 해시태그 만들기 테스트
def test_make_tags():
    sentences = kkma.sentences(u'네, 안녕하세요. 반갑습니다.')
    print(sentences)

    nouns = kkma.nouns(u'명사만을 추출하여 다빈도 분석을 합니다.')
    print(nouns)

    print("---------------")
    words = "명사만을 추출하여 다빈도 분석을 합니다."
    result = make_tags(words)
    print("===================")

    pos = kkma.pos(u'오류보고는 실행환경, 에러메세지와함께 설명을 최대한상세히!^^')
    print(pos)



if __name__ == '__main__':
    # 해시태그 만들기 테스트
    #test_make_tags()

    str = "mf"
    result = re.findall("mfa", str)
    print(result)
