
import common.config
import datetime



# 현재 일자/시간 추출
def current_time():

    now = datetime.datetime.now()
    current_time = now.strftime(common.config.currentTime_format)

    return current_time