
import re
import sys
import common.config


# 파일 읽기
def file_read(filename, type):
    f = open(filename, type)
    fr = f.read()
    f.close()
    return fr


# 파일 출력
def file_write(filename, type, msg):
    f = open(filename, type)
    f.write(msg)
    f.close()



# 에러 출력
def error_print(e, filename, last_no, type):

    # 화면 출력
    if(re.findall("M", type) == 'M'):
        print("Except " + filename + ".py [No:" + last_no + "]")
        print(e)
        print('ERROR =>> ', sys.exc_info())

    # 파일 출력
    if (re.findall("F", type) == 'F'):
        # f = open(config.file_txt_except_log, 'a')
        # f.write("\n[" + last_no + "] - " + filename + "\n")
        # f.write(e.__str__() + "\n")
        # f.write('ERROR(sys.exc_info) : ', sys.exc_info())
        # f.close()
        msg = "\n[" + last_no + "] - " + filename + "\n"
        msg += e.__str__() + "\n"
        msg += 'ERROR(sys.exc_info) : ' + sys.exc_info()
        file_write(common.config.file_txt_except_log, 'a', msg)



# 파일에서 마지막 인덱스번호 읽어오기
def get_last_index():
    last_no = ""

    # f = open(common.config.file_txt_last_index, 'r')
    # fr = f.read()
    # f.close()
    last_no = file_read(common.config.file_txt_last_index, 'r')
    print("file read (last_index) => " + last_no)

    return last_no


# 파일에 마지막 인덱스번호 쓰기
def set_last_index(last_no):
    # f = open(common.config.file_txt_last_index, 'w')
    # f.write(str(last_no))
    # f.close()
    file_write(common.config.file_txt_last_index, 'w', str(last_no))